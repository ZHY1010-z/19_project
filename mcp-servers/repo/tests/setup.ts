// Test setup file
import { promises as fs } from 'fs';
import path from 'path';

// Global test timeout
jest.setTimeout(30000);

// Helper function to create temporary test repositories
export async function createTestRepo(repoName: string, files: { [path: string]: string } = {}): Promise<string> {
  const testDir = path.join(__dirname, 'temp', repoName);
  
  // Clean up if exists
  try {
    await fs.rm(testDir, { recursive: true, force: true });
  } catch {}
  
  // Create directory structure
  await fs.mkdir(testDir, { recursive: true });
  
  // Create files
  for (const [filePath, content] of Object.entries(files)) {
    const fullPath = path.join(testDir, filePath);
    const dir = path.dirname(fullPath);
    
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(fullPath, content);
  }
  
  return testDir;
}

// Cleanup function
export async function cleanupTestRepo(repoPath: string): Promise<void> {
  try {
    await fs.rm(repoPath, { recursive: true, force: true });
  } catch {}
}

// Sample repository structures for testing
export const SAMPLE_NODE_REPO = {
  'package.json': JSON.stringify({
    name: 'sample-app',
    version: '1.0.0',
    main: 'index.js',
    dependencies: {
      express: '^4.18.0',
      mongoose: '^6.0.0'
    },
    devDependencies: {
      jest: '^29.0.0',
      '@types/node': '^18.0.0'
    }
  }, null, 2),
  'index.js': `
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
`,
  'src/models/User.js': `
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: String,
  email: String
});

module.exports = mongoose.model('User', userSchema);
`,
  'tests/user.test.js': `
describe('User', () => {
  test('should create user', () => {
    expect(true).toBe(true);
  });
});
`,
  'README.md': '# Sample Application\n\nThis is a sample Express.js application.',
  '.env.example': 'DATABASE_URL=mongodb://localhost:27017/sample',
  'docker-compose.yml': `
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
`
};

export const SAMPLE_LEGACY_REPO = {
  'app.php': `
<?php
require_once 'config/database.php';
require_once 'includes/functions.php';

// Legacy PHP application
class App {
    public function __construct() {
        $this->db = new Database();
    }
    
    public function run() {
        // Application logic
    }
}

$app = new App();
$app->run();
`,
  'config/database.php': `
<?php
class Database {
    private $host = 'localhost';
    private $dbname = 'legacy_db';
    
    public function connect() {
        // Database connection logic
    }
}
`,
  'includes/functions.php': `
<?php
function sanitize_input($input) {
    return htmlspecialchars(strip_tags($input));
}

function redirect($url) {
    header("Location: $url");
    exit;
}
`,
  'public/index.php': `
<?php
require_once '../app.php';
`,
  'public/css/style.css': `
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
}
`,
  'composer.json': JSON.stringify({
    name: 'legacy/app',
    description: 'Legacy PHP application',
    require: {
      'php': '>=7.0'
    }
  }, null, 2)
};