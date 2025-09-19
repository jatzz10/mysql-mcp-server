#!/usr/bin/env python3
"""
MySQL MCP Server - Optimized Version

A Model Context Protocol (MCP) server that provides read-only access to MySQL databases.
Uses smart caching for optimal performance with MCP resources and tools.
"""

import asyncio
import logging
import os
from typing import Dict, Any

from dotenv import load_dotenv
from fastmcp import FastMCP

from schema import get_schema, query_with_cache, refresh_schema
from database.connection import get_connection_params, get_db_connection

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("mysql-mcp-server")

# MCP Resource for database schema
@mcp.resource("database://schema")
def get_database_schema() -> str:
    """Get the complete database schema as a resource
    
    This resource provides comprehensive database metadata including:
    - Table structures and columns
    - Indexes and relationships
    - Row counts and table sizes
    - Sample data for understanding
    
    The data is automatically cached and refreshed when needed.
    """
    return get_schema()

# MCP Tool for querying data
@mcp.tool()
def query_mysql(query: str, limit: int = 1000) -> str:
    """Execute a SELECT query on the MySQL database
    
    Args:
        query: SQL SELECT query to execute
        limit: Maximum number of rows to return (default: 1000)
    
    Returns:
        JSON string containing query results
        
    Note:
        - Only SELECT queries are allowed for security
        - Results are cached for 5 minutes for performance
        - Query results are limited to prevent large responses
    """
    return query_with_cache(query, limit)

# MCP Tool for manual schema refresh
@mcp.tool()
def refresh_schema_manual() -> str:
    """Manually refresh the database schema
    
    Returns:
        JSON string with refresh status
        
    Note:
        - This tool forces a complete schema refresh
        - Use only when you need the latest schema immediately
        - Normal usage should rely on automatic refresh
    """
    return refresh_schema()

def validate_configuration() -> bool:
    """Validate server configuration"""
    try:
        params = get_connection_params()
        if not all([params['user'], params['password'], params['database']]):
            logger.error("Missing required MySQL connection parameters")
            return False
        
        # Test connection
        connection = get_db_connection()
        connection.close()
        logger.info("Database connection validated")
        return True
        
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        return False

def main():
    """Main entry point"""
    print("🚀 Starting MySQL MCP Server (Optimized) with streamable-http transport")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Validate configuration
    if not validate_configuration():
        print("❌ Configuration validation failed")
        print("Please check your .env file and database connection")
        return
    
    print("✅ Configuration validated")
    print("✅ Smart caching enabled (Schema: 60min, Queries: 5min)")
    print("✅ Auto-refresh enabled for schema changes")
    print("✅ Server ready for MCP client connections")
    print("-" * 60)
    
    # Run the MCP server with streamable-http transport
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()