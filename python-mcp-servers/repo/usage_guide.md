# How to Use Repo MCP Server for Legacy Code Analysis

## Input Format

**Input**: Complete legacy code repository folder path

```
Your Legacy Code Repository/
├── src/                    # Source code directory
│   ├── app.js
│   ├── models/
│   │   ├── User.js
│   │   └── Book.js
│   └── controllers/
├── package.json           # Configuration files
├── config/
├── tests/                 # Test files
├── public/                # Static assets
├── README.md              # Documentation
└── .env.example
```

## Usage Methods

### Method 1: Direct Command Line Analysis (Recommended)

```bash
# 1. Navigate to MCP server directory
cd /Users/ianzhou/19_project/python-mcp-servers/repo

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run analysis directly with your legacy code path
python analyze_legacy.py /path/to/your/legacy/code
```

**Examples**:
```bash
python analyze_legacy.py ~/projects/old-library-system
python analyze_legacy.py /var/www/legacy-website
python analyze_legacy.py "C:\Projects\LegacyApp"
```

### Method 2: As MCP Server (For AI Integration)

```bash
# 1. Start MCP server
cd /Users/ianzhou/19_project/python-mcp-servers/repo
source venv/bin/activate
python main.py

# 2. Server waits for MCP client connections
# Claude and other AI clients can communicate via stdio
```

## Supported Legacy Code Types

### ✅ Fully Supported
- **Node.js Projects** (Express.js, Koa.js, etc.)
- **Python Projects** (Django, Flask, etc.)
- **PHP Projects** (Laravel, CodeIgniter, etc.)
- **Mixed Technology Stack Projects**

### ✅ Detection Features
- **Frontend Frameworks**: React, Vue.js, Angular
- **Databases**: MongoDB, MySQL, PostgreSQL, Redis
- **Testing Frameworks**: Jest, Mocha, PHPUnit
- **Build Tools**: Webpack, Gulp, Grunt

### ✅ File Analysis
- Automatic classification of source, config, test, documentation files
- Application entry point identification
- Directory structure and architecture pattern analysis
- Git history and contributor analysis

## Output Results

### 1. Repository Structure Analysis
```json
{
  "total_files": 45,
  "total_directories": 12,
  "total_size": 1048576,
  "languages": [
    {"language": "JavaScript", "files": 20, "percentage": 65.5},
    {"language": "JSON", "files": 5, "percentage": 15.2}
  ],
  "architecture": {
    "type": "mvc",
    "confidence": 85,
    "indicators": ["MVC directory structure", "Express.js server"]
  }
}
```

### 2. Technology Stack Detection
```json
{
  "backend": [{"name": "Express.js", "version": "^4.18.0", "confidence": 95}],
  "database": [{"name": "MongoDB", "version": "^6.0.0", "confidence": 90}],
  "testing": [{"name": "Jest", "version": "^29.0.0", "confidence": 90}]
}
```

### 3. Modernization Suggestions
- Upgrade dependency versions
- Add TypeScript support
- Improve architecture patterns
- Increase test coverage
- Containerization deployment

## Real Usage Examples

### Example 1: Analyzing Auckland Library System
```bash
# Analyze a legacy library management system
python analyze_legacy.py /Users/yourname/auckland-library-legacy

# Results will show:
# - Node.js + Express.js backend
# - MongoDB database
# - Dependencies needing updates
# - Architecture improvement suggestions
```

### Example 2: Analyzing PHP Website
```bash
# PHP legacy website
python analyze_legacy.py /var/www/old-website

# Results will show:
# - PHP version and frameworks
# - Database connection types
# - Security issue identification
# - Modern PHP recommendations
```

## FAQ

### Q: Can I analyze code that's not in a Git repository?
A: Yes! The program analyzes file system structure; Git history is just additional information.

### Q: What's the maximum repository size supported?
A: Supports repositories up to 100K lines of code, typically completed within 30 seconds.

### Q: How accurate are the analysis results?
A: Based on file extensions, config files, dependency declarations, etc., accuracy is typically 80-95%.

### Q: Can it analyze encrypted or binary files?
A: Primarily analyzes text files; binary files are skipped without affecting overall analysis.

## Integration into Modernization Pipeline

This MCP server is the first step in the **AI-Driven Automated Upgrade** project:

1. **CodeUnderstandingAgent** uses this server to analyze legacy code
2. **ModernizationPlannerAgent** creates upgrade plans based on analysis results  
3. **CodemodAgent** executes automated code transformations
4. **ValidationAgent** validates upgrade results

---

**Ready to analyze your legacy code?** Run `python analyze_legacy.py /path/to/your/code`!