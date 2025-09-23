# Repo MCP Server

Repository analysis and structure mapping MCP server for Auckland Library legacy system modernization.

## Overview

This MCP server provides comprehensive repository analysis capabilities including:
- Repository structure analysis and metrics
- File classification and organization
- Git history and contribution analysis  
- Framework and technology detection
- Configuration file discovery
- Entry point identification

## Installation

```bash
cd /Users/ianzhou/19_project/mcp-servers/repo
npm install
npm run build
```

## Development

```bash
npm run dev    # Start in development mode
npm test       # Run tests
npm run lint   # Run linting
```

## Available Tools

### `analyze_structure`
Analyze repository structure and get comprehensive metrics.

**Parameters:**
- `repoPath` (string): Path to the repository to analyze

**Returns:** Complete repository structure analysis including file counts, languages, architecture patterns, and complexity metrics.

### `get_file_tree` 
Get hierarchical file tree of the repository.

**Parameters:**
- `repoPath` (string): Path to the repository
- `maxDepth` (number, optional): Maximum depth to traverse

**Returns:** Hierarchical file tree structure.

### `classify_files`
Classify files by their purpose (source, config, docs, etc.).

**Parameters:**
- `repoPath` (string): Path to the repository

**Returns:** File classification organized by type.

### `get_commit_history`
Get commit history with statistics.

**Parameters:**
- `repoPath` (string): Path to the repository
- `limit` (number, optional): Maximum number of commits to return

**Returns:** Array of commit information with statistics.

### `analyze_branches`
Analyze branch structure and status.

**Parameters:**
- `repoPath` (string): Path to the repository

**Returns:** Branch analysis including active/stale branches.

### `get_contributors`
Get contributor statistics.

**Parameters:**
- `repoPath` (string): Path to the repository

**Returns:** Array of contributor statistics.

### `detect_frameworks`
Detect frameworks and technologies used.

**Parameters:**
- `repoPath` (string): Path to the repository

**Returns:** Detected frameworks categorized by type.

### `find_config_files`
Find and categorize configuration files.

**Parameters:**
- `repoPath` (string): Path to the repository

**Returns:** Configuration files organized by category.

### `identify_entry_points`
Identify application entry points.

**Parameters:**
- `repoPath` (string): Path to the repository

**Returns:** Array of identified entry points.

## Usage Example

```bash
# Start the MCP server
node dist/index.js

# The server will communicate via stdio with the MCP client
```

## Integration with CodeUnderstandingAgent

This server is designed to work with the CodeUnderstandingAgent for Auckland Library's legacy system analysis:

1. **Repository Discovery**: Use `analyze_structure` to get overall repository metrics
2. **Code Organization**: Use `classify_files` and `get_file_tree` to understand code organization
3. **Technology Stack**: Use `detect_frameworks` to identify current technologies
4. **Migration Planning**: Use `identify_entry_points` and `find_config_files` to plan modernization
5. **Team Context**: Use `get_contributors` and `get_commit_history` to understand development history

## Performance

- Repository analysis completes within 30 seconds for typical legacy repositories
- Supports repositories up to 100K lines of code
- Memory efficient file tree traversal with configurable depth limits
- Optimized for Auckland Library's specific technology stack

## Error Handling

The server provides comprehensive error handling for:
- Invalid repository paths
- Permission issues
- Corrupted Git repositories
- Large file handling
- Network timeouts

All errors include descriptive messages to help with troubleshooting.