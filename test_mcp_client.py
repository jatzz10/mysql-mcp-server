#!/usr/bin/env python3
"""
MCP Client for testing the MySQL MCP Server

This script demonstrates how to connect to the MySQL MCP server
using the MCP client library with SSE transport.
"""

import asyncio
import json
import sys
from typing import Dict, Any

# Try to import MCP client libraries
try:
    from mcp import ClientSession
    from mcp.client.sse import sse_client
    from mcp.client.stdio import stdio_client
except ImportError:
    print("❌ MCP client libraries not found. Installing...")
    print("Run: pip install mcp")
    sys.exit(1)

async def test_mysql_mcp_server():
    """Test the MySQL MCP server with various operations"""
    
    print("🔌 Connecting to MySQL MCP Server")
    print("=" * 50)
    
    # Server parameters for SSE connection
    server_url = "http://localhost:8000/sse"
    
    try:
        # Connect to the server
        async with sse_client(server_url) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                print("✅ Connected to MySQL MCP Server")
                print("-" * 50)
                
                # List available tools
                print("\n📋 Available tools:")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test 1: List tables
                print("\n🗂️  Testing list_tables:")
                try:
                    result = await session.call_tool("list_tables", {})
                    print("✅ list_tables successful")
                    data = json.loads(result.content[0].text)
                    print(f"Found {len(data)} tables:")
                    for table in data[:3]:  # Show first 3 tables
                        print(f"  - {table['name']} ({table['rows']} rows)")
                except Exception as e:
                    print(f"❌ list_tables failed: {e}")
                
                # Test 2: Describe a table
                print("\n📊 Testing describe_table('users'):")
                try:
                    result = await session.call_tool("describe_table", {"table_name": "users"})
                    print("✅ describe_table successful")
                    data = json.loads(result.content[0].text)
                    print(f"Table: {data['table_name']}")
                    print(f"Columns: {len(data['columns'])}")
                    for col in data['columns'][:3]:  # Show first 3 columns
                        print(f"  - {col['Field']} ({col['Type']})")
                except Exception as e:
                    print(f"❌ describe_table failed: {e}")
                
                # Test 3: Query data
                print("\n🔍 Testing query_mysql:")
                try:
                    result = await session.call_tool("query_mysql", {
                        "query": "SELECT 1 as test_column, 'Hello MySQL MCP!' as message",
                        "limit": 5
                    })
                    print("✅ query_mysql successful")
                    data = json.loads(result.content[0].text)
                    print(json.dumps(data, indent=2))
                except Exception as e:
                    print(f"❌ query_mysql failed: {e}")
                
                # Test 4: Get table info
                print("\n📈 Testing get_table_info('users'):")
                try:
                    result = await session.call_tool("get_table_info", {"table_name": "users"})
                    print("✅ get_table_info successful")
                    data = json.loads(result.content[0].text)
                    table_info = data['table_info']
                    print(f"Table: {table_info['TABLE_NAME']}")
                    print(f"Rows: {table_info['TABLE_ROWS']}")
                    print(f"Data Length: {table_info['DATA_LENGTH']} bytes")
                except Exception as e:
                    print(f"❌ get_table_info failed: {e}")
                
                # Test 5: Sample queries from test database
                print("\n📋 Testing sample queries:")
                
                sample_queries = [
                    ("Active users", "SELECT username, email, first_name, last_name FROM users WHERE is_active = 1 LIMIT 3"),
                    ("Products with categories", "SELECT p.name, p.price, c.name as category FROM products p LEFT JOIN categories c ON p.category_id = c.id LIMIT 3"),
                    ("Recent orders", "SELECT o.id, u.username, o.total_amount, o.status FROM orders o JOIN users u ON o.user_id = u.id ORDER BY o.order_date DESC LIMIT 3")
                ]
                
                for description, query in sample_queries:
                    print(f"\n  {description}:")
                    try:
                        result = await session.call_tool("query_mysql", {
                            "query": query,
                            "limit": 5
                        })
                        print("  ✅ Query successful")
                        data = json.loads(result.content[0].text)
                        if data:
                            print(f"  Found {len(data)} results")
                            for row in data[:2]:  # Show first 2 results
                                print(f"    {row}")
                        else:
                            print("  No results found")
                    except Exception as e:
                        print(f"  ❌ Query failed: {e}")
                
                print("\n✅ Testing completed!")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Make sure the MySQL MCP server is running:")
        print("   python3 mysql_mcp_server.py")
        return False
    
    return True

async def main():
    """Main entry point"""
    print("🚀 Starting MySQL MCP Server Test")
    print("Make sure the server is running on http://localhost:8000/sse")
    print()
    
    try:
        success = await test_mysql_mcp_server()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
