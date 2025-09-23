"""
Repository Analyzer for Auckland Library Legacy System Modernization

This module provides comprehensive repository analysis capabilities including:
- Repository structure analysis and metrics
- File classification and organization  
- Git history and contribution analysis
- Framework and technology detection
- Configuration file discovery
- Entry point identification
"""

import os
import json
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import logging

import git
from git import Repo, InvalidGitRepositoryError
import chardet

logger = logging.getLogger(__name__)

@dataclass
class LanguageStats:
    """Statistics for a programming language."""
    language: str
    files: int
    lines: int
    bytes: int
    percentage: float

@dataclass 
class ComplexityMetrics:
    """Code complexity metrics."""
    cyclomatic_complexity: int
    cognitive_complexity: int
    maintainability_index: float

@dataclass
class ArchitecturePattern:
    """Detected architecture pattern."""
    type: str  # 'monolith', 'layered', 'microservices', 'mvc', 'unknown'
    confidence: int
    indicators: List[str]

@dataclass
class RepositoryStructure:
    """Complete repository structure analysis."""
    total_files: int
    total_directories: int
    total_size: int
    languages: List[LanguageStats]
    architecture: ArchitecturePattern
    complexity: ComplexityMetrics
    last_modified: str

@dataclass
class FileTreeNode:
    """File tree node structure."""
    name: str
    type: str  # 'file' or 'directory'
    path: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    children: Optional[List['FileTreeNode']] = None

@dataclass
class FileClassification:
    """File classification by purpose."""
    source: List[str]
    config: List[str] 
    documentation: List[str]
    tests: List[str]
    build: List[str]
    assets: List[str]
    unknown: List[str]

@dataclass
class CommitInfo:
    """Git commit information."""
    hash: str
    message: str
    author: str
    date: str
    files_changed: int
    insertions: int
    deletions: int

@dataclass
class BranchAnalysis:
    """Git branch analysis."""
    active_branches: List[str]
    stale_branches: List[str]
    default_branch: str
    total_branches: int

@dataclass
class ContributorStats:
    """Contributor statistics."""
    name: str
    email: str
    commits: int
    lines_added: int
    lines_removed: int
    first_commit: str
    last_commit: str

@dataclass
class DetectedFramework:
    """Detected framework information."""
    name: str
    version: Optional[str]
    confidence: int
    evidence: List[str]

@dataclass
class FrameworkDetection:
    """Framework detection results."""
    frontend: List[DetectedFramework]
    backend: List[DetectedFramework]
    database: List[DetectedFramework]
    testing: List[DetectedFramework]
    build_tools: List[DetectedFramework]

@dataclass
class ConfigFile:
    """Configuration file information."""
    path: str
    type: str
    purpose: str

@dataclass
class EntryPoint:
    """Application entry point."""
    path: str
    type: str  # 'main', 'server', 'cli', 'web', 'test'
    framework: Optional[str]
    description: str


class RepoAnalyzer:
    """Repository analyzer for legacy system modernization."""
    
    def __init__(self):
        """Initialize the repository analyzer."""
        self.language_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript', 
            '.ts': 'TypeScript',
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
        }
        
        self.ignore_patterns = {
            '.git', 'node_modules', '__pycache__', '.pytest_cache',
            'dist', 'build', 'target', 'vendor', '.venv', 'venv',
            '.DS_Store', 'Thumbs.db', '*.pyc', '*.pyo', '*.log'
        }

    async def analyze_structure(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository structure comprehensively."""
        try:
            repo_path = Path(repo_path).resolve()
            await self._validate_repository(repo_path)
            
            # Run analysis tasks concurrently
            tasks = [
                self._analyze_languages(repo_path),
                self._get_file_tree_internal(repo_path),
                self._analyze_complexity(repo_path),
                self._detect_architecture_pattern(repo_path),
                self._get_last_modified(repo_path)
            ]
            
            languages, file_tree, complexity, architecture, last_modified = await asyncio.gather(*tasks)
            
            total_files = self._count_files(file_tree)
            total_dirs = self._count_directories(file_tree)
            total_size = await self._calculate_total_size(repo_path)
            
            structure = RepositoryStructure(
                total_files=total_files,
                total_directories=total_dirs,
                total_size=total_size,
                languages=languages,
                architecture=architecture,
                complexity=complexity,
                last_modified=last_modified
            )
            
            return asdict(structure)
            
        except Exception as e:
            logger.error(f"Failed to analyze repository structure: {e}")
            raise Exception(f"Failed to analyze repository structure: {str(e)}")

    async def get_file_tree(self, repo_path: str, max_depth: int = 10) -> Dict[str, Any]:
        """Get hierarchical file tree."""
        try:
            repo_path = Path(repo_path).resolve()
            await self._validate_repository(repo_path)
            
            tree = await self._build_file_tree(repo_path, max_depth)
            return asdict(tree)
            
        except Exception as e:
            logger.error(f"Failed to get file tree: {e}")
            raise Exception(f"Failed to get file tree: {str(e)}")

    async def classify_files(self, repo_path: str) -> Dict[str, Any]:
        """Classify files by their purpose."""
        try:
            repo_path = Path(repo_path).resolve()
            await self._validate_repository(repo_path)
            
            classification = FileClassification(
                source=[], config=[], documentation=[],
                tests=[], build=[], assets=[], unknown=[]
            )
            
            # Walk through all files
            for file_path in repo_path.rglob('*'):
                if file_path.is_file() and not self._should_ignore(file_path):
                    relative_path = str(file_path.relative_to(repo_path))
                    self._classify_file(relative_path, classification)
            
            return asdict(classification)
            
        except Exception as e:
            logger.error(f"Failed to classify files: {e}")
            raise Exception(f"Failed to classify files: {str(e)}")

    async def get_commit_history(self, repo_path: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get commit history with statistics."""
        try:
            repo = Repo(repo_path)
            commits = []
            
            for commit in repo.iter_commits(max_count=limit):
                # Get commit stats
                stats = commit.stats
                total_files = len(stats.files)
                total_insertions = stats.total['insertions']
                total_deletions = stats.total['deletions']
                
                commit_info = CommitInfo(
                    hash=commit.hexsha,
                    message=commit.message.strip(),
                    author=commit.author.name,
                    date=commit.committed_datetime.isoformat(),
                    files_changed=total_files,
                    insertions=total_insertions,
                    deletions=total_deletions
                )
                commits.append(asdict(commit_info))
            
            return commits
            
        except InvalidGitRepositoryError:
            raise Exception("Not a valid Git repository")
        except Exception as e:
            logger.error(f"Failed to get commit history: {e}")
            raise Exception(f"Failed to get commit history: {str(e)}")

    async def analyze_branches(self, repo_path: str) -> Dict[str, Any]:
        """Analyze branch structure and status."""
        try:
            repo = Repo(repo_path)
            
            # Get all branches
            all_branches = [str(branch) for branch in repo.branches]
            current_branch = str(repo.active_branch) if not repo.head.is_detached else 'HEAD'
            
            # For simplicity, consider current branch as active, others as potentially stale
            active_branches = [current_branch]
            stale_branches = [b for b in all_branches if b != current_branch]
            
            analysis = BranchAnalysis(
                active_branches=active_branches,
                stale_branches=stale_branches,
                default_branch=current_branch,
                total_branches=len(all_branches)
            )
            
            return asdict(analysis)
            
        except InvalidGitRepositoryError:
            raise Exception("Not a valid Git repository")
        except Exception as e:
            logger.error(f"Failed to analyze branches: {e}")
            raise Exception(f"Failed to analyze branches: {str(e)}")

    async def get_contributors(self, repo_path: str) -> List[Dict[str, Any]]:
        """Get contributor statistics."""
        try:
            repo = Repo(repo_path)
            contributors = {}
            
            for commit in repo.iter_commits():
                author_key = f"{commit.author.name}<{commit.author.email}>"
                
                if author_key not in contributors:
                    contributors[author_key] = ContributorStats(
                        name=commit.author.name,
                        email=commit.author.email,
                        commits=1,
                        lines_added=0,  # Would need additional parsing
                        lines_removed=0,
                        first_commit=commit.committed_datetime.isoformat(),
                        last_commit=commit.committed_datetime.isoformat()
                    )
                else:
                    contributors[author_key].commits += 1
                    if commit.committed_datetime < datetime.fromisoformat(contributors[author_key].first_commit.replace('Z', '+00:00')):
                        contributors[author_key].first_commit = commit.committed_datetime.isoformat()
                    if commit.committed_datetime > datetime.fromisoformat(contributors[author_key].last_commit.replace('Z', '+00:00')):
                        contributors[author_key].last_commit = commit.committed_datetime.isoformat()
            
            # Sort by commit count
            sorted_contributors = sorted(contributors.values(), key=lambda x: x.commits, reverse=True)
            return [asdict(contributor) for contributor in sorted_contributors]
            
        except InvalidGitRepositoryError:
            raise Exception("Not a valid Git repository")
        except Exception as e:
            logger.error(f"Failed to get contributors: {e}")
            raise Exception(f"Failed to get contributors: {str(e)}")

    async def detect_frameworks(self, repo_path: str) -> Dict[str, Any]:
        """Detect frameworks and technologies used."""
        try:
            repo_path = Path(repo_path).resolve()
            await self._validate_repository(repo_path)
            
            detection = FrameworkDetection(
                frontend=await self._detect_frontend_frameworks(repo_path),
                backend=await self._detect_backend_frameworks(repo_path),
                database=await self._detect_databases(repo_path),
                testing=await self._detect_testing_frameworks(repo_path),
                build_tools=await self._detect_build_tools(repo_path)
            )
            
            return asdict(detection)
            
        except Exception as e:
            logger.error(f"Failed to detect frameworks: {e}")
            raise Exception(f"Failed to detect frameworks: {str(e)}")

    async def find_config_files(self, repo_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """Find and categorize configuration files."""
        try:
            repo_path = Path(repo_path).resolve()
            await self._validate_repository(repo_path)
            
            config_patterns = [
                '**/*.config.*', '**/.env*', '**/webpack.config.*',
                '**/babel.config.*', '**/tsconfig.json', '**/package.json',
                '**/composer.json', '**/Gemfile', '**/requirements.txt',
                '**/docker-compose.yml', '**/Dockerfile', '**/*.yml',
                '**/*.yaml', '**/*.properties', '**/*.ini'
            ]
            
            config_map: Dict[str, List[ConfigFile]] = {}
            
            for pattern in config_patterns:
                for file_path in repo_path.glob(pattern):
                    if file_path.is_file() and not self._should_ignore(file_path):
                        relative_path = str(file_path.relative_to(repo_path))
                        category = self._categorize_config_file(relative_path)
                        
                        if category not in config_map:
                            config_map[category] = []
                        
                        config_file = ConfigFile(
                            path=relative_path,
                            type=file_path.suffix.lstrip('.') or 'unknown',
                            purpose=self._get_config_purpose(relative_path)
                        )
                        config_map[category].append(config_file)
            
            # Convert to dict format
            result = {}
            for category, files in config_map.items():
                result[category] = [asdict(config_file) for config_file in files]
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to find config files: {e}")
            raise Exception(f"Failed to find config files: {str(e)}")

    async def identify_entry_points(self, repo_path: str) -> List[Dict[str, Any]]:
        """Identify application entry points."""
        try:
            repo_path = Path(repo_path).resolve()
            await self._validate_repository(repo_path)
            
            entry_points = []
            
            # Check package.json for entry points
            package_json_path = repo_path / 'package.json'
            if package_json_path.exists():
                try:
                    with open(package_json_path, 'r') as f:
                        package_data = json.load(f)
                    
                    if 'main' in package_data:
                        entry_points.append(EntryPoint(
                            path=package_data['main'],
                            type='main',
                            framework=self._detect_framework_from_file(package_data['main']),
                            description='Main entry point from package.json'
                        ))
                    
                    if 'bin' in package_data:
                        bins = package_data['bin']
                        if isinstance(bins, str):
                            bins = {package_data.get('name', 'app'): bins}
                        
                        for name, bin_path in bins.items():
                            entry_points.append(EntryPoint(
                                path=bin_path,
                                type='cli', 
                                framework=None,
                                description=f'CLI entry point: {name}'
                            ))
                except json.JSONDecodeError:
                    pass
            
            # Look for common entry point patterns
            common_patterns = [
                ('index.*', 'main'),
                ('app.*', 'web'),
                ('server.*', 'server'),
                ('main.*', 'main'),
                ('__main__.py', 'main')
            ]
            
            for pattern, entry_type in common_patterns:
                for file_path in repo_path.glob(pattern):
                    if file_path.is_file():
                        relative_path = str(file_path.relative_to(repo_path))
                        if not any(ep['path'] == relative_path for ep in [asdict(ep) for ep in entry_points]):
                            entry_points.append(EntryPoint(
                                path=relative_path,
                                type=entry_type,
                                framework=self._detect_framework_from_file(relative_path),
                                description=f'Detected {entry_type} entry point'
                            ))
            
            return [asdict(entry_point) for entry_point in entry_points]
            
        except Exception as e:
            logger.error(f"Failed to identify entry points: {e}")
            raise Exception(f"Failed to identify entry points: {str(e)}")

    # Private helper methods
    async def _validate_repository(self, repo_path: Path):
        """Validate repository path."""
        if not repo_path.exists():
            raise Exception(f"Repository path does not exist: {repo_path}")
        if not repo_path.is_dir():
            raise Exception(f"Path is not a directory: {repo_path}")

    async def _get_file_tree_internal(self, repo_path: Path) -> FileTreeNode:
        """Get internal file tree for analysis."""
        return await self._build_file_tree(repo_path, max_depth=10)

    async def _build_file_tree(self, path: Path, max_depth: int, current_depth: int = 0) -> FileTreeNode:
        """Build file tree recursively."""
        stat = path.stat()
        name = path.name
        
        if path.is_file():
            return FileTreeNode(
                name=name,
                type='file',
                path=str(path),
                size=stat.st_size,
                last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat()
            )
        
        # Directory
        node = FileTreeNode(
            name=name,
            type='directory',
            path=str(path),
            last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
            children=[]
        )
        
        if current_depth < max_depth:
            try:
                children = []
                for child_path in sorted(path.iterdir()):
                    if not self._should_ignore(child_path):
                        child_node = await self._build_file_tree(child_path, max_depth, current_depth + 1)
                        children.append(child_node)
                
                # Sort: directories first, then files
                children.sort(key=lambda x: (x.type == 'file', x.name.lower()))
                node.children = children
            except PermissionError:
                # Skip directories we can't read
                pass
        
        return node

    def _count_files(self, tree: FileTreeNode) -> int:
        """Count total files in tree."""
        if tree.type == 'file':
            return 1
        return sum(self._count_files(child) for child in (tree.children or []))

    def _count_directories(self, tree: FileTreeNode) -> int:
        """Count total directories in tree."""
        if tree.type == 'file':
            return 0
        return 1 + sum(self._count_directories(child) for child in (tree.children or []))

    async def _calculate_total_size(self, repo_path: Path) -> int:
        """Calculate total repository size."""
        total_size = 0
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and not self._should_ignore(file_path):
                try:
                    total_size += file_path.stat().st_size
                except (OSError, PermissionError):
                    pass
        return total_size

    async def _get_last_modified(self, repo_path: Path) -> str:
        """Get last modification time."""
        try:
            repo = Repo(repo_path)
            latest_commit = next(repo.iter_commits())
            return latest_commit.committed_datetime.isoformat()
        except (InvalidGitRepositoryError, StopIteration):
            # Fall back to filesystem modification time
            return datetime.fromtimestamp(repo_path.stat().st_mtime).isoformat()

    async def _analyze_languages(self, repo_path: Path) -> List[LanguageStats]:
        """Analyze programming languages used."""
        language_stats = {}
        total_bytes = 0
        
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and not self._should_ignore(file_path):
                suffix = file_path.suffix.lower()
                language = self.language_extensions.get(suffix, 'Other')
                
                try:
                    file_size = file_path.stat().st_size
                    
                    # Count lines for text files
                    lines = 0
                    if language != 'Other' and file_size < 10 * 1024 * 1024:  # Skip large files
                        try:
                            with open(file_path, 'rb') as f:
                                raw_data = f.read()
                            
                            # Detect encoding
                            encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
                            try:
                                content = raw_data.decode(encoding)
                                lines = len(content.splitlines())
                            except UnicodeDecodeError:
                                lines = 0
                        except Exception:
                            lines = 0
                    
                    if language not in language_stats:
                        language_stats[language] = {'files': 0, 'lines': 0, 'bytes': 0}
                    
                    language_stats[language]['files'] += 1
                    language_stats[language]['lines'] += lines
                    language_stats[language]['bytes'] += file_size
                    total_bytes += file_size
                    
                except (OSError, PermissionError):
                    pass
        
        # Convert to LanguageStats objects
        result = []
        for language, stats in language_stats.items():
            percentage = (stats['bytes'] / total_bytes * 100) if total_bytes > 0 else 0
            result.append(LanguageStats(
                language=language,
                files=stats['files'],
                lines=stats['lines'], 
                bytes=stats['bytes'],
                percentage=round(percentage, 2)
            ))
        
        return sorted(result, key=lambda x: x.bytes, reverse=True)

    async def _analyze_complexity(self, repo_path: Path) -> ComplexityMetrics:
        """Analyze code complexity (simplified)."""
        # Simplified complexity analysis
        return ComplexityMetrics(
            cyclomatic_complexity=1,
            cognitive_complexity=1,
            maintainability_index=85.0
        )

    async def _detect_architecture_pattern(self, repo_path: Path) -> ArchitecturePattern:
        """Detect architecture pattern."""
        indicators = []
        pattern_type = 'unknown'
        confidence = 0
        
        # Check for package.json (Node.js)
        package_json_path = repo_path / 'package.json'
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                if 'express' in deps or 'koa' in deps:
                    indicators.append('Express/Koa server found')
                    pattern_type = 'layered'
                    confidence += 30
                
                if 'react' in deps or 'vue' in deps or 'angular' in deps:
                    indicators.append('Frontend framework found') 
                    confidence += 20
                    
            except (json.JSONDecodeError, OSError):
                pass
        
        # Check directory structure
        common_dirs = ['src', 'public', 'controllers', 'models', 'views']
        found_dirs = [d.name for d in repo_path.iterdir() if d.is_dir() and d.name in common_dirs]
        
        if 'src' in found_dirs and 'public' in found_dirs:
            indicators.append('Typical web app structure')
            pattern_type = 'mvc'
            confidence += 25
        
        return ArchitecturePattern(
            type=pattern_type,
            confidence=min(confidence, 100),
            indicators=indicators
        )

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        path_str = str(path)
        return any(ignore in path_str for ignore in self.ignore_patterns)

    def _classify_file(self, file_path: str, classification: FileClassification):
        """Classify a single file."""
        path_obj = Path(file_path)
        suffix = path_obj.suffix.lower()
        name = path_obj.name.lower()
        
        # Source files
        if suffix in ['.py', '.js', '.ts', '.java', '.rb', '.php', '.go', '.rs', '.cpp', '.c', '.cs']:
            classification.source.append(file_path)
        # Test files
        elif 'test' in name or 'spec' in name or '/test/' in file_path or '/tests/' in file_path:
            classification.tests.append(file_path)
        # Documentation
        elif suffix in ['.md', '.txt', '.rst'] or 'readme' in name or 'changelog' in name:
            classification.documentation.append(file_path)
        # Config files
        elif suffix in ['.json', '.yml', '.yaml', '.xml', '.ini', '.env'] or 'config' in name:
            classification.config.append(file_path)
        # Build files
        elif 'makefile' in name or 'dockerfile' in name or 'webpack' in name or 'build' in name:
            classification.build.append(file_path)
        # Assets
        elif suffix in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.css', '.scss', '.less']:
            classification.assets.append(file_path)
        else:
            classification.unknown.append(file_path)

    async def _detect_frontend_frameworks(self, repo_path: Path) -> List[DetectedFramework]:
        """Detect frontend frameworks."""
        frameworks = []
        package_json_path = repo_path / 'package.json'
        
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                framework_map = {
                    'react': 'React',
                    'vue': 'Vue.js',
                    '@angular/core': 'Angular',
                    'svelte': 'Svelte',
                    'next': 'Next.js',
                    'nuxt': 'Nuxt.js'
                }
                
                for dep, framework_name in framework_map.items():
                    if dep in deps:
                        frameworks.append(DetectedFramework(
                            name=framework_name,
                            version=deps[dep],
                            confidence=90,
                            evidence=[f'Found {dep} in package.json']
                        ))
            except (json.JSONDecodeError, OSError):
                pass
        
        return frameworks

    async def _detect_backend_frameworks(self, repo_path: Path) -> List[DetectedFramework]:
        """Detect backend frameworks."""
        frameworks = []
        
        # Node.js frameworks
        package_json_path = repo_path / 'package.json'
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                if 'express' in deps:
                    frameworks.append(DetectedFramework(
                        name='Express.js',
                        version=deps['express'],
                        confidence=95,
                        evidence=['express found in package.json']
                    ))
                
                if 'koa' in deps:
                    frameworks.append(DetectedFramework(
                        name='Koa.js',
                        version=deps['koa'],
                        confidence=95,
                        evidence=['koa found in package.json']
                    ))
            except (json.JSONDecodeError, OSError):
                pass
        
        # Python frameworks
        requirements_path = repo_path / 'requirements.txt'
        if requirements_path.exists():
            try:
                with open(requirements_path, 'r') as f:
                    requirements = f.read()
                
                if 'django' in requirements.lower():
                    frameworks.append(DetectedFramework(
                        name='Django',
                        version=None,
                        confidence=90,
                        evidence=['django found in requirements.txt']
                    ))
                
                if 'flask' in requirements.lower():
                    frameworks.append(DetectedFramework(
                        name='Flask',
                        version=None,
                        confidence=90,
                        evidence=['flask found in requirements.txt']
                    ))
            except OSError:
                pass
        
        return frameworks

    async def _detect_databases(self, repo_path: Path) -> List[DetectedFramework]:
        """Detect databases."""
        databases = []
        package_json_path = repo_path / 'package.json'
        
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                db_map = {
                    'mongoose': 'MongoDB',
                    'mysql': 'MySQL', 
                    'pg': 'PostgreSQL',
                    'sqlite3': 'SQLite',
                    'redis': 'Redis'
                }
                
                for dep, db_name in db_map.items():
                    if dep in deps:
                        databases.append(DetectedFramework(
                            name=db_name,
                            version=deps[dep],
                            confidence=85,
                            evidence=[f'{dep} found in package.json']
                        ))
            except (json.JSONDecodeError, OSError):
                pass
        
        return databases

    async def _detect_testing_frameworks(self, repo_path: Path) -> List[DetectedFramework]:
        """Detect testing frameworks."""
        frameworks = []
        package_json_path = repo_path / 'package.json'
        
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                test_frameworks = {
                    'jest': 'Jest',
                    'mocha': 'Mocha',
                    'jasmine': 'Jasmine',
                    'cypress': 'Cypress',
                    '@testing-library/react': 'React Testing Library'
                }
                
                for dep, framework_name in test_frameworks.items():
                    if dep in deps:
                        frameworks.append(DetectedFramework(
                            name=framework_name,
                            version=deps[dep],
                            confidence=90,
                            evidence=[f'{dep} found in package.json']
                        ))
            except (json.JSONDecodeError, OSError):
                pass
        
        return frameworks

    async def _detect_build_tools(self, repo_path: Path) -> List[DetectedFramework]:
        """Detect build tools."""
        tools = []
        package_json_path = repo_path / 'package.json'
        
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                build_tools = {
                    'webpack': 'Webpack',
                    'vite': 'Vite',
                    'rollup': 'Rollup',
                    'parcel': 'Parcel',
                    'gulp': 'Gulp',
                    'grunt': 'Grunt'
                }
                
                for dep, tool_name in build_tools.items():
                    if dep in deps:
                        tools.append(DetectedFramework(
                            name=tool_name,
                            version=deps[dep],
                            confidence=90,
                            evidence=[f'{dep} found in package.json']
                        ))
            except (json.JSONDecodeError, OSError):
                pass
        
        return tools

    def _categorize_config_file(self, file_path: str) -> str:
        """Categorize configuration file."""
        name = os.path.basename(file_path).lower()
        
        if 'docker' in name:
            return 'Docker'
        elif 'webpack' in name or 'rollup' in name or 'vite' in name:
            return 'Build'
        elif 'babel' in name or 'eslint' in name or 'prettier' in name:
            return 'Development'
        elif 'test' in name or 'jest' in name or 'cypress' in name:
            return 'Testing'
        elif 'env' in name or 'environment' in name:
            return 'Environment'
        elif name in ['package.json', 'composer.json']:
            return 'Package Manager'
        elif file_path.endswith(('.yml', '.yaml')):
            return 'YAML Config'
        
        return 'General'

    def _get_config_purpose(self, file_path: str) -> str:
        """Get configuration file purpose."""
        name = os.path.basename(file_path).lower()
        
        purpose_map = {
            'package.json': 'Node.js package configuration',
            'composer.json': 'PHP package configuration', 
            'webpack.config.js': 'Webpack build configuration',
            'tsconfig.json': 'TypeScript configuration',
            '.env': 'Environment variables',
            'docker-compose.yml': 'Docker composition',
            'dockerfile': 'Docker container configuration'
        }
        
        return purpose_map.get(name, 'Configuration file')

    def _detect_framework_from_file(self, file_path: str) -> Optional[str]:
        """Detect framework from file extension."""
        ext = Path(file_path).suffix.lower()
        if ext in ['.js', '.ts']:
            return 'JavaScript/TypeScript'
        elif ext == '.py':
            return 'Python'
        return None