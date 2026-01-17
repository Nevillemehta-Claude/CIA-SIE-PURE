"""
Mercury REPL Interface
======================

Interactive command-line interface for Mercury.

CONSTITUTIONAL: MR-002 - Direct Communication
The interface presents AI responses directly without modification.
"""

import asyncio
import sys
from typing import Optional

from mercury.ai.engine import AIEngine
from mercury.chat.conversation import Conversation, ConversationManager
from mercury.chat.engine import ChatEngine
from mercury.kite.adapter import KiteAdapter
from mercury.core.config import get_settings


# ANSI color codes for terminal formatting
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


BANNER = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   {Colors.BOLD}☿ MERCURY{Colors.RESET}{Colors.CYAN}                                                       ║
║   {Colors.DIM}The Messenger of the Gods{Colors.RESET}{Colors.CYAN}                                        ║
║                                                                    ║
║   {Colors.YELLOW}LLM as Financial Market Cognitive Interface{Colors.CYAN}                     ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.DIM}Type your question in natural language. Use /help for commands.{Colors.RESET}
"""

HELP_TEXT = f"""
{Colors.BOLD}Mercury Commands:{Colors.RESET}

  {Colors.GREEN}/help{Colors.RESET}       - Show this help message
  {Colors.GREEN}/clear{Colors.RESET}      - Clear conversation history  
  {Colors.GREEN}/positions{Colors.RESET}  - Show your current positions
  {Colors.GREEN}/holdings{Colors.RESET}   - Show your holdings
  {Colors.GREEN}/auth{Colors.RESET}       - Re-authenticate with Kite
  {Colors.GREEN}/quit{Colors.RESET}       - Exit Mercury

{Colors.BOLD}Example Queries:{Colors.RESET}

  "What's the price of [ANY SYMBOL]?"
  "How has [SYMBOL] performed this week?"
  "Show me my portfolio summary"
  "Compare [SYMBOL A] and [SYMBOL B]"
  "What do you think about my positions?"

{Colors.DIM}Mercury is instrument-agnostic. Use any valid trading symbol.{Colors.RESET}
"""


class MercuryREPL:
    """
    Mercury Read-Eval-Print Loop.
    
    Provides an interactive terminal interface for Mercury.
    """
    
    def __init__(self):
        """Initialize the REPL."""
        self.kite = KiteAdapter()
        self.ai = AIEngine()
        self.engine = ChatEngine(kite=self.kite, ai=self.ai)
        self.conversation_manager = ConversationManager()
        self.running = False
    
    def print_banner(self) -> None:
        """Print the Mercury banner."""
        print(BANNER)
    
    def print_help(self) -> None:
        """Print help text."""
        print(HELP_TEXT)
    
    def print_response(self, response: str) -> None:
        """Print an AI response with formatting."""
        print()
        print(f"{Colors.GREEN}Mercury:{Colors.RESET}")
        print(f"  {response.replace(chr(10), chr(10) + '  ')}")
        print()
    
    def print_error(self, message: str) -> None:
        """Print an error message."""
        print(f"\n{Colors.RED}Error: {message}{Colors.RESET}\n")
    
    def print_info(self, message: str) -> None:
        """Print an info message."""
        print(f"\n{Colors.CYAN}{message}{Colors.RESET}\n")
    
    async def handle_command(self, command: str) -> Optional[str]:
        """
        Handle a special command (starting with /).
        
        Returns:
            Response string if command produces output, None otherwise
        """
        cmd = command.lower().strip()
        
        if cmd in ["/quit", "/exit", "/q"]:
            self.running = False
            return None
        
        elif cmd in ["/help", "/h", "/?"]:
            self.print_help()
            return None
        
        elif cmd in ["/clear", "/c"]:
            self.conversation_manager.clear_active()
            self.print_info("Conversation cleared.")
            return None
        
        elif cmd == "/positions":
            # Quick query for positions
            conv = self.conversation_manager.get_active_conversation()
            return await self.engine.process(
                "Show me a summary of my current open positions",
                conv
            )
        
        elif cmd == "/holdings":
            # Quick query for holdings
            conv = self.conversation_manager.get_active_conversation()
            return await self.engine.process(
                "Show me a summary of my holdings",
                conv
            )
        
        elif cmd == "/auth":
            self.print_info(
                "To authenticate with Kite:\n"
                "1. Set KITE_API_KEY and KITE_API_SECRET in your .env file\n"
                "2. Run: python -m mercury.scripts.authenticate_kite\n"
                "3. Complete OAuth flow in browser\n"
                "4. Set resulting KITE_ACCESS_TOKEN in .env"
            )
            return None
        
        else:
            self.print_error(f"Unknown command: {command}")
            return None
    
    async def process_input(self, user_input: str) -> Optional[str]:
        """
        Process user input (command or query).
        
        Args:
            user_input: Raw user input
            
        Returns:
            Response to display, or None if no response needed
        """
        user_input = user_input.strip()
        
        if not user_input:
            return None
        
        # Check for command
        if user_input.startswith("/"):
            return await self.handle_command(user_input)
        
        # Regular query
        conv = self.conversation_manager.get_active_conversation()
        return await self.engine.process(user_input, conv)
    
    async def run(self) -> None:
        """Run the REPL main loop."""
        self.running = True
        self.print_banner()
        
        # Check authentication status
        if not self.kite.is_authenticated():
            self.print_info(
                "Note: Kite is not authenticated. Using mock data.\n"
                "Run /auth to set up Kite Connect authentication."
            )
        
        while self.running:
            try:
                # Get user input
                user_input = input(f"{Colors.BLUE}You:{Colors.RESET} ")
                
                # Process input
                response = await self.process_input(user_input)
                
                # Display response if any
                if response:
                    self.print_response(response)
                    
            except KeyboardInterrupt:
                print("\n")
                self.print_info("Use /quit to exit Mercury.")
            except EOFError:
                self.running = False
            except Exception as e:
                self.print_error(f"Unexpected error: {e}")
        
        print(f"\n{Colors.CYAN}Goodbye! ☿{Colors.RESET}\n")


def run_mercury() -> None:
    """Main entry point to run Mercury REPL."""
    repl = MercuryREPL()
    asyncio.run(repl.run())


if __name__ == "__main__":
    run_mercury()
