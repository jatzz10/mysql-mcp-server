#!/usr/bin/env python3
"""
MySQL MCP Server

A Model Context Protocol (MCP) server that provides read-only access to MySQL databases.
Supports querying data using SQL SELECT statements with SSE transport.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

import pymysql
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("mysql-mcp-server")

def get_connection_params() -> Dict[str, Any]:
    """Get MySQL connection parameters from environment variables"""
    return {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE'),
        'charset': 'utf8mb4',
        'autocommit': True
    }

def get_db_connection():
    """Get database connection"""
    params = get_connection_params()
    if not all([params['user'], params['password'], params['database']]):
        raise ValueError("Missing required MySQL connection parameters")
    
    try:
        connection = pymysql.connect(**params)
        logger.info(f"Connected to MySQL database: {params['host']}:{params['port']}/{params['database']}")
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to MySQL: {e}")
        raise

@mcp.tool()
def query_mysql(query: str, limit: int = 1000) -> str:
    """Execute a SELECT query on the MySQL database
    
    Args:
        query: SQL SELECT query to execute
        limit: Maximum number of rows to return (default: 1000)
    
    Returns:
        JSON string containing query results
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
    
    # Basic security check - only allow SELECT statements
    if not query.upper().strip().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")
    
    # Add LIMIT if not present and limit is specified
    if limit and "LIMIT" not in query.upper():
        query += f" LIMIT {limit}"
    
    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Format results as JSON
            return json.dumps(results, indent=2, default=str)
            
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise

@mcp.tool()
def describe_table(table_name: str) -> str:
    """Get table structure and metadata
    
    Args:
        table_name: Name of the table to describe
    
    Returns:
        JSON string containing table structure and metadata
    """
    if not table_name.strip():
        raise ValueError("Table name cannot be empty")
    
    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Get column information
            cursor.execute(f"DESCRIBE `{table_name}`")
            columns = cursor.fetchall()
            
            # Get table information
            cursor.execute(f"""
                SELECT 
                    TABLE_NAME,
                    TABLE_ROWS,
                    DATA_LENGTH,
                    INDEX_LENGTH,
                    TABLE_COLLATION,
                    CREATE_TIME,
                    UPDATE_TIME
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = %s
            """, (table_name,))
            table_info = cursor.fetchone()
            
            result = {
                "table_name": table_name,
                "columns": columns,
                "table_info": table_info
            }
            
            return json.dumps(result, indent=2, default=str)
            
    except Exception as e:
        logger.error(f"Error describing table: {e}")
        raise

@mcp.tool()
def list_tables() -> str:
    """List all tables in the current database
    
    Returns:
        JSON string containing list of tables with metadata
    """
    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            # Get additional info for each table
            table_list = []
            for table in tables:
                table_name = list(table.values())[0]
                cursor.execute(f"""
                    SELECT 
                        TABLE_ROWS,
                        DATA_LENGTH,
                        INDEX_LENGTH
                    FROM information_schema.TABLES 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = %s
                """, (table_name,))
                info = cursor.fetchone()
                
                table_list.append({
                    "name": table_name,
                    "rows": info.get("TABLE_ROWS", 0) if info else 0,
                    "data_length": info.get("DATA_LENGTH", 0) if info else 0,
                    "index_length": info.get("INDEX_LENGTH", 0) if info else 0
                })
            
            return json.dumps(table_list, indent=2, default=str)
            
    except Exception as e:
        logger.error(f"Error listing tables: {e}")
        raise

@mcp.tool()
def get_table_info(table_name: str) -> str:
    """Get detailed table information including indexes
    
    Args:
        table_name: Name of the table to get info for
    
    Returns:
        JSON string containing detailed table information
    """
    if not table_name.strip():
        raise ValueError("Table name cannot be empty")
    
    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Get detailed table information
            cursor.execute(f"""
                SELECT 
                    TABLE_NAME,
                    TABLE_ROWS,
                    AVG_ROW_LENGTH,
                    DATA_LENGTH,
                    MAX_DATA_LENGTH,
                    INDEX_LENGTH,
                    DATA_FREE,
                    AUTO_INCREMENT,
                    CREATE_TIME,
                    UPDATE_TIME,
                    CHECK_TIME,
                    TABLE_COLLATION,
                    CHECKSUM,
                    CREATE_OPTIONS,
                    TABLE_COMMENT
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = %s
            """, (table_name,))
            table_info = cursor.fetchone()
            
            if not table_info:
                raise ValueError(f"Table '{table_name}' not found")
            
            # Get column information
            cursor.execute(f"DESCRIBE `{table_name}`")
            columns = cursor.fetchall()
            
            # Get index information
            cursor.execute(f"SHOW INDEX FROM `{table_name}`")
            indexes = cursor.fetchall()
            
            result = {
                "table_info": table_info,
                "columns": columns,
                "indexes": indexes
            }
            
            return json.dumps(result, indent=2, default=str)
            
    except Exception as e:
        logger.error(f"Error getting table info: {e}")
        raise

def main():
    """Main entry point"""
    print("🚀 Starting MySQL MCP Server with SSE transport")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Validate configuration
    try:
        params = get_connection_params()
        if not all([params['user'], params['password'], params['database']]):
            print("❌ Error: Missing required MySQL connection parameters")
            print("Please set MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE in .env file")
            return
        
        # Test connection
        connection = get_db_connection()
        connection.close()
        print("✅ Database connection successful")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Run the MCP server with SSE transport
    mcp.run(transport="sse")

if __name__ == "__main__":
    main()