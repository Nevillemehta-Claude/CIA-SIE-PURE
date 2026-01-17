#!/usr/bin/env python3
"""
Cursor Chat History Extractor v2
Extracts all chat conversations from Cursor's SQLite database
and exports them to readable markdown files.

This version correctly extracts bubbles (messages) associated with each conversation.
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Paths
GLOBAL_DB = os.path.expanduser(
    "~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
)
OUTPUT_DIR = Path(__file__).parent / "chat_history_export"

def extract_conversations():
    """Extract all composer/chat data from Cursor's database."""
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(GLOBAL_DB)
    cursor = conn.cursor()
    
    # Get all composerData entries
    cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
    composer_rows = cursor.fetchall()
    
    # Get all bubble entries (messages)
    cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
    bubble_rows = cursor.fetchall()
    
    print(f"Found {len(composer_rows)} conversations")
    print(f"Found {len(bubble_rows)} messages (bubbles)")
    
    # Build bubble map: conversation_id -> list of bubbles
    bubble_map = defaultdict(list)
    for key, value in bubble_rows:
        # Key format: bubbleId:CONVERSATION_ID:BUBBLE_ID
        parts = key.split(":")
        if len(parts) >= 3:
            conversation_id = parts[1]
            try:
                bubble_data = json.loads(value)
                bubble_map[conversation_id].append(bubble_data)
            except json.JSONDecodeError:
                pass
    
    # Parse conversations
    conversations = []
    for key, value in composer_rows:
        try:
            conversation_id = key.replace("composerData:", "")
            data = json.loads(value)
            
            # Get bubbles for this conversation
            bubbles = bubble_map.get(conversation_id, [])
            
            # Sort bubbles by creation time if available
            bubbles.sort(key=lambda b: b.get("createdAt", ""))
            
            conversations.append({
                "id": conversation_id,
                "data": data,
                "bubbles": bubbles
            })
        except json.JSONDecodeError as e:
            print(f"Error parsing {key}: {e}")
    
    # Sort by creation time
    def get_timestamp(conv):
        data = conv.get("data", {})
        created = data.get("createdAt", 0)
        if isinstance(created, (int, float)):
            return created
        return 0
    
    conversations.sort(key=get_timestamp)
    
    # Filter to only conversations with actual messages
    conversations_with_messages = [c for c in conversations if len(c["bubbles"]) > 0]
    
    print(f"Conversations with messages: {len(conversations_with_messages)}")
    
    # Export each conversation
    for i, conv in enumerate(conversations_with_messages, 1):
        export_conversation(conv, i)
    
    # Create an index file
    create_index(conversations_with_messages)
    
    conn.close()
    print(f"\nExported to: {OUTPUT_DIR}")
    
    return conversations_with_messages

def export_conversation(conv, index):
    """Export a single conversation to markdown."""
    conv_id = conv["id"]
    data = conv["data"]
    bubbles = conv["bubbles"]
    
    # Get metadata
    created_at = data.get("createdAt", "Unknown")
    if isinstance(created_at, (int, float)):
        try:
            created_at = datetime.fromtimestamp(created_at / 1000).strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
    
    # Generate filename with timestamp prefix if available
    filename = f"{index:03d}_{conv_id[:8]}.md"
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Conversation {index}\n\n")
        f.write(f"**ID:** `{conv_id}`\n\n")
        f.write(f"**Created:** {created_at}\n\n")
        f.write(f"**Messages:** {len(bubbles)}\n\n")
        
        # Add model info if available
        model_config = data.get("modelConfig", {})
        if model_config:
            f.write(f"**Model:** {model_config.get('modelName', 'default')}\n\n")
        
        f.write("---\n\n")
        
        for bubble in bubbles:
            bubble_type = bubble.get("type", 0)
            text = bubble.get("text", "")
            
            # Type 1 = User, Type 2 = Assistant
            if bubble_type == 1:
                f.write("## 👤 User\n\n")
            elif bubble_type == 2:
                f.write("## 🤖 Assistant\n\n")
            else:
                f.write(f"## [Type {bubble_type}]\n\n")
            
            # Write the message content
            if text:
                f.write(text)
                f.write("\n")
            
            # Check for tool calls (like terminal commands, file edits, etc.)
            tool_data = bubble.get("toolFormerData", {})
            if tool_data:
                tool_name = tool_data.get("name", "")
                if tool_name:
                    f.write(f"\n**Tool Used:** `{tool_name}`\n")
                    params = tool_data.get("params", "")
                    if params and isinstance(params, str):
                        try:
                            params_json = json.loads(params)
                            if "command" in params_json:
                                f.write(f"\n```bash\n{params_json['command']}\n```\n")
                        except:
                            pass
            
            f.write("\n---\n\n")
    
    print(f"  Exported: {filename} ({len(bubbles)} messages)")

def create_index(conversations):
    """Create an index file listing all conversations."""
    index_path = OUTPUT_DIR / "00_INDEX.md"
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# Cursor Chat History Index\n\n")
        f.write(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Conversations with Messages:** {len(conversations)}\n\n")
        f.write("---\n\n")
        f.write("| # | Created | Messages | First Message Preview |\n")
        f.write("|---|---------|----------|------------------------|\n")
        
        for i, conv in enumerate(conversations, 1):
            conv_id = conv["id"]
            bubbles = conv["bubbles"]
            data = conv.get("data", {})
            
            # Get creation date
            created_at = data.get("createdAt", "")
            if isinstance(created_at, (int, float)):
                try:
                    created_at = datetime.fromtimestamp(created_at / 1000).strftime("%Y-%m-%d %H:%M")
                except:
                    created_at = "Unknown"
            
            # Get first user message preview
            preview = ""
            for bubble in bubbles:
                if bubble.get("type") == 1:  # User message
                    text = bubble.get("text", "")
                    if text:
                        preview = text[:60].replace("\n", " ").replace("|", "\\|")
                        if len(text) > 60:
                            preview += "..."
                        break
            
            f.write(f"| [{i}]({i:03d}_{conv_id[:8]}.md) | {created_at} | {len(bubbles)} | {preview} |\n")
    
    print(f"\nCreated index: {index_path}")

def export_raw_json(conversations):
    """Also export raw JSON for full data access."""
    raw_path = OUTPUT_DIR / "raw_conversations.json"
    
    # Prepare data for export
    export_data = {}
    for conv in conversations:
        export_data[conv["id"]] = {
            "metadata": conv["data"],
            "messages": conv["bubbles"]
        }
    
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, default=str)
    
    print(f"Exported raw JSON: {raw_path}")

def create_combined_html(conversations):
    """Create a single HTML file with all conversations for easy browsing."""
    html_path = OUTPUT_DIR / "all_conversations.html"
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cursor Chat History</title>
    <style>
        :root {
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --bg-tertiary: #0f3460;
            --text-primary: #eee;
            --text-secondary: #aaa;
            --accent: #e94560;
            --user-bg: #1e3a5f;
            --assistant-bg: #2d2d44;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: var(--accent); margin-bottom: 20px; }
        .nav {
            position: sticky;
            top: 0;
            background: var(--bg-secondary);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            max-height: 300px;
            overflow-y: auto;
        }
        .nav h2 { color: var(--accent); font-size: 1rem; margin-bottom: 10px; }
        .nav-item {
            display: block;
            padding: 8px 12px;
            color: var(--text-primary);
            text-decoration: none;
            border-radius: 4px;
            margin-bottom: 4px;
        }
        .nav-item:hover { background: var(--bg-tertiary); }
        .nav-item small { color: var(--text-secondary); }
        .conversation {
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
        }
        .conversation-header {
            border-bottom: 1px solid var(--bg-tertiary);
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        .conversation-header h2 { color: var(--accent); }
        .message {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .message-user { background: var(--user-bg); }
        .message-assistant { background: var(--assistant-bg); }
        .message-header {
            font-weight: bold;
            margin-bottom: 8px;
            color: var(--accent);
        }
        .message-content {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        pre {
            background: #0d1117;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 10px 0;
        }
        code { font-family: 'Fira Code', 'Consolas', monospace; }
        .tool-info {
            background: var(--bg-tertiary);
            padding: 8px 12px;
            border-radius: 4px;
            margin-top: 10px;
            font-size: 0.9em;
        }
        .search-box {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: var(--bg-tertiary);
            color: var(--text-primary);
            font-size: 1rem;
            margin-bottom: 15px;
        }
        .search-box::placeholder { color: var(--text-secondary); }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗂️ Cursor Chat History</h1>
        <input type="text" class="search-box" placeholder="Search conversations..." id="searchBox" onkeyup="filterConversations()">
        
        <div class="nav">
            <h2>📋 Conversations (""" + str(len(conversations)) + """)</h2>
"""
    
    # Add navigation items
    for i, conv in enumerate(conversations, 1):
        data = conv.get("data", {})
        created_at = data.get("createdAt", "")
        if isinstance(created_at, (int, float)):
            try:
                created_at = datetime.fromtimestamp(created_at / 1000).strftime("%Y-%m-%d %H:%M")
            except:
                created_at = "Unknown"
        
        # Get first user message
        preview = ""
        for bubble in conv["bubbles"]:
            if bubble.get("type") == 1:
                text = bubble.get("text", "")
                if text:
                    preview = text[:40].replace("<", "&lt;").replace(">", "&gt;")
                    if len(text) > 40:
                        preview += "..."
                    break
        
        html_content += f'            <a href="#conv-{i}" class="nav-item">#{i}: {preview}<br><small>{created_at} • {len(conv["bubbles"])} msgs</small></a>\n'
    
    html_content += """        </div>
        
        <div id="conversationsContainer">
"""
    
    # Add conversations
    for i, conv in enumerate(conversations, 1):
        data = conv.get("data", {})
        created_at = data.get("createdAt", "")
        if isinstance(created_at, (int, float)):
            try:
                created_at = datetime.fromtimestamp(created_at / 1000).strftime("%Y-%m-%d %H:%M:%S")
            except:
                created_at = "Unknown"
        
        html_content += f'''
            <div class="conversation" id="conv-{i}" data-searchable="">
                <div class="conversation-header">
                    <h2>Conversation #{i}</h2>
                    <small>Created: {created_at} | Messages: {len(conv["bubbles"])}</small>
                </div>
'''
        
        for bubble in conv["bubbles"]:
            bubble_type = bubble.get("type", 0)
            text = bubble.get("text", "")
            
            msg_class = "message-user" if bubble_type == 1 else "message-assistant"
            role_emoji = "👤 User" if bubble_type == 1 else "🤖 Assistant"
            
            # Escape HTML in text
            text_escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") if text else ""
            
            html_content += f'''
                <div class="message {msg_class}">
                    <div class="message-header">{role_emoji}</div>
                    <div class="message-content">{text_escaped}</div>
'''
            
            # Add tool info if present
            tool_data = bubble.get("toolFormerData", {})
            if tool_data:
                tool_name = tool_data.get("name", "")
                if tool_name:
                    html_content += f'                    <div class="tool-info">🔧 Tool: {tool_name}</div>\n'
            
            html_content += '                </div>\n'
        
        html_content += '            </div>\n'
    
    html_content += """
        </div>
    </div>
    
    <script>
        function filterConversations() {
            const query = document.getElementById('searchBox').value.toLowerCase();
            const conversations = document.querySelectorAll('.conversation');
            
            conversations.forEach(conv => {
                const text = conv.textContent.toLowerCase();
                if (text.includes(query)) {
                    conv.classList.remove('hidden');
                } else {
                    conv.classList.add('hidden');
                }
            });
        }
    </script>
</body>
</html>
"""
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Created HTML viewer: {html_path}")

if __name__ == "__main__":
    print("=" * 60)
    print("Cursor Chat History Extractor v2")
    print("=" * 60)
    print()
    
    if not os.path.exists(GLOBAL_DB):
        print(f"ERROR: Database not found at {GLOBAL_DB}")
        exit(1)
    
    conversations = extract_conversations()
    export_raw_json(conversations)
    create_combined_html(conversations)
    
    print()
    print("=" * 60)
    print("Done! You can:")
    print("  1. Open chat_history_export/00_INDEX.md for the index")
    print("  2. Open chat_history_export/all_conversations.html in a browser")
    print("  3. Browse individual .md files for each conversation")
    print("=" * 60)
