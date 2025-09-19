"""
Database connection management for MySQL MCP Server
"""

import os
import logging
from typing import Any, Dict

import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

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
