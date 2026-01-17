#!/usr/bin/env python3
"""
CIA-SIE Complete Chat Chronicle Generator
Creates a self-contained HTML document with all chat history embedded.
"""

import json
import sqlite3
import os
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import html

GLOBAL_DB = os.path.expanduser(
    "~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
)
OUTPUT_DIR = Path(__file__).parent / "chat_history_export"

def load_conversations():
    """Load all conversations from Cursor's database."""
    conn = sqlite3.connect(GLOBAL_DB)
    cursor = conn.cursor()
    
    # Get composers
    cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
    composer_rows = cursor.fetchall()
    
    # Get bubbles
    cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
    bubble_rows = cursor.fetchall()
    
    # Build bubble map
    bubble_map = defaultdict(list)
    for key, value in bubble_rows:
        parts = key.split(':')
        if len(parts) >= 3:
            conv_id = parts[1]
            try:
                bubble_map[conv_id].append(json.loads(value))
            except:
                pass
    
    # Build conversations
    conversations = []
    for key, value in composer_rows:
        conv_id = key.replace('composerData:', '')
        try:
            data = json.loads(value)
            bubbles = bubble_map.get(conv_id, [])
            bubbles.sort(key=lambda b: b.get('createdAt', ''))
            if bubbles:
                conversations.append({
                    'id': conv_id,
                    'metadata': data,
                    'messages': bubbles
                })
        except:
            pass
    
    conversations.sort(key=lambda c: c.get('metadata', {}).get('createdAt', 0))
    conn.close()
    
    return conversations

def format_date(timestamp):
    """Format timestamp to readable date."""
    if not timestamp:
        return "Unknown"
    try:
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp / 1000)
        else:
            dt = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return "Unknown"

def get_first_user_message(messages):
    """Get preview from first user message."""
    for msg in messages:
        if msg.get('type') == 1 and msg.get('text'):
            text = msg['text'][:100]
            return text + ('...' if len(msg['text']) > 100 else '')
    return "No preview available"

def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ""
    return html.escape(str(text))

def generate_html(conversations):
    """Generate the complete HTML document."""
    
    total_messages = sum(len(c['messages']) for c in conversations)
    generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate TOC items
    toc_items = []
    for i, conv in enumerate(conversations, 1):
        preview = get_first_user_message(conv['messages'])
        date = format_date(conv['metadata'].get('createdAt'))
        msg_count = len(conv['messages'])
        toc_items.append(f'''
            <a href="#conv-{i}" class="toc-item">
                <span class="num">{i:02d}</span>
                <span class="preview">{escape_html(preview[:50])}</span>
                <span class="meta-line">{date} · {msg_count} msgs</span>
            </a>''')
    
    # Generate conversations
    conv_sections = []
    for i, conv in enumerate(conversations, 1):
        preview = get_first_user_message(conv['messages'])
        date = format_date(conv['metadata'].get('createdAt'))
        msg_count = len(conv['messages'])
        conv_id = conv['id'][:8]
        
        # Generate messages
        message_items = []
        for j, msg in enumerate(conv['messages'], 1):
            is_user = msg.get('type') == 1
            role_class = 'message-user' if is_user else 'message-assistant'
            role_label = '👤 USER' if is_user else '🤖 ASSISTANT'
            text = escape_html(msg.get('text', ''))
            
            tool_info = ''
            if msg.get('toolFormerData', {}).get('name'):
                tool_name = escape_html(msg['toolFormerData']['name'])
                tool_info = f'<div class="tool-badge">🔧 {tool_name}</div>'
            
            message_items.append(f'''
                <div class="message {role_class}">
                    <div class="message-header">
                        <span class="msg-num">§{j}</span>
                        <span class="message-role">{role_label}</span>
                    </div>
                    <div class="message-content">{text if text else '<em class="empty">[Tool execution / No text]</em>'}</div>
                    {tool_info}
                </div>''')
        
        messages_html = '\n'.join(message_items)
        is_large = msg_count > 50
        collapsed_class = 'collapsed' if is_large else ''
        expand_btn = f'<button class="expand-btn" onclick="toggleConv(this)">▶ Show {msg_count} Messages</button>' if is_large else ''
        
        conv_sections.append(f'''
            <article class="conversation {collapsed_class}" id="conv-{i}">
                <header class="conversation-header">
                    <div class="conversation-number">CONVERSATION {i:02d} OF {len(conversations)}</div>
                    <h2 class="conversation-title">{escape_html(preview[:70])}</h2>
                    <div class="conversation-meta">
                        <span>📅 {date}</span>
                        <span>💬 {msg_count} messages</span>
                        <span>🆔 {conv_id}</span>
                    </div>
                    {expand_btn}
                </header>
                <div class="messages-container">
                    {messages_html}
                </div>
            </article>''')
    
    toc_html = '\n'.join(toc_items)
    conversations_html = '\n'.join(conv_sections)
    
    html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIA-SIE Project | Complete Chat Chronicle</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');
        
        :root {{
            --parchment: #faf8f5;
            --parchment-dark: #f0ebe3;
            --ink: #1a1a1a;
            --ink-light: #4a4a4a;
            --ink-muted: #888;
            --gold: #b8860b;
            --gold-light: #d4a84b;
            --navy: #1a2a4a;
            --navy-light: #2a3a5a;
            --user-bg: #e3f2fd;
            --user-border: #1976d2;
            --assistant-bg: #fff8e1;
            --assistant-border: #f9a825;
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html {{ scroll-behavior: smooth; }}
        
        body {{
            font-family: 'Crimson Pro', Georgia, serif;
            background: var(--parchment);
            color: var(--ink);
            line-height: 1.7;
            font-size: 17px;
        }}
        
        /* Masthead */
        .masthead {{
            background: linear-gradient(135deg, var(--navy) 0%, #0f1a2a 100%);
            color: white;
            padding: 50px 30px;
            text-align: center;
            border-bottom: 4px solid var(--gold);
        }}
        
        .masthead h1 {{
            font-size: 2.8rem;
            letter-spacing: 0.08em;
            margin-bottom: 8px;
        }}
        
        .masthead .subtitle {{
            font-size: 1.2rem;
            color: var(--gold-light);
            font-style: italic;
        }}
        
        .masthead .meta {{
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            color: rgba(255,255,255,0.6);
            margin-top: 15px;
        }}
        
        /* Layout */
        .container {{
            display: grid;
            grid-template-columns: 300px 1fr;
            max-width: 1500px;
            margin: 0 auto;
        }}
        
        /* Sidebar */
        .sidebar {{
            background: var(--navy);
            color: white;
            padding: 25px 15px;
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            border-right: 3px solid var(--gold);
        }}
        
        .sidebar::-webkit-scrollbar {{ width: 6px; }}
        .sidebar::-webkit-scrollbar-thumb {{ background: var(--gold); border-radius: 3px; }}
        
        .sidebar-header {{
            text-align: center;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 15px;
        }}
        
        .sidebar-header h2 {{
            font-size: 1.1rem;
            color: var(--gold-light);
        }}
        
        .sidebar-header .stats {{
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.5);
            margin-top: 5px;
        }}
        
        .search-box {{
            width: 100%;
            padding: 10px 12px;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 5px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            margin-bottom: 15px;
        }}
        
        .search-box::placeholder {{ color: rgba(255,255,255,0.4); }}
        .search-box:focus {{ outline: none; border-color: var(--gold); }}
        
        .toc-item {{
            display: block;
            padding: 10px 12px;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-bottom: 3px;
            border-left: 3px solid transparent;
            transition: all 0.15s;
        }}
        
        .toc-item:hover {{
            background: rgba(255,255,255,0.1);
            border-left-color: var(--gold);
        }}
        
        .toc-item .num {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--gold);
            margin-right: 8px;
        }}
        
        .toc-item .preview {{
            display: block;
            font-size: 0.85rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .toc-item .meta-line {{
            font-family: 'Inter', sans-serif;
            font-size: 0.7rem;
            color: rgba(255,255,255,0.4);
        }}
        
        /* Main */
        .main-content {{
            padding: 40px 50px;
            background: var(--parchment);
        }}
        
        /* Conversation */
        .conversation {{
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 2px solid var(--parchment-dark);
        }}
        
        .conversation-header {{
            background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%);
            color: white;
            padding: 20px 25px;
            border-radius: 8px;
            margin-bottom: 25px;
        }}
        
        .conversation-number {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--gold);
            margin-bottom: 5px;
        }}
        
        .conversation-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        .conversation-meta {{
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            color: rgba(255,255,255,0.7);
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .expand-btn {{
            background: transparent;
            border: 1px solid var(--gold);
            color: var(--gold);
            padding: 8px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            margin-top: 12px;
            transition: all 0.2s;
        }}
        
        .expand-btn:hover {{
            background: var(--gold);
            color: var(--navy);
        }}
        
        .conversation.collapsed .messages-container {{
            display: none;
        }}
        
        /* Messages */
        .message {{
            margin-bottom: 20px;
            padding: 20px 25px;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
        
        .message-user {{
            background: var(--user-bg);
            border-left: 4px solid var(--user-border);
        }}
        
        .message-assistant {{
            background: var(--assistant-bg);
            border-left: 4px solid var(--assistant-border);
        }}
        
        .message-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(0,0,0,0.08);
        }}
        
        .msg-num {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: var(--ink-muted);
            background: rgba(0,0,0,0.05);
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        .message-role {{
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}
        
        .message-user .message-role {{ color: var(--user-border); }}
        .message-assistant .message-role {{ color: var(--assistant-border); }}
        
        .message-content {{
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 1rem;
            line-height: 1.7;
        }}
        
        .message-content .empty {{
            color: var(--ink-muted);
        }}
        
        .tool-badge {{
            display: inline-block;
            background: var(--navy);
            color: white;
            padding: 4px 10px;
            border-radius: 3px;
            font-family: 'Inter', sans-serif;
            font-size: 0.7rem;
            margin-top: 12px;
        }}
        
        /* Back to top */
        .back-to-top {{
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 45px;
            height: 45px;
            background: var(--navy);
            color: var(--gold);
            border: 2px solid var(--gold);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 1.3rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.3);
            z-index: 1000;
        }}
        
        .back-to-top:hover {{
            background: var(--gold);
            color: var(--navy);
        }}
        
        /* Footer */
        .footer {{
            background: var(--navy);
            color: rgba(255,255,255,0.6);
            text-align: center;
            padding: 30px;
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
        }}
        
        /* Responsive */
        @media (max-width: 900px) {{
            .container {{ grid-template-columns: 1fr; }}
            .sidebar {{ position: relative; height: auto; max-height: 350px; }}
            .main-content {{ padding: 25px; }}
        }}
        
        .hidden {{ display: none !important; }}
        
        /* Print */
        @media print {{
            .sidebar, .back-to-top {{ display: none; }}
            .container {{ display: block; }}
            .conversation.collapsed .messages-container {{ display: block; }}
        }}
    </style>
</head>
<body>
    <header class="masthead" id="top">
        <h1>CIA-SIE PROJECT</h1>
        <p class="subtitle">Complete Chat Chronicle &amp; Development Record</p>
        <p class="meta">Generated: {generated_time} | {len(conversations)} Conversations | {total_messages:,} Messages</p>
    </header>
    
    <div class="container">
        <nav class="sidebar">
            <div class="sidebar-header">
                <h2>📜 Table of Contents</h2>
                <p class="stats">{len(conversations)} Conversations · {total_messages:,} Messages</p>
            </div>
            <input type="text" class="search-box" placeholder="Search..." onkeyup="filterContent(this.value)">
            <div id="toc">
                {toc_html}
            </div>
        </nav>
        
        <main class="main-content">
            {conversations_html}
        </main>
    </div>
    
    <a href="#top" class="back-to-top" title="Back to Top">↑</a>
    
    <footer class="footer">
        <p>CIA-SIE Project Complete Chat Chronicle</p>
        <p>Comprehensive Seriatim Documentation of All Development Sessions</p>
    </footer>
    
    <script>
        function toggleConv(btn) {{
            const conv = btn.closest('.conversation');
            const isCollapsed = conv.classList.toggle('collapsed');
            const count = conv.querySelectorAll('.message').length;
            btn.textContent = isCollapsed ? '▶ Show ' + count + ' Messages' : '▼ Hide Messages';
        }}
        
        function filterContent(query) {{
            query = query.toLowerCase();
            document.querySelectorAll('.toc-item').forEach(item => {{
                const text = item.textContent.toLowerCase();
                item.classList.toggle('hidden', query && !text.includes(query));
            }});
            document.querySelectorAll('.conversation').forEach(conv => {{
                const text = conv.textContent.toLowerCase();
                conv.classList.toggle('hidden', query && !text.includes(query));
            }});
        }}
    </script>
</body>
</html>'''
    
    return html_doc

def main():
    print("=" * 60)
    print("CIA-SIE Complete Chat Chronicle Generator")
    print("=" * 60)
    print()
    
    print("Loading conversations from Cursor database...")
    conversations = load_conversations()
    print(f"Found {len(conversations)} conversations with messages")
    
    total_messages = sum(len(c['messages']) for c in conversations)
    print(f"Total messages: {total_messages:,}")
    
    print("\nGenerating HTML document...")
    html_content = generate_html(conversations)
    
    output_path = OUTPUT_DIR / "CIA_SIE_COMPLETE_CHAT_CHRONICLE.html"
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Generated: {output_path}")
    print(f"   File size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
