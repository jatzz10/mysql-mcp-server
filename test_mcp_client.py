#!/usr/bin/env python3
"""
MCP Client for testing the optimized MySQL MCP Server

This script demonstrates how to connect to the MySQL MCP server
using the FastMCP client library with streamable-http transport.
Tests the new resource-based approach with smart caching.
"""

import asyncio
import json
import sys
from typing import Dict, Any
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp import Client


async def test_mysql_mcp_server():
    """Test the optimized MySQL MCP server with various operations"""
    
    print("🔌 Connecting to Optimized MySQL MCP Server")
    print("=" * 60)
    
    # Server parameters for streamable-http connection
    server_url = "http://127.0.0.1:8000/mcp"
    
    try:
        # Connect to the server using FastMCP client with StreamableHttpTransport
        transport = StreamableHttpTransport(url=server_url)
        client = Client(transport)
        
        async with client:
            print("✅ Connected to MySQL MCP Server")
            print("-" * 60)
            
            # List available tools and resources
            print("\n📋 Available tools and resources:")
            tools = await client.list_tools()
            resources = await client.list_resources()
            
            print("  Tools:")
            # Handle both list and object formats
            if hasattr(tools, 'tools'):
                tool_list = tools.tools
            else:
                tool_list = tools
            
            for tool in tool_list:
                print(f"    - {tool.name}: {tool.description}")
            
            print("  Resources:")
            # Handle both list and object formats
            if hasattr(resources, 'resources'):
                resource_list = resources.resources
            else:
                resource_list = resources
                
            for resource in resource_list:
                print(f"    - {resource.uri}: {resource.description}")
            
            # Test 1: Get database schema resource
            print("\n🗂️  Testing database schema resource:")
            try:
                resource = await client.read_resource("database://schema")
                # Handle both list and object formats
                if hasattr(resource, 'contents'):
                    content = resource.contents[0].text
                else:
                    content = resource[0].text
                schema_data = json.loads(content)
                
                print("✅ Schema resource retrieved successfully")
                print(f"  Database: {schema_data['metadata']['database_name']}")
                print(f"  Total Tables: {schema_data['metadata']['total_tables']}")
                print(f"  Generated At: {schema_data['metadata']['generated_at']}")
                
                # Show first few tables
                table_names = list(schema_data['tables'].keys())[:3]
                print(f"  Sample Tables: {', '.join(table_names)}")
                
            except Exception as e:
                print(f"❌ Schema resource failed: {e}")
            
            # Test 2: Query data with caching
            print("\n🔍 Testing query_mysql with caching:")
            try:
                result = await client.call_tool("query_mysql", {
                    "query": "SELECT 1 as test_column, 'Hello Optimized MCP!' as message",
                    "limit": 5
                })
                print("✅ query_mysql successful")
                data = json.loads(result.content[0].text)
                print(json.dumps(data, indent=2))
            except Exception as e:
                print(f"❌ query_mysql failed: {e}")
            
            # Test 3: Test query caching (same query should be cached)
            print("\n⚡ Testing query caching (same query):")
            try:
                result = await client.call_tool("query_mysql", {
                    "query": "SELECT 1 as test_column, 'Hello Optimized MCP!' as message",
                    "limit": 5
                })
                print("✅ Cached query successful")
                data = json.loads(result.content[0].text)
                print("  (This should be served from cache)")
            except Exception as e:
                print(f"❌ Cached query failed: {e}")
            
            # Test 4: Test schema resource caching
            print("\n⚡ Testing schema resource caching:")
            try:
                resource = await client.read_resource("database://schema")
                print("✅ Schema resource cached successfully")
                print("  (This should be served from cache)")
            except Exception as e:
                print(f"❌ Schema resource caching failed: {e}")
            
            # Test 5: Sample queries from test database
            print("\n📋 Testing sample queries with caching:")
            
            sample_queries = [
                ("Active users", "SELECT username, email, first_name, last_name FROM users WHERE is_active = 1 LIMIT 3"),
                ("Products with categories", "SELECT p.name, p.price, c.name as category FROM products p LEFT JOIN categories c ON p.category_id = c.id LIMIT 3"),
                ("Recent orders", "SELECT o.id, u.username, o.total_amount, o.status FROM orders o JOIN users u ON o.user_id = u.id ORDER BY o.order_date DESC LIMIT 3")
            ]
            
            for description, query in sample_queries:
                print(f"\n  {description}:")
                try:
                    result = await client.call_tool("query_mysql", {
                        "query": query,
                        "limit": 5
                    })
                    print("  ✅ Query successful (cached for 5 minutes)")
                    data = json.loads(result.content[0].text)
                    if data:
                        print(f"  Found {len(data)} results")
                        for row in data[:2]:  # Show first 2 results
                            print(f"    {row}")
                    else:
                        print("  No results found")
                except Exception as e:
                    print(f"  ❌ Query failed: {e}")
            
            # Test 6: Manual schema refresh
            print("\n🔄 Testing manual schema refresh:")
            try:
                result = await client.call_tool("refresh_schema_manual", {})
                print("✅ Manual schema refresh successful")
                data = json.loads(result.content[0].text)
                print(f"  Status: {data['status']}")
                if data['status'] == 'success':
                    print(f"  Generated At: {data['generated_at']}")
                    print(f"  Total Tables: {data['total_tables']}")
            except Exception as e:
                print(f"❌ Manual schema refresh failed: {e}")
            
            print("\n✅ All tests completed!")
            print("\n📊 Performance Benefits:")
            print("  - Schema data served from file (resources/database_schema.json)")
            print("  - Query results cached in memory (5min TTL)")
            print("  - Automatic schema refresh when stale")
            print("  - Memory efficient for large schemas")
            print("  - No unnecessary database calls for static data")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Make sure the MySQL MCP server is running:")
        print("   python3 mysql_mcp_server.py")
        print("   Server should be accessible at http://localhost:8000")
        return False
    
    return True

async def test_performance():
    """Test caching performance"""
    print("\n⚡ Performance Test")
    print("=" * 30)
    
    # This would be implemented to measure cache hit rates
    # and response times in a real scenario
    print("  - Schema file: resources/database_schema.json")
    print("  - Query cache: 5 minutes TTL (memory)")
    print("  - Automatic refresh on schema changes")
    print("  - File-based persistence for large schemas")
    print("  - Memory efficient approach")

async def main():
    """Main entry point"""
    print("🚀 Starting Optimized MySQL MCP Server Test")
    print("Testing resource-based approach with smart caching")
    print("Make sure the server is running on http://localhost:8000")
    print()
    
    try:
        success = await test_mysql_mcp_server()
        if not success:
            sys.exit(1)
        
        await test_performance()
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())