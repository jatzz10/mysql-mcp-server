#!/usr/bin/env python3
"""
Chat-based MCP Client for MySQL MCP Server

This script provides an interactive chat interface to interact with the MySQL MCP server.
Perfect for LLM integration and interactive database exploration.
"""

import asyncio
import json
import sys
from typing import Dict, Any, List

# Try to import FastMCP client libraries
try:
    from fastmcp.client.transports import StreamableHttpTransport
    from fastmcp import Client
except ImportError:
    print("❌ FastMCP client library not found. Installing...")
    print("Run: pip install fastmcp")
    sys.exit(1)

class MySQLMCPChatClient:
    """Interactive chat client for MySQL MCP Server"""
    
    def __init__(self, server_url: str = "http://127.0.0.1:8000/mcp"):
        self.server_url = server_url
        self.transport = None
        self.client = None
        self.connected = False
        
    async def connect(self):
        """Connect to the MCP server"""
        try:
            self.transport = StreamableHttpTransport(url=self.server_url)
            self.client = Client(self.transport)
            await self.client.__aenter__()
            self.connected = True
            print("✅ Connected to MySQL MCP Server")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.connected and self.client:
            await self.client.__aexit__(None, None, None)
            self.connected = False
            print("👋 Disconnected from MySQL MCP Server")
    
    async def get_schema(self) -> str:
        """Get database schema"""
        try:
            resource = await self.client.read_resource("database://schema")
            # Handle both list and object formats
            if hasattr(resource, 'contents'):
                return resource.contents[0].text
            else:
                return resource[0].text
        except Exception as e:
            return f"Error getting schema: {e}"
    
    async def execute_query(self, query: str, limit: int = 1000) -> str:
        """Execute a SQL query"""
        try:
            result = await self.client.call_tool("query_mysql", {
                "query": query,
                "limit": limit
            })
            return result.content[0].text
        except Exception as e:
            return f"Error executing query: {e}"
    
    async def refresh_schema(self) -> str:
        """Refresh database schema"""
        try:
            result = await self.client.call_tool("refresh_schema_manual", {})
            return result.content[0].text
        except Exception as e:
            return f"Error refreshing schema: {e}"
    
    async def list_available_tools(self) -> List[str]:
        """List available tools and resources"""
        try:
            tools = await self.client.list_tools()
            resources = await self.client.list_resources()
            
            tool_list = [f"🔧 {tool.name}: {tool.description}" for tool in tools.tools]
            resource_list = [f"📄 {resource.uri}: {resource.description}" for resource in resources.resources]
            
            return tool_list + resource_list
        except Exception as e:
            return [f"Error listing tools: {e}"]
    
    def print_help(self):
        """Print help information"""
        print("\n📚 Available Commands:")
        print("  /help          - Show this help message")
        print("  /schema        - Get database schema")
        print("  /refresh       - Refresh database schema")
        print("  /tools         - List available tools and resources")
        print("  /query <sql>   - Execute SQL query")
        print("  /exit          - Exit the chat")
        print("\n💡 Examples:")
        print("  /query SELECT * FROM users LIMIT 5")
        print("  /query SELECT COUNT(*) FROM products")
        print("  /schema")
        print("  /refresh")
        print("\n🔍 You can also ask natural language questions about the database!")
    
    async def process_command(self, user_input: str) -> str:
        """Process user command"""
        user_input = user_input.strip()
        
        if not user_input:
            return "Please enter a command or question."
        
        # Handle commands
        if user_input.startswith('/'):
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if command == '/help':
                self.print_help()
                return ""
            
            elif command == '/schema':
                return await self.get_schema()
            
            elif command == '/refresh':
                return await self.refresh_schema()
            
            elif command == '/tools':
                tools = await self.list_available_tools()
                return "\n".join(tools)
            
            elif command == '/query':
                if not args:
                    return "Please provide a SQL query. Example: /query SELECT * FROM users LIMIT 5"
                return await self.execute_query(args)
            
            elif command == '/exit':
                return "EXIT"
            
            else:
                return f"Unknown command: {command}. Type /help for available commands."
        
        # Handle natural language questions
        else:
            # Simple natural language processing
            user_input_lower = user_input.lower()
            
            if any(word in user_input_lower for word in ['schema', 'structure', 'tables', 'columns']):
                return await self.get_schema()
            
            elif any(word in user_input_lower for word in ['query', 'select', 'show', 'find', 'get']):
                # Try to extract SQL from natural language
                if 'users' in user_input_lower:
                    return await self.execute_query("SELECT * FROM users LIMIT 10")
                elif 'products' in user_input_lower:
                    return await self.execute_query("SELECT * FROM products LIMIT 10")
                elif 'orders' in user_input_lower:
                    return await self.execute_query("SELECT * FROM orders LIMIT 10")
                else:
                    return "I can help you query the database. Try using /query with a specific SQL statement, or ask about 'users', 'products', or 'orders'."
            
            elif any(word in user_input_lower for word in ['refresh', 'update', 'reload']):
                return await self.refresh_schema()
            
            else:
                return "I can help you explore the database. Try asking about:\n- Database schema (/schema)\n- Querying data (/query SELECT * FROM users)\n- Available tools (/tools)\nOr type /help for more options."

async def main():
    """Main chat loop"""
    print("🚀 MySQL MCP Chat Client")
    print("=" * 50)
    print("Connecting to MySQL MCP Server...")
    
    client = MySQLMCPChatClient()
    
    if not await client.connect():
        print("❌ Failed to connect to server. Make sure it's running:")
        print("   python3 mysql_mcp_server.py")
        print("   Server should be accessible at http://localhost:8000")
        return
    
    print("\n✅ Connected! Type /help for commands or ask questions about the database.")
    print("Type /exit to quit.\n")
    
    try:
        while True:
            # Get user input
            user_input = input("💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Process command
            response = await client.process_command(user_input)
            
            if response == "EXIT":
                break
            
            if response:
                print(f"\n🤖 Assistant: {response}\n")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())