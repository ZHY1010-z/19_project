#!/usr/bin/env python3
"""
Final Comprehensive Code Evaluation Program

This program provides comprehensive evaluation of modernized code by comparing
original and upgraded versions using quality analysis, semantic analysis,
differential comparison, runtime validation, comprehensive scoring, and improvement tracking.

Features:
- Multi-dimensional quality scoring (6 components)
- AI-driven semantic analysis with evidence-based validation
- Improvement tracking and impact analysis
- Visual progress reporting with colored output
- Flexible configuration through environment variables
- Comprehensive markdown and JSON reporting

"""

import os
import sys
import json
import logging
import datetime
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
from dataclasses import dataclass

# Try to import colorama for colored output (optional)
try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    COLORAMA_AVAILABLE = True
except ImportError:
    # Fallback if colorama is not available
    class DummyColor:
        def __getattr__(self, name):
            return ""
    
    Fore = DummyColor()
    Back = DummyColor()
    Style = DummyColor()
    COLORAMA_AVAILABLE = False

# Import required classes from util.py
from util import QualityAnalyzer, ASTAnalyzer, DependencyAnalyzer, llm_call

# Flexible configuration with environment variables
ORIGINAL_CODE_PATH = os.getenv("ORIGINAL_CODE_PATH", "./original_code")
MODERNIZED_CODE_PATH = os.getenv("MODERNIZED_CODE_PATH", "./modernized_code")
OUTPUT_REPORT_PATH = os.getenv("OUTPUT_REPORT_PATH", "./evaluation_report.md")
OUTPUT_JSON_PATH = os.getenv("OUTPUT_JSON_PATH", "./evaluation_report.json")

# AI analysis configuration
MAX_FILE_SIZE_FOR_AI = int(os.getenv("MAX_FILE_SIZE_FOR_AI", "50000"))  # 50k characters default
AI_RETRY_MAX = int(os.getenv("AI_RETRY_MAX", "3"))
AI_RETRY_DELAY = int(os.getenv("AI_RETRY_DELAY", "2"))
PARALLEL_AI_WORKERS = int(os.getenv("PARALLEL_AI_WORKERS", "2"))

# Supported file extensions
SUPPORTED_EXTENSIONS = {'.js', '.py', '.php', '.ts', '.jsx', '.tsx', '.json'}

# Files and directories to exclude (configurable via environment)
EXCLUDED_DIRS = set(os.getenv("EXCLUDED_DIRS", "node_modules,__pycache__,.git,venv,env,.venv,dist,build,.next,coverage,.pytest_cache").split(","))
EXCLUDED_FILES = set(os.getenv("EXCLUDED_FILES", "package-lock.json,yarn.lock,pnpm-lock.yaml,poetry.lock,Pipfile.lock,.DS_Store,evaluation_report.json,evaluation_report.md").split(","))

# Logging configuration
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "evaluation.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class EvaluationConfig:
    """Configuration class for evaluation parameters"""
    original_path: str
    modernized_path: str
    output_report_path: str
    output_json_path: str
    parallel_processing: bool = True
    max_workers: int = 4
    include_ai_analysis: bool = True
    include_comprehensive_scoring: bool = True
    verbose: bool = True
    max_file_size_for_ai: int = MAX_FILE_SIZE_FOR_AI

@dataclass
class FileComparisonResult:
    """Result of comparing two files"""
    file_path: str
    original_exists: bool
    modernized_exists: bool
    size_change: float
    line_count_change: int
    quality_metrics: Dict[str, Any]
    semantic_analysis: Dict[str, Any]
    issues: List[Dict[str, Any]]
    recommendations: List[str]

def retry_with_backoff(func, max_retries=AI_RETRY_MAX, base_delay=AI_RETRY_DELAY):
    """
    Retry function with exponential backoff for rate limit handling
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        
    Returns:
        Function result or raises last exception
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check if it's a rate limit error
            if any(keyword in error_msg for keyword in ['rate', 'limit', 'quota', 'throttle', '429']):
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limit hit, retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries + 1})")
                    time.sleep(delay)
                    continue
                else:
                    logger.error(f"Max retries exceeded due to rate limiting: {e}")
                    raise
            else:
                # For non-rate-limit errors, don't retry
                raise
    
    # This shouldn't be reached, but just in case
    raise Exception("Unexpected end of retry logic")

class FinalCodeEvaluationProgram:
    """
    Final comprehensive code evaluation program combining all advanced features
    """
    
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.quality_analyzer = QualityAnalyzer()
        self.ast_analyzer = ASTAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        
        # Initialize comprehensive result storage
        self.evaluation_results = {
            "metadata": {
                "timestamp": datetime.datetime.now().isoformat(),
                "original_path": config.original_path,
                "modernized_path": config.modernized_path,
                "version": "2.0-final",
                "configuration": {
                    "ai_analysis_enabled": config.include_ai_analysis,
                    "comprehensive_scoring_enabled": config.include_comprehensive_scoring,
                    "max_file_size_for_ai": config.max_file_size_for_ai,
                    "parallel_processing": config.parallel_processing
                }
            },
            "summary": {},
            "file_comparisons": [],
            "quality_analysis": {},
            "semantic_analysis": {},
            "runtime_validation": {},
            "recommendations": [],
            "scoring": {
                "overall_score": 0,
                "component_scores": {},
                "score_breakdown": {},
                "improvement_areas": []
            },
            "improvements_implemented": {
                "categories": {},
                "detailed_improvements": [],
                "improvement_summary": {},
                "impact_analysis": {}
            }
        }
        
    def run_evaluation(self) -> Dict[str, Any]:
        """
        Run complete evaluation process with all advanced features
        
        Returns:
            Complete evaluation results
        """
        try:
            self._print_header()
            
            # Step 1: Discover files to compare
            file_pairs = self._discover_file_pairs()
            self._print_status(f"Found {len(file_pairs)} file pairs to analyze", "info")
            
            # Print discovered files for visibility
            if file_pairs:
                self._print_status("Discovered files:", "info")
                for i, (orig, mod) in enumerate(file_pairs[:10], 1):  # Show first 10
                    filename = Path(mod or orig).name
                    print(f"  {i}. {filename}")
                if len(file_pairs) > 10:
                    print(f"  ... and {len(file_pairs) - 10} more files")
            
            # Step 2: Quality Analysis
            self._print_section_header("Quality Analysis")
            quality_results = self._perform_quality_analysis(file_pairs)
            
            # Step 3: Semantic Analysis (AI-Powered)
            if self.config.include_ai_analysis:
                self._print_section_header("Semantic Analysis (AI-Powered)")
                self._print_status(f"This will analyze {len(file_pairs)} files with AI (may take time)", "warning")
                semantic_results = self._perform_semantic_analysis(file_pairs)
            else:
                semantic_results = {}
                self._print_status("AI analysis disabled in configuration", "info")
            
            # Step 4: Differential Comparison
            self._print_section_header("Differential Comparison")
            comparison_results = self._perform_differential_comparison(file_pairs)
            
            # Step 5: Runtime Validation
            self._print_section_header("Runtime Validation")
            runtime_results = self._perform_runtime_validation()
            
            # Step 6: Comprehensive Scoring & Improvement Analysis
            if self.config.include_comprehensive_scoring:
                self._print_section_header("Comprehensive Scoring & Improvement Analysis")
                self.calculate_comprehensive_scores()
            else:
                self._print_status("Comprehensive scoring disabled in configuration", "info")
            
            # Step 7: Generate Summary and Recommendations
            self._generate_summary_and_recommendations()
            
            # Step 8: Generate Reports
            self._generate_markdown_report()
            self._generate_json_report()
            
            self._print_completion_summary()
            
            return self.evaluation_results
            
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _discover_file_pairs(self) -> List[Tuple[str, str]]:
        """
        Discover file pairs between original and modernized directories
        
        Returns:
            List of (original_file, modernized_file) tuples
        """
        file_pairs = []
        
        def should_skip_path(path: Path) -> bool:
            """Check if path should be skipped"""
            # Skip excluded directories
            if any(excluded in path.parts for excluded in EXCLUDED_DIRS):
                return True
            # Skip excluded files
            if path.name in EXCLUDED_FILES:
                return True
            return False
        
        original_path = Path(self.config.original_path)
        modernized_path = Path(self.config.modernized_path)
        
        if not original_path.exists():
            raise FileNotFoundError(f"Original code path not found: {original_path}")
        
        if not modernized_path.exists():
            raise FileNotFoundError(f"Modernized code path not found: {modernized_path}")
        
        # Find all files in original directory
        for original_file in original_path.rglob("*"):
            if original_file.is_file() and original_file.suffix in SUPPORTED_EXTENSIONS:
                if should_skip_path(original_file):
                    continue
                    
                # Calculate relative path
                rel_path = original_file.relative_to(original_path)
                modernized_file = modernized_path / rel_path
                
                file_pairs.append((str(original_file), str(modernized_file)))
        
        # Find files that exist only in modernized directory
        for modernized_file in modernized_path.rglob("*"):
            if modernized_file.is_file() and modernized_file.suffix in SUPPORTED_EXTENSIONS:
                if should_skip_path(modernized_file):
                    continue
                    
                rel_path = modernized_file.relative_to(modernized_path)
                original_file = original_path / rel_path
                
                if not original_file.exists():
                    file_pairs.append((None, str(modernized_file)))
        
        return file_pairs
    
    def _perform_quality_analysis(self, file_pairs: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Perform quality analysis on both original and modernized code
        
        Args:
            file_pairs: List of file pairs to analyze
            
        Returns:
            Quality analysis results
        """
        # Analyze original code
        original_quality = {}
        if Path(self.config.original_path).exists():
            self._print_status("Analyzing original code quality...", "info")
            try:
                original_quality = self.quality_analyzer.analyze_repository_quality(
                    self.config.original_path
                )
            except Exception as e:
                logger.warning(f"Original code quality analysis failed: {e}")
                original_quality = {"error": str(e)}
        
        # Analyze modernized code
        modernized_quality = {}
        if Path(self.config.modernized_path).exists():
            self._print_status("Analyzing modernized code quality...", "info")
            try:
                modernized_quality = self.quality_analyzer.analyze_repository_quality(
                    self.config.modernized_path
                )
            except Exception as e:
                logger.warning(f"Modernized code quality analysis failed: {e}")
                modernized_quality = {"error": str(e)}
        
        quality_results = {
            "original": original_quality,
            "modernized": modernized_quality,
            "comparison": self._compare_quality_metrics(original_quality, modernized_quality)
        }
        
        self.evaluation_results["quality_analysis"] = quality_results
        return quality_results
    
    def _perform_semantic_analysis(self, file_pairs: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Perform AI-powered semantic analysis with evidence-based validation
        
        Args:
            file_pairs: List of file pairs to analyze
            
        Returns:
            Semantic analysis results
        """
        semantic_results = {
            "file_analyses": [],
            "overall_assessment": {},
            "functional_equivalence": "UNKNOWN",
            "confidence_score": 0
        }
        
        if self.config.parallel_processing and len(file_pairs) > 1:
            # Parallel processing with configurable workers for AI calls
            ai_workers = min(PARALLEL_AI_WORKERS, self.config.max_workers)
            with ThreadPoolExecutor(max_workers=ai_workers) as executor:
                future_to_file = {
                    executor.submit(self._analyze_file_semantically, original, modernized): (original, modernized)
                    for original, modernized in file_pairs
                }
                
                for future in as_completed(future_to_file):
                    original, modernized = future_to_file[future]
                    try:
                        result = future.result()
                        semantic_results["file_analyses"].append(result)
                        self._print_status(f"✓ Analyzed: {Path(modernized or original).name}", "success")
                    except Exception as e:
                        logger.error(f"Semantic analysis failed for {original} -> {modernized}: {e}")
        else:
            # Sequential processing with configurable delay
            for i, (original, modernized) in enumerate(file_pairs):
                try:
                    # Add delay between API calls to respect rate limits
                    if i > 0:
                        time.sleep(AI_RETRY_DELAY)
                        self._print_status(f"Rate limit protection: waiting {AI_RETRY_DELAY}s...", "info")
                    
                    result = self._analyze_file_semantically(original, modernized)
                    semantic_results["file_analyses"].append(result)
                    self._print_status(f"✓ Analyzed: {Path(modernized or original).name}", "success")
                except Exception as e:
                    logger.error(f"Semantic analysis failed for {original} -> {modernized}: {e}")
                    # Continue with other files even if one fails
        
        # Generate overall assessment
        semantic_results["overall_assessment"] = self._generate_overall_semantic_assessment(
            semantic_results["file_analyses"]
        )
        
        self.evaluation_results["semantic_analysis"] = semantic_results
        return semantic_results
    
    def _analyze_file_semantically(self, original_file: Optional[str], modernized_file: str) -> Dict[str, Any]:
        """
        Analyze a single file pair semantically using AI with evidence-based validation
        
        Args:
            original_file: Path to original file (None if new file)
            modernized_file: Path to modernized file
            
        Returns:
            Semantic analysis result for the file pair
        """
        result = {
            "original_file": original_file,
            "modernized_file": modernized_file,
            "analysis": {},
            "issues": [],
            "recommendations": []
        }
        
        try:
            # Read file contents
            original_content = ""
            if original_file and Path(original_file).exists():
                with open(original_file, 'r', encoding='utf-8') as f:
                    original_content = f.read()
            
            modernized_content = ""
            if Path(modernized_file).exists():
                with open(modernized_file, 'r', encoding='utf-8') as f:
                    modernized_content = f.read()
            
            # Construct AI prompt with configurable limits
            prompt = self._create_semantic_analysis_prompt(
                original_content, modernized_content, original_file, modernized_file
            )
            
            # Get AI analysis with retry logic and error handling
            try:
                def make_ai_call():
                    return llm_call(
                        prompt, 
                        "You are a precise code analyzer. You MUST base your analysis ONLY on the actual code provided. DO NOT make assumptions, DO NOT hallucinate issues, DO NOT report problems that don't exist in the code. Only report what you can directly observe and verify. If something is correctly implemented, say so. Output ONLY valid JSON as specified."
                    )
                
                # Use retry logic for rate limit handling
                ai_response = retry_with_backoff(make_ai_call, max_retries=AI_RETRY_MAX, base_delay=AI_RETRY_DELAY)
                
                # Parse AI response with comprehensive error handling
                try:
                    # Clean response - handle multiple formats
                    cleaned_response = ai_response.strip()
                    
                    # Remove markdown code blocks
                    if '```json' in cleaned_response:
                        start = cleaned_response.find('```json') + 7
                        end = cleaned_response.find('```', start)
                        if end > start:
                            cleaned_response = cleaned_response[start:end]
                    elif '```' in cleaned_response:
                        start = cleaned_response.find('```') + 3
                        end = cleaned_response.rfind('```')
                        if end > start:
                            cleaned_response = cleaned_response[start:end]
                    
                    # Remove any leading/trailing whitespace and non-JSON content
                    cleaned_response = cleaned_response.strip()
                    
                    # Find JSON object boundaries
                    if not cleaned_response.startswith('{'):
                        json_start = cleaned_response.find('{')
                        if json_start != -1:
                            cleaned_response = cleaned_response[json_start:]
                    
                    if not cleaned_response.endswith('}'):
                        json_end = cleaned_response.rfind('}')
                        if json_end != -1:
                            cleaned_response = cleaned_response[:json_end + 1]
                    
                    # Try to parse JSON
                    analysis = json.loads(cleaned_response)
                    
                    # Validate required fields and provide defaults
                    required_fields = {
                        "functional_equivalence": "WARNING",
                        "runtime_viability": "WARNING",
                        "confidence_score": 50,
                        "verified_issues": [],  # Evidence-based format
                        "intentional_modernizations": [],  # Positive changes
                        "code_completeness": "UNKNOWN",
                        "configuration_verified": {},
                        "breaking_changes": [],
                        "missing_functionality": [],
                        "improvements": [],
                        "critical_issues": [],
                        "will_run_in_production": True,
                        "recommendation": "NEEDS_FIXES",
                        "detailed_analysis": "AI analysis completed"
                    }
                    
                    for field, default_value in required_fields.items():
                        if field not in analysis:
                            analysis[field] = default_value
                    
                    result["analysis"] = analysis
                    
                    # Extract issues from evidence-based format
                    if "verified_issues" in analysis and analysis["verified_issues"]:
                        result["issues"].extend([
                            {
                                "severity": issue.get("severity", "unknown"), 
                                "description": issue.get("issue", ""),
                                "evidence": issue.get("evidence", ""),
                                "line_reference": issue.get("line_reference", "")
                            }
                            for issue in analysis["verified_issues"]
                        ])
                    # Fallback to legacy format
                    elif "critical_issues" in analysis and analysis["critical_issues"]:
                        result["issues"].extend([
                            {"severity": "critical", "description": issue}
                            for issue in analysis["critical_issues"]
                        ])
                    
                    # Extract recommendations (modernizations are positive)
                    if "intentional_modernizations" in analysis and analysis["intentional_modernizations"]:
                        result["recommendations"].extend([
                            f"✅ Intentional modernization: {mod}"
                            for mod in analysis["intentional_modernizations"]
                        ])
                    if "recommendations" in analysis:
                        result["recommendations"].extend(analysis.get("recommendations", []))
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse AI response for {modernized_file}: {e}")
                    # Provide fallback analysis
                    result["analysis"] = {
                        "functional_equivalence": "WARNING",
                        "runtime_viability": "WARNING",
                        "confidence_score": 50,
                        "breaking_changes": [],
                        "missing_functionality": [],
                        "improvements": [],
                        "critical_issues": [],
                        "will_run_in_production": True,
                        "recommendation": "NEEDS_FIXES",
                        "detailed_analysis": f"AI response parsing failed: {str(e)}. Manual review recommended.",
                        "error": "Failed to parse AI response",
                        "raw_response": ai_response[:500] + "..." if len(ai_response) > 500 else ai_response
                    }
                    
            except Exception as api_error:
                logger.warning(f"AI API call failed for {modernized_file}: {api_error}")
                # Provide fallback analysis when API fails
                result["analysis"] = {
                    "functional_equivalence": "UNKNOWN",
                    "runtime_viability": "UNKNOWN", 
                    "confidence_score": 0,
                    "breaking_changes": [],
                    "missing_functionality": [],
                    "improvements": [],
                    "critical_issues": [],
                    "will_run_in_production": False,
                    "recommendation": "NEEDS_FIXES",
                    "detailed_analysis": f"AI analysis failed due to API error: {str(api_error)}. Manual review required.",
                    "error": f"API call failed: {str(api_error)}"
                }
        
        except Exception as e:
            logger.error(f"Semantic analysis failed for {modernized_file}: {e}")
            result["analysis"] = {"error": str(e)}
        
        return result
    
    def _create_semantic_analysis_prompt(self, original_content: str, modernized_content: str, 
                                       original_file: Optional[str], modernized_file: str) -> str:
        """
        Create enhanced AI prompt for semantic analysis with explicit executability validation
        
        Args:
            original_content: Original file content
            modernized_content: Modernized file content
            original_file: Original file path
            modernized_file: Modernized file path
            
        Returns:
            Formatted prompt for AI analysis with executability focus
        """
        max_size = self.config.max_file_size_for_ai
        
        if not original_content:
            return f"""
Analyze this new file created during modernization for EXECUTABILITY:

File: {modernized_file}
Content:
```
{modernized_content[:max_size]}
```

CRITICAL QUESTION: Can this code be executed successfully?

Provide analysis in JSON format:
{{
    "is_new_file": true,
    "can_execute": "YES|NO|UNCERTAIN",
    "execution_blockers": ["specific issues preventing execution"],
    "runtime_viability": "PASS|FAIL|WARNING",
    "confidence_score": 0-100,
    "critical_issues": ["list of issues"],
    "recommendations": ["list of recommendations"],
    "detailed_analysis": "comprehensive explanation"
}}
"""
        
        return f"""
MAIN OBJECTIVE: Determine if the modernized code can be executed successfully.

You are a code execution specialist. Your primary task is to assess whether the modernized code can actually run without errors.

Original Code ({original_file}):
```
{original_content[:max_size]}
```

Modernized Code ({modernized_file}):
```
{modernized_content[:max_size]}
```

CRITICAL EXECUTABILITY ANALYSIS:

🔍 STEP 1: EXECUTION READINESS CHECK
Answer these specific questions about the modernized code:

A. Can this code be loaded by Node.js/Python interpreter?
   - Syntax is valid?
   - Module format is correct?
   - No obvious parsing errors?

B. Can all dependencies be resolved?
   - Are all imported packages available?
   - Are import paths correct?
   - Are there missing dependencies?

C. Can the code run to completion?
   - Are all variables defined before use?
   - Are all functions properly defined?
   - Are there runtime errors waiting to happen?

🚨 STEP 2: EXECUTION BLOCKERS IDENTIFICATION
Identify specific issues that would prevent execution:
- Missing dependencies
- Syntax errors
- Undefined variables/functions
- Module system mismatches (ES6 vs CommonJS)
- Configuration errors

✅ STEP 3: FUNCTIONAL EQUIVALENCE WITH EXECUTION FOCUS
- Does the modernized code preserve the same executable behavior?
- Are the entry points still functional?
- Would the app start and run successfully?

📊 STEP 4: EXECUTABILITY CONFIDENCE ASSESSMENT
Rate your confidence that this code would execute successfully:
- 90-100%: Very confident it will run
- 70-89%: Likely to run with minor issues
- 50-69%: Uncertain, may have execution problems
- 30-49%: Unlikely to run without fixes
- 0-29%: Will definitely fail to execute

OUTPUT FORMAT (strict JSON):
{{
    "can_execute": "YES|NO|UNCERTAIN",
    "execution_confidence": 0-100,
    "execution_blockers": [
        {{
            "blocker_type": "SYNTAX|DEPENDENCY|CONFIGURATION|LOGIC|OTHER",
            "severity": "CRITICAL|HIGH|MEDIUM|LOW",
            "description": "specific issue that prevents execution",
            "evidence": "exact code or evidence showing the problem",
            "fix_required": "what needs to be fixed for execution"
        }}
    ],
    "functional_equivalence": "PASS|FAIL|WARNING",
    "runtime_viability": "PASS|FAIL|WARNING",
    "execution_readiness": {{
        "syntax_valid": true/false,
        "dependencies_resolvable": true/false,
        "entry_points_functional": true/false,
        "configuration_correct": true/false
    }},
    "verified_issues": [
        {{
            "severity": "CRITICAL|HIGH|MEDIUM|LOW",
            "issue": "brief description",
            "evidence": "what you actually see in the code",
            "line_reference": "specific code snippet that proves this",
            "prevents_execution": true/false
        }}
    ],
    "intentional_modernizations": ["list of purposeful upgrades"],
    "code_completeness": "COMPLETE|TRUNCATED",
    "will_execute_successfully": "YES - High confidence this code will run|NO - This code will fail to execute|UNCERTAIN - May have execution issues",
    "recommendation": "READY_TO_RUN|NEEDS_FIXES_TO_RUN|WILL_NOT_RUN",
    "detailed_analysis": "comprehensive explanation focusing on executability"
}}

FOCUS: Your primary goal is to determine if someone can run this modernized code successfully. Be specific about execution blockers and provide clear YES/NO assessment on executability.
"""
    
    def _perform_differential_comparison(self, file_pairs: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Perform differential comparison between original and modernized files
        
        Args:
            file_pairs: List of file pairs to compare
            
        Returns:
            Differential comparison results
        """
        comparison_results = {
            "file_comparisons": [],
            "summary": {
                "total_files": len(file_pairs),
                "new_files": 0,
                "modified_files": 0,
                "deleted_files": 0,
                "size_changes": {}
            }
        }
        
        for original_file, modernized_file in file_pairs:
            file_result = self._compare_individual_files(original_file, modernized_file)
            comparison_results["file_comparisons"].append(file_result)
            
            # Update summary
            if not original_file:
                comparison_results["summary"]["new_files"] += 1
            elif not Path(modernized_file).exists():
                comparison_results["summary"]["deleted_files"] += 1
            else:
                comparison_results["summary"]["modified_files"] += 1
        
        self.evaluation_results["file_comparisons"] = comparison_results["file_comparisons"]
        return comparison_results
    
    def _compare_individual_files(self, original_file: Optional[str], modernized_file: str) -> FileComparisonResult:
        """
        Compare two individual files
        
        Args:
            original_file: Path to original file
            modernized_file: Path to modernized file
            
        Returns:
            File comparison result
        """
        result = FileComparisonResult(
            file_path=modernized_file,
            original_exists=original_file is not None and Path(original_file).exists(),
            modernized_exists=Path(modernized_file).exists(),
            size_change=0.0,
            line_count_change=0,
            quality_metrics={},
            semantic_analysis={},
            issues=[],
            recommendations=[]
        )
        
        try:
            # Compare file sizes and line counts
            if result.original_exists and result.modernized_exists:
                original_size = Path(original_file).stat().st_size
                modernized_size = Path(modernized_file).stat().st_size
                result.size_change = ((modernized_size - original_size) / original_size) * 100 if original_size > 0 else 0
                
                # Count lines
                with open(original_file, 'r', encoding='utf-8') as f:
                    original_lines = len(f.readlines())
                with open(modernized_file, 'r', encoding='utf-8') as f:
                    modernized_lines = len(f.readlines())
                
                result.line_count_change = modernized_lines - original_lines
                
                # Check for significant size reduction (potential truncation)
                if result.size_change < -50:  # More than 50% reduction
                    result.issues.append({
                        "severity": "critical",
                        "type": "potential_truncation",
                        "description": f"File size reduced by {abs(result.size_change):.1f}% - possible truncation"
                    })
        
        except Exception as e:
            logger.error(f"File comparison failed for {modernized_file}: {e}")
            result.issues.append({
                "severity": "error",
                "type": "comparison_error",
                "description": str(e)
            })
        
        return result
    
    def _perform_runtime_validation(self) -> Dict[str, Any]:
        """
        Perform runtime validation checks
        
        Returns:
            Runtime validation results
        """
        validation_results = {
            "package_validation": {},
            "syntax_validation": {},
            "dependency_validation": {},
            "import_validation": {},
            "overall_status": "UNKNOWN"
        }
        
        try:
            # Check package.json validity (for JS/TS projects)
            package_json_path = Path(self.config.modernized_path) / "package.json"
            if package_json_path.exists():
                validation_results["package_validation"] = self._validate_package_json(package_json_path)
            
            # Validate Python dependencies (for Python projects)
            requirements_path = Path(self.config.modernized_path) / "requirements.txt"
            if requirements_path.exists():
                validation_results["dependency_validation"] = self._validate_python_dependencies(requirements_path)
            
            # Syntax validation
            validation_results["syntax_validation"] = self._validate_syntax()
            
            # Import validation
            validation_results["import_validation"] = self._validate_imports()
            
            # Determine overall status
            validation_results["overall_status"] = self._determine_runtime_status(validation_results)
        
        except Exception as e:
            logger.error(f"Runtime validation failed: {e}")
            validation_results["overall_status"] = "ERROR"
            validation_results["error"] = str(e)
        
        self.evaluation_results["runtime_validation"] = validation_results
        return validation_results
    
    def _validate_package_json(self, package_json_path: Path) -> Dict[str, Any]:
        """
        Validate package.json file
        
        Args:
            package_json_path: Path to package.json
            
        Returns:
            Package validation results
        """
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            return {
                "valid_json": True,
                "has_dependencies": "dependencies" in package_data or "devDependencies" in package_data,
                "package_count": len(package_data.get("dependencies", {})) + len(package_data.get("devDependencies", {})),
                "issues": []
            }
        except json.JSONDecodeError as e:
            return {
                "valid_json": False,
                "error": str(e),
                "issues": [{"severity": "critical", "description": "Invalid JSON format"}]
            }
        except Exception as e:
            return {
                "valid_json": False,
                "error": str(e),
                "issues": [{"severity": "error", "description": str(e)}]
            }
    
    def _validate_python_dependencies(self, requirements_path: Path) -> Dict[str, Any]:
        """
        Validate Python requirements.txt file
        
        Args:
            requirements_path: Path to requirements.txt
            
        Returns:
            Dependency validation results
        """
        try:
            with open(requirements_path, 'r') as f:
                requirements = f.readlines()
            
            return {
                "valid_format": True,
                "package_count": len([line for line in requirements if line.strip() and not line.startswith('#')]),
                "issues": []
            }
        except Exception as e:
            return {
                "valid_format": False,
                "error": str(e),
                "issues": [{"severity": "error", "description": str(e)}]
            }
    
    def _validate_syntax(self) -> Dict[str, Any]:
        """
        Validate syntax of modernized files
        
        Returns:
            Syntax validation results
        """
        syntax_results = {
            "total_files": 0,
            "valid_files": 0,
            "syntax_errors": []
        }
        
        def should_skip_path(path: Path) -> bool:
            """Check if path should be skipped"""
            return any(excluded in path.parts for excluded in EXCLUDED_DIRS)
        
        modernized_path = Path(self.config.modernized_path)
        
        for file_path in modernized_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in SUPPORTED_EXTENSIONS:
                # Skip excluded directories
                if should_skip_path(file_path):
                    continue
                    
                syntax_results["total_files"] += 1
                
                try:
                    if file_path.suffix == '.py':
                        # Python syntax validation
                        with open(file_path, 'r', encoding='utf-8') as f:
                            compile(f.read(), str(file_path), 'exec')
                    elif file_path.suffix in {'.js', '.ts', '.jsx', '.tsx'}:
                        # Basic JS/TS syntax validation (would need proper parser for full validation)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Simple checks
                            if content.count('{') != content.count('}'):
                                raise SyntaxError("Mismatched braces")
                            if content.count('(') != content.count(')'):
                                raise SyntaxError("Mismatched parentheses")
                    
                    syntax_results["valid_files"] += 1
                
                except Exception as e:
                    syntax_results["syntax_errors"].append({
                        "file": str(file_path),
                        "error": str(e)
                    })
        
        return syntax_results
    
    def _validate_imports(self) -> Dict[str, Any]:
        """
        Validate imports in modernized files
        
        Returns:
            Import validation results
        """
        # Use AST analyzer to check imports
        try:
            ast_results = self.ast_analyzer.analyze_repository(self.config.modernized_path)
            return {
                "total_imports": ast_results.get("total_imports", 0),
                "import_analysis": ast_results.get("code_structure", {}).get("imports", []),
                "issues": []
            }
        except Exception as e:
            return {
                "error": str(e),
                "issues": [{"severity": "error", "description": f"Import validation failed: {e}"}]
            }
    
    def _determine_runtime_status(self, validation_results: Dict[str, Any]) -> str:
        """
        Determine overall runtime status based on validation results
        
        Args:
            validation_results: All validation results
            
        Returns:
            Overall runtime status
        """
        critical_issues = 0
        
        # Check for critical issues in each validation category
        for category, results in validation_results.items():
            if isinstance(results, dict) and "issues" in results:
                critical_issues += len([issue for issue in results["issues"] 
                                     if issue.get("severity") == "critical"])
        
        if critical_issues > 0:
            return "FAIL"
        elif any("error" in str(results) for results in validation_results.values()):
            return "WARNING"
        else:
            return "PASS"
    
    def calculate_comprehensive_scores(self):
        """Calculate comprehensive code quality scores and improvement tracking"""
        self._print_status("Calculating comprehensive quality scores...", "info")
        
        # Calculate component scores
        component_scores = self._calculate_component_scores()
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(component_scores)
        
        # Analyze improvements implemented
        improvements = self._analyze_improvements_implemented()
        
        # Update results
        self.evaluation_results["scoring"] = {
            "overall_score": overall_score,
            "component_scores": component_scores,
            "score_breakdown": self._generate_score_breakdown(component_scores),
            "improvement_areas": self._identify_improvement_areas(component_scores)
        }
        
        self.evaluation_results["improvements_implemented"] = improvements
        
        # Update summary with scoring info
        self.evaluation_results["summary"]["comprehensive_score"] = overall_score
        self.evaluation_results["summary"]["improvement_score"] = improvements["improvement_summary"].get("overall_improvement_score", 0)
    
    def _calculate_component_scores(self) -> Dict[str, float]:
        """Calculate scores for different code quality components"""
        scores = {}
        
        # 1. Code Quality Score (0-100)
        scores["code_quality"] = self._calculate_code_quality_score()
        
        # 2. Security Score (0-100)
        scores["security"] = self._calculate_security_score()
        
        # 3. Performance Score (0-100)
        scores["performance"] = self._calculate_performance_score()
        
        # 4. Maintainability Score (0-100)
        scores["maintainability"] = self._calculate_maintainability_score()
        
        # 5. Modern Practices Score (0-100)
        scores["modern_practices"] = self._calculate_modern_practices_score()
        
        # 6. Dependency Management Score (0-100)
        scores["dependency_management"] = self._calculate_dependency_score()
        
        return scores
    
    def _calculate_code_quality_score(self) -> float:
        """Calculate code quality score with modernization context awareness"""
        original_analysis = self.evaluation_results.get("quality_analysis", {}).get("original", {})
        modernized_analysis = self.evaluation_results.get("quality_analysis", {}).get("modernized", {})
        semantic_analysis = self.evaluation_results.get("semantic_analysis", {})
        
        modernized_smells = len(modernized_analysis.get("code_smells", []))
        
        # Base score starts at 75 (more lenient baseline)
        score = 75.0
        
        # More lenient code smell penalty
        score -= min(modernized_smells * 1, 25)  # Lower penalty: 1 point per smell, max 25 deduction
        
        # Modernization bonus - check AI-identified modernization improvements
        modernization_bonus = 0
        file_analyses = semantic_analysis.get("file_analyses", [])
        
        for file_analysis in file_analyses:
            analysis = file_analysis.get("analysis", {})
            modernizations = analysis.get("intentional_modernizations", [])
            
            # Give 2 points bonus per modernization improvement
            modernization_bonus += len(modernizations) * 2
        
        # Functional equivalence bonus
        overall_assessment = semantic_analysis.get("overall_assessment", {})
        equiv_status = overall_assessment.get("functional_equivalence", "UNKNOWN")
        if equiv_status == "PASS":
            modernization_bonus += 15  # 15 point bonus for passing functional equivalence
        elif equiv_status == "WARNING":
            modernization_bonus += 8   # 8 point bonus for warning status
        
        # Complexity context adjustment - be understanding of complexity increases for modernization
        original_complexity = original_analysis.get("complexity_summary", {})
        modernized_complexity = modernized_analysis.get("complexity_summary", {})
        
        orig_cyclomatic = original_complexity.get("average_cyclomatic_complexity", 0)
        mod_cyclomatic = modernized_complexity.get("average_cyclomatic_complexity", 0)
        
        # If complexity increases but has modernization improvements, reduce complexity penalty
        if mod_cyclomatic > orig_cyclomatic and modernization_bonus > 10:
            complexity_penalty = min((mod_cyclomatic - orig_cyclomatic) * 2, 8)  # Limited complexity penalty
        else:
            complexity_penalty = min((mod_cyclomatic - orig_cyclomatic) * 4, 15)
        
        score -= max(0, complexity_penalty)
        
        # Apply modernization bonus
        score += min(modernization_bonus, 30)  # Maximum 30 points modernization bonus
        
        # Line count growth tolerance - modernization may increase lines but improve quality
        original_lines = original_analysis.get("complexity_summary", {}).get("total_lines_analyzed", 0)
        modernized_lines = modernized_analysis.get("complexity_summary", {}).get("total_lines_analyzed", 0)
        
        if modernized_lines > original_lines and modernization_bonus > 5:
            # Be more tolerant of line growth if there are modernization improvements
            line_growth_ratio = (modernized_lines - original_lines) / original_lines if original_lines > 0 else 0
            if line_growth_ratio < 0.3:  # Growth within 30% is acceptable
                score += 5  # Reasonable growth bonus
        
        return max(30, min(100, score))  # Minimum 30 points, maximum 100 points
    
    def _calculate_security_score(self) -> float:
        """Calculate security score"""
        file_comparisons = self.evaluation_results.get("file_comparisons", [])
        
        security_issues = 0
        security_improvements = 0
        
        for comparison in file_comparisons:
            for issue in comparison.issues:
                if "security" in issue.get("category", "").lower():
                    if issue.get("severity") == "critical":
                        security_issues += 3
                    elif issue.get("severity") == "high":
                        security_issues += 2
                    else:
                        security_issues += 1
                        
                if "security improvement" in issue.get("description", "").lower():
                    security_improvements += 1
        
        # Base score
        score = 100.0 - min(security_issues * 5, 50)  # Max 50 point deduction
        score += min(security_improvements * 3, 20)   # Up to 20 bonus points
        
        return max(0, min(100, score))
    
    def _calculate_performance_score(self) -> float:
        """Calculate performance score"""
        semantic_analysis = self.evaluation_results.get("semantic_analysis", {})
        
        performance_improvements = 0
        performance_issues = 0
        
        for analysis in semantic_analysis.values():
            if isinstance(analysis, dict):
                analysis_text = str(analysis.get("detailed_analysis", "")).lower()
                
                # Count performance improvements
                if any(term in analysis_text for term in ["performance", "optimization", "faster", "efficient"]):
                    performance_improvements += 1
                
                # Count performance issues
                if any(term in analysis_text for term in ["slow", "inefficient", "performance issue"]):
                    performance_issues += 1
        
        score = 85.0  # Base performance score
        score += min(performance_improvements * 5, 15)
        score -= min(performance_issues * 8, 30)
        
        return max(0, min(100, score))
    
    def _calculate_maintainability_score(self) -> float:
        """Calculate maintainability score"""
        file_comparisons = self.evaluation_results.get("file_comparisons", [])
        
        maintainability_factors = {
            "code_organization": 0,
            "documentation": 0,
            "naming": 0,
            "complexity": 0
        }
        
        for comparison in file_comparisons:
            for issue in comparison.issues:
                desc = issue.get("description", "").lower()
                
                if any(term in desc for term in ["organization", "structure", "modular"]):
                    maintainability_factors["code_organization"] += 1
                if any(term in desc for term in ["comment", "documentation", "readme"]):
                    maintainability_factors["documentation"] += 1
                if any(term in desc for term in ["naming", "variable", "function name"]):
                    maintainability_factors["naming"] += 1
                if any(term in desc for term in ["complexity", "nested", "difficult"]):
                    maintainability_factors["complexity"] += 1
        
        # Calculate score based on factors
        base_score = 80.0
        organization_score = max(0, 20 - maintainability_factors["code_organization"] * 2)
        documentation_score = max(0, 15 - maintainability_factors["documentation"] * 3)
        naming_score = max(0, 10 - maintainability_factors["naming"] * 2)
        complexity_score = max(0, 15 - maintainability_factors["complexity"] * 3)
        
        return base_score + organization_score + documentation_score + naming_score + complexity_score
    
    def _calculate_modern_practices_score(self) -> float:
        """Calculate modern practices adoption score with enhanced detection"""
        semantic_analysis = self.evaluation_results.get("semantic_analysis", {})
        file_analyses = semantic_analysis.get("file_analyses", [])
        
        modern_practices_score = 75.0  # Base score of 75 points
        bonus_points = 0
        
        # Track modernization features
        modernization_features = {
            "es6_modules": 0,           # ES6 import/export
            "async_await": 0,           # async/await patterns
            "arrow_functions": 0,       # Arrow functions
            "const_let": 0,             # const/let declarations
            "template_literals": 0,     # Template literals
            "destructuring": 0,         # Destructuring assignment
            "promises": 0,              # Promise usage
            "error_handling": 0,        # Error handling improvements
            "code_organization": 0      # Code organization improvements
        }
        
        for file_analysis in file_analyses:
            analysis = file_analysis.get("analysis", {})
            
            # Check intentional_modernizations (AI-identified modernization improvements)
            modernizations = analysis.get("intentional_modernizations", [])
            for modernization in modernizations:
                mod_text = modernization.lower()
                
                # ES6 module system
                if any(term in mod_text for term in ["es6 import", "commonjs", "require() →", "import statement"]):
                    modernization_features["es6_modules"] += 2  # High value
                
                # async/await patterns
                if any(term in mod_text for term in ["async/await", "callback", "promise-based", "async pattern"]):
                    modernization_features["async_await"] += 3  # Highest value
                
                # Arrow functions and modern syntax
                if any(term in mod_text for term in ["arrow function", "→", "=>"]):
                    modernization_features["arrow_functions"] += 1
                
                # Error handling improvements
                if any(term in mod_text for term in ["error handling", "try-catch", "exception"]):
                    modernization_features["error_handling"] += 2
                
                # Code organization improvements
                if any(term in mod_text for term in ["helper function", "code duplication", "extracted", "organization"]):
                    modernization_features["code_organization"] += 2
            
            # Check detailed analysis text
            detailed_analysis = analysis.get("detailed_analysis", "").lower()
            
            # ES6 feature detection
            if any(term in detailed_analysis for term in ["const ", "let ", "const/let"]):
                modernization_features["const_let"] += 1
            
            if any(term in detailed_analysis for term in ["template literal", "`${", "template string"]):
                modernization_features["template_literals"] += 1
                
            if any(term in detailed_analysis for term in ["destructuring", "spread operator", "...args"]):
                modernization_features["destructuring"] += 1
            
            # Promise and async patterns
            if any(term in detailed_analysis for term in ["promise", "new promise", "promise-based"]):
                modernization_features["promises"] += 1
        
        # Calculate bonus points
        total_modernizations = sum(modernization_features.values())
        
        # Award significant bonus based on modernization feature count
        if total_modernizations >= 10:
            bonus_points = 25  # Excellent modernization
        elif total_modernizations >= 7:
            bonus_points = 20  # Good modernization
        elif total_modernizations >= 5:
            bonus_points = 15  # Medium modernization
        elif total_modernizations >= 3:
            bonus_points = 10  # Basic modernization
        elif total_modernizations >= 1:
            bonus_points = 5   # Minimal modernization
        
        # Special bonus: async/await conversion gets extra points
        if modernization_features["async_await"] > 0:
            bonus_points += 10
        
        # Special bonus: ES6 module conversion gets extra points
        if modernization_features["es6_modules"] > 0:
            bonus_points += 8
        
        final_score = modern_practices_score + bonus_points
        
        # Store detailed information for debugging
        self.evaluation_results["modern_practices_details"] = {
            "base_score": modern_practices_score,
            "bonus_points": bonus_points,
            "features_detected": modernization_features,
            "total_modernizations": total_modernizations
        }
        
        return min(100, final_score)
    
    def _calculate_dependency_score(self) -> float:
        """Calculate dependency management score"""
        file_comparisons = self.evaluation_results.get("file_comparisons", [])
        
        dependency_improvements = 0
        dependency_issues = 0
        
        for comparison in file_comparisons:
            if "package.json" in comparison.file_path or "package-lock.json" in comparison.file_path:
                for issue in comparison.issues:
                    desc = issue.get("description", "").lower()
                    
                    if any(term in desc for term in ["updated", "upgraded", "modern", "secure"]):
                        dependency_improvements += 1
                    if any(term in desc for term in ["vulnerable", "outdated", "deprecated"]):
                        dependency_issues += 1
        
        score = 75.0  # Base score
        score += min(dependency_improvements * 8, 25)
        score -= min(dependency_issues * 10, 40)
        
        return max(0, min(100, score))
    
    def _calculate_overall_score(self, component_scores: Dict[str, float]) -> float:
        """Calculate weighted overall score with emphasis on modernization"""
        weights = {
            "modern_practices": 0.30,      # Increased to 30% - modernization is most important
            "security": 0.20,             # Keep 20% - security is crucial
            "maintainability": 0.20,      # Keep 20% - maintainability matters
            "code_quality": 0.15,         # Reduced to 15% - lower weight for traditional static analysis
            "performance": 0.10,          # Keep 10%
            "dependency_management": 0.05  # Reduced to 5% - relatively less important
        }
        
        weighted_score = sum(
            component_scores.get(component, 0) * weight
            for component, weight in weights.items()
        )
        
        return round(weighted_score, 1)
    
    def _generate_score_breakdown(self, component_scores: Dict[str, float]) -> Dict[str, Any]:
        """Generate detailed score breakdown with explanations"""
        breakdown = {}
        
        for component, score in component_scores.items():
            grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
            
            breakdown[component] = {
                "score": score,
                "grade": grade,
                "description": self._get_score_description(component, score),
                "status": "Excellent" if score >= 90 else "Good" if score >= 80 else "Fair" if score >= 70 else "Poor" if score >= 60 else "Critical"
            }
        
        return breakdown
    
    def _get_score_description(self, component: str, score: float) -> str:
        """Get description for a component score"""
        descriptions = {
            "code_quality": f"Code quality assessment based on static analysis. Score: {score:.1f}/100",
            "security": f"Security assessment including vulnerability analysis. Score: {score:.1f}/100", 
            "performance": f"Performance evaluation and optimization analysis. Score: {score:.1f}/100",
            "maintainability": f"Code maintainability and readability assessment. Score: {score:.1f}/100",
            "modern_practices": f"Modern development practices adoption. Score: {score:.1f}/100",
            "dependency_management": f"Dependency and package management evaluation. Score: {score:.1f}/100"
        }
        return descriptions.get(component, f"Component score: {score:.1f}/100")
    
    def _identify_improvement_areas(self, component_scores: Dict[str, float]) -> List[str]:
        """Identify areas that need improvement based on component scores"""
        improvement_areas = []
        
        for component, score in component_scores.items():
            if score < 70:  # Scores below 70 need improvement
                component_name = component.replace('_', ' ').title()
                if score < 50:
                    improvement_areas.append(f"{component_name}: Critical - requires immediate attention (score: {score:.1f})")
                elif score < 60:
                    improvement_areas.append(f"{component_name}: Poor - significant improvements needed (score: {score:.1f})")
                else:
                    improvement_areas.append(f"{component_name}: Fair - room for improvement (score: {score:.1f})")
        
        # Sort by score (lowest first)
        improvement_areas.sort(key=lambda x: float(x.split("score: ")[1].split(")")[0]))
        
        return improvement_areas
    
    def _analyze_improvements_implemented(self) -> Dict[str, Any]:
        """Analyze what improvements have been implemented"""
        file_comparisons = self.evaluation_results.get("file_comparisons", [])
        semantic_analysis = self.evaluation_results.get("semantic_analysis", {})
        
        improvements = {
            "categories": {
                "dependency_updates": [],
                "security_fixes": [],
                "performance_improvements": [],
                "code_modernization": [],
                "bug_fixes": [],
                "documentation_improvements": []
            },
            "detailed_improvements": [],
            "improvement_summary": {},
            "impact_analysis": {}
        }
        
        # Analyze file-by-file improvements
        for comparison in file_comparisons:
            file_improvements = self._extract_file_improvements(comparison, semantic_analysis)
            
            for improvement in file_improvements:
                category = improvement["category"]
                if category in improvements["categories"]:
                    improvements["categories"][category].append(improvement)
                
                improvements["detailed_improvements"].append(improvement)
        
        # Generate improvement summary
        improvements["improvement_summary"] = self._generate_improvement_summary(improvements["categories"])
        
        # Analyze impact
        improvements["impact_analysis"] = self._analyze_improvement_impact(improvements["detailed_improvements"])
        
        return improvements
    
    def _extract_file_improvements(self, comparison, semantic_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract improvements from file comparison and semantic analysis"""
        improvements = []
        file_name = Path(comparison.file_path).name
        
        # Get semantic analysis for this file
        file_semantic = semantic_analysis.get(file_name, {})
        analysis_text = str(file_semantic.get("detailed_analysis", "")).lower()
        
        # Check for dependency updates
        if "package.json" in file_name or "package-lock.json" in file_name:
            if any(term in analysis_text for term in ["updated", "upgraded", "modern version"]):
                improvements.append({
                    "file": file_name,
                    "category": "dependency_updates",
                    "description": "Package dependencies updated to modern versions",
                    "impact": "security_and_compatibility",
                    "evidence": "Semantic analysis indicates version upgrades"
                })
        
        # Check for security improvements
        if any(term in analysis_text for term in ["security", "vulnerability", "patch", "cve"]):
            improvements.append({
                "file": file_name,
                "category": "security_fixes",
                "description": "Security vulnerabilities addressed",
                "impact": "security",
                "evidence": "Security-related changes identified in analysis"
            })
        
        # Check for modernization
        if any(term in analysis_text for term in ["es6", "modern", "async/await", "arrow function"]):
            improvements.append({
                "file": file_name,
                "category": "code_modernization",
                "description": "Code modernized with ES6+ features",
                "impact": "maintainability_and_performance",
                "evidence": "Modern JavaScript patterns adopted"
            })
        
        # Check for performance improvements
        if any(term in analysis_text for term in ["performance", "optimization", "efficient", "faster"]):
            improvements.append({
                "file": file_name,
                "category": "performance_improvements",
                "description": "Performance optimizations implemented",
                "impact": "performance",
                "evidence": "Performance improvements noted in analysis"
            })
        
        return improvements
    
    def _generate_improvement_summary(self, categories: Dict[str, List]) -> Dict[str, Any]:
        """Generate summary of improvements by category"""
        summary = {}
        
        for category, improvements in categories.items():
            count = len(improvements)
            summary[category] = {
                "count": count,
                "files_affected": len(set(imp["file"] for imp in improvements)),
                "impact_level": "High" if count > 3 else "Medium" if count > 1 else "Low"
            }
        
        # Calculate overall improvement score
        total_improvements = sum(len(improvements) for improvements in categories.values())
        total_files = len(set(imp["file"] for improvements in categories.values() for imp in improvements))
        
        if total_files > 0:
            improvement_density = total_improvements / total_files
            overall_score = min(100, 60 + (improvement_density * 10))
        else:
            overall_score = 60
        
        summary["overall_improvement_score"] = round(overall_score, 1)
        summary["total_improvements"] = total_improvements
        summary["files_improved"] = total_files
        
        return summary
    
    def _analyze_improvement_impact(self, improvements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the impact of implemented improvements"""
        impact_categories = {
            "security": 0,
            "performance": 0,
            "maintainability": 0,
            "compatibility": 0
        }
        
        for improvement in improvements:
            impact = improvement.get("impact", "")
            
            if "security" in impact:
                impact_categories["security"] += 1
            if "performance" in impact:
                impact_categories["performance"] += 1
            if "maintainability" in impact:
                impact_categories["maintainability"] += 1
            if "compatibility" in impact:
                impact_categories["compatibility"] += 1
        
        # Calculate impact scores
        total_improvements = len(improvements)
        impact_analysis = {}
        
        for category, count in impact_categories.items():
            if total_improvements > 0:
                percentage = (count / total_improvements) * 100
                impact_analysis[category] = {
                    "improvements_count": count,
                    "percentage": round(percentage, 1),
                    "impact_level": "High" if percentage > 30 else "Medium" if percentage > 15 else "Low"
                }
            else:
                impact_analysis[category] = {
                    "improvements_count": 0,
                    "percentage": 0,
                    "impact_level": "None"
                }
        
        return impact_analysis
    
    def _compare_quality_metrics(self, original: Dict[str, Any], modernized: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare quality metrics between original and modernized code
        
        Args:
            original: Original quality metrics
            modernized: Modernized quality metrics
            
        Returns:
            Quality comparison results
        """
        comparison = {
            "improvements": [],
            "regressions": [],
            "metrics_delta": {}
        }
        
        try:
            # Compare key metrics if available
            metrics_to_compare = [
                "total_code_smells",
                "maintainability_index", 
                "cyclomatic_complexity",
                "technical_debt_hours"
            ]
            
            for metric in metrics_to_compare:
                orig_val = self._extract_metric_value(original, metric)
                mod_val = self._extract_metric_value(modernized, metric)
                
                if orig_val is not None and mod_val is not None:
                    delta = mod_val - orig_val
                    comparison["metrics_delta"][metric] = {
                        "original": orig_val,
                        "modernized": mod_val,
                        "delta": delta,
                        "improvement": delta < 0 if metric in ["total_code_smells", "technical_debt_hours"] else delta > 0
                    }
        
        except Exception as e:
            logger.warning(f"Quality metrics comparison failed: {e}")
        
        return comparison
    
    def _extract_metric_value(self, quality_data: Dict[str, Any], metric: str) -> Optional[float]:
        """
        Extract a specific metric value from quality analysis data
        
        Args:
            quality_data: Quality analysis results
            metric: Metric name to extract
            
        Returns:
            Metric value or None if not found
        """
        if "error" in quality_data:
            return None
        
        # Try different paths where the metric might be located
        paths = [
            [metric],
            ["quality_scores", metric],
            ["complexity_summary", metric],
            ["maintainability_assessment", metric],
            ["technical_debt", metric]
        ]
        
        for path in paths:
            try:
                value = quality_data
                for key in path:
                    value = value[key]
                return float(value)
            except (KeyError, TypeError, ValueError):
                continue
        
        return None
    
    def _generate_overall_semantic_assessment(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate overall assessment from individual file analyses
        
        Args:
            file_analyses: List of individual file analysis results
            
        Returns:
            Overall semantic assessment
        """
        assessment = {
            "total_files": len(file_analyses),
            "functional_equivalence": "UNKNOWN",
            "runtime_viability": "UNKNOWN",
            "overall_recommendation": "UNKNOWN",
            "confidence_score": 0,
            "critical_issues_count": 0,
            "files_with_issues": 0
        }
        
        if not file_analyses:
            return assessment
        
        # Aggregate results
        equivalence_scores = []
        viability_scores = []
        confidence_scores = []
        critical_issues = 0
        files_with_issues = 0
        
        for file_analysis in file_analyses:
            analysis = file_analysis.get("analysis", {})
            
            # Map text values to scores
            equiv = analysis.get("functional_equivalence", "UNKNOWN")
            viab = analysis.get("runtime_viability", "UNKNOWN")
            
            equiv_score = {"PASS": 100, "WARNING": 50, "FAIL": 0}.get(equiv, 25)
            viab_score = {"PASS": 100, "WARNING": 50, "FAIL": 0}.get(viab, 25)
            
            equivalence_scores.append(equiv_score)
            viability_scores.append(viab_score)
            
            conf = analysis.get("confidence_score", 0)
            if isinstance(conf, (int, float)):
                confidence_scores.append(conf)
            
            # Count issues
            file_issues = len(analysis.get("critical_issues", []))
            critical_issues += file_issues
            if file_issues > 0:
                files_with_issues += 1
        
        # Calculate averages
        avg_equiv = sum(equivalence_scores) / len(equivalence_scores) if equivalence_scores else 0
        avg_viab = sum(viability_scores) / len(viability_scores) if viability_scores else 0
        avg_conf = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        # Determine overall status
        assessment["functional_equivalence"] = "PASS" if avg_equiv >= 80 else "WARNING" if avg_equiv >= 50 else "FAIL"
        assessment["runtime_viability"] = "PASS" if avg_viab >= 80 else "WARNING" if avg_viab >= 50 else "FAIL"
        assessment["confidence_score"] = round(avg_conf)
        assessment["critical_issues_count"] = critical_issues
        assessment["files_with_issues"] = files_with_issues
        
        # Overall recommendation
        if critical_issues == 0 and avg_equiv >= 80 and avg_viab >= 80:
            assessment["overall_recommendation"] = "APPROVE"
        elif critical_issues <= 2 and avg_equiv >= 50 and avg_viab >= 50:
            assessment["overall_recommendation"] = "NEEDS_FIXES"
        else:
            assessment["overall_recommendation"] = "REJECT"
        
        return assessment
    
    def _generate_summary_and_recommendations(self):
        """
        Generate evaluation summary and recommendations with enhanced logic
        """
        summary = {
            "overall_quality_score": 0,
            "functional_equivalence_status": "UNKNOWN",
            "critical_issues_count": 0,
            "recommendation": "UNKNOWN",
            "key_findings": [],
            "priority_actions": []
        }
        
        # Calculate overall quality score
        quality_comparison = self.evaluation_results.get("quality_analysis", {}).get("comparison", {})
        semantic_assessment = self.evaluation_results.get("semantic_analysis", {}).get("overall_assessment", {})
        runtime_validation = self.evaluation_results.get("runtime_validation", {})
        
        # Enhanced quality score with AI analysis emphasis (0-100)
        quality_factors = []
        
        # Factor 1: AI Semantic Analysis (50% - significantly increased AI analysis weight)
        equiv_score = {"PASS": 100, "WARNING": 70, "FAIL": 0}.get(
            semantic_assessment.get("functional_equivalence", "UNKNOWN"), 25)
        
        # AI confidence adjustment - high confidence AI analysis is more trustworthy
        confidence = semantic_assessment.get("confidence_score", 50)
        if confidence >= 85:
            equiv_score = min(100, equiv_score * 1.1)  # High confidence bonus
        
        quality_factors.append((equiv_score, 0.5))
        
        # Factor 2: Runtime viability (25%)
        runtime_score = {"PASS": 100, "WARNING": 75, "FAIL": 20}.get(
            runtime_validation.get("overall_status", "UNKNOWN"), 25)
        quality_factors.append((runtime_score, 0.25))
        
        # Factor 3: Static Quality improvements (25% - reduced weight for traditional metrics)
        if quality_comparison.get("metrics_delta"):
            improvements = sum(1 for delta in quality_comparison["metrics_delta"].values() 
                             if delta.get("improvement", False))
            total_metrics = len(quality_comparison["metrics_delta"])
            improvement_score = (improvements / total_metrics * 100) if total_metrics > 0 else 50
        else:
            improvement_score = 50  # Default medium score
        quality_factors.append((improvement_score, 0.25))
        
        if quality_factors:
            summary["overall_quality_score"] = round(
                sum(score * weight for score, weight in quality_factors)
            )
        
        # Functional equivalence
        summary["functional_equivalence_status"] = semantic_assessment.get("functional_equivalence", "UNKNOWN")
        
        # Critical issues
        summary["critical_issues_count"] = semantic_assessment.get("critical_issues_count", 0)
        
        # Enhanced recommendation logic prioritizing functional correctness
        critical_count = summary["critical_issues_count"]
        quality_score = summary["overall_quality_score"]
        functional_equiv = summary["functional_equivalence_status"]
        
        # Decision matrix: Functional equivalence is most important
        if critical_count == 0 and functional_equiv == "PASS":
            # No critical issues + functional correctness = good modernization
            if quality_score >= 80:
                summary["recommendation"] = "Ready for Production"
            elif quality_score >= 70:
                summary["recommendation"] = "Good - Minor Improvements Possible"
            elif quality_score >= 50:
                summary["recommendation"] = "Functional but Needs Quality Improvements"
            else:
                summary["recommendation"] = "Needs Fixes"
        elif critical_count <= 2 and functional_equiv in ["PASS", "WARNING"]:
            summary["recommendation"] = "Needs Fixes"
        else:
            summary["recommendation"] = "Major Issues"
        
        # Generate key findings and priority actions
        summary["key_findings"] = self._generate_key_findings()
        summary["priority_actions"] = self._generate_priority_actions()
        
        self.evaluation_results["summary"] = summary
    
    def _generate_key_findings(self) -> List[str]:
        """
        Generate key findings from the evaluation
        
        Returns:
            List of key findings
        """
        findings = []
        
        # Quality analysis findings
        quality_comparison = self.evaluation_results.get("quality_analysis", {}).get("comparison", {})
        for metric, delta in quality_comparison.get("metrics_delta", {}).items():
            if delta.get("improvement"):
                findings.append(f"✓ Improved {metric}: {delta['delta']:+.1f}")
            elif abs(delta["delta"]) > 0.1:  # Significant change
                findings.append(f"⚠ {metric} changed by {delta['delta']:+.1f}")
        
        # Semantic analysis findings
        semantic_assessment = self.evaluation_results.get("semantic_analysis", {}).get("overall_assessment", {})
        if semantic_assessment.get("files_with_issues", 0) > 0:
            findings.append(f"⚠ {semantic_assessment['files_with_issues']} files have semantic issues")
        
        # Runtime validation findings
        runtime_validation = self.evaluation_results.get("runtime_validation", {})
        syntax_validation = runtime_validation.get("syntax_validation", {})
        if syntax_validation.get("syntax_errors"):
            findings.append(f"❌ {len(syntax_validation['syntax_errors'])} files have syntax errors")
        
        # Comprehensive scoring findings
        if self.config.include_comprehensive_scoring:
            scoring = self.evaluation_results.get("scoring", {})
            component_scores = scoring.get("component_scores", {})
            excellent_areas = [area for area, score in component_scores.items() if score >= 90]
            if excellent_areas:
                findings.append(f"⭐ Excellent scores in: {', '.join(excellent_areas)}")
        
        return findings[:10]  # Limit to top 10 findings
    
    def _generate_priority_actions(self) -> List[str]:
        """
        Generate priority actions based on evaluation results
        
        Returns:
            List of priority actions
        """
        actions = []
        
        # Critical issues first
        semantic_assessment = self.evaluation_results.get("semantic_analysis", {}).get("overall_assessment", {})
        if semantic_assessment.get("critical_issues_count", 0) > 0:
            actions.append("Fix critical semantic issues identified in file analysis")
        
        # Syntax errors
        runtime_validation = self.evaluation_results.get("runtime_validation", {})
        syntax_validation = runtime_validation.get("syntax_validation", {})
        if syntax_validation.get("syntax_errors"):
            actions.append("Resolve syntax errors in modernized files")
        
        # Functional equivalence issues
        if semantic_assessment.get("functional_equivalence") in ["FAIL", "WARNING"]:
            actions.append("Verify and fix functional equivalence issues")
        
        # Runtime viability issues
        if runtime_validation.get("overall_status") in ["FAIL", "WARNING"]:
            actions.append("Address runtime validation issues")
        
        # Component score improvements
        if self.config.include_comprehensive_scoring:
            scoring = self.evaluation_results.get("scoring", {})
            improvement_areas = scoring.get("improvement_areas", [])
            for area in improvement_areas[:2]:  # Top 2 improvement areas
                actions.append(f"Improve {area}")
        
        return actions[:5]  # Limit to top 5 actions
    
    def _generate_markdown_report(self):
        """
        Generate comprehensive Markdown report
        """
        try:
            report_content = self._build_markdown_content()
            
            with open(self.config.output_report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self._print_status(f"Markdown report saved to: {self.config.output_report_path}", "success")
        
        except Exception as e:
            logger.error(f"Failed to generate Markdown report: {e}")
    
    def _build_markdown_content(self) -> str:
        """
        Build the complete Markdown report content with all advanced features
        
        Returns:
            Complete Markdown report as string
        """
        summary = self.evaluation_results.get("summary", {})
        metadata = self.evaluation_results.get("metadata", {})
        
        content = f"""# Final Code Evaluation Report

**Generated:** {metadata.get('timestamp', 'Unknown')}  
**Version:** {metadata.get('version', '2.0-final')}  
**Original Path:** `{metadata.get('original_path', 'Unknown')}`  
**Modernized Path:** `{metadata.get('modernized_path', 'Unknown')}`

## Executive Summary

| Metric | Value |
|--------|-------|
| **Overall Quality Score** | {summary.get('overall_quality_score', 0)}/100 |"""
        
        # Add comprehensive scoring if enabled
        if self.config.include_comprehensive_scoring:
            content += f"""
| **Comprehensive Score** | {summary.get('comprehensive_score', 0)}/100 |
| **Improvement Score** | {summary.get('improvement_score', 0)}/100 |"""
        
        content += f"""
| **Functional Equivalence** | {summary.get('functional_equivalence_status', 'Unknown')} |
| **Critical Issues** | {summary.get('critical_issues_count', 0)} |
| **Recommendation** | {summary.get('recommendation', 'Unknown')} |

### Key Findings

{self._format_findings_as_markdown(summary.get('key_findings', []))}

### Priority Actions

{self._format_actions_as_markdown(summary.get('priority_actions', []))}
"""
        
        # Add comprehensive scoring sections if enabled
        if self.config.include_comprehensive_scoring:
            content += f"""
## Comprehensive Scoring

{self._build_comprehensive_scoring_section()}

## Improvements Implemented

{self._build_improvements_section()}
"""
        
        content += f"""
## Quality Metrics Comparison

{self._build_quality_metrics_table()}

## Functional Equivalence Analysis

{self._build_semantic_analysis_section()}

## Runtime Validation

{self._build_runtime_validation_section()}

## Detailed File Analysis

{self._build_file_analysis_section()}

## Recommendations

{self._build_recommendations_section()}

---

*Report generated by Final Code Evaluation Program v{metadata.get('version', '2.0-final')}*
"""
        return content
    
    def _build_comprehensive_scoring_section(self) -> str:
        """Build comprehensive scoring section"""
        scoring = self.evaluation_results.get("scoring", {})
        
        if not scoring:
            return "*Comprehensive scoring not available.*"
        
        overall_score = scoring.get("overall_score", 0)
        component_scores = scoring.get("component_scores", {})
        improvement_areas = scoring.get("improvement_areas", [])
        
        section = f"""
**Overall Score:** {overall_score}/100

### Component Scores

| Component | Score | Grade |
|-----------|-------|-------|"""
        
        for component, score in component_scores.items():
            grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
            component_name = component.replace('_', ' ').title()
            section += f"\n| {component_name} | {score:.1f}/100 | {grade} |"
        
        if improvement_areas:
            section += "\n\n### Areas for Improvement\n"
            for area in improvement_areas[:5]:  # Show top 5
                section += f"- {area}\n"
        
        return section
    
    def _build_improvements_section(self) -> str:
        """Build improvements implemented section"""
        improvements = self.evaluation_results.get("improvements_implemented", {})
        
        if not improvements:
            return "*Improvement tracking not available.*"
        
        categories = improvements.get("categories", {})
        improvement_summary = improvements.get("improvement_summary", {})
        impact_analysis = improvements.get("impact_analysis", {})
        
        section = f"""
### Improvement Summary

- **Total Improvements:** {improvement_summary.get('total_improvements', 0)}
- **Files Improved:** {improvement_summary.get('files_improved', 0)}
- **Overall Improvement Score:** {improvement_summary.get('overall_improvement_score', 0)}/100

### Improvements by Category

| Category | Count | Files Affected | Impact Level |
|----------|-------|----------------|--------------|"""
        
        for category, data in categories.items():
            if data:  # Only show categories with improvements
                category_name = category.replace('_', ' ').title()
                count = data.get('count', 0) if isinstance(data, dict) else len(data)
                files_affected = data.get('files_affected', 0) if isinstance(data, dict) else len(set(imp.get("file", "") for imp in data))
                impact_level = data.get('impact_level', 'Unknown') if isinstance(data, dict) else 'Medium'
                section += f"\n| {category_name} | {count} | {files_affected} | {impact_level} |"
        
        # Add impact analysis
        if impact_analysis:
            section += "\n\n### Impact Analysis\n\n"
            for impact_type, data in impact_analysis.items():
                if isinstance(data, dict) and data.get('improvements_count', 0) > 0:
                    impact_name = impact_type.replace('_', ' ').title()
                    count = data.get('improvements_count', 0)
                    percentage = data.get('percentage', 0)
                    section += f"- **{impact_name}:** {count} improvements ({percentage:.1f}% of total)\n"
        
        return section
    
    def _format_findings_as_markdown(self, findings: List[str]) -> str:
        """Format findings as Markdown list"""
        if not findings:
            return "*No significant findings identified.*"
        return "\n".join(f"- {finding}" for finding in findings)
    
    def _format_actions_as_markdown(self, actions: List[str]) -> str:
        """Format actions as Markdown list"""
        if not actions:
            return "*No priority actions required.*"
        return "\n".join(f"{i+1}. {action}" for i, action in enumerate(actions))
    
    def _build_quality_metrics_table(self) -> str:
        """Build quality metrics comparison table"""
        quality_comparison = self.evaluation_results.get("quality_analysis", {}).get("comparison", {})
        metrics_delta = quality_comparison.get("metrics_delta", {})
        
        if not metrics_delta:
            return "*Quality metrics comparison not available.*"
        
        table = "| Metric | Original | Modernized | Delta | Status |\n"
        table += "|--------|----------|------------|-------|--------|\n"
        
        for metric, delta in metrics_delta.items():
            status = "✓ Improved" if delta.get("improvement", False) else "⚠ Changed"
            table += f"| {metric.replace('_', ' ').title()} | {delta['original']:.2f} | {delta['modernized']:.2f} | {delta['delta']:+.2f} | {status} |\n"
        
        return table
    
    def _build_semantic_analysis_section(self) -> str:
        """Build semantic analysis section"""
        semantic_analysis = self.evaluation_results.get("semantic_analysis", {})
        overall_assessment = semantic_analysis.get("overall_assessment", {})
        
        if not overall_assessment:
            return "*Semantic analysis not available.*"
        
        section = f"""
**Overall Assessment:**
- Functional Equivalence: {overall_assessment.get('functional_equivalence', 'Unknown')}
- Runtime Viability: {overall_assessment.get('runtime_viability', 'Unknown')}
- Confidence Score: {overall_assessment.get('confidence_score', 0)}/100
- Files with Issues: {overall_assessment.get('files_with_issues', 0)}/{overall_assessment.get('total_files', 0)}
- Critical Issues: {overall_assessment.get('critical_issues_count', 0)}
"""
        
        # Add file-specific issues if any
        file_analyses = semantic_analysis.get("file_analyses", [])
        files_with_critical_issues = [
            fa for fa in file_analyses 
            if fa.get("analysis", {}).get("critical_issues", [])
        ]
        
        if files_with_critical_issues:
            section += "\n**Files with Critical Issues:**\n"
            for file_analysis in files_with_critical_issues[:5]:  # Limit to first 5
                file_path = file_analysis.get("modernized_file", "Unknown")
                issues = file_analysis.get("analysis", {}).get("critical_issues", [])
                section += f"\n- `{Path(file_path).name}`: {len(issues)} critical issues\n"
                for issue in issues[:3]:  # Show first 3 issues
                    section += f"  - {issue}\n"
        
        return section
    
    def _build_runtime_validation_section(self) -> str:
        """Build enhanced runtime validation section with executability analysis"""
        runtime_validation = self.evaluation_results.get("runtime_validation", {})
        semantic_analysis = self.evaluation_results.get("semantic_analysis", {})
        
        section = f"**Overall Status:** {runtime_validation.get('overall_status', 'Unknown')}\n\n"

        # AI Executability Analysis - NEW ENHANCED SECTION
        if semantic_analysis.get("file_analyses"):
            section += "**🚀 AI Code Executability Analysis:**\n\n"
            
            executable_files = 0
            total_analyzed = 0
            execution_blockers = []
            high_confidence_files = 0
            
            for file_analysis in semantic_analysis["file_analyses"]:
                analysis = file_analysis.get("analysis", {})
                if analysis:
                    total_analyzed += 1
                    can_execute = analysis.get("can_execute", "UNCERTAIN")
                    execution_confidence = analysis.get("execution_confidence", 0)
                    will_execute = analysis.get("will_execute_successfully", "UNCERTAIN")
                    
                    # Count executable files
                    if can_execute == "YES" and execution_confidence >= 70:
                        executable_files += 1
                    
                    # Count high confidence files
                    if execution_confidence >= 90:
                        high_confidence_files += 1
                    
                    # Collect critical execution blockers
                    file_blockers = analysis.get("execution_blockers", [])
                    for blocker in file_blockers:
                        if isinstance(blocker, dict) and blocker.get("severity") in ["CRITICAL", "HIGH"]:
                            execution_blockers.append({
                                "file": Path(file_analysis.get("modernized_file", "unknown")).name,
                                "blocker": blocker
                            })
            
            # Overall executability assessment
            if total_analyzed > 0:
                executability_rate = (executable_files / total_analyzed) * 100
                section += f"- **📊 Code Executability Rate:** {executability_rate:.1f}% ({executable_files}/{total_analyzed} files can execute)\n"
                section += f"- **🎯 High Confidence Files:** {high_confidence_files}/{total_analyzed} files (90%+ execution confidence)\n"
                
                # Clear executability status
                if executability_rate >= 90:
                    section += f"- **✅ EXECUTABILITY STATUS: READY TO RUN**\n"
                    section += f"  - High confidence the modernized code will execute successfully\n"
                    section += f"  - Minimal execution issues expected\n"
                elif executability_rate >= 70:
                    section += f"- **⚠️ EXECUTABILITY STATUS: LIKELY RUNNABLE**\n"
                    section += f"  - Most code should execute with minor issues\n"
                    section += f"  - Some fixes may be needed for full functionality\n"
                elif executability_rate >= 50:
                    section += f"- **❓ EXECUTABILITY STATUS: UNCERTAIN**\n"
                    section += f"  - Significant execution issues possible\n"
                    section += f"  - Manual testing and fixes likely required\n"
                else:
                    section += f"- **❌ EXECUTABILITY STATUS: EXECUTION PROBLEMS**\n"
                    section += f"  - Code likely to fail without fixes\n"
                    section += f"  - Major intervention required before running\n"
            
            # Critical execution blockers
            if execution_blockers:
                section += f"\n**🚨 Critical Execution Blockers ({len(execution_blockers)}):**\n"
                for i, blocker_info in enumerate(execution_blockers[:5]):  # Show top 5
                    blocker = blocker_info["blocker"]
                    section += f"{i+1}. **{blocker_info['file']}** - {blocker.get('blocker_type', 'UNKNOWN')}\n"
                    section += f"   - Issue: {blocker.get('description', 'No description')}\n"
                    section += f"   - Fix: {blocker.get('fix_required', 'Not specified')}\n"
                if len(execution_blockers) > 5:
                    section += f"   ... and {len(execution_blockers) - 5} more blockers\n"
            else:
                section += f"\n**✅ No Critical Execution Blockers Detected**\n"
            
            section += "\n"

        # Package validation
        package_validation = runtime_validation.get("package_validation", {})
        if package_validation:
            section += f"**Package Validation:**\n"
            section += f"- Valid JSON: {package_validation.get('valid_json', 'Unknown')}\n"
            section += f"- Package Count: {package_validation.get('package_count', 'Unknown')}\n\n"

        # Syntax validation
        syntax_validation = runtime_validation.get("syntax_validation", {})
        if syntax_validation:
            section += f"**Syntax Validation:**\n"
            section += f"- Total Files: {syntax_validation.get('total_files', 0)}\n"
            section += f"- Valid Files: {syntax_validation.get('valid_files', 0)}\n"
            
            syntax_errors = syntax_validation.get("syntax_errors", [])
            if syntax_errors:
                section += f"- Syntax Errors: {len(syntax_errors)}\n\n"
                section += "**Files with Syntax Errors:**\n"
                for error in syntax_errors[:5]:  # Show first 5 errors
                    section += f"- `{Path(error['file']).name}`: {error['error']}\n"
            else:
                section += "- Syntax Errors: 0\n"
        
        return section
    
    def _build_file_analysis_section(self) -> str:
        """Build detailed file analysis section"""
        file_comparisons = self.evaluation_results.get("file_comparisons", [])
        
        if not file_comparisons:
            return "*No file comparisons available.*"
        
        section = "| File | Size Change | Line Change | Issues | Status |\n"
        section += "|------|-------------|-------------|--------|--------|\n"
        
        for comparison in file_comparisons[:20]:  # Limit to first 20 files
            file_name = Path(comparison.file_path).name
            size_change = f"{comparison.size_change:+.1f}%" if comparison.size_change != 0 else "0%"
            line_change = f"{comparison.line_count_change:+d}" if comparison.line_count_change != 0 else "0"
            issues_count = len(comparison.issues)
            status = "❌" if any(issue["severity"] == "critical" for issue in comparison.issues) else "✓"
            
            section += f"| `{file_name}` | {size_change} | {line_change} | {issues_count} | {status} |\n"
        
        return section
    
    def _build_recommendations_section(self) -> str:
        """Build recommendations section"""
        recommendations = self.evaluation_results.get("recommendations", [])
        
        if not recommendations:
            recommendations = [
                "Continue monitoring code quality metrics",
                "Implement automated testing for modernized code",
                "Set up continuous integration for quality checks",
                "Regular security audits of dependencies"
            ]
        
        section = ""
        for i, rec in enumerate(recommendations, 1):
            section += f"{i}. {rec}\n"
        
        return section
    
    def _generate_json_report(self):
        """
        Generate JSON report for CI/CD integration
        """
        try:
            with open(self.config.output_json_path, 'w', encoding='utf-8') as f:
                json.dump(self.evaluation_results, f, indent=2, default=str)
            
            self._print_status(f"JSON report saved to: {self.config.output_json_path}", "success")
        
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {e}")
    
    def _print_header(self):
        """Print program header"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Style.BRIGHT}Final Code Evaluation Program v2.0{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}Configuration:{Style.RESET_ALL}")
        print(f"  Original Path:       {self.config.original_path}")
        print(f"  Modernized Path:     {self.config.modernized_path}")
        print(f"  Report Output:       {self.config.output_report_path}")
        print(f"  JSON Output:         {self.config.output_json_path}")
        print(f"  AI Analysis:         {'Enabled' if self.config.include_ai_analysis else 'Disabled'}")
        print(f"  Comprehensive Score: {'Enabled' if self.config.include_comprehensive_scoring else 'Disabled'}")
        print(f"  Max File Size (AI):  {self.config.max_file_size_for_ai} characters")
        print()
    
    def _print_section_header(self, title: str):
        """Print section header"""
        print(f"\n{Fore.BLUE}{Style.BRIGHT}{'='*60}")
        print(f"{title}")
        print(f"{'='*60}{Style.RESET_ALL}")
    
    def _print_status(self, message: str, status: str = "info"):
        """Print colored status message"""
        if status == "success":
            print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
        elif status == "warning":
            print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
        elif status == "error":
            print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")
    
    def _print_completion_summary(self):
        """Print enhanced completion summary with visual elements"""
        summary = self.evaluation_results.get("summary", {})
        quality_comparison = self.evaluation_results.get("quality_analysis", {}).get("comparison", {})
        semantic_assessment = self.evaluation_results.get("semantic_analysis", {}).get("overall_assessment", {})
        runtime_validation = self.evaluation_results.get("runtime_validation", {})
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*80}")
        print("EVALUATION COMPLETE")
        print(f"{'='*80}{Style.RESET_ALL}\n")
        
        # Calculate detailed scores for visual display
        quality_factors = self._calculate_detailed_scores(quality_comparison, semantic_assessment, runtime_validation)
        
        # Overall Score with visual bar
        overall_score = summary.get('overall_quality_score', 0)
        print(f"{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}OVERALL QUALITY SCORE:{Style.RESET_ALL} {self._get_score_color(overall_score)}{overall_score}/100{Style.RESET_ALL}")
        print(self._create_progress_bar(overall_score, 100, width=60))
        print(f"{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
        
        # Score Breakdown
        print(f"{Style.BRIGHT}📊 SCORE BREAKDOWN:{Style.RESET_ALL}\n")
        
        for component, score_info in quality_factors.items():
            score = score_info['score']
            weight = score_info['weight']
            weighted_contribution = score * weight / 100
            
            print(f"  {Style.BRIGHT}{component}:{Style.RESET_ALL}")
            print(f"    Raw Score:      {self._get_score_color(score)}{score:.1f}/100{Style.RESET_ALL}")
            print(f"    Weight:         {weight*100:.0f}%")
            print(f"    Contribution:   {self._get_score_color(weighted_contribution*100)}{weighted_contribution*100:.1f}/100{Style.RESET_ALL}")
            print(f"    {self._create_progress_bar(score, 100, width=50)}")
            print()
        
        # Comprehensive scoring summary if enabled
        if self.config.include_comprehensive_scoring:
            scoring = self.evaluation_results.get("scoring", {})
            comprehensive_score = scoring.get("overall_score", 0)
            improvement_score = summary.get("improvement_score", 0)
            
            print(f"{Style.BRIGHT}🎯 COMPREHENSIVE ANALYSIS:{Style.RESET_ALL}")
            print(f"  Comprehensive Score: {self._get_score_color(comprehensive_score)}{comprehensive_score}/100{Style.RESET_ALL}")
            print(f"  Improvement Score:   {self._get_score_color(improvement_score)}{improvement_score}/100{Style.RESET_ALL}")
            print()
        
        # Status Indicators
        print(f"{Style.BRIGHT}📋 STATUS INDICATORS:{Style.RESET_ALL}\n")
        
        equiv_status = summary.get('functional_equivalence_status', 'Unknown')
        equiv_color = self._get_status_color(equiv_status)
        print(f"  Functional Equivalence:  {equiv_color}{equiv_status}{Style.RESET_ALL}")
        
        critical_count = summary.get('critical_issues_count', 0)
        critical_color = Fore.GREEN if critical_count == 0 else Fore.RED
        print(f"  Critical Issues:         {critical_color}{critical_count}{Style.RESET_ALL}")
        
        runtime_status = runtime_validation.get("overall_status", "UNKNOWN")
        runtime_color = self._get_status_color(runtime_status)
        
        # Enhanced executability display
        semantic_analysis = self.evaluation_results.get("semantic_analysis", {})
        if semantic_analysis.get("file_analyses"):
            executable_files = 0
            total_analyzed = 0
            for file_analysis in semantic_analysis["file_analyses"]:
                analysis = file_analysis.get("analysis", {})
                if analysis:
                    total_analyzed += 1
                    can_execute = analysis.get("can_execute", "UNCERTAIN")
                    execution_confidence = analysis.get("execution_confidence", 0)
                    if can_execute == "YES" and execution_confidence >= 70:
                        executable_files += 1
            
            if total_analyzed > 0:
                executability_rate = (executable_files / total_analyzed) * 100
                if executability_rate >= 90:
                    exec_status = "✅ READY TO RUN"
                    exec_color = Fore.GREEN
                elif executability_rate >= 70:
                    exec_status = "⚠️ LIKELY RUNNABLE"
                    exec_color = Fore.YELLOW
                elif executability_rate >= 50:
                    exec_status = "❓ UNCERTAIN"
                    exec_color = Fore.YELLOW
                else:
                    exec_status = "❌ EXECUTION PROBLEMS"
                    exec_color = Fore.RED
                
                print(f"  Runtime Validation:      {runtime_color}{runtime_status}{Style.RESET_ALL}")
                print(f"  Code Executability:      {exec_color}{exec_status} ({executability_rate:.1f}%){Style.RESET_ALL}")
            else:
                print(f"  Runtime Validation:      {runtime_color}{runtime_status}{Style.RESET_ALL}")
        else:
            print(f"  Runtime Validation:      {runtime_color}{runtime_status}{Style.RESET_ALL}")
        
        # File Statistics
        print(f"\n{Style.BRIGHT}📁 FILE STATISTICS:{Style.RESET_ALL}\n")
        file_comparisons = self.evaluation_results.get("file_comparisons", [])
        print(f"  Files Analyzed:          {len(file_comparisons)}")
        print(f"  Files with Issues:       {semantic_assessment.get('files_with_issues', 0)}")
        if self.config.include_ai_analysis:
            print(f"  AI Analysis Coverage:    {len(self.evaluation_results.get('semantic_analysis', {}).get('file_analyses', []))} files")
        
        # Key Findings
        if summary.get('key_findings'):
            print(f"\n{Style.BRIGHT}🔍 KEY FINDINGS:{Style.RESET_ALL}\n")
            for finding in summary['key_findings'][:5]:
                print(f"  {finding}")
        
        # Priority Actions
        if summary.get('priority_actions'):
            print(f"\n{Style.BRIGHT}⚡ PRIORITY ACTIONS:{Style.RESET_ALL}\n")
            for i, action in enumerate(summary['priority_actions'][:5], 1):
                print(f"  {i}. {action}")
        
        # Final Recommendation
        print(f"\n{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        rec = summary.get('recommendation', 'Unknown')
        rec_color = self._get_recommendation_color(rec)
        rec_icon = self._get_recommendation_icon(rec)
        print(f"{Style.BRIGHT}FINAL RECOMMENDATION:{Style.RESET_ALL} {rec_color}{rec_icon} {rec}{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
        
        # Reports Generated
        print(f"{Style.BRIGHT}📄 REPORTS GENERATED:{Style.RESET_ALL}")
        print(f"  Markdown: {Fore.CYAN}{self.config.output_report_path}{Style.RESET_ALL}")
        print(f"  JSON:     {Fore.CYAN}{self.config.output_json_path}{Style.RESET_ALL}")
        print()
    
    def _calculate_detailed_scores(self, quality_comparison, semantic_assessment, runtime_validation):
        """Calculate detailed scores for each component"""
        scores = {}
        
        # Factor 1: Quality Improvements (30%)
        if quality_comparison.get("metrics_delta"):
            improvements = sum(1 for delta in quality_comparison["metrics_delta"].values() 
                             if delta.get("improvement", False))
            total_metrics = len(quality_comparison["metrics_delta"])
            quality_score = (improvements / total_metrics * 100) if total_metrics > 0 else 0
        else:
            quality_score = 0
        
        scores["Quality Improvements"] = {
            'score': quality_score,
            'weight': 0.3,
            'status': 'GOOD' if quality_score >= 70 else 'FAIR' if quality_score >= 40 else 'POOR'
        }
        
        # Factor 2: Semantic Equivalence (40%)
        equiv_status = semantic_assessment.get("functional_equivalence", "UNKNOWN")
        equiv_score = {"PASS": 100, "WARNING": 50, "FAIL": 0}.get(equiv_status, 25)
        
        scores["Semantic Equivalence"] = {
            'score': equiv_score,
            'weight': 0.4,
            'status': equiv_status
        }
        
        # Factor 3: Runtime Viability (30%)
        runtime_status = runtime_validation.get("overall_status", "UNKNOWN")
        runtime_score = {"PASS": 100, "WARNING": 50, "FAIL": 0}.get(runtime_status, 25)
        
        scores["Runtime Viability"] = {
            'score': runtime_score,
            'weight': 0.3,
            'status': runtime_status
        }
        
        return scores
    
    def _create_progress_bar(self, value, max_value, width=50):
        """Create a colored progress bar"""
        percentage = (value / max_value) * 100 if max_value > 0 else 0
        filled_width = int((value / max_value) * width) if max_value > 0 else 0
        
        # Determine color based on percentage
        if percentage >= 80:
            bar_color = Fore.GREEN
        elif percentage >= 60:
            bar_color = Fore.YELLOW
        elif percentage >= 40:
            bar_color = Fore.LIGHTYELLOW_EX
        else:
            bar_color = Fore.RED
        
        filled = "█" * filled_width
        empty = "░" * (width - filled_width)
        
        return f"    [{bar_color}{filled}{Fore.WHITE}{empty}{Style.RESET_ALL}] {percentage:.1f}%"
    
    def _get_score_color(self, score):
        """Get color for score based on value"""
        if score >= 80:
            return Fore.GREEN + Style.BRIGHT
        elif score >= 60:
            return Fore.YELLOW + Style.BRIGHT
        elif score >= 40:
            return Fore.LIGHTYELLOW_EX
        else:
            return Fore.RED + Style.BRIGHT
    
    def _get_status_color(self, status):
        """Get color for status"""
        if status in ["PASS", "GOOD"]:
            return Fore.GREEN + Style.BRIGHT
        elif status in ["WARNING", "FAIR"]:
            return Fore.YELLOW + Style.BRIGHT
        elif status in ["FAIL", "POOR"]:
            return Fore.RED + Style.BRIGHT
        else:
            return Fore.WHITE
    
    def _get_recommendation_color(self, recommendation):
        """Get color for recommendation"""
        if recommendation == "Ready for Production":
            return Fore.GREEN + Style.BRIGHT
        elif recommendation in ["Good - Minor Improvements Possible", "Functional but Needs Quality Improvements"]:
            return Fore.YELLOW + Style.BRIGHT
        elif recommendation == "Needs Fixes":
            return Fore.LIGHTYELLOW_EX + Style.BRIGHT
        else:
            return Fore.RED + Style.BRIGHT
    
    def _get_recommendation_icon(self, recommendation):
        """Get icon for recommendation"""
        if recommendation == "Ready for Production":
            return "✅"
        elif recommendation in ["Good - Minor Improvements Possible", "Functional but Needs Quality Improvements"]:
            return "⚠️"
        elif recommendation == "Needs Fixes":
            return "🔧"
        else:
            return "❌"


def main():
    """
    Main entry point for the final evaluation program
    """
    try:
        # Load configuration with environment variable support
        config = EvaluationConfig(
            original_path=ORIGINAL_CODE_PATH,
            modernized_path=MODERNIZED_CODE_PATH,
            output_report_path=OUTPUT_REPORT_PATH,
            output_json_path=OUTPUT_JSON_PATH,
            parallel_processing=os.getenv("PARALLEL_PROCESSING", "true").lower() == "true",
            max_workers=int(os.getenv("MAX_WORKERS", "4")),
            include_ai_analysis=os.getenv("INCLUDE_AI_ANALYSIS", "true").lower() == "true",
            include_comprehensive_scoring=os.getenv("INCLUDE_COMPREHENSIVE_SCORING", "true").lower() == "true",
            verbose=os.getenv("VERBOSE", "true").lower() == "true",
            max_file_size_for_ai=MAX_FILE_SIZE_FOR_AI
        )
        
        # Create and run evaluation
        evaluator = FinalCodeEvaluationProgram(config)
        results = evaluator.run_evaluation()
        
        # Return appropriate exit code based on results
        summary = results.get("summary", {})
        recommendation = summary.get("recommendation", "Unknown")
        
        # Enhanced exit code logic
        if recommendation == "Ready for Production":
            sys.exit(0)
        elif recommendation in ["Good - Minor Improvements Possible", "Functional but Needs Quality Improvements"]:
            sys.exit(0)  # Still acceptable for production
        elif recommendation == "Needs Fixes":
            sys.exit(1)
        else:
            sys.exit(2)  # Major issues
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Evaluation interrupted by user{Style.RESET_ALL}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Fore.RED}Evaluation failed: {e}{Style.RESET_ALL}")
        logger.error(f"Evaluation failed: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()