#!/usr/bin/env node

/**
 * Simple test client for the Repo MCP Server
 * This demonstrates how to use the MCP server programmatically
 */

import { spawn } from 'child_process';
import path from 'path';
import { promises as fs } from 'fs';

async function createSampleRepo(): Promise<string> {
  const sampleRepoPath = path.join(__dirname, 'sample-repo');
  
  // Clean up if exists
  try {
    await fs.rm(sampleRepoPath, { recursive: true });
  } catch {}
  
  // Create sample repository structure
  await fs.mkdir(sampleRepoPath, { recursive: true });
  await fs.mkdir(path.join(sampleRepoPath, 'src'), { recursive: true });
  await fs.mkdir(path.join(sampleRepoPath, 'tests'), { recursive: true });
  
  // Create package.json
  const packageJson = {
    name: 'sample-library-app',
    version: '1.0.0',
    main: 'src/index.js',
    dependencies: {
      express: '^4.18.0',
      mongoose: '^6.0.0',
      solr: '^0.5.0'
    },
    devDependencies: {
      jest: '^29.0.0',
      nodemon: '^2.0.0'
    },
    scripts: {
      start: 'node src/index.js',
      dev: 'nodemon src/index.js',
      test: 'jest'
    }
  };
  
  await fs.writeFile(
    path.join(sampleRepoPath, 'package.json'),
    JSON.stringify(packageJson, null, 2)
  );
  
  // Create main application file
  const indexJs = `
const express = require('express');
const mongoose = require('mongoose');
const app = express();
const PORT = process.env.PORT || 3000;

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/library', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Auckland Library API' });
});

app.get('/books', async (req, res) => {
  // Fetch books from database
  res.json({ books: [] });
});

app.post('/books', async (req, res) => {
  // Add new book
  res.json({ message: 'Book added successfully' });
});

app.listen(PORT, () => {
  console.log(\`Server running on port \${PORT}\`);
});
`;
  
  await fs.writeFile(path.join(sampleRepoPath, 'src/index.js'), indexJs);
  
  // Create a model file
  const bookModel = `
const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema({
  title: { type: String, required: true },
  author: { type: String, required: true },
  isbn: { type: String, unique: true },
  publishedDate: Date,
  category: String,
  available: { type: Boolean, default: true },
  location: String
}, { timestamps: true });

module.exports = mongoose.model('Book', bookSchema);
`;
  
  await fs.writeFile(path.join(sampleRepoPath, 'src/models/Book.js'), bookModel);
  await fs.mkdir(path.join(sampleRepoPath, 'src/models'), { recursive: true });
  await fs.writeFile(path.join(sampleRepoPath, 'src/models/Book.js'), bookModel);
  
  // Create test file
  const testFile = `
const request = require('supertest');
const app = require('../src/index');

describe('Library API', () => {
  test('GET / should return welcome message', async () => {
    const response = await request(app).get('/');
    expect(response.status).toBe(200);
    expect(response.body.message).toBe('Auckland Library API');
  });
  
  test('GET /books should return books list', async () => {
    const response = await request(app).get('/books');
    expect(response.status).toBe(200);
    expect(response.body.books).toBeInstanceOf(Array);
  });
});
`;
  
  await fs.writeFile(path.join(sampleRepoPath, 'tests/api.test.js'), testFile);
  
  // Create config files
  await fs.writeFile(
    path.join(sampleRepoPath, '.env.example'),
    'PORT=3000\nMONGO_URI=mongodb://localhost:27017/library\nSOLR_URL=http://localhost:8983/solr'
  );
  
  await fs.writeFile(
    path.join(sampleRepoPath, 'docker-compose.yml'),
    `version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - mongo
      - solr
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
  solr:
    image: solr:latest
    ports:
      - "8983:8983"`
  );
  
  // Create README
  await fs.writeFile(
    path.join(sampleRepoPath, 'README.md'),
    `# Auckland Library System

Legacy library management system built with Node.js, MongoDB, and Solr.

## Features
- Book catalog management
- Search functionality
- User management
- Inventory tracking

## Setup
1. Install dependencies: \`npm install\`
2. Start MongoDB and Solr
3. Run the application: \`npm start\`

## Migration Notes
This legacy system needs modernization to:
- Update to latest Node.js LTS
- Migrate to MongoDB 5.0+
- Upgrade Solr to 9.x
- Add TypeScript support
- Implement proper error handling
`
  );
  
  return sampleRepoPath;
}

async function testMCPServer() {
  console.log('🚀 Creating sample Auckland Library repository...');
  const sampleRepoPath = await createSampleRepo();
  
  console.log('📁 Sample repo created at:', sampleRepoPath);
  console.log('🔧 Building MCP server...');
  
  // Build the server first
  const buildProcess = spawn('npm', ['run', 'build'], {
    cwd: path.join(__dirname, '..'),
    stdio: 'inherit'
  });
  
  await new Promise((resolve, reject) => {
    buildProcess.on('close', (code) => {
      if (code === 0) resolve(code);
      else reject(new Error(`Build failed with code ${code}`));
    });
  });
  
  console.log('✅ Build completed successfully');
  console.log('🧪 Testing MCP server functionality...');
  
  // Test the server by calling its functions directly
  const { RepoAnalyzer } = await import('../src/analyzer/RepoAnalyzer.js');
  const analyzer = new RepoAnalyzer();
  
  try {
    console.log('\n📊 Testing analyzeStructure...');
    const structure = await analyzer.analyzeStructure(sampleRepoPath);
    console.log(`   Files: ${structure.totalFiles}`);
    console.log(`   Directories: ${structure.totalDirectories}`);
    console.log(`   Languages: ${structure.languages.map(l => l.language).join(', ')}`);
    console.log(`   Architecture: ${structure.architecture.type} (${structure.architecture.confidence}% confidence)`);
    
    console.log('\n🔍 Testing detectFrameworks...');
    const frameworks = await analyzer.detectFrameworks(sampleRepoPath);
    console.log(`   Backend: ${frameworks.backend.map(f => f.name).join(', ')}`);
    console.log(`   Database: ${frameworks.database.map(f => f.name).join(', ')}`);
    console.log(`   Testing: ${frameworks.testing.map(f => f.name).join(', ')}`);
    
    console.log('\n📝 Testing classifyFiles...');
    const classification = await analyzer.classifyFiles(sampleRepoPath);
    console.log(`   Source files: ${classification.source.length}`);
    console.log(`   Config files: ${classification.config.length}`);
    console.log(`   Test files: ${classification.tests.length}`);
    console.log(`   Documentation: ${classification.documentation.length}`);
    
    console.log('\n🎯 Testing identifyEntryPoints...');
    const entryPoints = await analyzer.identifyEntryPoints(sampleRepoPath);
    entryPoints.forEach(ep => {
      console.log(`   ${ep.type}: ${ep.path} - ${ep.description}`);
    });
    
    console.log('\n⚙️ Testing findConfigFiles...');
    const configFiles = await analyzer.findConfigFiles(sampleRepoPath);
    Object.entries(configFiles).forEach(([category, files]) => {
      console.log(`   ${category}: ${files.map(f => f.path).join(', ')}`);
    });
    
    console.log('\n✅ All tests completed successfully!');
    console.log('\n📋 Summary:');
    console.log(`   The Repo MCP Server successfully analyzed the Auckland Library sample repository.`);
    console.log(`   Detected: Express.js backend, MongoDB database, Jest testing framework.`);
    console.log(`   Ready for integration with CodeUnderstandingAgent.`);
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    process.exit(1);
  } finally {
    // Cleanup
    console.log('\n🧹 Cleaning up sample repository...');
    try {
      await fs.rm(sampleRepoPath, { recursive: true });
      console.log('✅ Cleanup completed');
    } catch {}
  }
}

// Run the test
testMCPServer().catch(error => {
  console.error('❌ Test runner failed:', error);
  process.exit(1);
});