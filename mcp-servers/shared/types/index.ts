// Shared types for MCP servers

export interface Location {
  line: number;
  column: number;
}

export interface LanguageStats {
  language: string;
  files: number;
  lines: number;
  bytes: number;
  percentage: number;
}

export interface ComplexityMetrics {
  cyclomaticComplexity: number;
  cognitiveComplexity: number;
  maintainabilityIndex: number;
}

export interface ArchitecturePattern {
  type: 'monolith' | 'layered' | 'microservices' | 'mvc' | 'unknown';
  confidence: number;
  indicators: string[];
}

// Repository Analysis Types
export interface RepositoryStructure {
  totalFiles: number;
  totalDirectories: number;
  totalSize: number; // in bytes
  languages: LanguageStats[];
  architecture: ArchitecturePattern;
  complexity: ComplexityMetrics;
  lastModified: Date;
}

export interface FileTree {
  name: string;
  type: 'file' | 'directory';
  path: string;
  size?: number;
  lastModified?: Date;
  children?: FileTree[];
}

export interface FileClassification {
  source: string[];
  config: string[];
  documentation: string[];
  tests: string[];
  build: string[];
  assets: string[];
  unknown: string[];
}

export interface CommitHistory {
  hash: string;
  message: string;
  author: string;
  date: Date;
  filesChanged: number;
  insertions: number;
  deletions: number;
}

export interface BranchAnalysis {
  activeBranches: string[];
  staleBranches: string[];
  defaultBranch: string;
  totalBranches: number;
}

export interface ContributorStats {
  name: string;
  email: string;
  commits: number;
  linesAdded: number;
  linesRemoved: number;
  firstCommit: Date;
  lastCommit: Date;
}

export interface FrameworkDetection {
  frontend: DetectedFramework[];
  backend: DetectedFramework[];
  database: DetectedFramework[];
  testing: DetectedFramework[];
  buildTools: DetectedFramework[];
}

export interface DetectedFramework {
  name: string;
  version?: string;
  confidence: number;
  evidence: string[];
}

export interface ConfigFileMap {
  [category: string]: ConfigFile[];
}

export interface ConfigFile {
  path: string;
  type: string;
  purpose: string;
}

export interface EntryPoint {
  path: string;
  type: 'main' | 'server' | 'cli' | 'web' | 'test';
  framework?: string;
  description: string;
}