"""
Smart caching system for MySQL MCP Server

Implements TTL-based caching for schema and query results with automatic refresh.
"""

import json
import logging
import os
from typing import Any, Dict, Optional
from cachetools import TTLCache

from .generator import generate_database_schema, check_schema_needs_refresh
from database.connection import get_db_connection
from utils.helpers import save_json_file, load_json_file, create_hash
import pymysql

logger = logging.getLogger(__name__)

# Cache configuration
SCHEMA_FILE = "resources/database_schema.json"
SCHEMA_CACHE_TTL = 3600  # 60 minutes
QUERY_CACHE_TTL = 300    # 5 minutes
QUERY_CACHE_SIZE = 100   # Maximum 100 cached queries

# Initialize caches (only for small metadata and queries)
schema_metadata_cache = TTLCache(maxsize=1, ttl=SCHEMA_CACHE_TTL)  # Only timestamps
query_cache = TTLCache(maxsize=QUERY_CACHE_SIZE, ttl=QUERY_CACHE_TTL)

def get_schema() -> str:
    """Get database schema with file-based smart caching
    
    Returns:
        JSON string containing complete database schema
    """
    try:
        # Check if file exists and is fresh
        if os.path.exists(SCHEMA_FILE):
            # Check if file is fresh using metadata cache
            if 'schema_fresh' in schema_metadata_cache:
                logger.debug("Schema file is fresh (cached)")
                with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
                    return f.read()
            
            # Check if file is actually fresh
            if not check_schema_needs_refresh():
                logger.debug("Schema file is fresh")
                schema_metadata_cache['schema_fresh'] = True
                with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
                    return f.read()
        
        # File is stale or doesn't exist - refresh
        logger.info("Schema file is stale or missing, generating fresh schema...")
        schema_data = generate_database_schema()
        save_schema_to_file(schema_data)
        schema_metadata_cache['schema_fresh'] = True
        
        return json.dumps(schema_data, indent=2, default=str)
        
    except Exception as e:
        logger.error(f"Error getting schema: {e}")
        return json.dumps({"error": str(e)}, indent=2)

def query_with_cache(query: str, limit: int = 1000) -> str:
    """Execute query with smart caching
    
    Args:
        query: SQL SELECT query to execute
        limit: Maximum number of rows to return
        
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
    
    # Create cache key
    cache_key = create_hash(f"{query}:{limit}")
    
    try:
        # Check query cache first
        if cache_key in query_cache:
            logger.debug(f"Query cache hit for: {query[:50]}...")
            return query_cache[cache_key]
        
        # Execute query
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Format results as JSON
            result_json = json.dumps(results, indent=2, default=str)
            
            # Cache the result
            query_cache[cache_key] = result_json
            logger.debug(f"Query cached: {query[:50]}...")
            
            return result_json
            
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise
    finally:
        if 'connection' in locals():
            connection.close()

def refresh_schema() -> str:
    """Manually refresh the database schema
    
    Returns:
        JSON string with refresh status
    """
    try:
        logger.info("Manual schema refresh requested...")
        
        # Clear metadata cache
        schema_metadata_cache.clear()
        
        # Generate fresh schema
        schema_data = generate_database_schema()
        save_schema_to_file(schema_data)
        schema_metadata_cache['schema_fresh'] = True
        
        result = {
            "status": "success",
            "message": "Schema refreshed successfully",
            "generated_at": schema_data["metadata"]["generated_at"],
            "total_tables": schema_data["metadata"]["total_tables"],
            "file_path": SCHEMA_FILE
        }
        
        logger.info("Manual schema refresh completed")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error refreshing schema: {e}")
        error_result = {
            "status": "error",
            "message": str(e)
        }
        return json.dumps(error_result, indent=2)

def save_schema_to_file(schema_data: Dict[str, Any]) -> None:
    """Save schema data to JSON file"""
    try:
        save_json_file(schema_data, SCHEMA_FILE)
        logger.info(f"Schema saved to {SCHEMA_FILE}")
    except Exception as e:
        logger.error(f"Error saving schema: {e}")
        raise

def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics for monitoring
    
    Returns:
        Dictionary with cache statistics
    """
    return {
        "schema_metadata_cache": {
            "size": len(schema_metadata_cache),
            "max_size": schema_metadata_cache.maxsize,
            "ttl": schema_metadata_cache.ttl,
            "file_path": SCHEMA_FILE,
            "file_exists": os.path.exists(SCHEMA_FILE)
        },
        "query_cache": {
            "size": len(query_cache),
            "max_size": query_cache.maxsize,
            "ttl": query_cache.ttl
        }
    }
