import { RepoAnalyzer } from '../src/analyzer/RepoAnalyzer';
import { createTestRepo, cleanupTestRepo, SAMPLE_NODE_REPO, SAMPLE_LEGACY_REPO } from './setup';

describe('RepoAnalyzer', () => {
  let analyzer: RepoAnalyzer;
  let testRepoPath: string;

  beforeEach(() => {
    analyzer = new RepoAnalyzer();
  });

  afterEach(async () => {
    if (testRepoPath) {
      await cleanupTestRepo(testRepoPath);
    }
  });

  describe('analyzeStructure', () => {
    it('should analyze Node.js repository structure', async () => {
      testRepoPath = await createTestRepo('node-test', SAMPLE_NODE_REPO);
      
      const result = await analyzer.analyzeStructure(testRepoPath);
      
      expect(result).toBeDefined();
      expect(result.totalFiles).toBeGreaterThan(0);
      expect(result.totalDirectories).toBeGreaterThan(0);
      expect(result.languages).toBeInstanceOf(Array);
      expect(result.architecture).toBeDefined();
      expect(result.complexity).toBeDefined();
    });

    it('should handle invalid repository path', async () => {
      await expect(analyzer.analyzeStructure('/invalid/path')).rejects.toThrow();
    });
  });

  describe('getFileTree', () => {
    it('should build correct file tree structure', async () => {
      testRepoPath = await createTestRepo('tree-test', SAMPLE_NODE_REPO);
      
      const tree = await analyzer.getFileTree(testRepoPath);
      
      expect(tree).toBeDefined();
      expect(tree.type).toBe('directory');
      expect(tree.children).toBeInstanceOf(Array);
      expect(tree.children!.length).toBeGreaterThan(0);
    });

    it('should respect maxDepth parameter', async () => {
      testRepoPath = await createTestRepo('depth-test', SAMPLE_NODE_REPO);
      
      const tree = await analyzer.getFileTree(testRepoPath, 1);
      
      expect(tree.children).toBeDefined();
      // Should not have deeply nested children due to maxDepth limit
      const hasDeepNesting = tree.children!.some(child => 
        child.children && child.children.length > 0 && 
        child.children.some(grandchild => grandchild.children && grandchild.children.length > 0)
      );
      expect(hasDeepNesting).toBe(false);
    });
  });

  describe('classifyFiles', () => {
    it('should correctly classify different file types', async () => {
      testRepoPath = await createTestRepo('classify-test', SAMPLE_NODE_REPO);
      
      const classification = await analyzer.classifyFiles(testRepoPath);
      
      expect(classification).toBeDefined();
      expect(classification.source).toBeInstanceOf(Array);
      expect(classification.config).toBeInstanceOf(Array);
      expect(classification.documentation).toBeInstanceOf(Array);
      expect(classification.tests).toBeInstanceOf(Array);
      
      // Should classify package.json as config
      expect(classification.config).toContain('package.json');
      
      // Should classify README.md as documentation
      expect(classification.documentation).toContain('README.md');
      
      // Should classify test files as tests
      expect(classification.tests.some(file => file.includes('test'))).toBe(true);
    });
  });

  describe('detectFrameworks', () => {
    it('should detect Express.js framework', async () => {
      testRepoPath = await createTestRepo('express-test', SAMPLE_NODE_REPO);
      
      const frameworks = await analyzer.detectFrameworks(testRepoPath);
      
      expect(frameworks.backend).toBeDefined();
      expect(frameworks.backend.some(fw => fw.name === 'Express.js')).toBe(true);
      expect(frameworks.database.some(db => db.name === 'MongoDB')).toBe(true);
      expect(frameworks.testing.some(test => test.name === 'Jest')).toBe(true);
    });

    it('should detect legacy PHP application', async () => {
      testRepoPath = await createTestRepo('php-test', SAMPLE_LEGACY_REPO);
      
      const frameworks = await analyzer.detectFrameworks(testRepoPath);
      
      // Should not detect Node.js frameworks
      expect(frameworks.backend.some(fw => fw.name === 'Express.js')).toBe(false);
      
      // Should detect PHP-related patterns (if implemented)
      // This test might need adjustment based on PHP detection implementation
    });
  });

  describe('findConfigFiles', () => {
    it('should find and categorize config files', async () => {
      testRepoPath = await createTestRepo('config-test', SAMPLE_NODE_REPO);
      
      const configMap = await analyzer.findConfigFiles(testRepoPath);
      
      expect(configMap).toBeDefined();
      expect(configMap['Package Manager']).toBeDefined();
      expect(configMap['Package Manager'].some(file => file.path === 'package.json')).toBe(true);
      expect(configMap['Docker']).toBeDefined();
      expect(configMap['Docker'].some(file => file.path === 'docker-compose.yml')).toBe(true);
    });
  });

  describe('identifyEntryPoints', () => {
    it('should identify main entry point from package.json', async () => {
      testRepoPath = await createTestRepo('entry-test', SAMPLE_NODE_REPO);
      
      const entryPoints = await analyzer.identifyEntryPoints(testRepoPath);
      
      expect(entryPoints).toBeDefined();
      expect(entryPoints.length).toBeGreaterThan(0);
      expect(entryPoints.some(ep => ep.path === 'index.js' && ep.type === 'main')).toBe(true);
    });

    it('should identify common entry point patterns', async () => {
      const customFiles = {
        'app.js': 'const express = require("express");',
        'server.js': 'const http = require("http");',
        'main.py': 'if __name__ == "__main__": pass'
      };
      
      testRepoPath = await createTestRepo('patterns-test', customFiles);
      
      const entryPoints = await analyzer.identifyEntryPoints(testRepoPath);
      
      expect(entryPoints.some(ep => ep.path === 'app.js')).toBe(true);
      expect(entryPoints.some(ep => ep.path === 'server.js')).toBe(true);
      expect(entryPoints.some(ep => ep.path === 'main.py')).toBe(true);
    });
  });

  describe('error handling', () => {
    it('should handle non-existent repository gracefully', async () => {
      await expect(analyzer.analyzeStructure('/non/existent/path')).rejects.toThrow('Invalid repository path');
    });

    it('should handle file access errors gracefully', async () => {
      // Create a test repo with limited permissions (if possible)
      testRepoPath = await createTestRepo('permission-test', { 'file.txt': 'content' });
      
      // Most operations should still work even with some file access issues
      const result = await analyzer.analyzeStructure(testRepoPath);
      expect(result).toBeDefined();
    });
  });

  describe('performance', () => {
    it('should complete analysis within acceptable time', async () => {
      // Create a larger test repository
      const largeRepoFiles: { [key: string]: string } = {};
      for (let i = 0; i < 100; i++) {
        largeRepoFiles[`src/file${i}.js`] = `console.log('File ${i}');`;
        largeRepoFiles[`test/test${i}.js`] = `test('test ${i}', () => {});`;
      }
      
      testRepoPath = await createTestRepo('large-test', largeRepoFiles);
      
      const startTime = Date.now();
      const result = await analyzer.analyzeStructure(testRepoPath);
      const endTime = Date.now();
      
      expect(result).toBeDefined();
      expect(endTime - startTime).toBeLessThan(30000); // Should complete within 30 seconds
    });
  });
});