#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';

import { RepoAnalyzer } from './analyzer/RepoAnalyzer.js';
import { 
  RepositoryStructure, 
  FileTree, 
  FileClassification,
  CommitHistory,
  BranchAnalysis,
  ContributorStats,
  FrameworkDetection,
  ConfigFileMap,
  EntryPoint
} from '../../shared/types/index.js';

class RepoMCPServer {
  private server: Server;
  private analyzer: RepoAnalyzer;

  constructor() {
    this.server = new Server(
      {
        name: 'repo-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.analyzer = new RepoAnalyzer();
    this.setupToolHandlers();
  }

  private setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'analyze_structure',
            description: 'Analyze repository structure and get comprehensive metrics',
            inputSchema: {
              type: 'object',
              properties: {
                repoPath: {
                  type: 'string',
                  description: 'Path to the repository to analyze',
                },
              },
              required: ['repoPath'],
            },
          },
          {
            name: 'get_file_tree',
            description: 'Get hierarchical file tree of the repository',
            inputSchema: {
              type: 'object',
              properties: {
                repoPath: {
                  type: 'string',
                  description: 'Path to the repository',
                },
                maxDepth: {
                  type: 'number',
                  description: 'Maximum depth to traverse (optional)',
                },
              },
              required: ['repoPath'],
            },
          },
          {
            name: 'classify_files',
            description: 'Classify files by their purpose (source, config, docs, etc.)',
            inputSchema: {
              type: 'object',
              properties: {
                repoPath: {
                  type: 'string',
                  description: 'Path to the repository',
                },
              },
              required: ['repoPath'],
            },
          },
          {
            name: 'get_commit_history',
            description: 'Get commit history with statistics',
            inputSchema: {
              type: 'object',
              properties: {
                repoPath: {
                  type: 'string',
                  description: 'Path to the repository',
                },
                limit: {
                  type: 'number',
                  description: 'Maximum number of commits to return (optional)',
                },
              },
              required: ['repoPath'],
            },
          },
          {
            name: 'analyze_branches',
            description: 'Analyze branch structure and status',
            inputSchema: {
              type: 'object',
              properties: {
                repoPath: {
                  type: 'string',
                  description: 'Path to the repository',
                },
              },
              required: ['repoPath'],
            },
          },
          {
            name: 'get_contributors',
            description: 'Get contributor statistics',
            inputSchema: {
              type: 'object',
              properties: {
                repoPath: {
                  type: 'string',
                  description: 'Path to the repository',
                },
              },
              required: ['repoPath'],
            },
          },
          {
            name: 'detect_frameworks',
            description: 'Detect frameworks and technologies used',
            inputSchema: {
              type: 'object',
              properties: {
                repoPath: {
                  type: 'string',
                  description: 'Path to the repository',
                },
              },
              required: ['repoPath'],
            },
          },
          {
            name: 'find_config_files',
            description: 'Find and categorize configuration files',
            inputSchema: {
              type: 'object',
              properties: {
                repoPath: {
                  type: 'string',
                  description: 'Path to the repository',
                },
              },
              required: ['repoPath'],
            },
          },
          {
            name: 'identify_entry_points',
            description: 'Identify application entry points',
            inputSchema: {
              type: 'object',
              properties: {
                repoPath: {
                  type: 'string',
                  description: 'Path to the repository',
                },
              },
              required: ['repoPath'],
            },
          },
        ] as Tool[],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'analyze_structure':
            return await this.handleAnalyzeStructure(args as { repoPath: string });

          case 'get_file_tree':
            return await this.handleGetFileTree(args as { repoPath: string; maxDepth?: number });

          case 'classify_files':
            return await this.handleClassifyFiles(args as { repoPath: string });

          case 'get_commit_history':
            return await this.handleGetCommitHistory(args as { repoPath: string; limit?: number });

          case 'analyze_branches':
            return await this.handleAnalyzeBranches(args as { repoPath: string });

          case 'get_contributors':
            return await this.handleGetContributors(args as { repoPath: string });

          case 'detect_frameworks':
            return await this.handleDetectFrameworks(args as { repoPath: string });

          case 'find_config_files':
            return await this.handleFindConfigFiles(args as { repoPath: string });

          case 'identify_entry_points':
            return await this.handleIdentifyEntryPoints(args as { repoPath: string });

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  private async handleAnalyzeStructure(args: { repoPath: string }) {
    const result = await this.analyzer.analyzeStructure(args.repoPath);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async handleGetFileTree(args: { repoPath: string; maxDepth?: number }) {
    const result = await this.analyzer.getFileTree(args.repoPath, args.maxDepth);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async handleClassifyFiles(args: { repoPath: string }) {
    const result = await this.analyzer.classifyFiles(args.repoPath);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async handleGetCommitHistory(args: { repoPath: string; limit?: number }) {
    const result = await this.analyzer.getCommitHistory(args.repoPath, args.limit);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async handleAnalyzeBranches(args: { repoPath: string }) {
    const result = await this.analyzer.analyzeBranches(args.repoPath);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async handleGetContributors(args: { repoPath: string }) {
    const result = await this.analyzer.getContributors(args.repoPath);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async handleDetectFrameworks(args: { repoPath: string }) {
    const result = await this.analyzer.detectFrameworks(args.repoPath);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async handleFindConfigFiles(args: { repoPath: string }) {
    const result = await this.analyzer.findConfigFiles(args.repoPath);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  private async handleIdentifyEntryPoints(args: { repoPath: string }) {
    const result = await this.analyzer.identifyEntryPoints(args.repoPath);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    
    // Cleanup on process termination
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }
}

// Start the server
const server = new RepoMCPServer();
server.run().catch((error) => {
  console.error('Failed to run server:', error);
  process.exit(1);
});