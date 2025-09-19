# MySQL MCP Server - Quick Setup

## 🚀 **Minimal Setup (3 files + modules)**

### **Core Files:**
- `mysql_mcp_server.py` - Main server
- `test_mcp_client.py` - Test client
- `mcp_chat_client.py` - Interactive chat client

### **Required Modules:**
- `schema/` - Schema generation and caching
- `database/` - Database connection management
- `utils/` - Utility functions

## 📋 **Quick Start**

### **1. Install Dependencies:**
```bash
pip install -r requirements.txt
# This installs fastmcp, PyMySQL, python-dotenv, and cachetools
```

### **2. Configure Database:**
```bash
cp env.example .env
# Edit .env with your MySQL credentials
```

### **3. Start Server:**
```bash
python3 mysql_mcp_server.py
```

### **4. Test Server:**
```bash
# In another terminal
python3 test_mcp_client.py
```

### **5. Use Chat Client:**
```bash
# In another terminal
python3 mcp_chat_client.py
```

## 🔧 **Available Tools & Resources**

### **MCP Resource:**
- `database://schema` - Complete database schema

### **MCP Tools:**
- `query_mysql` - Execute SELECT queries
- `refresh_schema_manual` - Manual schema refresh

## 💬 **Chat Client Commands**

- `/help` - Show help
- `/schema` - Get database schema
- `/query SELECT * FROM users` - Execute query
- `/refresh` - Refresh schema
- `/tools` - List tools
- `/exit` - Exit

## 📊 **Features**

- ✅ **File-based schema storage** (memory efficient)
- ✅ **Smart query caching** (5min TTL)
- ✅ **Automatic schema refresh** when stale
- ✅ **Interactive chat interface**
- ✅ **FastMCP with streamable-HTTP transport** for real-time communication

## 🎯 **Perfect For**

- Database exploration
- LLM integration
- Interactive queries
- Learning database structure

That's it! Clean, simple, and powerful. 🎉
