#!/usr/bin/env python3
"""
Utility functions for Auckland Library Multi-Agent Modernization Framework

Reusable components for workflow orchestration, validation, and agent communication.
Includes advanced static analysis capabilities: AST analysis, dependency analysis, 
quality analysis, and architecture analysis.
"""

import ast
import os
import re
import json
import math
import logging
import functools
from typing import Dict, Any, Optional, List, Set, Tuple, Callable, Union
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict, deque

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Configure logging
logger = logging.getLogger(__name__)


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text
    
    Args:
        text: The text containing the XML
        tag: The XML tag to extract content from
    
    Returns:
        The content of the specified XML tag, or empty string if not found
    """
    match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
    return match.group(1) if match else ""


# ================== UNIFIED ERROR HANDLING ==================

def handle_errors(default_return: Any = None, log_errors: bool = True):
    """
    Decorator for unified error handling across all functions
    
    Args:
        default_return: Value to return on error (None, {}, [], etc.)
        log_errors: Whether to log errors
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Validate inputs
                if hasattr(func, '__annotations__'):
                    _validate_function_inputs(func, args, kwargs)
                
                return func(*args, **kwargs)
                
            except Exception as e:
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {str(e)}")
                
                # Return structured error response for Dict returns
                if default_return is None and hasattr(func, '__annotations__'):
                    return_type = func.__annotations__.get('return', None)
                    if return_type and hasattr(return_type, '__origin__') and return_type.__origin__ is dict:
                        return {
                            "status": "error", 
                            "error": str(e),
                            "function": func.__name__
                        }
                
                return default_return
                
        return wrapper
    return decorator


def _validate_function_inputs(func: Callable, args: tuple, kwargs: dict):
    """Validate function inputs based on type annotations"""
    annotations = func.__annotations__
    
    # Get parameter names
    import inspect
    sig = inspect.signature(func)
    param_names = list(sig.parameters.keys())
    
    # Validate positional arguments
    for i, arg in enumerate(args):
        if i < len(param_names):
            param_name = param_names[i]
            expected_type = annotations.get(param_name)
            
            if expected_type and expected_type == str and not isinstance(arg, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            elif expected_type and expected_type == dict and not isinstance(arg, dict):
                raise ValueError(f"Parameter '{param_name}' must be a dictionary")


def validate_path(path: str, must_exist: bool = True) -> bool:
    """
    Validate file/directory path
    
    Args:
        path: Path to validate
        must_exist: Whether path must exist
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If path is invalid
    """
    if not path or not isinstance(path, str):
        raise ValueError("Path must be a non-empty string")
    
    path = os.path.abspath(path)  # Convert to absolute path
    
    if must_exist and not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")
    
    return True


def standardize_return_format(data: Any, status: str = "success", message: str = "") -> Dict[str, Any]:
    """
    Standardize return format for consistency
    
    Args:
        data: The actual data to return
        status: Status ("success", "error", "warning")
        message: Optional message
        
    Returns:
        Standardized response dictionary
    """
    return {
        "status": status,
        "data": data,
        "message": message,
        "timestamp": "2024"
    }


def validate_project_config(config: Dict[str, Any]) -> bool:
    """
    Validate project configuration
    
    Args:
        config: Project configuration dictionary
    
    Returns:
        True if configuration is valid
    
    Raises:
        ValueError: If required configuration is missing or invalid
    """
    required_fields = ["project_name", "legacy_repo_path", "target_stack"]
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required configuration field: {field}")
        
        if not config[field]:
            raise ValueError(f"Configuration field cannot be empty: {field}")
    
    # Validate specific field formats
    if not isinstance(config.get("legacy_repo_path"), str):
        raise ValueError("legacy_repo_path must be a string")
    
    if not isinstance(config.get("target_stack"), str):
        raise ValueError("target_stack must be a string")
    
    logger.info("Project configuration validated successfully")
    return True


# ================== OPTIMIZED FILE SCANNING ==================

@handle_errors(default_return={})
def unified_repository_scan(repo_path: str) -> Dict[str, Any]:
    """
    Unified repository scanning to avoid multiple file traversals
    
    Performs all file system analysis in a single pass:
    - File structure analysis
    - Language detection
    - Framework detection
    - Security analysis
    - Database file discovery
    
    Args:
        repo_path: Path to repository root
        
    Returns:
        Comprehensive scan results
    """
    validate_path(repo_path)
    
    # Initialize all analysis structures
    scan_results = {
        "file_structure": {
            "total_files": 0,
            "directories": [],
            "file_types": {},
            "large_files": [],
            "empty_files": []
        },
        "language_analysis": {
            "languages": {},
            "frameworks": {"detected": [], "config_files": []},
            "package_managers": []
        },
        "security_analysis": {
            "config_files": [],
            "potential_secrets": [],
            "dependencies": []
        },
        "database_files": [],
        "file_details": []  # Store detailed file info for further processing
    }
    
    logger.info(f"Starting unified repository scan: {repo_path}")
    
    for root, dirs, files in os.walk(repo_path):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'vendor', '.env', 'dist', 'build']]
        
        # Track directories
        rel_dir = os.path.relpath(root, repo_path)
        if rel_dir != '.':
            scan_results["file_structure"]["directories"].append(rel_dir)
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_path)
            
            try:
                file_size = os.path.getsize(file_path)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Store detailed file info
                file_info = {
                    "path": rel_path,
                    "full_path": file_path,
                    "size": file_size,
                    "extension": file_ext,
                    "name": file
                }
                scan_results["file_details"].append(file_info)
                
                # === File Structure Analysis ===
                scan_results["file_structure"]["total_files"] += 1
                
                # Count file types
                if file_ext:
                    scan_results["file_structure"]["file_types"][file_ext] = \
                        scan_results["file_structure"]["file_types"].get(file_ext, 0) + 1
                
                # Track large files (>1MB)
                if file_size > 1024 * 1024:
                    scan_results["file_structure"]["large_files"].append({
                        "path": rel_path,
                        "size": file_size
                    })
                
                # Track empty files
                if file_size == 0:
                    scan_results["file_structure"]["empty_files"].append(rel_path)
                
                # === Language Analysis ===
                _analyze_file_language(file_info, scan_results["language_analysis"])
                
                # === Security Analysis ===
                _analyze_file_security(file_info, scan_results["security_analysis"])
                
                # === Database File Analysis ===
                _analyze_database_file(file_info, scan_results["database_files"])
                
            except (OSError, IOError) as e:
                logger.warning(f"Cannot access file {file_path}: {str(e)}")
                continue
    
    logger.info(f"Unified scan completed: {scan_results['file_structure']['total_files']} files analyzed")
    return scan_results


def _analyze_file_language(file_info: Dict[str, Any], language_analysis: Dict[str, Any]):
    """Analyze language and framework for a single file"""
    file_ext = file_info["extension"]
    file_name = file_info["name"]
    file_path = file_info["full_path"]
    
    # Language detection based on file extensions
    if file_ext == '.php':
        language_analysis["languages"]["php"] = language_analysis["languages"].get("php", 0) + 1
    elif file_ext in ['.js', '.jsx']:
        language_analysis["languages"]["javascript"] = language_analysis["languages"].get("javascript", 0) + 1
    elif file_ext == '.py':
        language_analysis["languages"]["python"] = language_analysis["languages"].get("python", 0) + 1
    elif file_ext in ['.html', '.htm']:
        language_analysis["languages"]["html"] = language_analysis["languages"].get("html", 0) + 1
    elif file_ext == '.css':
        language_analysis["languages"]["css"] = language_analysis["languages"].get("css", 0) + 1
    elif file_ext in ['.ts', '.tsx']:
        language_analysis["languages"]["typescript"] = language_analysis["languages"].get("typescript", 0) + 1
    
    # Framework and package manager detection
    if file_name == 'composer.json':
        language_analysis["frameworks"]["config_files"].append(file_info["path"])
        language_analysis["package_managers"].append("composer")
        _detect_php_frameworks(file_path, language_analysis)
    elif file_name == 'package.json':
        language_analysis["frameworks"]["config_files"].append(file_info["path"])
        language_analysis["package_managers"].append("npm")
        _detect_js_frameworks(file_path, language_analysis)
    elif file_name == 'requirements.txt' or file_name == 'Pipfile':
        language_analysis["package_managers"].append("pip")
    elif file_name.endswith('.blade.php'):
        if "Laravel" not in language_analysis["frameworks"]["detected"]:
            language_analysis["frameworks"]["detected"].append("Laravel")


def _analyze_file_security(file_info: Dict[str, Any], security_analysis: Dict[str, Any]):
    """Analyze security aspects for a single file"""
    file_name = file_info["name"]
    file_path = file_info["path"]
    
    # Config files that might contain secrets
    config_patterns = ['.env', 'config.', 'settings.', '.conf', '.cfg', '.ini']
    if any(pattern in file_name.lower() for pattern in config_patterns):
        security_analysis["config_files"].append(file_path)
    
    # Files that might contain secrets
    secret_patterns = ['key', 'secret', 'password', 'token', 'auth']
    if any(pattern in file_name.lower() for pattern in secret_patterns):
        security_analysis["potential_secrets"].append(file_path)


def _analyze_database_file(file_info: Dict[str, Any], database_files: List[Dict[str, Any]]):
    """Analyze database-related files"""
    file_ext = file_info["extension"]
    file_name = file_info["name"]
    
    # Database schema files
    if file_ext in ['.sql', '.ddl', '.dml']:
        database_files.append({
            "type": "sql_schema",
            "path": file_info["path"],
            "size": file_info["size"]
        })
    
    # Database config files
    elif 'database' in file_name.lower() or 'db' in file_name.lower():
        database_files.append({
            "type": "db_config",
            "path": file_info["path"],
            "size": file_info["size"]
        })
    
    # Migration files
    elif 'migration' in file_name.lower() or 'migrate' in file_name.lower():
        database_files.append({
            "type": "migration",
            "path": file_info["path"],
            "size": file_info["size"]
        })


def _detect_php_frameworks(file_path: str, language_analysis: Dict[str, Any]):
    """Detect PHP frameworks from composer.json"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            composer_data = json.load(f)
            
        require_section = composer_data.get('require', {})
        if 'laravel/framework' in require_section:
            if "Laravel" not in language_analysis["frameworks"]["detected"]:
                language_analysis["frameworks"]["detected"].append("Laravel")
        elif 'symfony/symfony' in require_section:
            if "Symfony" not in language_analysis["frameworks"]["detected"]:
                language_analysis["frameworks"]["detected"].append("Symfony")
        elif 'cakephp/cakephp' in require_section:
            if "CakePHP" not in language_analysis["frameworks"]["detected"]:
                language_analysis["frameworks"]["detected"].append("CakePHP")
                
    except (json.JSONDecodeError, IOError):
        pass


def _detect_js_frameworks(file_path: str, language_analysis: Dict[str, Any]):
    """Detect JavaScript frameworks from package.json"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
            
        dependencies = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
        
        frameworks_map = {
            'react': 'React',
            'vue': 'Vue.js',
            'angular': 'Angular',
            'express': 'Express.js',
            'next': 'Next.js',
            'nuxt': 'Nuxt.js'
        }
        
        for dep_name, framework_name in frameworks_map.items():
            if any(dep_name in dep for dep in dependencies.keys()):
                if framework_name not in language_analysis["frameworks"]["detected"]:
                    language_analysis["frameworks"]["detected"].append(framework_name)
                    
    except (json.JSONDecodeError, IOError):
        pass


def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """
    Setup logging configuration
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    log_level = getattr(logging, level.upper())
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Setup file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    logger.info(f"Logging configured: level={level}, file={log_file or 'console only'}")


# ================== STATIC ANALYSIS DATA CLASSES ==================

@dataclass
class FunctionInfo:
    """Information about a function extracted from AST"""
    name: str
    line_start: int
    line_end: int
    params: List[str]
    return_type: Optional[str]
    docstring: Optional[str]
    complexity: int
    calls: List[str]  # Functions this function calls

@dataclass
class ClassInfo:
    """Information about a class extracted from AST"""
    name: str
    line_start: int
    line_end: int
    parent_classes: List[str]
    methods: List[FunctionInfo]
    properties: List[str]
    docstring: Optional[str]

@dataclass
class ImportInfo:
    """Information about imports/includes"""
    module: str
    alias: Optional[str]
    line: int
    import_type: str  # 'import', 'from', 'include', 'require'

@dataclass
class DependencyEdge:
    """Represents a dependency relationship between two code entities"""
    source: str
    target: str
    dependency_type: str  # 'import', 'include', 'extend', 'implement', 'call'
    line_number: int
    strength: float = 1.0  # Coupling strength

@dataclass
class ModuleInfo:
    """Information about a code module/file"""
    file_path: str
    module_name: str
    language: str
    dependencies_out: List[str]  # What this module depends on
    dependencies_in: List[str]   # What depends on this module
    coupling_in: int = 0
    coupling_out: int = 0
    instability: float = 0.0  # Ce / (Ca + Ce)

@dataclass
class CodeSmell:
    """Represents a detected code smell"""
    type: str
    file_path: str
    line_number: int
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    suggestion: str

@dataclass
class ComplexityMetrics:
    """Code complexity metrics"""
    cyclomatic_complexity: float
    cognitive_complexity: float
    halstead_complexity: Dict[str, float]
    maintainability_index: float
    lines_of_code: int
    logical_lines: int

@dataclass
class QualityScore:
    """Overall quality assessment"""
    overall_score: float  # 0-100
    maintainability: float
    reliability: float
    security: float
    performance: float
    readability: float

@dataclass
class ArchitecturalPattern:
    """Represents a detected architectural pattern"""
    pattern_type: str
    confidence: float  # 0.0 to 1.0
    components: List[str]
    description: str
    files_involved: List[str]

@dataclass
class LayerInfo:
    """Information about an architectural layer"""
    name: str
    files: List[str]
    responsibilities: List[str]
    dependencies_to: List[str]
    dependencies_from: List[str]

@dataclass
class DesignPattern:
    """Represents a detected design pattern"""
    pattern_name: str
    location: str
    confidence: float
    participants: List[str]
    description: str



# ================== STATIC ANALYSIS CLASSES ==================

class ASTAnalyzer:
    """
    Advanced AST analyzer for multiple programming languages
    
    Provides deep code structure analysis including:
    - Function and class extraction
    - Complexity metrics calculation
    - Import/dependency analysis
    - Code pattern detection
    """
    
    def __init__(self):
        self.supported_extensions = {
            '.py': self.analyze_python_file,
            '.php': self.analyze_php_file,
            '.js': self.analyze_javascript_file,
            '.ts': self.analyze_typescript_file
        }
    
    def analyze_repository(self, repo_path: str) -> Dict[str, Any]:
        """
        Analyze entire repository for AST-based insights
        
        Args:
            repo_path: Path to repository root
            
        Returns:
            Comprehensive AST analysis results
        """
        logger.info(f"Starting AST analysis of repository: {repo_path}")
        
        analysis_results = {
            "files_analyzed": 0,
            "total_functions": 0,
            "total_classes": 0,
            "total_imports": 0,
            "language_breakdown": {},
            "complexity_metrics": {
                "avg_function_complexity": 0,
                "max_function_complexity": 0,
                "total_cyclomatic_complexity": 0
            },
            "code_structure": {
                "functions": [],
                "classes": [],
                "imports": []
            },
            "architectural_insights": {
                "mvc_components": {"models": [], "views": [], "controllers": []},
                "design_patterns": [],
                "coupling_analysis": {}
            }
        }
        
        total_complexity = 0
        max_complexity = 0
        complexity_count = 0
        
        try:
            for root, dirs, files in os.walk(repo_path):
                # Skip common non-source directories
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'vendor', '.env']]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = Path(file).suffix.lower()
                    
                    if file_ext in self.supported_extensions:
                        try:
                            file_analysis = self.supported_extensions[file_ext](file_path)
                            if file_analysis:
                                analysis_results["files_analyzed"] += 1
                                
                                # Update language breakdown
                                lang = file_ext[1:]  # Remove dot
                                if lang not in analysis_results["language_breakdown"]:
                                    analysis_results["language_breakdown"][lang] = {"files": 0, "functions": 0, "classes": 0}
                                
                                analysis_results["language_breakdown"][lang]["files"] += 1
                                analysis_results["language_breakdown"][lang]["functions"] += len(file_analysis["functions"])
                                analysis_results["language_breakdown"][lang]["classes"] += len(file_analysis["classes"])
                                
                                # Aggregate functions and classes
                                analysis_results["code_structure"]["functions"].extend(file_analysis["functions"])
                                analysis_results["code_structure"]["classes"].extend(file_analysis["classes"])
                                analysis_results["code_structure"]["imports"].extend(file_analysis["imports"])
                                
                                # Update totals
                                analysis_results["total_functions"] += len(file_analysis["functions"])
                                analysis_results["total_classes"] += len(file_analysis["classes"])
                                analysis_results["total_imports"] += len(file_analysis["imports"])
                                
                                # Calculate complexity metrics
                                for func in file_analysis["functions"]:
                                    if func.complexity > 0:
                                        total_complexity += func.complexity
                                        max_complexity = max(max_complexity, func.complexity)
                                        complexity_count += 1
                                
                                # Detect architectural patterns
                                self._detect_architectural_patterns(file_path, file_analysis, analysis_results["architectural_insights"])
                                
                        except Exception as e:
                            logger.warning(f"Failed to analyze {file_path}: {str(e)}")
                            continue
        
        except Exception as e:
            logger.error(f"Repository analysis failed: {str(e)}")
            return analysis_results
        
        # Calculate final metrics
        if complexity_count > 0:
            analysis_results["complexity_metrics"]["avg_function_complexity"] = total_complexity / complexity_count
            analysis_results["complexity_metrics"]["max_function_complexity"] = max_complexity
            analysis_results["complexity_metrics"]["total_cyclomatic_complexity"] = total_complexity
        
        logger.info(f"AST analysis completed: {analysis_results['files_analyzed']} files, "
                   f"{analysis_results['total_functions']} functions, {analysis_results['total_classes']} classes")
        
        return analysis_results
    
    def analyze_python_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Analyze Python file using AST"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            functions = []
            classes = []
            imports = []
            
            # Extract top-level elements
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = self._extract_python_function(node, content)
                    functions.append(func_info)
                elif isinstance(node, ast.ClassDef):
                    class_info = self._extract_python_class(node, content)
                    classes.append(class_info)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_info = self._extract_python_import(node)
                    imports.append(import_info)
            
            return {
                "file_path": file_path,
                "language": "python",
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "lines_of_code": len(content.splitlines())
            }
            
        except Exception as e:
            logger.warning(f"Failed to parse Python file {file_path}: {str(e)}")
            return None
    
    def analyze_php_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Analyze PHP file using regex patterns (simplified AST-like analysis)"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            functions = self._extract_php_functions(content, file_path)
            classes = self._extract_php_classes(content, file_path)
            imports = self._extract_php_includes(content)
            
            return {
                "file_path": file_path,
                "language": "php",
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "lines_of_code": len(content.splitlines())
            }
            
        except Exception as e:
            logger.warning(f"Failed to parse PHP file {file_path}: {str(e)}")
            return None
    
    def analyze_javascript_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Analyze JavaScript file using regex patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            functions = self._extract_js_functions(content, file_path)
            classes = self._extract_js_classes(content, file_path)
            imports = self._extract_js_imports(content)
            
            return {
                "file_path": file_path,
                "language": "javascript",
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "lines_of_code": len(content.splitlines())
            }
            
        except Exception as e:
            logger.warning(f"Failed to parse JavaScript file {file_path}: {str(e)}")
            return None
    
    def analyze_typescript_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Analyze TypeScript file (similar to JavaScript)"""
        return self.analyze_javascript_file(file_path)
    
    def _extract_python_function(self, node: ast.FunctionDef, content: str) -> FunctionInfo:
        """Extract function information from Python AST node"""
        params = [arg.arg for arg in node.args.args]
        
        # Calculate cyclomatic complexity
        complexity = self._calculate_python_complexity(node)
        
        # Extract function calls
        calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                calls.append(child.func.id)
        
        # Get docstring
        docstring = ast.get_docstring(node)
        
        return FunctionInfo(
            name=node.name,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            params=params,
            return_type=None,  # Could extract from annotations
            docstring=docstring,
            complexity=complexity,
            calls=calls
        )
    
    def _extract_python_class(self, node: ast.ClassDef, content: str) -> ClassInfo:
        """Extract class information from Python AST node"""
        parent_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                parent_classes.append(base.id)
        
        methods = []
        properties = []
        
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                method_info = self._extract_python_function(child, content)
                methods.append(method_info)
            elif isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name):
                        properties.append(target.id)
        
        docstring = ast.get_docstring(node)
        
        return ClassInfo(
            name=node.name,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            parent_classes=parent_classes,
            methods=methods,
            properties=properties,
            docstring=docstring
        )
    
    def _extract_python_import(self, node) -> ImportInfo:
        """Extract import information from Python AST node"""
        if isinstance(node, ast.Import):
            for alias in node.names:
                return ImportInfo(
                    module=alias.name,
                    alias=alias.asname,
                    line=node.lineno,
                    import_type="import"
                )
        elif isinstance(node, ast.ImportFrom):
            return ImportInfo(
                module=node.module or "",
                alias=None,
                line=node.lineno,
                import_type="from"
            )
    
    def _extract_php_functions(self, content: str, file_path: str) -> List[FunctionInfo]:
        """Extract PHP functions using regex"""
        functions = []
        
        # PHP function pattern
        pattern = r'function\s+(\w+)\s*\(([^)]*)\)\s*\{'
        matches = re.finditer(pattern, content, re.IGNORECASE)
        
        for match in matches:
            name = match.group(1)
            params_str = match.group(2).strip()
            params = [p.strip().split()[-1].lstrip('$') for p in params_str.split(',') if p.strip()] if params_str else []
            
            line_start = content[:match.start()].count('\n') + 1
            
            functions.append(FunctionInfo(
                name=name,
                line_start=line_start,
                line_end=line_start + 10,  # Approximate
                params=params,
                return_type=None,
                docstring=None,
                complexity=1,  # Simplified
                calls=[]
            ))
        
        return functions
    
    def _extract_php_classes(self, content: str, file_path: str) -> List[ClassInfo]:
        """Extract PHP classes using regex"""
        classes = []
        
        # PHP class pattern
        pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'
        matches = re.finditer(pattern, content, re.IGNORECASE)
        
        for match in matches:
            name = match.group(1)
            parent = match.group(2) if match.group(2) else None
            parent_classes = [parent] if parent else []
            
            line_start = content[:match.start()].count('\n') + 1
            
            classes.append(ClassInfo(
                name=name,
                line_start=line_start,
                line_end=line_start + 20,  # Approximate
                parent_classes=parent_classes,
                methods=[],  # Could extract methods
                properties=[],
                docstring=None
            ))
        
        return classes
    
    def _extract_php_includes(self, content: str) -> List[ImportInfo]:
        """Extract PHP includes/requires"""
        imports = []
        
        # PHP include patterns
        patterns = [
            (r'include\s+[\'"]([^\'"]+)[\'"]', 'include'),
            (r'require\s+[\'"]([^\'"]+)[\'"]', 'require'),
            (r'include_once\s+[\'"]([^\'"]+)[\'"]', 'include_once'),
            (r'require_once\s+[\'"]([^\'"]+)[\'"]', 'require_once')
        ]
        
        for pattern, import_type in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line = content[:match.start()].count('\n') + 1
                imports.append(ImportInfo(
                    module=match.group(1),
                    alias=None,
                    line=line,
                    import_type=import_type
                ))
        
        return imports
    
    def _extract_js_functions(self, content: str, file_path: str) -> List[FunctionInfo]:
        """Extract JavaScript functions using regex"""
        functions = []
        
        # JavaScript function patterns
        patterns = [
            r'function\s+(\w+)\s*\(([^)]*)\)\s*\{',  # function declaration
            r'(\w+)\s*:\s*function\s*\(([^)]*)\)\s*\{',  # object method
            r'const\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>\s*\{',  # arrow function
            r'(\w+)\s*=\s*function\s*\(([^)]*)\)\s*\{'  # function expression
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                name = match.group(1)
                params_str = match.group(2).strip() if len(match.groups()) > 1 else ""
                params = [p.strip() for p in params_str.split(',') if p.strip()] if params_str else []
                
                line_start = content[:match.start()].count('\n') + 1
                
                functions.append(FunctionInfo(
                    name=name,
                    line_start=line_start,
                    line_end=line_start + 10,  # Approximate
                    params=params,
                    return_type=None,
                    docstring=None,
                    complexity=1,  # Simplified
                    calls=[]
                ))
        
        return functions
    
    def _extract_js_classes(self, content: str, file_path: str) -> List[ClassInfo]:
        """Extract JavaScript classes using regex"""
        classes = []
        
        # JavaScript class pattern
        pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            name = match.group(1)
            parent = match.group(2) if match.group(2) else None
            parent_classes = [parent] if parent else []
            
            line_start = content[:match.start()].count('\n') + 1
            
            classes.append(ClassInfo(
                name=name,
                line_start=line_start,
                line_end=line_start + 20,  # Approximate
                parent_classes=parent_classes,
                methods=[],
                properties=[],
                docstring=None
            ))
        
        return classes
    
    def _extract_js_imports(self, content: str) -> List[ImportInfo]:
        """Extract JavaScript imports"""
        imports = []
        
        # JavaScript import patterns
        patterns = [
            (r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', 'import'),
            (r'import\s+\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]', 'import'),
            (r'const\s+(\w+)\s*=\s*require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', 'require')
        ]
        
        for pattern, import_type in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                line = content[:match.start()].count('\n') + 1
                if len(match.groups()) >= 2:
                    imports.append(ImportInfo(
                        module=match.group(2),
                        alias=match.group(1) if import_type != 'import' or '{' not in match.group(1) else None,
                        line=line,
                        import_type=import_type
                    ))
        
        return imports
    
    def _calculate_python_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for Python function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            # Decision points that increase complexity
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _detect_architectural_patterns(self, file_path: str, file_analysis: Dict[str, Any], insights: Dict[str, Any]):
        """Detect architectural patterns from file analysis"""
        file_name = os.path.basename(file_path).lower()
        
        # MVC pattern detection
        if 'model' in file_name or file_path.endswith('Model.php'):
            insights["mvc_components"]["models"].append(file_path)
        elif 'view' in file_name or file_path.endswith('View.php') or file_name.endswith('.blade.php'):
            insights["mvc_components"]["views"].append(file_path)
        elif 'controller' in file_name or file_path.endswith('Controller.php'):
            insights["mvc_components"]["controllers"].append(file_path)
        
        # Design pattern detection based on class names and structure
        for class_info in file_analysis["classes"]:
            class_name = class_info.name.lower()
            
            if 'factory' in class_name:
                if "Factory Pattern" not in insights["design_patterns"]:
                    insights["design_patterns"].append("Factory Pattern")
            elif 'singleton' in class_name:
                if "Singleton Pattern" not in insights["design_patterns"]:
                    insights["design_patterns"].append("Singleton Pattern")
            elif 'observer' in class_name:
                if "Observer Pattern" not in insights["design_patterns"]:
                    insights["design_patterns"].append("Observer Pattern")
            elif 'adapter' in class_name:
                if "Adapter Pattern" not in insights["design_patterns"]:
                    insights["design_patterns"].append("Adapter Pattern")

class DependencyAnalyzer:
    """
    Analyzes code dependencies and architectural relationships
    
    Features:
    - Builds comprehensive dependency graphs
    - Detects circular dependencies
    - Calculates coupling metrics
    - Identifies architectural violations
    - Suggests refactoring opportunities
    """
    
    def __init__(self):
        self.dependency_graph = defaultdict(set)  # source -> {targets}
        self.reverse_graph = defaultdict(set)     # target -> {sources}
        self.modules = {}  # file_path -> ModuleInfo
        self.dependency_edges = []  # List of DependencyEdge objects
    
    def analyze_repository_dependencies(self, repo_path: str, ast_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze dependency relationships in entire repository
        
        Args:
            repo_path: Path to repository root
            ast_analysis: Optional AST analysis results for enhanced accuracy
            
        Returns:
            Comprehensive dependency analysis results
        """
        logger.info(f"Starting dependency analysis of repository: {repo_path}")
        
        # Clear previous analysis
        self.dependency_graph.clear()
        self.reverse_graph.clear()
        self.modules.clear()
        self.dependency_edges.clear()
        
        # Scan repository for dependency relationships
        self._scan_repository(repo_path, ast_analysis)
        
        # Build analysis results
        analysis_results = {
            "total_modules": len(self.modules),
            "total_dependencies": len(self.dependency_edges),
            "dependency_graph": self._serialize_graph(),
            "circular_dependencies": self._detect_circular_dependencies(),
            "coupling_metrics": self._calculate_coupling_metrics(),
            "architectural_violations": self._detect_architectural_violations(),
            "refactoring_suggestions": self._generate_refactoring_suggestions(),
            "dependency_breakdown": self._analyze_dependency_types(),
            "critical_modules": self._identify_critical_modules(),
            "module_details": {path: self._module_to_dict(module) for path, module in self.modules.items()}
        }
        
        logger.info(f"Dependency analysis completed: {analysis_results['total_modules']} modules, "
                   f"{analysis_results['total_dependencies']} dependencies, "
                   f"{len(analysis_results['circular_dependencies'])} circular dependencies")
        
        return analysis_results
    
    def _scan_repository(self, repo_path: str, ast_analysis: Dict[str, Any] = None):
        """Scan repository files for dependency information"""
        supported_extensions = {'.py', '.php', '.js', '.ts', '.jsx', '.tsx'}
        
        for root, dirs, files in os.walk(repo_path):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'vendor', '.env']]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                if file_ext in supported_extensions:
                    try:
                        self._analyze_file_dependencies(file_path, repo_path, ast_analysis)
                    except Exception as e:
                        logger.warning(f"Failed to analyze dependencies for {file_path}: {str(e)}")
                        continue
    
    def _analyze_file_dependencies(self, file_path: str, repo_path: str, ast_analysis: Dict[str, Any] = None):
        """Analyze dependencies for a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Cannot read file {file_path}: {str(e)}")
            return
        
        # Determine file language and module name
        file_ext = Path(file_path).suffix.lower()
        language = self._get_language_from_extension(file_ext)
        module_name = self._get_module_name(file_path, repo_path)
        
        # Create module info
        module_info = ModuleInfo(
            file_path=file_path,
            module_name=module_name,
            language=language,
            dependencies_out=[],
            dependencies_in=[]
        )
        
        # Extract dependencies based on language
        if language == 'python':
            dependencies = self._extract_python_dependencies(content, file_path)
        elif language == 'php':
            dependencies = self._extract_php_dependencies(content, file_path)
        elif language in ['javascript', 'typescript']:
            dependencies = self._extract_js_dependencies(content, file_path)
        else:
            dependencies = []
        
        # Process extracted dependencies
        for dep in dependencies:
            self._add_dependency(module_name, dep.target, dep.dependency_type, dep.line_number)
            module_info.dependencies_out.append(dep.target)
        
        self.modules[file_path] = module_info
    
    def _extract_python_dependencies(self, content: str, file_path: str) -> List[DependencyEdge]:
        """Extract Python dependencies (imports)"""
        dependencies = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Standard imports
            import_match = re.match(r'import\s+([\w\.]+)(?:\s+as\s+\w+)?', line)
            if import_match:
                module = import_match.group(1)
                dependencies.append(DependencyEdge(
                    source=file_path,
                    target=module,
                    dependency_type='import',
                    line_number=i
                ))
            
            # From imports
            from_match = re.match(r'from\s+([\w\.]+)\s+import\s+', line)
            if from_match:
                module = from_match.group(1)
                dependencies.append(DependencyEdge(
                    source=file_path,
                    target=module,
                    dependency_type='from_import',
                    line_number=i
                ))
        
        return dependencies
    
    def _extract_php_dependencies(self, content: str, file_path: str) -> List[DependencyEdge]:
        """Extract PHP dependencies (includes, requires, use statements)"""
        dependencies = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Include/require statements
            include_patterns = [
                (r'include\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', 'include'),
                (r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', 'require'),
                (r'include_once\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', 'include_once'),
                (r'require_once\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', 'require_once'),
                (r'include\s+[\'"]([^\'"]+)[\'"]', 'include'),
                (r'require\s+[\'"]([^\'"]+)[\'"]', 'require')
            ]
            
            for pattern, dep_type in include_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    target = match.group(1)
                    dependencies.append(DependencyEdge(
                        source=file_path,
                        target=target,
                        dependency_type=dep_type,
                        line_number=i
                    ))
            
            # Use statements (namespaces)
            use_match = re.match(r'use\s+([\w\\]+)(?:\s+as\s+\w+)?;?', line, re.IGNORECASE)
            if use_match:
                namespace = use_match.group(1)
                dependencies.append(DependencyEdge(
                    source=file_path,
                    target=namespace,
                    dependency_type='use',
                    line_number=i
                ))
            
            # Class extends
            extends_match = re.search(r'class\s+\w+\s+extends\s+([\w\\]+)', line, re.IGNORECASE)
            if extends_match:
                parent_class = extends_match.group(1)
                dependencies.append(DependencyEdge(
                    source=file_path,
                    target=parent_class,
                    dependency_type='extends',
                    line_number=i,
                    strength=2.0  # Higher coupling for inheritance
                ))
            
            # Interface implements
            implements_match = re.search(r'implements\s+([\w\\,\s]+)', line, re.IGNORECASE)
            if implements_match:
                interfaces = [iface.strip() for iface in implements_match.group(1).split(',')]
                for interface in interfaces:
                    dependencies.append(DependencyEdge(
                        source=file_path,
                        target=interface,
                        dependency_type='implements',
                        line_number=i,
                        strength=1.5  # Medium coupling for interfaces
                    ))
        
        return dependencies
    
    def _extract_js_dependencies(self, content: str, file_path: str) -> List[DependencyEdge]:
        """Extract JavaScript/TypeScript dependencies"""
        dependencies = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # ES6 imports
            import_patterns = [
                (r'import\s+\w+\s+from\s+[\'"]([^\'"]+)[\'"]', 'import_default'),
                (r'import\s+\{[^}]+\}\s+from\s+[\'"]([^\'"]+)[\'"]', 'import_named'),
                (r'import\s+\*\s+as\s+\w+\s+from\s+[\'"]([^\'"]+)[\'"]', 'import_namespace'),
                (r'import\s+[\'"]([^\'"]+)[\'"]', 'import_side_effect')
            ]
            
            for pattern, dep_type in import_patterns:
                match = re.search(pattern, line)
                if match:
                    module = match.group(1)
                    dependencies.append(DependencyEdge(
                        source=file_path,
                        target=module,
                        dependency_type=dep_type,
                        line_number=i
                    ))
            
            # CommonJS require
            require_match = re.search(r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', line)
            if require_match:
                module = require_match.group(1)
                dependencies.append(DependencyEdge(
                    source=file_path,
                    target=module,
                    dependency_type='require',
                    line_number=i
                ))
            
            # Class extends
            extends_match = re.search(r'class\s+\w+\s+extends\s+([\w\.]+)', line)
            if extends_match:
                parent_class = extends_match.group(1)
                dependencies.append(DependencyEdge(
                    source=file_path,
                    target=parent_class,
                    dependency_type='extends',
                    line_number=i,
                    strength=2.0
                ))
        
        return dependencies
    
    def _add_dependency(self, source: str, target: str, dep_type: str, line_number: int):
        """Add a dependency relationship to the graph"""
        self.dependency_graph[source].add(target)
        self.reverse_graph[target].add(source)
        
        edge = DependencyEdge(
            source=source,
            target=target,
            dependency_type=dep_type,
            line_number=line_number
        )
        self.dependency_edges.append(edge)
    
    def _detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies using DFS"""
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node, path):
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                if len(cycle) > 2:  # Ignore self-loops
                    cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.dependency_graph.get(node, []):
                dfs(neighbor, path + [node])
            
            rec_stack.remove(node)
        
        for node in self.dependency_graph:
            if node not in visited:
                dfs(node, [])
        
        # Remove duplicates and sort by length
        unique_cycles = []
        for cycle in cycles:
            normalized = self._normalize_cycle(cycle)
            if normalized not in unique_cycles:
                unique_cycles.append(normalized)
        
        return sorted(unique_cycles, key=len)
    
    def _normalize_cycle(self, cycle: List[str]) -> List[str]:
        """Normalize cycle representation for deduplication"""
        if not cycle:
            return cycle
        
        # Find the lexicographically smallest starting point
        min_idx = cycle.index(min(cycle))
        return cycle[min_idx:] + cycle[:min_idx]
    
    def _calculate_coupling_metrics(self) -> Dict[str, Any]:
        """Calculate various coupling metrics"""
        total_modules = len(self.modules)
        if total_modules == 0:
            return {}
        
        # Calculate coupling for each module
        for module_info in self.modules.values():
            module_name = module_info.module_name
            
            # Efferent coupling (Ce) - dependencies going out
            module_info.coupling_out = len(self.dependency_graph.get(module_name, set()))
            
            # Afferent coupling (Ca) - dependencies coming in
            module_info.coupling_in = len(self.reverse_graph.get(module_name, set()))
            
            # Instability (I) = Ce / (Ca + Ce)
            total_coupling = module_info.coupling_in + module_info.coupling_out
            module_info.instability = module_info.coupling_out / total_coupling if total_coupling > 0 else 0
        
        # Calculate aggregate metrics
        coupling_values = [(m.coupling_in, m.coupling_out, m.instability) for m in self.modules.values()]
        
        if coupling_values:
            avg_coupling_in = sum(c[0] for c in coupling_values) / len(coupling_values)
            avg_coupling_out = sum(c[1] for c in coupling_values) / len(coupling_values)
            avg_instability = sum(c[2] for c in coupling_values) / len(coupling_values)
            
            max_coupling_in = max(c[0] for c in coupling_values)
            max_coupling_out = max(c[1] for c in coupling_values)
        else:
            avg_coupling_in = avg_coupling_out = avg_instability = 0
            max_coupling_in = max_coupling_out = 0
        
        return {
            "average_coupling_in": avg_coupling_in,
            "average_coupling_out": avg_coupling_out,
            "average_instability": avg_instability,
            "max_coupling_in": max_coupling_in,
            "max_coupling_out": max_coupling_out,
            "total_dependency_relationships": len(self.dependency_edges)
        }
    
    def _detect_architectural_violations(self) -> List[Dict[str, Any]]:
        """Detect architectural violations and anti-patterns"""
        violations = []
        
        # Detect modules with excessive coupling
        for module_info in self.modules.values():
            if module_info.coupling_out > 10:  # Threshold for excessive efferent coupling
                violations.append({
                    "type": "excessive_outgoing_dependencies",
                    "module": module_info.module_name,
                    "file_path": module_info.file_path,
                    "coupling_out": module_info.coupling_out,
                    "severity": "medium",
                    "description": f"Module has {module_info.coupling_out} outgoing dependencies (threshold: 10)"
                })
            
            if module_info.coupling_in > 15:  # Threshold for excessive afferent coupling
                violations.append({
                    "type": "excessive_incoming_dependencies",
                    "module": module_info.module_name,
                    "file_path": module_info.file_path,
                    "coupling_in": module_info.coupling_in,
                    "severity": "medium",
                    "description": f"Module has {module_info.coupling_in} incoming dependencies (threshold: 15)"
                })
            
            if module_info.instability > 0.8 and module_info.coupling_in > 5:
                violations.append({
                    "type": "unstable_dependency",
                    "module": module_info.module_name,
                    "file_path": module_info.file_path,
                    "instability": module_info.instability,
                    "severity": "high",
                    "description": f"Module is highly unstable (I={module_info.instability:.2f}) but heavily depended upon"
                })
        
        return violations
    
    def _generate_refactoring_suggestions(self) -> List[Dict[str, Any]]:
        """Generate refactoring suggestions based on dependency analysis"""
        suggestions = []
        
        # Suggest breaking circular dependencies
        cycles = self._detect_circular_dependencies()
        for cycle in cycles:
            suggestions.append({
                "type": "break_circular_dependency",
                "priority": "high",
                "modules": cycle,
                "description": f"Break circular dependency: {' -> '.join(cycle)}",
                "techniques": ["Dependency Injection", "Interface Segregation", "Extract Interface"]
            })
        
        # Suggest reducing coupling for highly coupled modules
        for module_info in self.modules.values():
            if module_info.coupling_out > 8:
                suggestions.append({
                    "type": "reduce_coupling",
                    "priority": "medium",
                    "module": module_info.module_name,
                    "file_path": module_info.file_path,
                    "current_coupling": module_info.coupling_out,
                    "description": f"Reduce outgoing dependencies from {module_info.coupling_out} to under 8",
                    "techniques": ["Extract Service", "Facade Pattern", "Dependency Injection"]
                })
        
        return suggestions
    
    def _analyze_dependency_types(self) -> Dict[str, int]:
        """Analyze the distribution of dependency types"""
        type_counts = defaultdict(int)
        for edge in self.dependency_edges:
            type_counts[edge.dependency_type] += 1
        return dict(type_counts)
    
    def _identify_critical_modules(self) -> List[Dict[str, Any]]:
        """Identify critical modules based on coupling metrics"""
        critical_modules = []
        
        for module_info in self.modules.values():
            # Critical if high incoming coupling (many modules depend on it)
            if module_info.coupling_in > 8:
                critical_modules.append({
                    "module": module_info.module_name,
                    "file_path": module_info.file_path,
                    "coupling_in": module_info.coupling_in,
                    "coupling_out": module_info.coupling_out,
                    "instability": module_info.instability,
                    "criticality_reason": "high_incoming_dependencies"
                })
        
        # Sort by incoming coupling (descending)
        critical_modules.sort(key=lambda x: x["coupling_in"], reverse=True)
        
        return critical_modules[:10]  # Return top 10 critical modules
    
    def _serialize_graph(self) -> Dict[str, List[str]]:
        """Serialize dependency graph for JSON output"""
        return {source: list(targets) for source, targets in self.dependency_graph.items()}
    
    def _module_to_dict(self, module: ModuleInfo) -> Dict[str, Any]:
        """Convert ModuleInfo to dictionary"""
        return {
            "module_name": module.module_name,
            "language": module.language,
            "dependencies_out": module.dependencies_out,
            "dependencies_in": module.dependencies_in,
            "coupling_in": module.coupling_in,
            "coupling_out": module.coupling_out,
            "instability": module.instability
        }
    
    def _get_language_from_extension(self, ext: str) -> str:
        """Map file extension to language"""
        mapping = {
            '.py': 'python',
            '.php': 'php',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript'
        }
        return mapping.get(ext.lower(), 'unknown')
    
    def _get_module_name(self, file_path: str, repo_path: str) -> str:
        """Generate module name from file path"""
        rel_path = os.path.relpath(file_path, repo_path)
        return rel_path.replace(os.sep, '.').replace('.py', '').replace('.php', '').replace('.js', '').replace('.ts', '')

class QualityAnalyzer:
    """
    Comprehensive code quality analyzer
    
    Features:
    - Cyclomatic and cognitive complexity analysis
    - Halstead complexity metrics
    - Code smell detection
    - Maintainability index calculation
    - Quality scoring and assessment
    - Multi-language support
    """
    
    def __init__(self):
        self.quality_rules = self._load_quality_rules()
        self.code_smells = []
        self.complexity_metrics = {}
    
    def analyze_repository_quality(self, repo_path: str, ast_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze code quality for entire repository
        
        Args:
            repo_path: Path to repository root
            ast_analysis: Optional AST analysis results for enhanced accuracy
            
        Returns:
            Comprehensive quality analysis results
        """
        logger.info(f"Starting quality analysis of repository: {repo_path}")
        
        # Clear previous analysis
        self.code_smells.clear()
        self.complexity_metrics.clear()
        
        # Scan repository for quality issues
        quality_results = {
            "files_analyzed": 0,
            "total_code_smells": 0,
            "complexity_summary": {},
            "quality_scores": {},
            "code_smells": [],
            "maintainability_assessment": {},
            "technical_debt": {},
            "quality_trends": {},
            "recommendations": []
        }
        
        supported_extensions = {'.py', '.php', '.js', '.ts', '.jsx', '.tsx'}
        file_complexities = []
        all_code_smells = []
        
        try:
            for root, dirs, files in os.walk(repo_path):
                # Skip common non-source directories
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'vendor', '.env']]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = Path(file).suffix.lower()
                    
                    if file_ext in supported_extensions:
                        try:
                            file_quality = self._analyze_file_quality(file_path, ast_analysis)
                            if file_quality:
                                quality_results["files_analyzed"] += 1
                                file_complexities.append(file_quality["complexity_metrics"])
                                all_code_smells.extend(file_quality["code_smells"])
                                
                        except Exception as e:
                            logger.warning(f"Failed to analyze quality for {file_path}: {str(e)}")
                            continue
        
        except Exception as e:
            logger.error(f"Quality analysis failed: {str(e)}")
            return quality_results
        
        # Aggregate results
        quality_results["total_code_smells"] = len(all_code_smells)
        quality_results["code_smells"] = all_code_smells
        quality_results["complexity_summary"] = self._calculate_complexity_summary(file_complexities)
        quality_results["quality_scores"] = self._calculate_overall_quality_score(file_complexities, all_code_smells)
        quality_results["maintainability_assessment"] = self._assess_maintainability(file_complexities, all_code_smells)
        quality_results["technical_debt"] = self._calculate_technical_debt(all_code_smells, file_complexities)
        quality_results["recommendations"] = self._generate_quality_recommendations(all_code_smells, file_complexities)
        
        logger.info(f"Quality analysis completed: {quality_results['files_analyzed']} files, "
                   f"{quality_results['total_code_smells']} code smells detected")
        
        return quality_results
    
    def _analyze_file_quality(self, file_path: str, ast_analysis: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Analyze quality metrics for a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Cannot read file {file_path}: {str(e)}")
            return None
        
        file_ext = Path(file_path).suffix.lower()
        language = self._get_language_from_extension(file_ext)
        
        # Calculate complexity metrics
        complexity_metrics = self._calculate_file_complexity(content, file_path, language)
        
        # Detect code smells
        code_smells = self._detect_code_smells(content, file_path, language)
        
        # Calculate file quality score
        quality_score = self._calculate_file_quality_score(complexity_metrics, code_smells)
        
        return {
            "file_path": file_path,
            "language": language,
            "complexity_metrics": complexity_metrics,
            "code_smells": code_smells,
            "quality_score": quality_score,
            "lines_of_code": len(content.splitlines())
        }
    
    def _calculate_file_complexity(self, content: str, file_path: str, language: str) -> ComplexityMetrics:
        """Calculate various complexity metrics for a file"""
        lines = content.splitlines()
        total_lines = len(lines)
        logical_lines = len([line for line in lines if line.strip() and not line.strip().startswith(('#', '//', '/*'))])
        
        if language == 'python':
            cyclomatic = self._calculate_python_cyclomatic_complexity(content)
            cognitive = self._calculate_python_cognitive_complexity(content)
            halstead = self._calculate_python_halstead_complexity(content)
        elif language == 'php':
            cyclomatic = self._calculate_php_cyclomatic_complexity(content)
            cognitive = self._calculate_php_cognitive_complexity(content)
            halstead = self._calculate_generic_halstead_complexity(content, language)
        elif language in ['javascript', 'typescript']:
            cyclomatic = self._calculate_js_cyclomatic_complexity(content)
            cognitive = self._calculate_js_cognitive_complexity(content)
            halstead = self._calculate_generic_halstead_complexity(content, language)
        else:
            cyclomatic = cognitive = 1.0
            halstead = {"volume": 0, "difficulty": 0, "effort": 0}
        
        # Calculate maintainability index
        maintainability = self._calculate_maintainability_index(
            halstead.get("volume", 0), cyclomatic, logical_lines
        )
        
        return ComplexityMetrics(
            cyclomatic_complexity=cyclomatic,
            cognitive_complexity=cognitive,
            halstead_complexity=halstead,
            maintainability_index=maintainability,
            lines_of_code=total_lines,
            logical_lines=logical_lines
        )
    
    def _calculate_python_cyclomatic_complexity(self, content: str) -> float:
        """Calculate cyclomatic complexity for Python code"""
        try:
            tree = ast.parse(content)
            complexity = 1  # Base complexity
            
            for node in ast.walk(tree):
                # Decision points that increase complexity
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                    complexity += 1
                elif isinstance(node, ast.ExceptHandler):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
                elif isinstance(node, ast.ListComp):
                    complexity += 1
                elif isinstance(node, ast.SetComp):
                    complexity += 1
                elif isinstance(node, ast.DictComp):
                    complexity += 1
                elif isinstance(node, ast.GeneratorExp):
                    complexity += 1
            
            return float(complexity)
            
        except Exception as e:
            logger.warning(f"Failed to calculate Python cyclomatic complexity: {str(e)}")
            return 1.0
    
    def _calculate_php_cyclomatic_complexity(self, content: str) -> float:
        """Calculate cyclomatic complexity for PHP code using regex"""
        complexity = 1  # Base complexity
        
        # PHP decision points
        patterns = [
            r'\bif\s*\(',
            r'\bwhile\s*\(',
            r'\bfor\s*\(',
            r'\bforeach\s*\(',
            r'\bdo\s*\{',
            r'\bswitch\s*\(',
            r'\bcase\s+',
            r'\bcatch\s*\(',
            r'\b\|\|\b',
            r'\b&&\b',
            r'\?\s*.*\s*:'  # Ternary operator
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            complexity += len(matches)
        
        return float(complexity)
    
    def _calculate_js_cyclomatic_complexity(self, content: str) -> float:
        """Calculate cyclomatic complexity for JavaScript/TypeScript code"""
        complexity = 1  # Base complexity
        
        # JavaScript decision points
        patterns = [
            r'\bif\s*\(',
            r'\bwhile\s*\(',
            r'\bfor\s*\(',
            r'\bdo\s*\{',
            r'\bswitch\s*\(',
            r'\bcase\s+',
            r'\bcatch\s*\(',
            r'\b\|\|\b',
            r'\b&&\b',
            r'\?\s*.*\s*:'  # Ternary operator
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            complexity += len(matches)
        
        return float(complexity)
    
    def _calculate_python_cognitive_complexity(self, content: str) -> float:
        """Calculate cognitive complexity for Python code"""
        try:
            tree = ast.parse(content)
            complexity = 0
            nesting_level = 0
            
            def visit_node(node, level=0):
                nonlocal complexity, nesting_level
                
                # Increase complexity based on node type and nesting
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                    complexity += 1 + level
                elif isinstance(node, ast.BoolOp):
                    complexity += 1
                elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                    complexity += 1
                
                # Increase nesting for certain constructs
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.With, ast.AsyncWith)):
                    for child in ast.iter_child_nodes(node):
                        visit_node(child, level + 1)
                else:
                    for child in ast.iter_child_nodes(node):
                        visit_node(child, level)
            
            visit_node(tree)
            return float(complexity)
            
        except Exception as e:
            logger.warning(f"Failed to calculate Python cognitive complexity: {str(e)}")
            return 1.0
    
    def _calculate_php_cognitive_complexity(self, content: str) -> float:
        """Calculate cognitive complexity for PHP code"""
        # Simplified cognitive complexity for PHP
        complexity = 0
        lines = content.split('\n')
        nesting_level = 0
        
        for line in lines:
            line = line.strip()
            
            # Count opening braces to track nesting
            if '{' in line:
                nesting_level += line.count('{')
            if '}' in line:
                nesting_level = max(0, nesting_level - line.count('}'))
            
            # Add complexity based on control structures
            if re.search(r'\b(if|while|for|foreach)\s*\(', line, re.IGNORECASE):
                complexity += 1 + nesting_level
            elif re.search(r'\b(case|catch)\b', line, re.IGNORECASE):
                complexity += 1
        
        return float(complexity)
    
    def _calculate_js_cognitive_complexity(self, content: str) -> float:
        """Calculate cognitive complexity for JavaScript/TypeScript code"""
        # Simplified cognitive complexity for JavaScript
        complexity = 0
        lines = content.split('\n')
        nesting_level = 0
        
        for line in lines:
            line = line.strip()
            
            # Count braces to track nesting
            if '{' in line:
                nesting_level += line.count('{')
            if '}' in line:
                nesting_level = max(0, nesting_level - line.count('}'))
            
            # Add complexity based on control structures
            if re.search(r'\b(if|while|for)\s*\(', line):
                complexity += 1 + nesting_level
            elif re.search(r'\b(case|catch)\b', line):
                complexity += 1
        
        return float(complexity)
    
    def _calculate_python_halstead_complexity(self, content: str) -> Dict[str, float]:
        """Calculate Halstead complexity metrics for Python code"""
        try:
            tree = ast.parse(content)
            
            operators = set()
            operands = set()
            total_operators = 0
            total_operands = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow)):
                    operators.add(type(node).__name__)
                    total_operators += 1
                elif isinstance(node, ast.Name):
                    operands.add(node.id)
                    total_operands += 1
                elif isinstance(node, (ast.Num, ast.Str, ast.Constant)):
                    operands.add(str(node.n if hasattr(node, 'n') else getattr(node, 'value', 'constant')))
                    total_operands += 1
            
            return self._calculate_halstead_metrics(
                len(operators), len(operands), total_operators, total_operands
            )
            
        except Exception as e:
            logger.warning(f"Failed to calculate Python Halstead complexity: {str(e)}")
            return {"volume": 0, "difficulty": 0, "effort": 0}
    
    def _calculate_generic_halstead_complexity(self, content: str, language: str) -> Dict[str, float]:
        """Calculate simplified Halstead complexity for any language"""
        # Simplified approach using regex patterns
        operators = set(re.findall(r'[+\-*/=%<>!&|]', content))
        operands = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', content))
        
        total_operators = len(re.findall(r'[+\-*/=%<>!&|]', content))
        total_operands = len(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', content))
        
        return self._calculate_halstead_metrics(
            len(operators), len(operands), total_operators, total_operands
        )
    
    def _calculate_halstead_metrics(self, n1: int, n2: int, N1: int, N2: int) -> Dict[str, float]:
        """Calculate Halstead complexity metrics"""
        if n1 == 0 or n2 == 0 or N1 == 0 or N2 == 0:
            return {"volume": 0, "difficulty": 0, "effort": 0}
        
        # Halstead metrics
        vocabulary = n1 + n2
        length = N1 + N2
        
        # Avoid log(0)
        if vocabulary <= 0:
            return {"volume": 0, "difficulty": 0, "effort": 0}
        
        volume = length * math.log2(vocabulary)
        difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
        effort = difficulty * volume
        
        return {
            "volume": volume,
            "difficulty": difficulty,
            "effort": effort,
            "vocabulary": vocabulary,
            "length": length
        }
    
    def _calculate_maintainability_index(self, halstead_volume: float, cyclomatic: float, loc: int) -> float:
        """Calculate maintainability index"""
        if loc == 0:
            return 100.0
        
        # Maintainability Index formula
        # MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)
        # Where HV = Halstead Volume, CC = Cyclomatic Complexity, LOC = Lines of Code
        
        if halstead_volume <= 0:
            halstead_volume = 1
        if cyclomatic <= 0:
            cyclomatic = 1
        if loc <= 0:
            loc = 1
        
        mi = 171 - 5.2 * math.log(halstead_volume) - 0.23 * cyclomatic - 16.2 * math.log(loc)
        
        # Normalize to 0-100 scale
        return max(0, min(100, mi))
    
    def _detect_code_smells(self, content: str, file_path: str, language: str) -> List[CodeSmell]:
        """Detect various code smells in the file"""
        code_smells = []
        lines = content.split('\n')
        
        # Common code smells across languages
        code_smells.extend(self._detect_long_methods(lines, file_path, language))
        code_smells.extend(self._detect_long_parameter_lists(content, file_path, language))
        code_smells.extend(self._detect_duplicate_code(lines, file_path))
        code_smells.extend(self._detect_dead_code(content, file_path, language))
        code_smells.extend(self._detect_magic_numbers(lines, file_path))
        code_smells.extend(self._detect_long_lines(lines, file_path))
        code_smells.extend(self._detect_deeply_nested_code(lines, file_path, language))
        
        # Language-specific smells
        if language == 'python':
            code_smells.extend(self._detect_python_specific_smells(content, file_path))
        elif language == 'php':
            code_smells.extend(self._detect_php_specific_smells(content, file_path))
        elif language in ['javascript', 'typescript']:
            code_smells.extend(self._detect_js_specific_smells(content, file_path))
        
        return code_smells
    
    def _detect_long_methods(self, lines: List[str], file_path: str, language: str) -> List[CodeSmell]:
        """Detect methods that are too long"""
        smells = []
        current_method = None
        method_start = 0
        brace_count = 0
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Detect method starts
            if language == 'python':
                if line.startswith('def '):
                    current_method = line
                    method_start = i
            elif language == 'php':
                if re.search(r'function\s+\w+\s*\(', line, re.IGNORECASE):
                    current_method = line
                    method_start = i
                    brace_count = 0
            elif language in ['javascript', 'typescript']:
                if re.search(r'function\s+\w+\s*\(|^\s*\w+\s*\(.*\)\s*\{', line):
                    current_method = line
                    method_start = i
                    brace_count = 0
            
            # Track braces for non-Python languages
            if language != 'python':
                brace_count += line.count('{') - line.count('}')
                
                if current_method and brace_count == 0 and '}' in line:
                    method_length = i - method_start + 1
                    if method_length > 50:  # Threshold for long methods
                        smells.append(CodeSmell(
                            type="long_method",
                            file_path=file_path,
                            line_number=method_start,
                            severity="medium",
                            description=f"Method is {method_length} lines long (threshold: 50)",
                            suggestion="Consider breaking this method into smaller, more focused methods"
                        ))
                    current_method = None
            else:
                # Python: detect method end by indentation
                if current_method and line and not line.startswith(' ') and not line.startswith('\t'):
                    method_length = i - method_start
                    if method_length > 40:  # Lower threshold for Python due to indentation
                        smells.append(CodeSmell(
                            type="long_method",
                            file_path=file_path,
                            line_number=method_start,
                            severity="medium",
                            description=f"Method is {method_length} lines long (threshold: 40)",
                            suggestion="Consider breaking this method into smaller, more focused methods"
                        ))
                    current_method = None
        
        return smells
    
    def _detect_long_parameter_lists(self, content: str, file_path: str, language: str) -> List[CodeSmell]:
        """Detect methods with too many parameters"""
        smells = []
        
        if language == 'python':
            pattern = r'def\s+\w+\s*\(([^)]+)\)'
        elif language == 'php':
            pattern = r'function\s+\w+\s*\(([^)]+)\)'
        elif language in ['javascript', 'typescript']:
            pattern = r'function\s+\w+\s*\(([^)]+)\)|^\s*\w+\s*\(([^)]+)\)\s*\{'
        else:
            return smells
        
        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            params_str = match.group(1) or match.group(2) if match.lastindex == 2 else match.group(1)
            if params_str:
                params = [p.strip() for p in params_str.split(',') if p.strip()]
                if len(params) > 6:  # Threshold for too many parameters
                    line_number = content[:match.start()].count('\n') + 1
                    smells.append(CodeSmell(
                        type="long_parameter_list",
                        file_path=file_path,
                        line_number=line_number,
                        severity="medium",
                        description=f"Method has {len(params)} parameters (threshold: 6)",
                        suggestion="Consider using a parameter object or breaking the method down"
                    ))
        
        return smells
    
    def _detect_duplicate_code(self, lines: List[str], file_path: str) -> List[CodeSmell]:
        """Detect potential duplicate code blocks"""
        smells = []
        line_groups = defaultdict(list)
        
        # Group lines by content (ignoring whitespace)
        for i, line in enumerate(lines, 1):
            normalized = re.sub(r'\s+', ' ', line.strip())
            if len(normalized) > 10:  # Only check substantial lines
                line_groups[normalized].append(i)
        
        # Find duplicated lines
        for normalized_line, line_numbers in line_groups.items():
            if len(line_numbers) > 2:  # More than 2 occurrences
                smells.append(CodeSmell(
                    type="duplicate_code",
                    file_path=file_path,
                    line_number=line_numbers[0],
                    severity="low",
                    description=f"Line appears {len(line_numbers)} times in the file",
                    suggestion="Consider extracting common code into a reusable function"
                ))
        
        return smells
    
    def _detect_dead_code(self, content: str, file_path: str, language: str) -> List[CodeSmell]:
        """Detect potentially dead code"""
        smells = []
        
        # Look for unreachable code after return statements
        if language == 'python':
            pattern = r'^\s*return\s+.*\n(.*\n)*?\s*\w+'
        elif language in ['php', 'javascript', 'typescript']:
            pattern = r'return\s+.*;\s*\n\s*\w+'
        else:
            return smells
        
        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            line_number = content[:match.start()].count('\n') + 2  # Line after return
            smells.append(CodeSmell(
                type="dead_code",
                file_path=file_path,
                line_number=line_number,
                severity="medium",
                description="Code appears after return statement",
                suggestion="Remove unreachable code or restructure the logic"
            ))
        
        return smells
    
    def _detect_magic_numbers(self, lines: List[str], file_path: str) -> List[CodeSmell]:
        """Detect magic numbers in code"""
        smells = []
        
        for i, line in enumerate(lines, 1):
            # Look for numeric literals (excluding 0, 1, -1)
            numbers = re.findall(r'\b(?<![\w\.])\d{2,}\b(?![\w\.])', line)
            for number in numbers:
                if int(number) not in [0, 1, 100]:  # Common acceptable numbers
                    smells.append(CodeSmell(
                        type="magic_number",
                        file_path=file_path,
                        line_number=i,
                        severity="low",
                        description=f"Magic number '{number}' found",
                        suggestion="Consider defining this as a named constant"
                    ))
        
        return smells
    
    def _detect_long_lines(self, lines: List[str], file_path: str) -> List[CodeSmell]:
        """Detect lines that are too long - disabled for complete content processing"""
        smells = []
        # Line length checking disabled to avoid artificial content limitations
        return smells
        
        return smells
    
    def _detect_deeply_nested_code(self, lines: List[str], file_path: str, language: str) -> List[CodeSmell]:
        """Detect deeply nested code structures"""
        smells = []
        max_nesting = 4
        
        for i, line in enumerate(lines, 1):
            if language == 'python':
                # Count indentation level
                stripped = line.lstrip()
                if stripped:
                    indentation = len(line) - len(stripped)
                    nesting_level = indentation // 4  # Assuming 4-space indentation
                    
                    if nesting_level > max_nesting:
                        smells.append(CodeSmell(
                            type="deep_nesting",
                            file_path=file_path,
                            line_number=i,
                            severity="medium",
                            description=f"Code is nested {nesting_level} levels deep (threshold: {max_nesting})",
                            suggestion="Consider extracting nested logic into separate methods"
                        ))
            else:
                # Count brace nesting for other languages
                if '{' in line:
                    brace_level = line.count('{') - line.count('}')
                    if brace_level > max_nesting:
                        smells.append(CodeSmell(
                            type="deep_nesting",
                            file_path=file_path,
                            line_number=i,
                            severity="medium",
                            description=f"Code appears to be deeply nested",
                            suggestion="Consider extracting nested logic into separate methods"
                        ))
        
        return smells
    
    def _detect_python_specific_smells(self, content: str, file_path: str) -> List[CodeSmell]:
        """Detect Python-specific code smells"""
        smells = []
        
        # Unused imports
        imports = re.findall(r'import\s+([\w\.]+)', content)
        for imp in imports:
            if content.count(imp.split('.')[-1]) == 1:  # Only appears in import
                line_number = content.find(f'import {imp}')
                line_number = content[:line_number].count('\n') + 1
                smells.append(CodeSmell(
                    type="unused_import",
                    file_path=file_path,
                    line_number=line_number,
                    severity="low",
                    description=f"Import '{imp}' appears to be unused",
                    suggestion="Remove unused imports to improve code clarity"
                ))
        
        return smells
    
    def _detect_php_specific_smells(self, content: str, file_path: str) -> List[CodeSmell]:
        """Detect PHP-specific code smells"""
        smells = []
        
        # Global variables
        global_vars = re.finditer(r'\$GLOBALS\[|global\s+\$', content, re.IGNORECASE)
        for match in global_vars:
            line_number = content[:match.start()].count('\n') + 1
            smells.append(CodeSmell(
                type="global_variable",
                file_path=file_path,
                line_number=line_number,
                severity="medium",
                description="Global variable usage detected",
                suggestion="Consider using dependency injection or class properties"
            ))
        
        return smells
    
    def _detect_js_specific_smells(self, content: str, file_path: str) -> List[CodeSmell]:
        """Detect JavaScript/TypeScript-specific code smells"""
        smells = []
        
        # == instead of ===
        loose_equality = re.finditer(r'==(?!=)', content)
        for match in loose_equality:
            line_number = content[:match.start()].count('\n') + 1
            smells.append(CodeSmell(
                type="loose_equality",
                file_path=file_path,
                line_number=line_number,
                severity="medium",
                description="Use of loose equality (==) instead of strict equality (===)",
                suggestion="Use strict equality (===) to avoid type coercion issues"
            ))
        
        return smells
    
    def _calculate_complexity_summary(self, complexities: List[ComplexityMetrics]) -> Dict[str, Any]:
        """Calculate summary statistics for complexity metrics"""
        if not complexities:
            return {}
        
        cyclomatic_values = [c.cyclomatic_complexity for c in complexities]
        cognitive_values = [c.cognitive_complexity for c in complexities]
        maintainability_values = [c.maintainability_index for c in complexities]
        
        return {
            "average_cyclomatic_complexity": sum(cyclomatic_values) / len(cyclomatic_values),
            "max_cyclomatic_complexity": max(cyclomatic_values),
            "average_cognitive_complexity": sum(cognitive_values) / len(cognitive_values),
            "max_cognitive_complexity": max(cognitive_values),
            "average_maintainability_index": sum(maintainability_values) / len(maintainability_values),
            "min_maintainability_index": min(maintainability_values),
            "total_lines_analyzed": sum(c.lines_of_code for c in complexities)
        }
    
    def _calculate_overall_quality_score(self, complexities: List[ComplexityMetrics], code_smells: List[CodeSmell]) -> QualityScore:
        """Calculate overall quality score"""
        if not complexities:
            return QualityScore(0, 0, 0, 0, 0, 0)
        
        # Maintainability based on maintainability index
        avg_maintainability = sum(c.maintainability_index for c in complexities) / len(complexities)
        maintainability_score = min(100, max(0, avg_maintainability))
        
        # Reliability based on complexity and code smells
        avg_complexity = sum(c.cyclomatic_complexity for c in complexities) / len(complexities)
        complexity_penalty = min(50, avg_complexity * 2)
        smell_penalty = min(30, len([s for s in code_smells if s.severity in ['high', 'critical']]) * 5)
        reliability_score = max(0, 100 - complexity_penalty - smell_penalty)
        
        # Security based on security-related smells
        security_issues = len([s for s in code_smells if 'security' in s.type.lower()])
        security_score = max(0, 100 - security_issues * 10)
        
        # Performance based on complexity
        performance_score = max(0, 100 - avg_complexity)
        
        # Readability based on code smells
        readability_issues = len([s for s in code_smells if s.type in ['long_line', 'deep_nesting', 'magic_number']])
        readability_score = max(0, 100 - readability_issues * 2)
        
        # Overall score
        overall_score = (maintainability_score + reliability_score + security_score + performance_score + readability_score) / 5
        
        return QualityScore(
            overall_score=overall_score,
            maintainability=maintainability_score,
            reliability=reliability_score,
            security=security_score,
            performance=performance_score,
            readability=readability_score
        )
    
    def _assess_maintainability(self, complexities: List[ComplexityMetrics], code_smells: List[CodeSmell]) -> Dict[str, Any]:
        """Assess maintainability of the codebase"""
        if not complexities:
            return {}
        
        avg_maintainability = sum(c.maintainability_index for c in complexities) / len(complexities)
        
        if avg_maintainability >= 80:
            assessment = "Excellent"
        elif avg_maintainability >= 60:
            assessment = "Good"
        elif avg_maintainability >= 40:
            assessment = "Fair"
        elif avg_maintainability >= 20:
            assessment = "Poor"
        else:
            assessment = "Critical"
        
        return {
            "overall_assessment": assessment,
            "average_maintainability_index": avg_maintainability,
            "files_needing_attention": len([c for c in complexities if c.maintainability_index < 40]),
            "main_issues": [s.type for s in code_smells if s.severity in ['high', 'critical']]
        }
    
    def _calculate_technical_debt(self, code_smells: List[CodeSmell], complexities: List[ComplexityMetrics]) -> Dict[str, Any]:
        """Calculate technical debt metrics"""
        # Estimate remediation effort in hours
        effort_mapping = {
            'critical': 8,
            'high': 4,
            'medium': 2,
            'low': 0.5
        }
        
        total_effort = sum(effort_mapping.get(smell.severity, 1) for smell in code_smells)
        
        # Calculate debt ratio (effort / total LOC * 1000)
        total_loc = sum(c.lines_of_code for c in complexities) if complexities else 1
        debt_ratio = (total_effort / total_loc) * 1000
        
        return {
            "estimated_remediation_hours": total_effort,
            "technical_debt_ratio": debt_ratio,
            "debt_level": "Low" if debt_ratio < 5 else "Medium" if debt_ratio < 15 else "High",
            "issues_by_severity": {
                severity: len([s for s in code_smells if s.severity == severity])
                for severity in ['critical', 'high', 'medium', 'low']
            }
        }
    
    def _generate_quality_recommendations(self, code_smells: List[CodeSmell], complexities: List[ComplexityMetrics]) -> List[Dict[str, Any]]:
        """Generate recommendations for improving code quality"""
        recommendations = []
        
        # Priority recommendations based on severity
        critical_smells = [s for s in code_smells if s.severity == 'critical']
        if critical_smells:
            recommendations.append({
                "priority": "critical",
                "title": "Address Critical Code Issues",
                "description": f"Resolve {len(critical_smells)} critical code issues immediately",
                "impact": "Prevents potential runtime failures and security vulnerabilities"
            })
        
        # Complexity recommendations
        if complexities:
            high_complexity_files = [c for c in complexities if c.cyclomatic_complexity > 10]
            if high_complexity_files:
                recommendations.append({
                    "priority": "high",
                    "title": "Reduce Code Complexity",
                    "description": f"Refactor {len(high_complexity_files)} files with high cyclomatic complexity",
                    "impact": "Improves maintainability and reduces bug risk"
                })
        
        # Maintainability recommendations
        if complexities:
            low_maintainability = [c for c in complexities if c.maintainability_index < 40]
            if low_maintainability:
                recommendations.append({
                    "priority": "medium",
                    "title": "Improve Maintainability",
                    "description": f"Focus on {len(low_maintainability)} files with low maintainability scores",
                    "impact": "Reduces future development and maintenance costs"
                })
        
        return recommendations
    
    def _calculate_file_quality_score(self, complexity: ComplexityMetrics, smells: List[CodeSmell]) -> float:
        """Calculate quality score for a single file"""
        base_score = 100
        
        # Deduct points for complexity
        complexity_penalty = min(30, complexity.cyclomatic_complexity * 2)
        
        # Deduct points for code smells
        smell_penalty = sum({
            'critical': 20,
            'high': 10,
            'medium': 5,
            'low': 1
        }.get(smell.severity, 1) for smell in smells)
        
        return max(0, base_score - complexity_penalty - smell_penalty)
    
    def _get_language_from_extension(self, ext: str) -> str:
        """Map file extension to language"""
        mapping = {
            '.py': 'python',
            '.php': 'php',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript'
        }
        return mapping.get(ext.lower(), 'unknown')
    
    def _load_quality_rules(self) -> Dict[str, Any]:
        """Load quality rules and thresholds"""
        return {
            "max_cyclomatic_complexity": 10,
            "max_cognitive_complexity": 15,
            "max_method_length": 50,
            "max_parameter_count": 6,
            "max_line_length": 120,
            "max_nesting_level": 4,
            "min_maintainability_index": 40
        }

class ArchitectureAnalyzer:
    """
    Comprehensive architecture analysis system
    
    Features:
    - MVC/MVP/MVVM pattern detection
    - Layered architecture analysis
    - Design pattern recognition
    - Microservices vs monolith assessment
    - Architectural anti-pattern detection
    - Modernization recommendations
    """
    
    def __init__(self):
        self.detected_patterns = []
        self.architectural_layers = {}
        self.design_patterns = []
        self.architecture_violations = []
    
    def analyze_repository_architecture(self, repo_path: str, ast_analysis: Dict[str, Any] = None, 
                                     dependency_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze architectural patterns and structure in repository
        
        Args:
            repo_path: Path to repository root
            ast_analysis: Optional AST analysis results
            dependency_analysis: Optional dependency analysis results
            
        Returns:
            Comprehensive architectural analysis results
        """
        logger.info(f"Starting architecture analysis of repository: {repo_path}")
        
        # Clear previous analysis
        self.detected_patterns.clear()
        self.architectural_layers.clear()
        self.design_patterns.clear()
        self.architecture_violations.clear()
        
        # Gather structural information
        file_structure = self._analyze_directory_structure(repo_path)
        
        # Detect architectural patterns
        mvc_analysis = self._detect_mvc_pattern(file_structure, repo_path)
        layered_analysis = self._detect_layered_architecture(file_structure, dependency_analysis)
        microservices_analysis = self._analyze_microservices_architecture(file_structure, repo_path)
        
        # Detect design patterns
        design_patterns = self._detect_design_patterns(repo_path, ast_analysis)
        
        # Detect anti-patterns
        anti_patterns = self._detect_architectural_antipatterns(file_structure, dependency_analysis)
        
        # Generate modernization recommendations
        modernization_recommendations = self._generate_modernization_recommendations(
            file_structure, mvc_analysis, layered_analysis, microservices_analysis
        )
        
        # Assess architecture quality
        architecture_quality = self._assess_architecture_quality(
            mvc_analysis, layered_analysis, design_patterns, anti_patterns
        )
        
        analysis_results = {
            "repository_structure": file_structure,
            "architectural_patterns": {
                "mvc_analysis": mvc_analysis,
                "layered_architecture": layered_analysis,
                "microservices_assessment": microservices_analysis
            },
            "design_patterns": design_patterns,
            "anti_patterns": anti_patterns,
            "architecture_quality": architecture_quality,
            "modernization_recommendations": modernization_recommendations,
            "architectural_insights": self._generate_architectural_insights(
                mvc_analysis, layered_analysis, design_patterns
            ),
            "refactoring_opportunities": self._identify_refactoring_opportunities(
                file_structure, dependency_analysis
            )
        }
        
        logger.info(f"Architecture analysis completed: {len(design_patterns)} design patterns, "
                   f"{len(anti_patterns)} anti-patterns detected")
        
        return analysis_results
    
    def _analyze_directory_structure(self, repo_path: str) -> Dict[str, Any]:
        """Analyze the directory structure for architectural insights"""
        structure = {
            "directories": {},
            "file_types": defaultdict(int),
            "naming_conventions": [],
            "organization_style": "",
            "depth": 0
        }
        
        max_depth = 0
        directory_purposes = {}
        
        for root, _, files in os.walk(repo_path):
            level = root.replace(repo_path, '').count(os.sep)
            max_depth = max(max_depth, level)
            
            # Analyze directory purposes
            dir_name = os.path.basename(root).lower()
            purpose = self._classify_directory_purpose(dir_name, files)
            if purpose:
                directory_purposes[root] = purpose
            
            # Count file types
            for file in files:
                ext = Path(file).suffix.lower()
                if ext:
                    structure["file_types"][ext] += 1
        
        structure["depth"] = max_depth
        structure["directories"] = directory_purposes
        structure["organization_style"] = self._determine_organization_style(directory_purposes)
        
        return structure
    
    def _classify_directory_purpose(self, dir_name: str, files: List[str]) -> Optional[str]:
        """Classify the purpose of a directory based on name and contents"""
        # Common directory patterns
        purpose_patterns = {
            "model": ["model", "models", "entity", "entities", "domain"],
            "view": ["view", "views", "template", "templates", "ui", "frontend"],
            "controller": ["controller", "controllers", "handler", "handlers"],
            "service": ["service", "services", "business", "logic"],
            "repository": ["repository", "repositories", "dao", "data"],
            "config": ["config", "configuration", "settings"],
            "test": ["test", "tests", "spec", "specs"],
            "util": ["util", "utils", "helper", "helpers", "common"],
            "middleware": ["middleware", "filter", "filters"],
            "api": ["api", "rest", "endpoint", "endpoints"],
            "database": ["database", "db", "migration", "migrations"],
            "asset": ["asset", "assets", "public", "static", "resource"],
            "library": ["lib", "vendor", "third-party", "external"]
        }
        
        # Check directory name
        for purpose, patterns in purpose_patterns.items():
            if any(pattern in dir_name for pattern in patterns):
                return purpose
        
        # Check file contents
        if files:
            php_files = [f for f in files if f.endswith('.php')]
            js_files = [f for f in files if f.endswith(('.js', '.ts'))]
            
            if any('controller' in f.lower() for f in php_files):
                return "controller"
            elif any('model' in f.lower() for f in php_files):
                return "model"
            elif any('view' in f.lower() or f.endswith('.blade.php') for f in files):
                return "view"
            elif any('test' in f.lower() for f in files):
                return "test"
        
        return None
    
    def _determine_organization_style(self, directory_purposes: Dict[str, str]) -> str:
        """Determine the overall organization style"""
        purposes = list(directory_purposes.values())
        
        # Check for MVC structure
        has_model = "model" in purposes
        has_view = "view" in purposes  
        has_controller = "controller" in purposes
        
        if has_model and has_view and has_controller:
            return "MVC"
        
        # Check for layered architecture
        has_service = "service" in purposes
        has_repository = "repository" in purposes
        
        if has_service and has_repository:
            return "Layered"
        
        # Check for feature-based organization
        feature_indicators = ["api", "middleware", "config"]
        if any(purpose in feature_indicators for purpose in purposes):
            return "Feature-based"
        
        return "Mixed/Unclear"
    
    def _detect_mvc_pattern(self, file_structure: Dict[str, Any], repo_path: str) -> Dict[str, Any]:
        """Detect MVC (Model-View-Controller) pattern"""
        mvc_analysis = {
            "pattern_detected": False,
            "confidence": 0.0,
            "components": {"models": [], "views": [], "controllers": []},
            "framework": "Unknown",
            "mvc_variant": "Traditional",
            "separation_quality": "Unknown"
        }
        
        # Look for MVC directories
        directories = file_structure.get("directories", {})
        
        model_dirs = [path for path, purpose in directories.items() if purpose == "model"]
        view_dirs = [path for path, purpose in directories.items() if purpose == "view"]
        controller_dirs = [path for path, purpose in directories.items() if purpose == "controller"]
        
        # Scan for MVC files
        for root, _, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = file.lower()
                
                # Detect Laravel MVC
                if file.endswith('.php'):
                    if 'controller' in file_name and file.endswith('Controller.php'):
                        mvc_analysis["components"]["controllers"].append(file_path)
                        mvc_analysis["framework"] = "Laravel"
                    elif file.endswith('.blade.php'):
                        mvc_analysis["components"]["views"].append(file_path)
                        mvc_analysis["framework"] = "Laravel"
                    elif 'model' in file_name or any('model' in d for d in root.split(os.sep)):
                        mvc_analysis["components"]["models"].append(file_path)
                
                # Detect other MVC patterns
                elif file.endswith(('.js', '.ts')):
                    if 'controller' in file_name:
                        mvc_analysis["components"]["controllers"].append(file_path)
                    elif 'model' in file_name:
                        mvc_analysis["components"]["models"].append(file_path)
                    elif 'view' in file_name or file.endswith(('.vue', '.jsx', '.tsx')):
                        mvc_analysis["components"]["views"].append(file_path)
        
        # Calculate confidence and pattern detection
        has_models = len(mvc_analysis["components"]["models"]) > 0
        has_views = len(mvc_analysis["components"]["views"]) > 0
        has_controllers = len(mvc_analysis["components"]["controllers"]) > 0
        
        confidence = 0.0
        if has_models:
            confidence += 0.33
        if has_views:
            confidence += 0.33
        if has_controllers:
            confidence += 0.34
        
        mvc_analysis["pattern_detected"] = confidence > 0.5
        mvc_analysis["confidence"] = confidence
        
        # Assess separation quality
        if confidence > 0.8:
            mvc_analysis["separation_quality"] = "Excellent"
        elif confidence > 0.6:
            mvc_analysis["separation_quality"] = "Good"
        elif confidence > 0.3:
            mvc_analysis["separation_quality"] = "Fair"
        else:
            mvc_analysis["separation_quality"] = "Poor"
        
        return mvc_analysis
    
    def _detect_layered_architecture(self, file_structure: Dict[str, Any], 
                                   dependency_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """Detect layered architecture pattern"""
        layered_analysis = {
            "pattern_detected": False,
            "confidence": 0.0,
            "layers": {},
            "layer_violations": [],
            "architecture_type": "Unknown"
        }
        
        # Define common layers
        layer_mappings = {
            "presentation": ["view", "controller", "ui", "frontend"],
            "business": ["service", "business", "logic"],
            "data_access": ["repository", "dao", "data"],
            "database": ["database", "db", "migration"]
        }
        
        directories = file_structure.get("directories", {})
        
        # Identify layers
        for layer_name, indicators in layer_mappings.items():
            layer_files = []
            for path, purpose in directories.items():
                if purpose in indicators:
                    # Get files in this directory
                    try:
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                if file.endswith(('.php', '.py', '.js', '.ts')):
                                    layer_files.append(os.path.join(root, file))
                    except:
                        pass
            
            if layer_files:
                layered_analysis["layers"][layer_name] = {
                    "files": layer_files,
                    "file_count": len(layer_files)
                }
        
        # Calculate confidence
        detected_layers = len(layered_analysis["layers"])
        if detected_layers >= 3:
            layered_analysis["pattern_detected"] = True
            layered_analysis["confidence"] = min(1.0, detected_layers / 4.0)
            layered_analysis["architecture_type"] = f"{detected_layers}-Layer Architecture"
        
        # Check for layer violations (if dependency analysis available)
        if dependency_analysis and layered_analysis["pattern_detected"]:
            violations = self._check_layer_violations(layered_analysis["layers"], dependency_analysis)
            layered_analysis["layer_violations"] = violations
        
        return layered_analysis
    
    def _analyze_microservices_architecture(self, file_structure: Dict[str, Any], repo_path: str) -> Dict[str, Any]:
        """Analyze if the system follows microservices architecture"""
        microservices_analysis = {
            "architecture_style": "Monolith",
            "service_indicators": [],
            "microservices_readiness": 0.0,
            "decomposition_suggestions": []
        }
        
        # Look for microservices indicators
        indicators = []
        
        # Check for service-oriented directory structure
        directories = file_structure.get("directories", {})
        service_dirs = [path for path, purpose in directories.items() if purpose == "service"]
        api_dirs = [path for path, purpose in directories.items() if purpose == "api"]
        
        if len(service_dirs) > 2:
            indicators.append("Multiple service directories")
        
        if len(api_dirs) > 1:
            indicators.append("Multiple API endpoints")
        
        # Check for configuration files indicating microservices
        config_files = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file in ['docker-compose.yml', 'Dockerfile', 'kubernetes.yml', 'k8s.yml']:
                    config_files.append(file)
                    indicators.append(f"Container configuration: {file}")
        
        # Check for independent database access
        db_configs = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if 'database' in file.lower() or 'db' in file.lower():
                    if file.endswith(('.yml', '.yaml', '.json', '.env')):
                        db_configs.append(file)
        
        if len(db_configs) > 1:
            indicators.append("Multiple database configurations")
        
        # Calculate microservices readiness
        readiness_score = 0.0
        
        if len(service_dirs) > 2:
            readiness_score += 0.3
        if len(api_dirs) > 1:
            readiness_score += 0.2
        if config_files:
            readiness_score += 0.2
        if len(db_configs) > 1:
            readiness_score += 0.2
        
        # Check for business domain separation
        business_domains = self._identify_business_domains(file_structure)
        if len(business_domains) > 1:
            readiness_score += 0.1
            indicators.append(f"Multiple business domains: {', '.join(business_domains)}")
        
        microservices_analysis["service_indicators"] = indicators
        microservices_analysis["microservices_readiness"] = readiness_score
        
        # Determine architecture style
        if readiness_score > 0.7:
            microservices_analysis["architecture_style"] = "Microservices"
        elif readiness_score > 0.4:
            microservices_analysis["architecture_style"] = "Service-Oriented"
        else:
            microservices_analysis["architecture_style"] = "Monolith"
        
        # Generate decomposition suggestions
        if readiness_score < 0.5:
            suggestions = self._generate_decomposition_suggestions(file_structure, business_domains)
            microservices_analysis["decomposition_suggestions"] = suggestions
        
        return microservices_analysis
    
    def _detect_design_patterns(self, repo_path: str, ast_analysis: Dict[str, Any] = None) -> List[DesignPattern]:
        """Detect common design patterns in the codebase"""
        patterns = []
        
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(('.php', '.py', '.js', '.ts')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # Detect various design patterns
                        patterns.extend(self._detect_singleton_pattern(content, file_path))
                        patterns.extend(self._detect_factory_pattern(content, file_path))
                        patterns.extend(self._detect_observer_pattern(content, file_path))
                        patterns.extend(self._detect_adapter_pattern(content, file_path))
                        patterns.extend(self._detect_decorator_pattern(content, file_path))
                        patterns.extend(self._detect_strategy_pattern(content, file_path))
                        
                    except Exception as e:
                        logger.warning(f"Failed to analyze patterns in {file_path}: {str(e)}")
        
        return patterns
    
    def _detect_singleton_pattern(self, content: str, file_path: str) -> List[DesignPattern]:
        """Detect Singleton pattern"""
        patterns = []
        
        # Look for singleton indicators
        singleton_indicators = [
            r'private\s+static\s+\$instance',  # PHP
            r'private\s+static\s+instance',    # Java/C#
            r'_instance\s*=\s*None',           # Python
            r'getInstance\s*\(',               # Generic
        ]
        
        for pattern in singleton_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                patterns.append(DesignPattern(
                    pattern_name="Singleton",
                    location=file_path,
                    confidence=0.8,
                    participants=[file_path],
                    description="Singleton pattern ensures only one instance of a class"
                ))
                break
        
        return patterns
    
    def _detect_factory_pattern(self, content: str, file_path: str) -> List[DesignPattern]:
        """Detect Factory pattern"""
        patterns = []
        
        # Look for factory indicators
        if 'factory' in file_path.lower() or 'Factory' in content:
            # Check for create methods
            create_patterns = [
                r'create\w*\s*\(',
                r'make\w*\s*\(',
                r'build\w*\s*\(',
            ]
            
            for pattern in create_patterns:
                if re.search(pattern, content):
                    patterns.append(DesignPattern(
                        pattern_name="Factory",
                        location=file_path,
                        confidence=0.7,
                        participants=[file_path],
                        description="Factory pattern creates objects without specifying exact classes"
                    ))
                    break
        
        return patterns
    
    def _detect_observer_pattern(self, content: str, file_path: str) -> List[DesignPattern]:
        """Detect Observer pattern"""
        patterns = []
        
        # Look for observer indicators
        observer_indicators = [
            r'attach\s*\(',
            r'detach\s*\(',
            r'notify\s*\(',
            r'subscribe\s*\(',
            r'addEventListener\s*\(',
        ]
        
        indicator_count = sum(1 for pattern in observer_indicators if re.search(pattern, content))
        
        if indicator_count >= 2:
            patterns.append(DesignPattern(
                pattern_name="Observer",
                location=file_path,
                confidence=0.6 + (indicator_count * 0.1),
                participants=[file_path],
                description="Observer pattern defines one-to-many dependency between objects"
            ))
        
        return patterns
    
    def _detect_adapter_pattern(self, content: str, file_path: str) -> List[DesignPattern]:
        """Detect Adapter pattern"""
        patterns = []
        
        if 'adapter' in file_path.lower() or 'Adapter' in content:
            # Look for adaptation/wrapping behavior
            adapter_indicators = [
                r'adapt\s*\(',
                r'wrap\s*\(',
                r'convert\s*\(',
            ]
            
            for pattern in adapter_indicators:
                if re.search(pattern, content):
                    patterns.append(DesignPattern(
                        pattern_name="Adapter",
                        location=file_path,
                        confidence=0.6,
                        participants=[file_path],
                        description="Adapter pattern allows incompatible interfaces to work together"
                    ))
                    break
        
        return patterns
    
    def _detect_decorator_pattern(self, content: str, file_path: str) -> List[DesignPattern]:
        """Detect Decorator pattern"""
        patterns = []
        
        # Look for decorator indicators
        if 'decorator' in file_path.lower() or 'Decorator' in content:
            patterns.append(DesignPattern(
                pattern_name="Decorator",
                location=file_path,
                confidence=0.7,
                participants=[file_path],
                description="Decorator pattern adds behavior to objects dynamically"
            ))
        
        # Python decorator syntax
        if re.search(r'@\w+', content):
            patterns.append(DesignPattern(
                pattern_name="Decorator",
                location=file_path,
                confidence=0.5,
                participants=[file_path],
                description="Python decorator syntax detected"
            ))
        
        return patterns
    
    def _detect_strategy_pattern(self, content: str, file_path: str) -> List[DesignPattern]:
        """Detect Strategy pattern"""
        patterns = []
        
        if 'strategy' in file_path.lower() or 'Strategy' in content:
            # Look for strategy switching behavior
            strategy_indicators = [
                r'setStrategy\s*\(',
                r'execute\s*\(',
                r'algorithm\s*\(',
            ]
            
            for pattern in strategy_indicators:
                if re.search(pattern, content):
                    patterns.append(DesignPattern(
                        pattern_name="Strategy",
                        location=file_path,
                        confidence=0.6,
                        participants=[file_path],
                        description="Strategy pattern defines family of algorithms"
                    ))
                    break
        
        return patterns
    
    def _detect_architectural_antipatterns(self, file_structure: Dict[str, Any], 
                                         dependency_analysis: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Detect architectural anti-patterns"""
        anti_patterns = []
        
        # God Object anti-pattern
        if dependency_analysis:
            modules = dependency_analysis.get("module_details", {})
            for module_path, module_info in modules.items():
                if module_info.get("coupling_out", 0) > 15:
                    anti_patterns.append({
                        "type": "God Object",
                        "location": module_path,
                        "severity": "high",
                        "description": f"Module has {module_info['coupling_out']} outgoing dependencies",
                        "impact": "High coupling reduces maintainability and testability"
                    })
        
        # Monolithic Architecture anti-pattern
        directories = file_structure.get("directories", {})
        if len(directories) < 3:
            anti_patterns.append({
                "type": "Monolithic Structure",
                "location": "Repository root",
                "severity": "medium",
                "description": "Insufficient architectural separation",
                "impact": "Poor separation of concerns affects scalability"
            })
        
        # Configuration in Code anti-pattern
        # This would require content analysis of files
        
        return anti_patterns
    
    def _check_layer_violations(self, layers: Dict[str, Any], dependency_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for architectural layer violations"""
        violations = []
        
        # Define layer hierarchy (higher layers should not depend on lower layers)
        layer_hierarchy = ["database", "data_access", "business", "presentation"]
        
        # This is a simplified implementation
        # In practice, you'd analyze the dependency graph more thoroughly
        
        return violations
    
    def _identify_business_domains(self, file_structure: Dict[str, Any]) -> List[str]:
        """Identify potential business domains from directory structure"""
        directories = file_structure.get("directories", {})
        
        # Look for domain-specific directories
        business_domains = []
        
        for path, purpose in directories.items():
            dir_name = os.path.basename(path).lower()
            
            # Common business domain indicators
            domain_patterns = [
                'user', 'account', 'auth', 'catalog', 'inventory', 
                'order', 'payment', 'billing', 'shipping', 'product',
                'customer', 'vendor', 'report', 'analytics'
            ]
            
            for pattern in domain_patterns:
                if pattern in dir_name and pattern not in business_domains:
                    business_domains.append(pattern)
        
        return business_domains
    
    def _generate_decomposition_suggestions(self, file_structure: Dict[str, Any], 
                                          business_domains: List[str]) -> List[Dict[str, Any]]:
        """Generate suggestions for decomposing monolith into microservices"""
        suggestions = []
        
        if len(business_domains) > 1:
            suggestions.append({
                "type": "Domain-based decomposition",
                "description": f"Split into services based on business domains: {', '.join(business_domains)}",
                "effort": "High",
                "benefits": ["Better scalability", "Team autonomy", "Technology diversity"]
            })
        
        # Check for large directories that could be services
        directories = file_structure.get("directories", {})
        large_dirs = [path for path, purpose in directories.items() 
                     if purpose in ["service", "api", "controller"]]
        
        if len(large_dirs) > 2:
            suggestions.append({
                "type": "Service extraction",
                "description": "Extract existing service directories into independent services",
                "effort": "Medium",
                "benefits": ["Reduced deployment coupling", "Independent scaling"]
            })
        
        return suggestions
    
    def _assess_architecture_quality(self, mvc_analysis: Dict[str, Any], layered_analysis: Dict[str, Any],
                                   design_patterns: List[DesignPattern], anti_patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess overall architecture quality"""
        
        quality_score = 0.0
        max_score = 100.0
        
        # MVC pattern adherence (25 points)
        if mvc_analysis.get("pattern_detected", False):
            quality_score += mvc_analysis.get("confidence", 0) * 25
        
        # Layered architecture (25 points)
        if layered_analysis.get("pattern_detected", False):
            quality_score += layered_analysis.get("confidence", 0) * 25
        
        # Design patterns usage (25 points)
        pattern_score = min(25, len(design_patterns) * 5)
        quality_score += pattern_score
        
        # Anti-patterns penalty (up to -25 points)
        anti_pattern_penalty = min(25, len(anti_patterns) * 5)
        quality_score = max(0, quality_score - anti_pattern_penalty)
        
        # Determine quality level
        if quality_score >= 80:
            quality_level = "Excellent"
        elif quality_score >= 60:
            quality_level = "Good"
        elif quality_score >= 40:
            quality_level = "Fair"
        elif quality_score >= 20:
            quality_level = "Poor"
        else:
            quality_level = "Critical"
        
        return {
            "overall_score": quality_score,
            "quality_level": quality_level,
            "strengths": self._identify_architectural_strengths(mvc_analysis, layered_analysis, design_patterns),
            "weaknesses": self._identify_architectural_weaknesses(anti_patterns),
            "improvement_areas": self._suggest_improvements(quality_score, mvc_analysis, layered_analysis)
        }
    
    def _identify_architectural_strengths(self, mvc_analysis: Dict[str, Any], 
                                        layered_analysis: Dict[str, Any], 
                                        design_patterns: List[DesignPattern]) -> List[str]:
        """Identify architectural strengths"""
        strengths = []
        
        if mvc_analysis.get("pattern_detected", False):
            strengths.append("Well-defined MVC structure")
        
        if layered_analysis.get("pattern_detected", False):
            strengths.append("Clear architectural layers")
        
        if len(design_patterns) > 3:
            strengths.append("Good use of design patterns")
        
        return strengths
    
    def _identify_architectural_weaknesses(self, anti_patterns: List[Dict[str, Any]]) -> List[str]:
        """Identify architectural weaknesses"""
        weaknesses = []
        
        for anti_pattern in anti_patterns:
            weaknesses.append(f"{anti_pattern['type']}: {anti_pattern['description']}")
        
        return weaknesses
    
    def _suggest_improvements(self, quality_score: float, mvc_analysis: Dict[str, Any], 
                            layered_analysis: Dict[str, Any]) -> List[str]:
        """Suggest architectural improvements"""
        improvements = []
        
        if quality_score < 40:
            improvements.append("Implement clear architectural patterns (MVC/Layered)")
        
        if not mvc_analysis.get("pattern_detected", False):
            improvements.append("Implement MVC separation of concerns")
        
        if not layered_analysis.get("pattern_detected", False):
            improvements.append("Establish clear architectural layers")
        
        improvements.append("Reduce coupling between components")
        improvements.append("Implement more design patterns for flexibility")
        
        return improvements
    
    def _generate_modernization_recommendations(self, file_structure: Dict[str, Any],
                                              mvc_analysis: Dict[str, Any],
                                              layered_analysis: Dict[str, Any],
                                              microservices_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific modernization recommendations"""
        recommendations = []
        
        # MVC modernization
        if mvc_analysis.get("confidence", 0) < 0.7:
            recommendations.append({
                "category": "Architectural Pattern",
                "priority": "High",
                "title": "Strengthen MVC Implementation",
                "description": "Improve separation between models, views, and controllers",
                "effort": "Medium",
                "impact": "Improved maintainability and testability"
            })
        
        # Microservices transition
        if microservices_analysis.get("microservices_readiness", 0) > 0.4:
            recommendations.append({
                "category": "Architecture Style",
                "priority": "Medium",
                "title": "Consider Microservices Architecture",
                "description": "Evaluate decomposing monolith into microservices",
                "effort": "High",
                "impact": "Better scalability and team autonomy"
            })
        
        # API modernization
        recommendations.append({
            "category": "API Design",
            "priority": "Medium",
            "title": "Implement RESTful API Design",
            "description": "Modernize API endpoints to follow REST principles",
            "effort": "Medium",
            "impact": "Better integration and developer experience"
        })
        
        return recommendations
    
    def _generate_architectural_insights(self, mvc_analysis: Dict[str, Any],
                                       layered_analysis: Dict[str, Any],
                                       design_patterns: List[DesignPattern]) -> Dict[str, Any]:
        """Generate architectural insights and observations"""
        
        insights = {
            "pattern_adoption": {
                "mvc_maturity": mvc_analysis.get("confidence", 0),
                "layering_maturity": layered_analysis.get("confidence", 0),
                "design_pattern_usage": len(design_patterns)
            },
            "modernization_readiness": self._calculate_modernization_readiness(
                mvc_analysis, layered_analysis, design_patterns
            ),
            "architectural_debt": self._assess_architectural_debt(mvc_analysis, layered_analysis),
            "key_observations": self._generate_key_observations(mvc_analysis, layered_analysis, design_patterns)
        }
        
        return insights
    
    def _calculate_modernization_readiness(self, mvc_analysis: Dict[str, Any],
                                         layered_analysis: Dict[str, Any],
                                         design_patterns: List[DesignPattern]) -> float:
        """Calculate how ready the architecture is for modernization"""
        readiness = 0.0
        
        # MVC structure readiness
        readiness += mvc_analysis.get("confidence", 0) * 0.4
        
        # Layered architecture readiness
        readiness += layered_analysis.get("confidence", 0) * 0.3
        
        # Design pattern usage
        pattern_score = min(1.0, len(design_patterns) / 5.0)
        readiness += pattern_score * 0.3
        
        return readiness
    
    def _assess_architectural_debt(self, mvc_analysis: Dict[str, Any], 
                                 layered_analysis: Dict[str, Any]) -> str:
        """Assess the level of architectural debt"""
        debt_score = 0
        
        if mvc_analysis.get("confidence", 0) < 0.5:
            debt_score += 1
        
        if layered_analysis.get("confidence", 0) < 0.5:
            debt_score += 1
        
        if debt_score == 0:
            return "Low"
        elif debt_score == 1:
            return "Medium"
        else:
            return "High"
    
    def _generate_key_observations(self, mvc_analysis: Dict[str, Any],
                                 layered_analysis: Dict[str, Any],
                                 design_patterns: List[DesignPattern]) -> List[str]:
        """Generate key architectural observations"""
        observations = []
        
        if mvc_analysis.get("pattern_detected", False):
            observations.append(f"MVC pattern detected with {mvc_analysis['confidence']:.0%} confidence")
        
        if layered_analysis.get("pattern_detected", False):
            layer_count = len(layered_analysis.get("layers", {}))
            observations.append(f"{layer_count}-layer architecture identified")
        
        if design_patterns:
            pattern_types = list(set(p.pattern_name for p in design_patterns))
            observations.append(f"Design patterns in use: {', '.join(pattern_types)}")
        
        return observations
    
    def _identify_refactoring_opportunities(self, file_structure: Dict[str, Any],
                                          dependency_analysis: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Identify specific refactoring opportunities"""
        opportunities = []
        
        # Large directory refactoring
        directories = file_structure.get("directories", {})
        for path, purpose in directories.items():
            try:
                file_count = len([f for root, dirs, files in os.walk(path) 
                                for f in files if f.endswith(('.php', '.py', '.js', '.ts'))])
                if file_count > 20:
                    opportunities.append({
                        "type": "Directory Decomposition",
                        "location": path,
                        "description": f"Directory contains {file_count} files, consider splitting",
                        "effort": "Medium",
                        "benefit": "Improved code organization and maintainability"
                    })
            except:
                pass
        
        # Coupling-based refactoring
        if dependency_analysis:
            critical_modules = dependency_analysis.get("critical_modules", [])
            for module in critical_modules[:3]:  # Top 3 critical modules
                opportunities.append({
                    "type": "Coupling Reduction",
                    "location": module.get("file_path", "Unknown"),
                    "description": f"High coupling detected ({module.get('coupling_in', 0)} dependencies)",
                    "effort": "High",
                    "benefit": "Reduced complexity and improved testability"
                })
        
        return opportunities


# ================== ENHANCED ANALYSIS HELPER FUNCTIONS ==================

def calculate_enhanced_modernization_readiness(repo_data: Dict[str, Any]) -> float:
    """Calculate enhanced modernization readiness score using advanced analysis"""
    score = 0.0
    max_score = 100.0
    
    # AST Analysis contribution (25 points)
    ast_analysis = repo_data.get("ast_analysis", {})
    if ast_analysis.get("total_functions", 0) > 0:
        score += 15  # Has analyzable functions
        if ast_analysis.get("complexity_metrics", {}).get("avg_function_complexity", 0) < 5:
            score += 10  # Low complexity is good for modernization
    
    # Dependency Analysis contribution (25 points)
    dependency_analysis = repo_data.get("dependency_analysis", {})
    circular_deps = len(dependency_analysis.get("circular_dependencies", []))
    if circular_deps == 0:
        score += 15  # No circular dependencies
    elif circular_deps < 3:
        score += 10  # Few circular dependencies
    else:
        score += 5   # Many circular dependencies
    
    coupling_metrics = dependency_analysis.get("coupling_metrics", {})
    avg_coupling = coupling_metrics.get("average_coupling_out", 0)
    if avg_coupling < 5:
        score += 10  # Low coupling
    elif avg_coupling < 10:
        score += 5   # Medium coupling
    
    # Quality Analysis contribution (25 points)
    quality_analysis = repo_data.get("quality_analysis", {})
    quality_scores = quality_analysis.get("quality_scores", {})
    overall_quality = quality_scores.get("overall_score", 0) if isinstance(quality_scores, dict) else 0
    score += (overall_quality / 100) * 25
    
    # Architecture Analysis contribution (25 points)
    architecture_analysis = repo_data.get("architecture_analysis", {})
    architectural_patterns = architecture_analysis.get("architectural_patterns", {})
    
    if architectural_patterns.get("mvc_analysis", {}).get("pattern_detected", False):
        score += 10  # Has MVC pattern
    
    if architectural_patterns.get("layered_architecture", {}).get("pattern_detected", False):
        score += 10  # Has layered architecture
    
    design_patterns = len(architecture_analysis.get("design_patterns", []))
    score += min(5, design_patterns)  # Up to 5 points for design patterns
    
    return min(max_score, score)


def generate_comprehensive_recommendations(ast_analysis: Dict[str, Any], 
                                          dependency_analysis: Dict[str, Any],
                                          quality_analysis: Dict[str, Any], 
                                          architecture_analysis: Dict[str, Any],
                                          solr_analysis: Dict[str, Any] = None) -> List[str]:
    """Generate comprehensive recommendations based on all advanced analyses including Solr upgrade"""
    recommendations = []
    
    # AST-based recommendations
    total_functions = ast_analysis.get("total_functions", 0)
    if total_functions > 0:
        avg_complexity = ast_analysis.get("complexity_metrics", {}).get("avg_function_complexity", 0)
        if avg_complexity > 10:
            recommendations.append("Refactor high-complexity functions to improve maintainability")
        
        recommendations.append(f"Leverage AST analysis of {total_functions} functions for targeted modernization")
    
    # Dependency-based recommendations
    circular_deps = len(dependency_analysis.get("circular_dependencies", []))
    if circular_deps > 0:
        recommendations.append(f"Resolve {circular_deps} circular dependencies before modernization")
    
    coupling_metrics = dependency_analysis.get("coupling_metrics", {})
    high_coupling_modules = coupling_metrics.get("max_coupling_out", 0)
    if high_coupling_modules > 10:
        recommendations.append("Reduce coupling in highly coupled modules")
    
    # Quality-based recommendations
    code_smells = quality_analysis.get("total_code_smells", 0)
    if code_smells > 10:
        recommendations.append(f"Address {code_smells} code smells to improve code quality")
    
    quality_recommendations = quality_analysis.get("recommendations", [])
    for rec in quality_recommendations[:2]:  # Top 2 quality recommendations
        if isinstance(rec, dict):
            recommendations.append(rec.get("description", "Improve code quality"))
    
    # Architecture-based recommendations
    architecture_quality = architecture_analysis.get("architecture_quality", {})
    if architecture_quality.get("quality_level") in ["Poor", "Critical"]:
        recommendations.append("Implement clear architectural patterns before modernization")
    
    modernization_recs = architecture_analysis.get("modernization_recommendations", [])
    for rec in modernization_recs[:2]:  # Top 2 architecture recommendations
        if isinstance(rec, dict):
            recommendations.append(rec.get("description", "Improve architecture"))
    
    # Solr analysis-based recommendations
    if solr_analysis:
        solr_upgrade_required = solr_analysis.get("solr_version_compatibility", {}).get("major_upgrade_required", False)
        if solr_upgrade_required:
            recommendations.append("CRITICAL: Upgrade Apache Solr from 5.x to 9.x required")
        
        breaking_changes = len(solr_analysis.get("breaking_changes", []))
        if breaking_changes > 0:
            recommendations.append(f"Address {breaking_changes} Solr breaking changes during upgrade")
        
        solr_requirements = solr_analysis.get("upgrade_requirements", [])
        for req in solr_requirements[:2]:  # Top 2 Solr requirements
            if isinstance(req, str) and "CRITICAL" in req:
                recommendations.append(req)
    
    # Default enhanced recommendations
    if not recommendations:
        recommendations = [
            "Proceed with modernization using AST-guided transformation",
            "Leverage dependency analysis for impact assessment",
            "Use quality metrics to prioritize refactoring efforts",
            "Apply architectural insights for modernization planning"
        ]
    
    return recommendations[:8]  # Limit to 8 recommendations


# ================== LLM INTEGRATION ==================

def llm_call(prompt: str, system_prompt: str = "", model: str = "llama-3.1-8b-instant") -> str:
    """
    Unified LLM call interface supporting Groq API
    
    Args:
        prompt: The user prompt/query
        system_prompt: System instructions for the LLM
        model: Model to use (default: llama3-8b-8192 for Groq)
        
    Returns:
        LLM response text
    """
    try:
        import os
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        # Determine AI provider
        ai_provider = os.getenv("AI_PROVIDER", "groq")  # Default to Groq
        
        # Calculate optimal max_tokens based on input size
        input_tokens = len(prompt) // 4 + len(system_prompt or "") // 4  # Rough estimation
        
        if ai_provider.lower() == "anthropic":
            # Claude/Anthropic setup
            try:
                from anthropic import Anthropic
            except ImportError:
                logger.error("Anthropic package not installed. Run: pip install anthropic")
                return "Error: Anthropic package not installed"
            
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            
            client = Anthropic(api_key=api_key)
            model = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
            
            # Claude token limits - using actual API maximums (as of Oct 2024)
            # Sonnet 3.5: 200K context, 64K output
            # Opus 3: 200K context, 64K output  
            # Haiku 3: 200K context, 32K output
            if "opus" in model.lower():
                max_output_tokens = min(200000 - input_tokens, 64000)  # Opus: 64K max
            elif "sonnet" in model.lower():
                max_output_tokens = min(200000 - input_tokens, 64000)  # Sonnet: 64K max
            else:  # Haiku
                max_output_tokens = min(200000 - input_tokens, 64000)  # Sonnet: 64K max
            
            max_output_tokens = max(max_output_tokens, 1000)
            
            # Claude API call - use streaming for large outputs (>8K tokens)
            # Streaming is required for operations that may take longer than 10 minutes
            if max_output_tokens > 8000:
                # Use streaming for large outputs
                response_text = ""
                with client.messages.stream(
                    model=model,
                    max_tokens=max_output_tokens,
                    temperature=0.1,
                    system=system_prompt or "",
                    messages=[{"role": "user", "content": prompt}]
                ) as stream:
                    for text in stream.text_stream:
                        response_text += text
                return response_text
            else:
                # Use regular non-streaming call for smaller outputs
                response = client.messages.create(
                    model=model,
                    max_tokens=max_output_tokens,
                    temperature=0.1,
                    system=system_prompt or "",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            
        else:
            # Default: Groq setup
            try:
                from groq import Groq
            except ImportError:
                logger.error("Groq package not installed. Run: pip install groq")
                return "Error: Groq package not installed"
            
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY environment variable not set")
            
            client = Groq(api_key=api_key)
            model = os.getenv("GROQ_MODEL", "llama3-8b-8192")
            
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Groq token limits
            if "70b" in model.lower() or "32b" in model.lower():
                max_output_tokens = min(8192 - input_tokens, 7000)  # Larger models
            else:
                max_output_tokens = min(8192 - input_tokens, 5000)   # Standard models
            
            max_output_tokens = max(max_output_tokens, 1000)
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.1,
                max_tokens=max_output_tokens
            )
            
            return response.choices[0].message.content
        
    except ImportError as e:
        if "anthropic" in str(e):
            logger.error("Anthropic package not installed. Run: pip install anthropic")
            return "Error: Anthropic package not installed"
        else:
            logger.error("Required AI package not installed. Check your configuration.")
            return "Error: AI package not installed"
    except Exception as e:
        logger.error(f"Error calling LLM: {str(e)}")
        return f"Error: {str(e)}"


# ================== API COMPATIBILITY ANALYSIS UTILITIES ==================

class APICompatibilityAnalyzer:
    """Utility class for analyzing and maintaining API compatibility during modernization"""
    
    def __init__(self):
        self.api_patterns = {
            'http_endpoints': ['fetch(', 'axios.', '$.ajax', 'request(', 'http.request', 'XMLHttpRequest'],
            'express_routes': ['app.get(', 'app.post(', 'app.put(', 'app.delete(', 'router.'],
            'database_calls': ['db.', 'collection.', 'mongoose.', 'MongoClient', '.find(', '.save(', '.update('],
            'socket_connections': ['socket.emit', 'socket.on', 'io.connect', 'io('],
            'auth_flows': ['passport.', 'jwt.', 'session.', 'auth.', 'bcrypt'],
            'middleware': ['app.use(', 'express.static', 'bodyParser', 'cors'],
            'third_party': ['stripe.', 'paypal.', 'aws.', 'cloudinary.']
        }
        
    def compare_api_signatures(self, original_apis: Dict[str, Any], 
                             modernized_apis: Dict[str, Any]) -> Dict[str, Any]:
        """Compare API signatures between original and modernized code"""
        comparison = {
            'added_apis': [],
            'removed_apis': [],
            'modified_apis': [],
            'preserved_apis': [],
            'compatibility_score': 0.0
        }
        
        for category in self.api_patterns.keys():
            original_calls = original_apis.get(category, [])
            modernized_calls = modernized_apis.get(category, [])
            
            # Create sets of API signatures for comparison
            original_sigs = {self._extract_api_signature(call) for call in original_calls}
            modernized_sigs = {self._extract_api_signature(call) for call in modernized_calls}
            
            # Find differences
            removed = original_sigs - modernized_sigs
            added = modernized_sigs - original_sigs
            preserved = original_sigs & modernized_sigs
            
            comparison['removed_apis'].extend([{'category': category, 'signature': sig} for sig in removed])
            comparison['added_apis'].extend([{'category': category, 'signature': sig} for sig in added])
            comparison['preserved_apis'].extend([{'category': category, 'signature': sig} for sig in preserved])
        
        # Calculate compatibility score
        total_original = sum(len(original_apis.get(cat, [])) for cat in self.api_patterns.keys())
        total_preserved = len(comparison['preserved_apis'])
        
        if total_original > 0:
            comparison['compatibility_score'] = total_preserved / total_original
        
        return comparison
    
    def _extract_api_signature(self, api_call: Dict[str, Any]) -> str:
        """Extract a comparable signature from an API call"""
        code = api_call.get('code', '')
        pattern = api_call.get('pattern', '')
        
        # For route definitions, extract the route pattern
        if any(route_pattern in code for route_pattern in ['app.get(', 'app.post(', 'app.put(', 'app.delete(']):
            import re
            route_match = re.search(r'app\.\w+\(\s*[\'"`]([^\'"`]+)[\'"`]', code)
            if route_match:
                return f"route:{route_match.group(1)}"
        
        # For database calls, extract the operation type
        if any(db_pattern in code for db_pattern in ['.find(', '.save(', '.update(', '.delete(']):
            import re
            operation_match = re.search(r'\.(\w+)\(', code)
            if operation_match:
                return f"db_operation:{operation_match.group(1)}"
        
        # For socket events, extract event name
        if 'socket.emit(' in code:
            import re
            event_match = re.search(r'socket\.emit\(\s*[\'"`]([^\'"`]+)[\'"`]', code)
            if event_match:
                return f"socket_event:{event_match.group(1)}"
        
        # Default: use pattern and basic code structure
        return f"{pattern}:{code.strip()[:50]}"
    
    def _is_critical_api(self, api_info: Dict[str, Any]) -> bool:
        """Determine if an API is critical for system functionality"""
        signature = api_info.get('signature', '')
        category = api_info.get('category', '')
        
        critical_indicators = [
            'route:/api/', 'route:/auth/', 'route:/login',
            'db_operation:find', 'db_operation:save', 'db_operation:update',
            'socket_event:connect', 'socket_event:disconnect'
        ]
        
        return any(indicator in signature for indicator in critical_indicators) or \
               category in ['express_routes', 'database_calls', 'auth_flows']
    
    def _generate_compatibility_recommendations(self, comparison: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations for maintaining compatibility"""
        recommendations = []
        
        if comparison['compatibility_score'] < 0.8:
            recommendations.append("CRITICAL: Low API compatibility score detected - manual review required")
        
        if comparison['removed_apis']:
            recommendations.append(f"WARNING: {len(comparison['removed_apis'])} APIs were removed during modernization")
            recommendations.append("Action: Review removed APIs and ensure they are intentionally deprecated")
        
        critical_removals = [api for api in comparison['removed_apis'] if self._is_critical_api(api)]
        if critical_removals:
            recommendations.append(f"URGENT: {len(critical_removals)} critical APIs were removed")
            recommendations.append("Action: Restore critical APIs or provide backward compatibility layer")
        
        if comparison['compatibility_score'] > 0.95:
            recommendations.append("EXCELLENT: High API compatibility maintained")
        
        return recommendations


def validate_api_backwards_compatibility(original_api_analysis: Dict[str, Any], 
                                       modernized_code: str) -> Dict[str, Any]:
    """Validate that modernized code maintains backwards compatibility with original APIs"""
    analyzer = APICompatibilityAnalyzer()
    
    # Simple pattern matching for modernized code
    modernized_apis = {}
    for category, patterns in analyzer.api_patterns.items():
        modernized_apis[category] = []
        for pattern in patterns:
            if pattern in modernized_code:
                modernized_apis[category].append({
                    'code': pattern,
                    'pattern': pattern
                })
    
    # Compare with original
    comparison = analyzer.compare_api_signatures(original_api_analysis, modernized_apis)
    
    return {
        'is_compatible': comparison['compatibility_score'] >= 0.8,
        'compatibility_score': comparison['compatibility_score'],
        'issues': comparison['removed_apis'],
        'recommendations': analyzer._generate_compatibility_recommendations(comparison)
    }


class BackendCompatibilityAnalyzer:
    """Utility class for analyzing backend modernization compatibility (Node.js/Express)"""
    
    def __init__(self):
        self.node_patterns = {
            'callbacks': ['function(err,', 'callback(err', 'function (err,'],
            'async_await': ['async function', 'await ', 'async ('],
            'promises': ['.then(', '.catch(', 'Promise.'],
            'old_modules': ['require(', 'module.exports', '__dirname'],
            'new_modules': ['import ', 'export ', 'import.meta.url']
        }
        
        self.express_patterns = {
            'v3_deprecated': [
                'app.configure(', 'express.bodyParser(', 'express.cookieParser(',
                'express.session(', 'express.methodOverride(', 'express.csrf('
            ],
            'v4_required': [
                'body-parser', 'cookie-parser', 'express-session',
                'method-override', 'csurf'
            ],
            'middleware': ['app.use(', 'express.static(', 'app.get(', 'app.post(']
        }
    
    def analyze_node_modernization(self, original_code: str, modernized_code: str) -> Dict[str, Any]:
        """Analyze Node.js modernization changes"""
        analysis = {
            'callback_migration': {},
            'module_system_upgrade': {},
            'async_pattern_adoption': {},
            'compatibility_score': 0.0
        }
        
        # Analyze callback to async/await migration
        original_callbacks = self._count_patterns(original_code, self.node_patterns['callbacks'])
        modernized_callbacks = self._count_patterns(modernized_code, self.node_patterns['callbacks'])
        modernized_async = self._count_patterns(modernized_code, self.node_patterns['async_await'])
        
        analysis['callback_migration'] = {
            'original_callbacks': original_callbacks,
            'remaining_callbacks': modernized_callbacks,
            'async_await_added': modernized_async,
            'migration_rate': (original_callbacks - modernized_callbacks) / max(original_callbacks, 1)
        }
        
        # Analyze module system upgrade
        original_requires = self._count_patterns(original_code, self.node_patterns['old_modules'])
        modernized_imports = self._count_patterns(modernized_code, self.node_patterns['new_modules'])
        
        analysis['module_system_upgrade'] = {
            'original_require_count': original_requires,
            'modernized_import_count': modernized_imports,
            'es6_adoption_rate': modernized_imports / max(original_requires, 1)
        }
        
        # Calculate overall compatibility score
        callback_score = analysis['callback_migration']['migration_rate']
        module_score = min(analysis['module_system_upgrade']['es6_adoption_rate'], 1.0)
        analysis['compatibility_score'] = (callback_score + module_score) / 2
        
        return analysis
    
    def analyze_express_modernization(self, original_code: str, modernized_code: str) -> Dict[str, Any]:
        """Analyze Express.js modernization changes"""
        analysis = {
            'deprecated_removal': {},
            'middleware_migration': {},
            'v4_compliance': {},
            'compatibility_score': 0.0
        }
        
        # Check for deprecated Express 3.x patterns
        deprecated_count = 0
        for pattern in self.express_patterns['v3_deprecated']:
            if pattern in original_code:
                deprecated_count += 1
                if pattern in modernized_code:
                    analysis['deprecated_removal'][pattern] = 'FAILED_TO_REMOVE'
                else:
                    analysis['deprecated_removal'][pattern] = 'SUCCESSFULLY_REMOVED'
        
        # Check for Express 4.x required patterns
        v4_compliance = 0
        for pattern in self.express_patterns['v4_required']:
            if pattern in modernized_code:
                v4_compliance += 1
                analysis['v4_compliance'][pattern] = 'PRESENT'
            else:
                analysis['v4_compliance'][pattern] = 'MISSING'
        
        # Calculate compatibility score
        removal_score = len([v for v in analysis['deprecated_removal'].values() if v == 'SUCCESSFULLY_REMOVED']) / max(deprecated_count, 1)
        compliance_score = len([v for v in analysis['v4_compliance'].values() if v == 'PRESENT']) / len(self.express_patterns['v4_required'])
        analysis['compatibility_score'] = (removal_score + compliance_score) / 2
        
        return analysis
    
    def _count_patterns(self, code: str, patterns: List[str]) -> int:
        """Count occurrences of patterns in code"""
        count = 0
        for pattern in patterns:
            count += code.count(pattern)
        return count
    
    def generate_backend_migration_report(self, original_code: str, modernized_code: str) -> Dict[str, Any]:
        """Generate comprehensive backend migration report"""
        node_analysis = self.analyze_node_modernization(original_code, modernized_code)
        express_analysis = self.analyze_express_modernization(original_code, modernized_code)
        
        overall_score = (node_analysis['compatibility_score'] + express_analysis['compatibility_score']) / 2
        
        return {
            'overall_compatibility_score': overall_score,
            'node_modernization': node_analysis,
            'express_modernization': express_analysis,
            'migration_quality': 'excellent' if overall_score > 0.9 else 'good' if overall_score > 0.7 else 'needs_improvement',
            'recommendations': self._generate_backend_recommendations(node_analysis, express_analysis)
        }
    
    def _generate_backend_recommendations(self, node_analysis: Dict[str, Any], express_analysis: Dict[str, Any]) -> List[str]:
        """Generate backend modernization recommendations"""
        recommendations = []
        
        # Node.js recommendations
        if node_analysis['callback_migration']['migration_rate'] < 0.8:
            recommendations.append("Consider migrating more callback patterns to async/await")
        
        if node_analysis['module_system_upgrade']['es6_adoption_rate'] < 0.8:
            recommendations.append("Migrate more require() statements to ES6 import/export")
        
        # Express recommendations
        if express_analysis['compatibility_score'] < 0.8:
            recommendations.append("Complete Express 3.x to 4.x migration")
        
        failed_removals = [k for k, v in express_analysis.get('deprecated_removal', {}).items() if v == 'FAILED_TO_REMOVE']
        if failed_removals:
            recommendations.append(f"Remove remaining deprecated Express 3.x patterns: {', '.join(failed_removals)}")
        
        return recommendations


class DatabaseCompatibilityAnalyzer:
    """Utility class for analyzing database modernization compatibility (MongoDB/Mongoose)"""
    
    def __init__(self):
        self.mongodb_patterns = {
            'deprecated_methods': ['.insert(', '.update(', '.remove('],
            'modern_methods': ['.insertOne(', '.insertMany(', '.updateOne(', '.updateMany(', '.deleteOne(', '.deleteMany('],
            'connection_patterns': ['MongoClient.connect(', 'mongoose.connect('],
            'callback_patterns': ['function(err,', 'callback(err'],
            'promise_patterns': ['async function', 'await ', '.then(']
        }
        
        self.mongoose_patterns = {
            'schema_patterns': ['new Schema(', 'mongoose.Schema('],
            'middleware_patterns': ['schema.pre(', 'schema.post('],
            'deprecated_options': ['safe:', 'strict:'],
            'modern_options': ['writeConcern:', 'strictMode:']
        }
    
    def analyze_mongodb_modernization(self, original_code: str, modernized_code: str) -> Dict[str, Any]:
        """Analyze MongoDB modernization changes"""
        analysis = {
            'query_method_migration': {},
            'connection_modernization': {},
            'async_pattern_adoption': {},
            'compatibility_score': 0.0
        }
        
        # Analyze deprecated method migration
        original_deprecated = self._count_patterns(original_code, self.mongodb_patterns['deprecated_methods'])
        modernized_deprecated = self._count_patterns(modernized_code, self.mongodb_patterns['deprecated_methods'])
        modernized_modern = self._count_patterns(modernized_code, self.mongodb_patterns['modern_methods'])
        
        analysis['query_method_migration'] = {
            'original_deprecated_count': original_deprecated,
            'remaining_deprecated_count': modernized_deprecated,
            'modern_methods_added': modernized_modern,
            'migration_rate': (original_deprecated - modernized_deprecated) / max(original_deprecated, 1)
        }
        
        # Analyze connection modernization
        has_callback_connection = any(pattern in modernized_code for pattern in self.mongodb_patterns['callback_patterns'])
        has_async_connection = any(pattern in modernized_code for pattern in self.mongodb_patterns['promise_patterns'])
        
        analysis['connection_modernization'] = {
            'uses_callback_style': has_callback_connection,
            'uses_async_await': has_async_connection,
            'modernization_complete': has_async_connection and not has_callback_connection
        }
        
        # Calculate compatibility score
        method_score = analysis['query_method_migration']['migration_rate']
        connection_score = 1.0 if analysis['connection_modernization']['modernization_complete'] else 0.5
        analysis['compatibility_score'] = (method_score + connection_score) / 2
        
        return analysis
    
    def analyze_mongoose_modernization(self, original_code: str, modernized_code: str) -> Dict[str, Any]:
        """Analyze Mongoose ODM modernization changes"""
        analysis = {
            'schema_modernization': {},
            'middleware_modernization': {},
            'options_migration': {},
            'compatibility_score': 0.0
        }
        
        # Analyze schema modernization
        original_deprecated = self._count_patterns(original_code, self.mongoose_patterns['deprecated_options'])
        modernized_deprecated = self._count_patterns(modernized_code, self.mongoose_patterns['deprecated_options'])
        modern_options = self._count_patterns(modernized_code, self.mongoose_patterns['modern_options'])
        schema_count = self._count_patterns(modernized_code, self.mongoose_patterns['schema_patterns'])
        
        analysis['schema_modernization'] = {
            'schema_count': schema_count,
            'original_deprecated_options': original_deprecated,
            'deprecated_options_remaining': modernized_deprecated,
            'modern_options_used': modern_options,
            'modernization_rate': (original_deprecated - modernized_deprecated) / max(original_deprecated, 1)
        }
        
        # Analyze middleware modernization
        middleware_count = self._count_patterns(modernized_code, self.mongoose_patterns['middleware_patterns'])
        has_async_middleware = 'async function' in modernized_code and any(pattern in modernized_code for pattern in self.mongoose_patterns['middleware_patterns'])
        
        analysis['middleware_modernization'] = {
            'middleware_count': middleware_count,
            'uses_async_middleware': has_async_middleware,
            'modernization_complete': has_async_middleware if middleware_count > 0 else True
        }
        
        # Calculate compatibility score
        schema_score = analysis['schema_modernization']['modernization_rate']
        middleware_score = 1.0 if analysis['middleware_modernization']['modernization_complete'] else 0.5
        analysis['compatibility_score'] = (schema_score + middleware_score) / 2
        
        return analysis
    
    def _count_patterns(self, code: str, patterns: List[str]) -> int:
        """Count occurrences of patterns in code"""
        count = 0
        for pattern in patterns:
            count += code.count(pattern)
        return count
    
    def generate_database_migration_report(self, original_code: str, modernized_code: str) -> Dict[str, Any]:
        """Generate comprehensive database migration report"""
        mongodb_analysis = self.analyze_mongodb_modernization(original_code, modernized_code)
        mongoose_analysis = self.analyze_mongoose_modernization(original_code, modernized_code)
        
        overall_score = (mongodb_analysis['compatibility_score'] + mongoose_analysis['compatibility_score']) / 2
        
        return {
            'overall_compatibility_score': overall_score,
            'mongodb_modernization': mongodb_analysis,
            'mongoose_modernization': mongoose_analysis,
            'migration_quality': 'excellent' if overall_score > 0.9 else 'good' if overall_score > 0.7 else 'needs_improvement',
            'recommendations': self._generate_database_recommendations(mongodb_analysis, mongoose_analysis)
        }
    
    def _generate_database_recommendations(self, mongodb_analysis: Dict[str, Any], mongoose_analysis: Dict[str, Any]) -> List[str]:
        """Generate database modernization recommendations"""
        recommendations = []
        
        # MongoDB recommendations
        if mongodb_analysis['query_method_migration']['migration_rate'] < 0.8:
            recommendations.append("Complete migration of deprecated MongoDB query methods (insert, update, remove)")
        
        if not mongodb_analysis['connection_modernization']['modernization_complete']:
            recommendations.append("Migrate MongoDB connections from callbacks to async/await")
        
        # Mongoose recommendations
        if mongoose_analysis['schema_modernization']['modernization_rate'] < 0.8:
            recommendations.append("Update Mongoose schema options to 7.x compatible format")
        
        if not mongoose_analysis['middleware_modernization']['modernization_complete']:
            recommendations.append("Migrate Mongoose middleware to async/await pattern")
        
        return recommendations


def validate_full_stack_compatibility(original_code: str, modernized_code: str) -> Dict[str, Any]:
    """Validate complete full-stack modernization compatibility"""
    
    api_analyzer = APICompatibilityAnalyzer()
    backend_analyzer = BackendCompatibilityAnalyzer()
    database_analyzer = DatabaseCompatibilityAnalyzer()
    
    # Generate individual reports
    api_report = api_analyzer.compare_api_signatures({}, {})  # Simplified for now
    backend_report = backend_analyzer.generate_backend_migration_report(original_code, modernized_code)
    database_report = database_analyzer.generate_database_migration_report(original_code, modernized_code)
    
    # Calculate overall compatibility
    overall_score = (
        backend_report['overall_compatibility_score'] + 
        database_report['overall_compatibility_score']
    ) / 2
    
    return {
        'overall_compatibility_score': overall_score,
        'api_compatibility': api_report,
        'backend_modernization': backend_report,
        'database_modernization': database_report,
        'system_ready': overall_score >= 0.8,
        'critical_issues': _identify_critical_issues(backend_report, database_report),
        'next_steps': _generate_next_steps(backend_report, database_report)
    }


def _identify_critical_issues(backend_report: Dict[str, Any], database_report: Dict[str, Any]) -> List[str]:
    """Identify critical issues requiring immediate attention"""
    issues = []
    
    if backend_report['overall_compatibility_score'] < 0.7:
        issues.append("Backend modernization incomplete - Express/Node.js migration required")
    
    if database_report['overall_compatibility_score'] < 0.7:
        issues.append("Database modernization incomplete - MongoDB/Mongoose migration required")
    
    return issues


def _generate_next_steps(backend_report: Dict[str, Any], database_report: Dict[str, Any]) -> List[str]:
    """Generate actionable next steps for full-stack modernization"""
    next_steps = []
    
    next_steps.extend(backend_report.get('recommendations', []))
    next_steps.extend(database_report.get('recommendations', []))
    
    if not next_steps:
        next_steps.append("Full-stack modernization complete - ready for production deployment")
    
    return next_steps

