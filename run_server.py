#!/usr/bin/env python3
"""
Quick start script for MySQL MCP Server
"""

import sys
import os
import argparse
from mysql_mcp_server import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MySQL MCP Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to (default: localhost)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to (default: 8000)")
    
    args = parser.parse_args()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found!")
        print("Please copy env.example to .env and configure your MySQL connection details.")
        print("Example:")
        print("  cp env.example .env")
        print("  # Then edit .env with your MySQL credentials")
        sys.exit(1)
    
    print(f"🚀 Starting MySQL MCP Server")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)
