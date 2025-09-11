#!/usr/bin/env python3
"""
Test script to verify MySQL MCP Server installation
"""

import sys
import importlib.util

def test_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        'fastmcp',
        'pymysql',
        'dotenv'
    ]
    
    print("🔍 Testing imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            spec = importlib.util.find_spec(module)
            if spec is None:
                raise ImportError(f"Module {module} not found")
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_config():
    """Test configuration loading"""
    print("\n⚙️  Testing configuration...")
    
    try:
        from config import MySQLConfig
        config = MySQLConfig()
        
        print(f"  Host: {config.host}")
        print(f"  Port: {config.port}")
        print(f"  User: {config.user or 'Not set'}")
        print(f"  Database: {config.database or 'Not set'}")
        
        if config.validate():
            print("  ✅ Configuration is valid")
            return True
        else:
            print("  ⚠️  Configuration is incomplete (missing required fields)")
            print("     Please set MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE in .env file")
            return False
            
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 MySQL MCP Server Installation Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test configuration
    config_ok = test_config()
    
    print("\n" + "=" * 50)
    if imports_ok and config_ok:
        print("✅ All tests passed! MySQL MCP Server is ready to use.")
        print("\nNext steps:")
        print("1. Configure your .env file with MySQL connection details")
        print("2. Run: python run_server.py")
        print("3. Or test with: python example_client.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        if not imports_ok:
            print("   Install missing dependencies with: pip install -r requirements.txt")
        if not config_ok:
            print("   Set up your .env file with MySQL connection details")
        sys.exit(1)

if __name__ == "__main__":
    main()
