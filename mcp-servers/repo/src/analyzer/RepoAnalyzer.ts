import simpleGit, { SimpleGit, LogResult } from 'simple-git';
import { promises as fs } from 'fs';
import path from 'path';
import { glob } from 'glob';
import mimeTypes from 'mime-types';

import {
  RepositoryStructure,
  FileTree,
  FileClassification,
  CommitHistory,
  BranchAnalysis,
  ContributorStats,
  FrameworkDetection,
  ConfigFileMap,
  EntryPoint,
  LanguageStats,
  ArchitecturePattern,
  ComplexityMetrics,
  DetectedFramework,
  ConfigFile
} from '../../../shared/types/index.js';

export class RepoAnalyzer {
  private git: SimpleGit | null = null;

  private getGitInstance(repoPath: string): SimpleGit {
    if (!this.git || this.git.cwd !== repoPath) {
      this.git = simpleGit(repoPath);
    }
    return this.git;
  }

  async analyzeStructure(repoPath: string): Promise<RepositoryStructure> {
    try {
      await this.validateRepository(repoPath);
      
      const [languages, fileTree, complexity] = await Promise.all([
        this.analyzeLanguages(repoPath),
        this.getFileTree(repoPath),
        this.analyzeComplexity(repoPath)
      ]);

      const architecture = await this.detectArchitecturePattern(repoPath);
      
      return {
        totalFiles: this.countFiles(fileTree),
        totalDirectories: this.countDirectories(fileTree),
        totalSize: await this.calculateTotalSize(repoPath),
        languages,
        architecture,
        complexity,
        lastModified: await this.getLastModified(repoPath)
      };
    } catch (error) {
      throw new Error(`Failed to analyze repository structure: ${error.message}`);
    }
  }

  async getFileTree(repoPath: string, maxDepth?: number): Promise<FileTree> {
    try {
      await this.validateRepository(repoPath);
      return await this.buildFileTree(repoPath, maxDepth || 10);
    } catch (error) {
      throw new Error(`Failed to get file tree: ${error.message}`);
    }
  }

  async classifyFiles(repoPath: string): Promise<FileClassification> {
    try {
      await this.validateRepository(repoPath);
      
      const files = await glob('**/*', { 
        cwd: repoPath, 
        dot: true,
        ignore: ['.git/**', 'node_modules/**', '.DS_Store']
      });

      const classification: FileClassification = {
        source: [],
        config: [],
        documentation: [],
        tests: [],
        build: [],
        assets: [],
        unknown: []
      };

      for (const file of files) {
        const filePath = path.join(repoPath, file);
        const stats = await fs.stat(filePath);
        
        if (stats.isFile()) {
          this.classifyFile(file, classification);
        }
      }

      return classification;
    } catch (error) {
      throw new Error(`Failed to classify files: ${error.message}`);
    }
  }

  async getCommitHistory(repoPath: string, limit: number = 100): Promise<CommitHistory[]> {
    try {
      const git = this.getGitInstance(repoPath);
      const log = await git.log({ maxCount: limit, format: 'fuller' });
      
      const commits: CommitHistory[] = [];
      
      for (const commit of log.all) {
        const stats = await git.show(['--stat', '--format=', commit.hash]);
        const { insertions, deletions, filesChanged } = this.parseGitStats(stats);
        
        commits.push({
          hash: commit.hash,
          message: commit.message,
          author: commit.author_name,
          date: new Date(commit.date),
          filesChanged,
          insertions,
          deletions
        });
      }
      
      return commits;
    } catch (error) {
      throw new Error(`Failed to get commit history: ${error.message}`);
    }
  }

  async analyzeBranches(repoPath: string): Promise<BranchAnalysis> {
    try {
      const git = this.getGitInstance(repoPath);
      
      const [branches, remotes] = await Promise.all([
        git.branchLocal(),
        git.branch(['-r'])
      ]);

      const now = new Date();
      const staleBranches: string[] = [];
      const activeBranches: string[] = [];

      // Check branch activity (simplified - in production you'd check last commit dates)
      for (const branch of branches.all) {
        if (branch === branches.current) {
          activeBranches.push(branch);
        } else {
          // For now, consider non-current branches as potentially stale
          // In a real implementation, check last commit date
          staleBranches.push(branch);
        }
      }

      return {
        activeBranches,
        staleBranches,
        defaultBranch: branches.current || 'main',
        totalBranches: branches.all.length
      };
    } catch (error) {
      throw new Error(`Failed to analyze branches: ${error.message}`);
    }
  }

  async getContributors(repoPath: string): Promise<ContributorStats[]> {
    try {
      const git = this.getGitInstance(repoPath);
      const log = await git.log({ format: 'fuller' });
      
      const contributors = new Map<string, ContributorStats>();
      
      for (const commit of log.all) {
        const key = `${commit.author_name}<${commit.author_email}>`;
        const existing = contributors.get(key);
        const commitDate = new Date(commit.date);
        
        if (existing) {
          existing.commits++;
          if (commitDate < existing.firstCommit) existing.firstCommit = commitDate;
          if (commitDate > existing.lastCommit) existing.lastCommit = commitDate;
        } else {
          contributors.set(key, {
            name: commit.author_name,
            email: commit.author_email,
            commits: 1,
            linesAdded: 0, // Would need additional parsing for accurate stats
            linesRemoved: 0,
            firstCommit: commitDate,
            lastCommit: commitDate
          });
        }
      }
      
      return Array.from(contributors.values()).sort((a, b) => b.commits - a.commits);
    } catch (error) {
      throw new Error(`Failed to get contributors: ${error.message}`);
    }
  }

  async detectFrameworks(repoPath: string): Promise<FrameworkDetection> {
    try {
      await this.validateRepository(repoPath);
      
      const [packageJson, requirements, gemfile, composerJson, buildFiles] = await Promise.all([
        this.readFileIfExists(path.join(repoPath, 'package.json')),
        this.readFileIfExists(path.join(repoPath, 'requirements.txt')),
        this.readFileIfExists(path.join(repoPath, 'Gemfile')),
        this.readFileIfExists(path.join(repoPath, 'composer.json')),
        this.findBuildFiles(repoPath)
      ]);

      return {
        frontend: this.detectFrontendFrameworks(packageJson, repoPath),
        backend: this.detectBackendFrameworks(packageJson, requirements, gemfile, composerJson),
        database: this.detectDatabases(packageJson, requirements, repoPath),
        testing: this.detectTestingFrameworks(packageJson, requirements, repoPath),
        buildTools: this.detectBuildTools(packageJson, buildFiles, repoPath)
      };
    } catch (error) {
      throw new Error(`Failed to detect frameworks: ${error.message}`);
    }
  }

  async findConfigFiles(repoPath: string): Promise<ConfigFileMap> {
    try {
      await this.validateRepository(repoPath);
      
      const configPatterns = [
        '**/*.config.{js,ts,json}',
        '**/.{env,env.*}',
        '**/webpack.config.*',
        '**/babel.config.*',
        '**/tsconfig.json',
        '**/package.json',
        '**/composer.json',
        '**/Gemfile',
        '**/requirements.txt',
        '**/docker-compose.yml',
        '**/Dockerfile',
        '**/*.yml',
        '**/*.yaml',
        '**/*.properties',
        '**/*.ini'
      ];

      const files = await glob(configPatterns, {
        cwd: repoPath,
        ignore: ['node_modules/**', '.git/**']
      });

      const configMap: ConfigFileMap = {};

      for (const file of files) {
        const category = this.categorizeConfigFile(file);
        if (!configMap[category]) {
          configMap[category] = [];
        }
        
        configMap[category].push({
          path: file,
          type: path.extname(file).slice(1) || 'unknown',
          purpose: this.getConfigPurpose(file)
        });
      }

      return configMap;
    } catch (error) {
      throw new Error(`Failed to find config files: ${error.message}`);
    }
  }

  async identifyEntryPoints(repoPath: string): Promise<EntryPoint[]> {
    try {
      await this.validateRepository(repoPath);
      
      const entryPoints: EntryPoint[] = [];
      
      // Check package.json for entry points
      const packageJsonPath = path.join(repoPath, 'package.json');
      const packageJson = await this.readFileIfExists(packageJsonPath);
      
      if (packageJson) {
        const pkg = JSON.parse(packageJson);
        if (pkg.main) {
          entryPoints.push({
            path: pkg.main,
            type: 'main',
            framework: this.detectFrameworkFromFile(pkg.main),
            description: 'Main entry point from package.json'
          });
        }
        if (pkg.bin) {
          const bins = typeof pkg.bin === 'string' ? { [pkg.name]: pkg.bin } : pkg.bin;
          Object.entries(bins).forEach(([name, binPath]) => {
            entryPoints.push({
              path: binPath as string,
              type: 'cli',
              description: `CLI entry point: ${name}`
            });
          });
        }
      }

      // Look for common entry point patterns
      const commonEntryPoints = [
        { pattern: 'index.{js,ts}', type: 'main' as const },
        { pattern: 'app.{js,ts}', type: 'web' as const },
        { pattern: 'server.{js,ts}', type: 'server' as const },
        { pattern: 'main.{js,ts,py}', type: 'main' as const },
        { pattern: '__main__.py', type: 'main' as const }
      ];

      for (const { pattern, type } of commonEntryPoints) {
        const files = await glob(pattern, { cwd: repoPath });
        files.forEach(file => {
          if (!entryPoints.some(ep => ep.path === file)) {
            entryPoints.push({
              path: file,
              type,
              framework: this.detectFrameworkFromFile(file),
              description: `Detected ${type} entry point`
            });
          }
        });
      }

      return entryPoints;
    } catch (error) {
      throw new Error(`Failed to identify entry points: ${error.message}`);
    }
  }

  // Private helper methods
  private async validateRepository(repoPath: string): Promise<void> {
    try {
      const stats = await fs.stat(repoPath);
      if (!stats.isDirectory()) {
        throw new Error('Path is not a directory');
      }
    } catch (error) {
      throw new Error(`Invalid repository path: ${repoPath}`);
    }
  }

  private async buildFileTree(dirPath: string, maxDepth: number, currentDepth = 0): Promise<FileTree> {
    const stats = await fs.stat(dirPath);
    const name = path.basename(dirPath);
    
    if (stats.isFile()) {
      return {
        name,
        type: 'file',
        path: dirPath,
        size: stats.size,
        lastModified: stats.mtime
      };
    }

    const tree: FileTree = {
      name,
      type: 'directory',
      path: dirPath,
      lastModified: stats.mtime,
      children: []
    };

    if (currentDepth < maxDepth) {
      try {
        const entries = await fs.readdir(dirPath);
        const children = await Promise.all(
          entries
            .filter(entry => !entry.startsWith('.git') && entry !== 'node_modules')
            .map(async entry => {
              const fullPath = path.join(dirPath, entry);
              return await this.buildFileTree(fullPath, maxDepth, currentDepth + 1);
            })
        );
        tree.children = children.sort((a, b) => {
          if (a.type !== b.type) return a.type === 'directory' ? -1 : 1;
          return a.name.localeCompare(b.name);
        });
      } catch (error) {
        // Skip directories we can't read
      }
    }

    return tree;
  }

  private countFiles(tree: FileTree): number {
    if (tree.type === 'file') return 1;
    return (tree.children || []).reduce((sum, child) => sum + this.countFiles(child), 0);
  }

  private countDirectories(tree: FileTree): number {
    if (tree.type === 'file') return 0;
    return 1 + (tree.children || []).reduce((sum, child) => sum + this.countDirectories(child), 0);
  }

  private async calculateTotalSize(repoPath: string): Promise<number> {
    const files = await glob('**/*', { 
      cwd: repoPath, 
      nodir: true,
      ignore: ['.git/**', 'node_modules/**']
    });
    
    let totalSize = 0;
    for (const file of files) {
      try {
        const stats = await fs.stat(path.join(repoPath, file));
        totalSize += stats.size;
      } catch {
        // Skip files we can't stat
      }
    }
    
    return totalSize;
  }

  private async getLastModified(repoPath: string): Promise<Date> {
    try {
      const git = this.getGitInstance(repoPath);
      const log = await git.log({ maxCount: 1 });
      return new Date(log.latest?.date || Date.now());
    } catch {
      const stats = await fs.stat(repoPath);
      return stats.mtime;
    }
  }

  private async analyzeLanguages(repoPath: string): Promise<LanguageStats[]> {
    const files = await glob('**/*', {
      cwd: repoPath,
      nodir: true,
      ignore: ['.git/**', 'node_modules/**', 'dist/**', 'build/**']
    });

    const languageMap = new Map<string, { files: number; lines: number; bytes: number }>();
    let totalBytes = 0;

    for (const file of files) {
      const filePath = path.join(repoPath, file);
      const ext = path.extname(file).toLowerCase();
      const language = this.getLanguageFromExtension(ext);
      
      try {
        const stats = await fs.stat(filePath);
        const content = await fs.readFile(filePath, 'utf-8');
        const lines = content.split('\n').length;
        
        const existing = languageMap.get(language) || { files: 0, lines: 0, bytes: 0 };
        languageMap.set(language, {
          files: existing.files + 1,
          lines: existing.lines + lines,
          bytes: existing.bytes + stats.size
        });
        
        totalBytes += stats.size;
      } catch {
        // Skip files we can't read
      }
    }

    return Array.from(languageMap.entries())
      .map(([language, stats]) => ({
        language,
        files: stats.files,
        lines: stats.lines,
        bytes: stats.bytes,
        percentage: totalBytes > 0 ? (stats.bytes / totalBytes) * 100 : 0
      }))
      .sort((a, b) => b.bytes - a.bytes);
  }

  private getLanguageFromExtension(ext: string): string {
    const languageMap: { [key: string]: string } = {
      '.js': 'JavaScript',
      '.ts': 'TypeScript',
      '.py': 'Python',
      '.java': 'Java',
      '.rb': 'Ruby',
      '.php': 'PHP',
      '.go': 'Go',
      '.rs': 'Rust',
      '.cpp': 'C++',
      '.c': 'C',
      '.cs': 'C#',
      '.html': 'HTML',
      '.css': 'CSS',
      '.scss': 'SCSS',
      '.less': 'LESS',
      '.json': 'JSON',
      '.xml': 'XML',
      '.yml': 'YAML',
      '.yaml': 'YAML',
      '.md': 'Markdown',
      '.sh': 'Shell',
      '.sql': 'SQL'
    };
    
    return languageMap[ext] || 'Other';
  }

  private async analyzeComplexity(repoPath: string): Promise<ComplexityMetrics> {
    // Simplified complexity analysis - in production you'd use proper AST analysis
    return {
      cyclomaticComplexity: 1, // Would calculate from control flow
      cognitiveComplexity: 1,  // Would calculate from nested structures
      maintainabilityIndex: 85 // Would calculate from various metrics
    };
  }

  private async detectArchitecturePattern(repoPath: string): Promise<ArchitecturePattern> {
    const indicators: string[] = [];
    let type: ArchitecturePattern['type'] = 'unknown';
    let confidence = 0;

    // Check for common patterns
    const packageJsonPath = path.join(repoPath, 'package.json');
    const packageJson = await this.readFileIfExists(packageJsonPath);
    
    if (packageJson) {
      const pkg = JSON.parse(packageJson);
      
      if (pkg.dependencies?.express || pkg.dependencies?.koa) {
        indicators.push('Express/Koa server found');
        type = 'layered';
        confidence += 30;
      }
      
      if (pkg.dependencies?.react || pkg.dependencies?.vue || pkg.dependencies?.angular) {
        indicators.push('Frontend framework found');
        confidence += 20;
      }
    }

    // Check directory structure
    const dirs = await glob('*/', { cwd: repoPath });
    if (dirs.includes('src/') && dirs.includes('public/')) {
      indicators.push('Typical web app structure');
      type = 'mvc';
      confidence += 25;
    }

    return { type, confidence: Math.min(confidence, 100), indicators };
  }

  private classifyFile(filePath: string, classification: FileClassification): void {
    const ext = path.extname(filePath).toLowerCase();
    const basename = path.basename(filePath).toLowerCase();
    
    // Source files
    if (['.js', '.ts', '.py', '.java', '.rb', '.php', '.go', '.rs', '.cpp', '.c', '.cs'].includes(ext)) {
      classification.source.push(filePath);
    }
    // Test files
    else if (basename.includes('test') || basename.includes('spec') || filePath.includes('/test/') || filePath.includes('/tests/')) {
      classification.tests.push(filePath);
    }
    // Documentation
    else if (['.md', '.txt', '.rst'].includes(ext) || basename.includes('readme') || basename.includes('changelog')) {
      classification.documentation.push(filePath);
    }
    // Config files
    else if (['.json', '.yml', '.yaml', '.xml', '.ini', '.env', '.config'].includes(ext) || basename.includes('config')) {
      classification.config.push(filePath);
    }
    // Build files
    else if (basename.includes('makefile') || basename.includes('dockerfile') || basename.includes('webpack') || basename.includes('build')) {
      classification.build.push(filePath);
    }
    // Assets
    else if (['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.css', '.scss', '.less'].includes(ext)) {
      classification.assets.push(filePath);
    }
    else {
      classification.unknown.push(filePath);
    }
  }

  private parseGitStats(stats: string): { insertions: number; deletions: number; filesChanged: number } {
    const lines = stats.trim().split('\n');
    const summaryLine = lines.find(line => line.includes('changed') || line.includes('insertion') || line.includes('deletion'));
    
    if (!summaryLine) {
      return { insertions: 0, deletions: 0, filesChanged: 0 };
    }

    const filesMatch = summaryLine.match(/(\d+)\s+files?\s+changed/);
    const insertionsMatch = summaryLine.match(/(\d+)\s+insertions?\(\+\)/);
    const deletionsMatch = summaryLine.match(/(\d+)\s+deletions?\(-\)/);

    return {
      filesChanged: filesMatch ? parseInt(filesMatch[1]) : 0,
      insertions: insertionsMatch ? parseInt(insertionsMatch[1]) : 0,
      deletions: deletionsMatch ? parseInt(deletionsMatch[1]) : 0
    };
  }

  private async readFileIfExists(filePath: string): Promise<string | null> {
    try {
      return await fs.readFile(filePath, 'utf-8');
    } catch {
      return null;
    }
  }

  private detectFrontendFrameworks(packageJson: string | null, repoPath: string): DetectedFramework[] {
    if (!packageJson) return [];
    
    try {
      const pkg = JSON.parse(packageJson);
      const frameworks: DetectedFramework[] = [];
      const deps = { ...pkg.dependencies, ...pkg.devDependencies };
      
      const frameworkMap = {
        react: { name: 'React', keywords: ['react'] },
        vue: { name: 'Vue.js', keywords: ['vue'] },
        angular: { name: 'Angular', keywords: ['@angular/core'] },
        svelte: { name: 'Svelte', keywords: ['svelte'] },
        'next.js': { name: 'Next.js', keywords: ['next'] },
        'nuxt.js': { name: 'Nuxt.js', keywords: ['nuxt'] }
      };
      
      Object.entries(frameworkMap).forEach(([key, framework]) => {
        const found = framework.keywords.find(keyword => deps[keyword]);
        if (found) {
          frameworks.push({
            name: framework.name,
            version: deps[found],
            confidence: 90,
            evidence: [`Found ${found} in package.json`]
          });
        }
      });
      
      return frameworks;
    } catch {
      return [];
    }
  }

  private detectBackendFrameworks(
    packageJson: string | null, 
    requirements: string | null, 
    gemfile: string | null, 
    composerJson: string | null
  ): DetectedFramework[] {
    const frameworks: DetectedFramework[] = [];
    
    // Node.js frameworks
    if (packageJson) {
      try {
        const pkg = JSON.parse(packageJson);
        const deps = { ...pkg.dependencies, ...pkg.devDependencies };
        
        if (deps.express) {
          frameworks.push({
            name: 'Express.js',
            version: deps.express,
            confidence: 95,
            evidence: ['express found in package.json']
          });
        }
        if (deps.koa) {
          frameworks.push({
            name: 'Koa.js',
            version: deps.koa,
            confidence: 95,
            evidence: ['koa found in package.json']
          });
        }
      } catch {}
    }
    
    // Python frameworks
    if (requirements) {
      if (requirements.includes('django')) {
        frameworks.push({
          name: 'Django',
          confidence: 90,
          evidence: ['django found in requirements.txt']
        });
      }
      if (requirements.includes('flask')) {
        frameworks.push({
          name: 'Flask',
          confidence: 90,
          evidence: ['flask found in requirements.txt']
        });
      }
    }
    
    return frameworks;
  }

  private detectDatabases(packageJson: string | null, requirements: string | null, repoPath: string): DetectedFramework[] {
    const databases: DetectedFramework[] = [];
    
    if (packageJson) {
      try {
        const pkg = JSON.parse(packageJson);
        const deps = { ...pkg.dependencies, ...pkg.devDependencies };
        
        const dbMap = {
          mongoose: 'MongoDB',
          mysql: 'MySQL',
          pg: 'PostgreSQL',
          sqlite3: 'SQLite',
          redis: 'Redis'
        };
        
        Object.entries(dbMap).forEach(([dep, dbName]) => {
          if (deps[dep]) {
            databases.push({
              name: dbName,
              version: deps[dep],
              confidence: 85,
              evidence: [`${dep} found in package.json`]
            });
          }
        });
      } catch {}
    }
    
    return databases;
  }

  private detectTestingFrameworks(packageJson: string | null, requirements: string | null, repoPath: string): DetectedFramework[] {
    const frameworks: DetectedFramework[] = [];
    
    if (packageJson) {
      try {
        const pkg = JSON.parse(packageJson);
        const deps = { ...pkg.dependencies, ...pkg.devDependencies };
        
        const testFrameworks = {
          jest: 'Jest',
          mocha: 'Mocha',
          jasmine: 'Jasmine',
          cypress: 'Cypress',
          '@testing-library/react': 'React Testing Library'
        };
        
        Object.entries(testFrameworks).forEach(([dep, name]) => {
          if (deps[dep]) {
            frameworks.push({
              name,
              version: deps[dep],
              confidence: 90,
              evidence: [`${dep} found in package.json`]
            });
          }
        });
      } catch {}
    }
    
    return frameworks;
  }

  private detectBuildTools(packageJson: string | null, buildFiles: string[], repoPath: string): DetectedFramework[] {
    const tools: DetectedFramework[] = [];
    
    if (packageJson) {
      try {
        const pkg = JSON.parse(packageJson);
        const deps = { ...pkg.dependencies, ...pkg.devDependencies };
        
        const buildTools = {
          webpack: 'Webpack',
          vite: 'Vite',
          rollup: 'Rollup',
          parcel: 'Parcel',
          gulp: 'Gulp',
          grunt: 'Grunt'
        };
        
        Object.entries(buildTools).forEach(([dep, name]) => {
          if (deps[dep]) {
            tools.push({
              name,
              version: deps[dep],
              confidence: 90,
              evidence: [`${dep} found in package.json`]
            });
          }
        });
      } catch {}
    }
    
    return tools;
  }

  private async findBuildFiles(repoPath: string): Promise<string[]> {
    return await glob([
      'webpack.config.*',
      'rollup.config.*',
      'vite.config.*',
      'gulpfile.*',
      'Gruntfile.*',
      'Makefile',
      'build.gradle',
      'pom.xml'
    ], { cwd: repoPath });
  }

  private categorizeConfigFile(filePath: string): string {
    const basename = path.basename(filePath).toLowerCase();
    
    if (basename.includes('docker')) return 'Docker';
    if (basename.includes('webpack') || basename.includes('rollup') || basename.includes('vite')) return 'Build';
    if (basename.includes('babel') || basename.includes('eslint') || basename.includes('prettier')) return 'Development';
    if (basename.includes('test') || basename.includes('jest') || basename.includes('cypress')) return 'Testing';
    if (basename.includes('env') || basename.includes('environment')) return 'Environment';
    if (basename === 'package.json' || basename === 'composer.json') return 'Package Manager';
    if (['.yml', '.yaml'].includes(path.extname(filePath))) return 'YAML Config';
    
    return 'General';
  }

  private getConfigPurpose(filePath: string): string {
    const basename = path.basename(filePath).toLowerCase();
    
    const purposeMap: { [key: string]: string } = {
      'package.json': 'Node.js package configuration',
      'composer.json': 'PHP package configuration',
      'webpack.config.js': 'Webpack build configuration',
      'tsconfig.json': 'TypeScript configuration',
      '.env': 'Environment variables',
      'docker-compose.yml': 'Docker composition',
      'dockerfile': 'Docker container configuration'
    };
    
    return purposeMap[basename] || 'Configuration file';
  }

  private detectFrameworkFromFile(filePath: string): string | undefined {
    const ext = path.extname(filePath);
    if (['.js', '.ts'].includes(ext)) return 'JavaScript/TypeScript';
    if (ext === '.py') return 'Python';
    return undefined;
  }
}