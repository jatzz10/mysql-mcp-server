"""
Database schema generation for MySQL MCP Server
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict

import pymysql
from database.connection import get_db_connection

logger = logging.getLogger(__name__)

def generate_database_schema() -> Dict[str, Any]:
    """Generate comprehensive database schema with metadata"""
    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Get database information
            cursor.execute("SELECT DATABASE() as database_name")
            db_info = cursor.fetchone()
            
            # Get all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            schema_data = {
                "metadata": {
                    "database_name": db_info['database_name'],
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "version": "1.0.0",
                    "total_tables": len(tables)
                },
                "tables": {}
            }
            
            # Process each table
            for table in tables:
                table_name = list(table.values())[0]
                
                # Get table information
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
                
                # Get column information
                cursor.execute(f"DESCRIBE `{table_name}`")
                columns = cursor.fetchall()
                
                # Get index information
                cursor.execute(f"SHOW INDEX FROM `{table_name}`")
                indexes = cursor.fetchall()
                
                # Get foreign key relationships
                cursor.execute(f"""
                    SELECT 
                        COLUMN_NAME,
                        REFERENCED_TABLE_NAME,
                        REFERENCED_COLUMN_NAME,
                        CONSTRAINT_NAME
                    FROM information_schema.KEY_COLUMN_USAGE 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = %s 
                    AND REFERENCED_TABLE_NAME IS NOT NULL
                """, (table_name,))
                foreign_keys = cursor.fetchall()
                
                # Get sample data (first 3 rows) for understanding
                cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 3")
                sample_data = cursor.fetchall()
                
                schema_data["tables"][table_name] = {
                    "table_info": table_info,
                    "columns": columns,
                    "indexes": indexes,
                    "foreign_keys": foreign_keys,
                    "sample_data": sample_data,
                    "relationships": {
                        "references": [fk for fk in foreign_keys],
                        "referenced_by": []
                    }
                }
            
            # Build relationship map
            for table_name, table_data in schema_data["tables"].items():
                for fk in table_data["foreign_keys"]:
                    ref_table = fk["REFERENCED_TABLE_NAME"]
                    if ref_table in schema_data["tables"]:
                        schema_data["tables"][ref_table]["relationships"]["referenced_by"].append({
                            "table": table_name,
                            "column": fk["COLUMN_NAME"],
                            "constraint": fk["CONSTRAINT_NAME"]
                        })
            
            return schema_data
            
    except Exception as e:
        logger.error(f"Error generating schema: {e}")
        raise
    finally:
        if 'connection' in locals():
            connection.close()

def check_schema_needs_refresh() -> bool:
    """Check if schema needs refresh based on database changes"""
    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Get current database timestamp
            cursor.execute("""
                SELECT MAX(UPDATE_TIME) as last_update 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
            """)
            result = cursor.fetchone()
            db_last_update = result['last_update']
            
            # Get schema file timestamp
            from utils.helpers import load_json_file
            schema_data = load_json_file("database_schema.json")
            if not schema_data:
                return True
                
            schema_generated = schema_data.get('metadata', {}).get('generated_at')
            if not schema_generated:
                return True
            
            # Compare timestamps
            from datetime import datetime
            schema_time = datetime.fromisoformat(schema_generated.replace('Z', '+00:00'))
            if db_last_update and db_last_update > schema_time.replace(tzinfo=None):
                logger.info("Database schema has changed, refresh needed")
                return True
                
            return False
            
    except Exception as e:
        logger.error(f"Error checking schema refresh: {e}")
        return True
    finally:
        if 'connection' in locals():
            connection.close()
