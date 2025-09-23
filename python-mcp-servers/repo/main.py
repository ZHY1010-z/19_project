#!/usr/bin/env python3
"""
Repo MCP Server - Repository Analysis and Structure Mapping

This MCP server provides comprehensive repository analysis capabilities 
for the Auckland Library legacy system modernization project.

Usage:
    python main.py

The server communicates via stdio with MCP clients (like Claude).
"""

import asyncio
import logging
from typing import Any, Dict, List

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from repo_analyzer import RepoAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("repo-mcp-server")

class RepoMCPServer:
    """MCP Server for repository analysis and structure mapping."""
    
    def __init__(self):
        self.server = Server("repo-mcp-server")
        self.analyzer = RepoAnalyzer()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available tools."""
            return [
                types.Tool(
                    name="analyze_structure",
                    description="Analyze repository structure and get comprehensive metrics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {
                                "type": "string",
                                "description": "Path to the repository to analyze"
                            }
                        },
                        "required": ["repo_path"]
                    }
                ),
                types.Tool(
                    name="get_file_tree", 
                    description="Get hierarchical file tree of the repository",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {
                                "type": "string",
                                "description": "Path to the repository"
                            },
                            "max_depth": {
                                "type": "integer",
                                "description": "Maximum depth to traverse (optional)",
                                "default": 10
                            }
                        },
                        "required": ["repo_path"]
                    }
                ),
                types.Tool(
                    name="classify_files",
                    description="Classify files by their purpose (source, config, docs, etc.)",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "repo_path": {
                                "type": "string",
                                "description": "Path to the repository"
                            }
                        },
                        "required": ["repo_path"]
                    }
                ),
                types.Tool(
                    name="get_commit_history",
                    description="Get commit history with statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {
                                "type": "string", 
                                "description": "Path to the repository"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of commits to return (optional)",
                                "default": 100
                            }
                        },
                        "required": ["repo_path"]
                    }
                ),
                types.Tool(
                    name="analyze_branches",
                    description="Analyze branch structure and status",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {
                                "type": "string",
                                "description": "Path to the repository" 
                            }
                        },
                        "required": ["repo_path"]
                    }
                ),
                types.Tool(
                    name="get_contributors",
                    description="Get contributor statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {
                                "type": "string",
                                "description": "Path to the repository"
                            }
                        },
                        "required": ["repo_path"]
                    }
                ),
                types.Tool(
                    name="detect_frameworks",
                    description="Detect frameworks and technologies used",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {
                                "type": "string",
                                "description": "Path to the repository"
                            }
                        },
                        "required": ["repo_path"]
                    }
                ),
                types.Tool(
                    name="find_config_files",
                    description="Find and categorize configuration files", 
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {
                                "type": "string",
                                "description": "Path to the repository"
                            }
                        },
                        "required": ["repo_path"]
                    }
                ),
                types.Tool(
                    name="identify_entry_points",
                    description="Identify application entry points",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repo_path": {
                                "type": "string", 
                                "description": "Path to the repository"
                            }
                        },
                        "required": ["repo_path"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> List[types.TextContent]:
            """Handle tool calls."""
            
            try:
                if name == "analyze_structure":
                    result = await self.analyzer.analyze_structure(arguments["repo_path"])
                    
                elif name == "get_file_tree":
                    max_depth = arguments.get("max_depth", 10)
                    result = await self.analyzer.get_file_tree(arguments["repo_path"], max_depth)
                    
                elif name == "classify_files":
                    result = await self.analyzer.classify_files(arguments["repo_path"])
                    
                elif name == "get_commit_history":
                    limit = arguments.get("limit", 100)
                    result = await self.analyzer.get_commit_history(arguments["repo_path"], limit)
                    
                elif name == "analyze_branches":
                    result = await self.analyzer.analyze_branches(arguments["repo_path"])
                    
                elif name == "get_contributors":
                    result = await self.analyzer.get_contributors(arguments["repo_path"])
                    
                elif name == "detect_frameworks":
                    result = await self.analyzer.detect_frameworks(arguments["repo_path"])
                    
                elif name == "find_config_files":
                    result = await self.analyzer.find_config_files(arguments["repo_path"])
                    
                elif name == "identify_entry_points":
                    result = await self.analyzer.identify_entry_points(arguments["repo_path"])
                    
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                # Convert result to JSON string
                import orjson
                result_json = orjson.dumps(result, default=str, option=orjson.OPT_INDENT_2).decode()
                
                return [types.TextContent(type="text", text=result_json)]
                
            except Exception as e:
                error_msg = f"Error executing {name}: {str(e)}"
                logger.error(error_msg)
                return [types.TextContent(type="text", text=error_msg)]

    async def run(self):
        """Run the MCP server."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="repo-mcp-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


async def main():
    """Main entry point."""
    server = RepoMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())