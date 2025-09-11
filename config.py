"""
Configuration module for MySQL MCP Server
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MySQLConfig:
    """MySQL configuration class"""
    
    def __init__(self):
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.port = int(os.getenv('MYSQL_PORT', 3306))
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.database = os.getenv('MYSQL_DATABASE')
        self.charset = 'utf8mb4'
        self.autocommit = True
    
    def get_connection_params(self) -> Dict[str, Any]:
        """Get connection parameters as dictionary"""
        return {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'charset': self.charset,
            'autocommit': self.autocommit
        }
    
    def validate(self) -> bool:
        """Validate that all required parameters are set"""
        required_params = [self.user, self.password, self.database]
        return all(param is not None and param.strip() for param in required_params)
    
    def __str__(self) -> str:
        """String representation (without password)"""
        return f"MySQLConfig(host={self.host}, port={self.port}, user={self.user}, database={self.database})"
