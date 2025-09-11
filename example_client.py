#!/usr/bin/env python3
"""
Example client for testing the MySQL MCP Server

This script demonstrates how to interact with the MySQL MCP server
using direct function calls (since FastMCP runs as a local server).
"""

import json
import subprocess
import sys
import time
from typing import Dict, Any

def test_mysql_mcp_server():
    """Test the MySQL MCP server with various operations"""
    
    print("🔌 Testing MySQL MCP Server")
    print("=" * 50)
    
    # Test 1: List tables
    print("\n🗂️  Testing list_tables:")
    try:
        result = subprocess.run([
            sys.executable, "-c", 
            "from mysql_mcp_server import mcp; print(mcp.list_tables())"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ list_tables successful")
            data = json.loads(result.stdout)
            print(f"Found {len(data)} tables:")
            for table in data[:3]:  # Show first 3 tables
                print(f"  - {table['name']} ({table['rows']} rows)")
        else:
            print(f"❌ list_tables failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Describe a table
    print("\n📊 Testing describe_table('users'):")
    try:
        result = subprocess.run([
            sys.executable, "-c", 
            "from mysql_mcp_server import mcp; print(mcp.describe_table('users'))"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ describe_table successful")
            data = json.loads(result.stdout)
            print(f"Table: {data['table_name']}")
            print(f"Columns: {len(data['columns'])}")
            for col in data['columns'][:3]:  # Show first 3 columns
                print(f"  - {col['Field']} ({col['Type']})")
        else:
            print(f"❌ describe_table failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Query data
    print("\n🔍 Testing query_mysql:")
    try:
        result = subprocess.run([
            sys.executable, "-c", 
            "from mysql_mcp_server import mcp; print(mcp.query_mysql('SELECT 1 as test_column, \\'Hello MySQL MCP!\\' as message', 5))"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ query_mysql successful")
            data = json.loads(result.stdout)
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ query_mysql failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Get table info
    print("\n📈 Testing get_table_info('users'):")
    try:
        result = subprocess.run([
            sys.executable, "-c", 
            "from mysql_mcp_server import mcp; print(mcp.get_table_info('users'))"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ get_table_info successful")
            data = json.loads(result.stdout)
            table_info = data['table_info']
            print(f"Table: {table_info['TABLE_NAME']}")
            print(f"Rows: {table_info['TABLE_ROWS']}")
            print(f"Data Length: {table_info['DATA_LENGTH']} bytes")
        else:
            print(f"❌ get_table_info failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
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
            result = subprocess.run([
                sys.executable, "-c", 
                f"from mysql_mcp_server import mcp; print(mcp.query_mysql('{query}', 5))"
            ], capture_output=True, text=True, cwd=".")
            
            if result.returncode == 0:
                print("  ✅ Query successful")
                data = json.loads(result.stdout)
                if data:
                    print(f"  Found {len(data)} results")
                    for row in data[:2]:  # Show first 2 results
                        print(f"    {row}")
                else:
                    print("  No results found")
            else:
                print(f"  ❌ Query failed: {result.stderr}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n✅ Testing completed!")

def test_server_running():
    """Test if the server is running by trying to connect"""
    print("🔍 Checking if MySQL MCP Server is running...")
    
    try:
        # Try to import and run a simple function
        result = subprocess.run([
            sys.executable, "-c", 
            "from mysql_mcp_server import mcp; print('Server available')"
        ], capture_output=True, text=True, cwd=".", timeout=5)
        
        if result.returncode == 0:
            print("✅ Server is available")
            return True
        else:
            print("❌ Server not available")
            return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting MySQL MCP Server Test")
    print("Make sure your .env file is configured with MySQL connection details!")
    print()
    
    # Check if server is available
    if not test_server_running():
        print("\n💡 To start the server, run:")
        print("   python3 mysql_mcp_server.py")
        print("   # or")
        print("   python3 run_server.py")
        print("\nThen run this test again in another terminal.")
        sys.exit(1)
    
    try:
        test_mysql_mcp_server()
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Make sure the MySQL database is running and accessible.")