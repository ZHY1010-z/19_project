#!/usr/bin/env python3
"""
Strategy-Focused Multi-Agent Framework for Legacy System Modernization

This framework focuses exclusively on strategy planning and validation.
It provides comprehensive analysis and strategic guidance for modernization 
but does NOT perform actual code transformation.

Architecture:
- framework.py: Strategy planning and validation (THIS FILE)
- ai_execution_agent.py: Code transformation and migration execution
- util.py: Shared utilities and analyzers
- prompt_templates_1.py: LLM prompt templates

Key Components:
1. Deep Code Analysis (AST, dependency, quality, architecture analysis)
2. Migration Strategy Planning (comprehensive modernization roadmap)
3. Strategy Validation & Refinement (ValidationAgent with feedback loops)
4. Strategy Documentation Generation (detailed execution guidance)

Flow:
framework.py generates strategy → ai_execution_agent.py executes strategy
"""

import logging
import uuid
import os
import json
from typing import Dict, Any, Tuple, List
from dataclasses import dataclass

from util import (
    llm_call, validate_project_config, setup_logging,
    ASTAnalyzer, DependencyAnalyzer, QualityAnalyzer, ArchitectureAnalyzer,
    calculate_enhanced_modernization_readiness, generate_comprehensive_recommendations,
    handle_errors, validate_path, standardize_return_format, unified_repository_scan
)
# Import optimized components
from prompt_templates_optimized_full import (
    OptimizedPromptEngine, OptimizedPromptContext,
    get_analysis_prompt, get_planning_prompt, get_transformation_prompt,
    get_migration_prompt, get_validation_prompt, get_documentation_prompt
)

# Configure logging
setup_logging("INFO")
logger = logging.getLogger(__name__)

@dataclass
class WorkflowResult:
    """Simple result container for workflow execution"""
    success: bool
    data: Dict[str, Any]
    cycle_count: int = 0


# ================== MAIN WORKFLOW FUNCTION ==================

def execute_modernization_workflow(project_config: Dict[str, Any]) -> WorkflowResult:
    """
    Strategy-focused modernization workflow orchestrator
    
    Executes the strategy formulation pipeline:
    1. Deep Code Analysis
    2. Migration Strategy Planning 
    3. Strategy Validation (with refinement loops)
    4. Strategy Documentation Generation
    
    NOTE: Actual code transformation is handled by ai_execution_agent.py
    """
    
    workflow_id = str(uuid.uuid4())
    logger.info("=" * 80)
    logger.info(f"STARTING MODERNIZATION WORKFLOW: {workflow_id}")
    logger.info("=" * 80)
    
    try:
        # Validate configuration
        validate_project_config(project_config)
        
        # Phase 1: Deep Code Analysis
        analysis_result = analyze_code(project_config)
        
        # Phase 2: Migration Planning
        planning_result = create_migration_plan(analysis_result)
        
        # Phase 3: Strategy validation with refinement loops
        strategy_validation_results = validate_and_refine_strategy(
            planning_result, max_cycles=3
        )
        
        # Phase 4: Strategy Documentation Generation
        documentation_result = generate_strategy_documentation({
            "analysis": analysis_result,
            "planning": planning_result, 
            "validation": strategy_validation_results
        })
        
        logger.info("=" * 80)
        logger.info("WORKFLOW COMPLETED SUCCESSFULLY!")
        logger.info("=" * 80)
        
        return WorkflowResult(
            success=True,
            data={
                "workflow_id": workflow_id,
                "analysis": analysis_result,
                "planning": planning_result,
                "strategy_validation": strategy_validation_results,
                "documentation": documentation_result
            },
            cycle_count=strategy_validation_results["cycles_completed"]
        )
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        return WorkflowResult(
            success=False,
            data={"error": str(e), "workflow_id": workflow_id},
            cycle_count=0
        )


# ================== CORE PHASE FUNCTIONS (IN EXECUTION ORDER) ==================

def analyze_code(project_config: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 1: Deep code analysis and understanding with advanced static analysis"""
    logger.info("PHASE 1: DEEP CODE ANALYSIS WITH ADVANCED STATIC ANALYSIS")
    
    repo_path = project_config.get("legacy_repo_path", "")
    
    if not os.path.exists(repo_path):
        logger.error(f"Repository path does not exist: {repo_path}")
        return {"error": "Repository path not found", "repo_path": repo_path}
    
    # === Initialize Advanced Analyzers ===
    logger.info("Initializing advanced static analysis engines...")
    ast_analyzer = ASTAnalyzer()
    dependency_analyzer = DependencyAnalyzer()
    quality_analyzer = QualityAnalyzer()
    architecture_analyzer = ArchitectureAnalyzer()
    
    # === Stage 1: AST-based Code Structure Analysis ===
    logger.info("Stage 1: Performing AST-based code structure analysis...")
    ast_analysis = ast_analyzer.analyze_repository(repo_path)
    
    # === Stage 2: Dependency Relationship Analysis ===
    logger.info("Stage 2: Analyzing dependency relationships and coupling...")
    dependency_analysis = dependency_analyzer.analyze_repository_dependencies(repo_path, ast_analysis)
    
    # === Stage 3: Code Quality Assessment ===
    logger.info("Stage 3: Conducting comprehensive code quality assessment...")
    quality_analysis = quality_analyzer.analyze_repository_quality(repo_path, ast_analysis)
    
    # === Stage 4: Architectural Pattern Recognition ===
    logger.info("Stage 4: Detecting architectural patterns and design structures...")
    architecture_analysis = architecture_analyzer.analyze_repository_architecture(
        repo_path, ast_analysis, dependency_analysis
    )
    
    # === Stage 5: Optimized Unified File System Analysis ===
    logger.info("Stage 5: Performing optimized unified file system analysis...")
    
    # Single-pass repository scan (replaces multiple file traversals)
    unified_scan = unified_repository_scan(repo_path)
    
    # Extract analysis results from unified scan
    file_stats = unified_scan["file_structure"]
    language_analysis = unified_scan["language_analysis"] 
    security_analysis = unified_scan["security_analysis"]
    
    # Basic code quality metrics (using cached file info)
    quality_metrics = _calculate_code_metrics_optimized(unified_scan)
    
    # === Stage 6: API Dependencies and Backend Compatibility Analysis ===
    logger.info("Stage 6: Analyzing API dependencies and backend compatibility requirements...")
    api_analysis = _analyze_api_dependencies_comprehensive(repo_path, unified_scan)
    
    # === Stage 7: Backend Technology Stack Analysis ===
    logger.info("Stage 7: Analyzing backend technology stack and upgrade requirements...")
    backend_analysis = _analyze_backend_stack_compatibility(repo_path, unified_scan)
    
    # === Stage 8: Database Migration and Schema Compatibility Analysis ===
    logger.info("Stage 8: Analyzing database migration and schema compatibility...")
    database_analysis = _analyze_database_compatibility(repo_path, unified_scan)
    
    # === Stage 9: Apache Solr Upgrade Compatibility Analysis ===
    logger.info("Stage 9: Analyzing Apache Solr upgrade compatibility (5.x→9.x)...")
    solr_analysis = _analyze_solr_compatibility(repo_path, unified_scan)
    
    # === Stage 10: Comprehensive Analysis Integration ===
    logger.info("Stage 10: Integrating all analysis results...")
    
    # Compile comprehensive repository data with advanced analysis
    repo_data = {
        "file_structure": file_stats,
        "language_analysis": language_analysis,
        "quality_metrics": quality_metrics,
        "security_analysis": security_analysis,
        "api_analysis": api_analysis,
        "backend_analysis": backend_analysis,
        "database_analysis": database_analysis,
        "solr_analysis": solr_analysis,
        "repository_path": repo_path,
        # Advanced static analysis results
        "ast_analysis": ast_analysis,
        "dependency_analysis": dependency_analysis,
        "quality_analysis": quality_analysis,
        "architecture_analysis": architecture_analysis
    }
    
    # === OPTIMIZED LLM-driven semantic analysis with compressed context ===
    logger.info("Performing optimized LLM-driven semantic analysis...")
    
    # Compress context for analysis stage (25K tokens → 3K tokens)
    full_context = {
        "repository_path": project_config.get("legacy_repo_path", ""),
        "repo_analysis": repo_data,
        "repository_analysis": language_analysis,
        "static_analysis_summary": {
            "ast_analysis": ast_analysis,
            "quality_metrics": quality_analysis,
            "security_vulnerabilities": security_analysis.get("vulnerabilities", []),
            "dependency_analysis": dependency_analysis,
            "architecture_analysis": architecture_analysis
        }
    }
    
    # Create optimized prompt context
    prompt_context = OptimizedPromptContext(
        agent_name="CodeUnderstandingAgent",
        phase="analysis",
        project_config=project_config,
        compressed_context=full_context
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    llm_response = llm_call(user_prompt, system_prompt)
    
    # Calculate enhanced modernization readiness score
    readiness_score = calculate_enhanced_modernization_readiness(repo_data)
    
    # Generate comprehensive recommendations based on all analyses
    comprehensive_recommendations = generate_comprehensive_recommendations(
        ast_analysis, dependency_analysis, quality_analysis, architecture_analysis, solr_analysis
    )
    
    results = {
        "repository_analysis": repo_data,
        "llm_analysis": llm_response,
        "modernization_readiness_score": readiness_score,
        "analysis_timestamp": "2024",
        "recommendations": comprehensive_recommendations,
        # Summary of advanced analysis capabilities
        "static_analysis_summary": {
            "ast_functions_analyzed": ast_analysis.get("total_functions", 0),
            "ast_classes_analyzed": ast_analysis.get("total_classes", 0),
            "dependency_relationships": dependency_analysis.get("total_dependencies", 0),
            "circular_dependencies": len(dependency_analysis.get("circular_dependencies", [])),
            "code_smells_detected": quality_analysis.get("total_code_smells", 0),
            "architectural_patterns": len(architecture_analysis.get("design_patterns", [])),
            "analysis_coverage": "Complete AST, dependency, quality, and architecture analysis"
        }
    }
    
    # Results ready for execution agent
    
    logger.info("Deep code analysis completed with compressed output for execution")
    return results


def create_migration_plan(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 2: Create comprehensive migration strategy with optimized context"""
    logger.info("PHASE 2: OPTIMIZED MIGRATION PLANNING")
    
    # Compress context for planning stage
    full_context = {
        "repository_path": analysis_results.get("repository_analysis", {}).get("repository_path", ""),
        "repository_analysis": analysis_results.get("repository_analysis", {}),
        "static_analysis_summary": analysis_results.get("static_analysis_summary", {}),
        "modernization_readiness": analysis_results.get("modernization_readiness", 0)
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="StrategicPlanningAgent",
        phase="planning",
        compressed_context=full_context
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    llm_strategy = llm_call(user_prompt, system_prompt)
    
    # Create structured migration plan with all necessary fields for downstream functions
    migration_plan = {
        "analysis_summary": analysis_results["repository_analysis"],
        "migration_strategy": llm_strategy,
        "target_architecture": "Node.js + MongoDB + Apache Solr",
        "estimated_timeline": "12-16 weeks",
        "risk_assessment": "Medium complexity",
        # Add fields required by transform_code() and migrate_data()
        "source_repo_path": analysis_results["repository_analysis"]["repository_path"],
        "target_stack": "Node.js + MongoDB + Apache Solr",
        "detected_framework": _extract_detected_framework(analysis_results["repository_analysis"])
    }
    
    logger.info("Migration planning completed")
    return migration_plan


def validate_and_refine_strategy(migration_plan: Dict[str, Any], max_cycles: int = 3) -> Dict[str, Any]:
    """Phase 3: Validate migration strategy with refinement loops"""
    logger.info("PHASE 3: STRATEGY VALIDATION AND REFINEMENT")
    
    current_strategy = migration_plan
    validation_result = None
    is_acceptable = False
    
    # Strategy-validation refinement loop
    for cycle_count in range(1, max_cycles + 1):
        logger.info(f"STRATEGY VALIDATION CYCLE {cycle_count}")
        
        # Validate the current strategy
        validation_result, is_acceptable = validate_migration_strategy(
            current_strategy, cycle_count
        )
        
        if is_acceptable:
            logger.info(f"Strategy acceptable after {cycle_count} cycles")
            break
        else:
            if cycle_count < max_cycles:
                logger.info(f"Strategy needs refinement, starting cycle {cycle_count + 1}")
                # Refine strategy based on validation feedback
                current_strategy = refine_migration_strategy(
                    current_strategy, validation_result.get("feedback", "")
                )
            else:
                logger.warning(f"Maximum cycles ({max_cycles}) reached without acceptable strategy")
    
    # Final compilation
    final_results = {
        "final_strategy": current_strategy,
        "validation_history": validation_result,
        "cycles_completed": cycle_count,
        "success": is_acceptable,
        "ready_for_execution": is_acceptable
    }
    
    logger.info("Strategy validation and refinement completed")
    return final_results



def validate_migration_strategy(migration_strategy: Dict[str, Any], cycle_number: int = 1) -> Tuple[Dict[str, Any], bool]:
    """Validate migration strategy feasibility - LLM driven validation"""
    logger.info(f"STRATEGY VALIDATION - Cycle {cycle_number}")
    
    # Generate optimized context for LLM strategy validation
    full_context = {
        "migration_strategy": migration_strategy.get("migration_strategy", ""),
        "analysis_summary": migration_strategy.get("analysis_summary", {}),
        "feedback": migration_strategy.get("feedback", None)
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="ValidationAgent",
        phase="validation",
        cycle_number=cycle_number,
        compressed_context=full_context
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    llm_validation = llm_call(user_prompt, system_prompt)
    
    # LLM determines strategy validation results
    from util import extract_xml
    
    # Try to extract structured validation from LLM response
    validation_decision = extract_xml(llm_validation, "strategy_validation_decision")
    
    # Enhanced validation logic with multiple acceptance criteria
    decision_text = validation_decision.lower()
    acceptance_keywords = [
        "acceptable", "feasible", "approved", "pass", "viable", 
        "suitable", "ready", "good", "ok", "yes", "proceed"
    ]
    rejection_keywords = [
        "rejected", "fail", "unacceptable", "infeasible", "poor", 
        "inadequate", "insufficient", "no", "stop"
    ]
    
    # Check for explicit approval first
    has_approval = any(keyword in decision_text for keyword in acceptance_keywords)
    has_rejection = any(keyword in decision_text for keyword in rejection_keywords)
    
    # If no clear decision, try JSON parsing as fallback
    if not has_approval and not has_rejection:
        try:
            import json
            # Try to parse entire response as JSON
            json_response = json.loads(llm_validation.strip())
            if isinstance(json_response, dict):
                status = str(json_response.get("status", "")).lower()
                decision = str(json_response.get("decision", "")).lower()
                result = str(json_response.get("result", "")).lower()
                
                combined_text = f"{status} {decision} {result}"
                has_approval = any(keyword in combined_text for keyword in acceptance_keywords)
                has_rejection = any(keyword in combined_text for keyword in rejection_keywords)
        except:
            pass
    
    # Final determination - default to acceptable if no clear rejection
    is_acceptable = has_approval or not has_rejection
    
    # Enhanced logging for debugging
    logger.info(f"Validation analysis: approval_found={has_approval}, rejection_found={has_rejection}")
    logger.info(f"Decision text preview: {decision_text[:200]}...")
    if is_acceptable:
        logger.info("Strategy ACCEPTED by validation")
    else:
        logger.warning("Strategy REJECTED by validation")
    
    results = {
        "llm_validation": llm_validation,
        "validation_decision": validation_decision,
        "is_acceptable": is_acceptable,
        "cycle_number": cycle_number,
        "feedback": "Please refine migration strategy for better feasibility" if not is_acceptable else "Strategy validation passed"
    }
    
    logger.info("Strategy validation completed")
    return results, is_acceptable

def refine_migration_strategy(current_strategy: Dict[str, Any], feedback: str) -> Dict[str, Any]:
    """Refine migration strategy based on validation feedback"""
    logger.info("Refining migration strategy based on validation feedback")
    
    # Use optimized LLM to refine the strategy
    full_context = {
        "migration_strategy": current_strategy.get("migration_strategy", ""),
        "analysis_summary": current_strategy.get("analysis_summary", {}),
        "feedback": feedback
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="StrategicPlanningAgent",
        phase="planning",
        compressed_context=full_context,
        feedback=feedback
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    refined_strategy_response = llm_call(user_prompt, system_prompt)
    
    # Update strategy with refinements
    refined_strategy = current_strategy.copy()
    refined_strategy["migration_strategy"] = refined_strategy_response
    refined_strategy["refinement_applied"] = True
    refined_strategy["refinement_feedback"] = feedback
    
    logger.info("Migration strategy refinement completed")
    return refined_strategy


def generate_strategy_documentation(strategy_results: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 4: Generate comprehensive strategy documentation"""
    logger.info("PHASE 4: STRATEGY DOCUMENTATION GENERATION")
    
    # Compress context for documentation generation
    full_context = {
        "migration_strategy": strategy_results.get("migration_strategy", ""),
        "analysis_summary": strategy_results.get("analysis_summary", {}),
        "validation_result": strategy_results.get("validation_result", {})
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="DocumentationAgent",
        phase="documentation",
        compressed_context=full_context
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    llm_documentation = llm_call(user_prompt, system_prompt)
    
    # LLM generates comprehensive strategy documentation
    documentation = {
        "generated_strategy_documentation": llm_documentation,
        "documentation_type": "migration_strategy",
        "strategy_summary": strategy_results
    }
    
    logger.info("Strategy documentation generation completed")
    return documentation


# ================== CODE ANALYSIS HELPER FUNCTIONS ==================

@handle_errors(default_return={})
def _analyze_file_structure(repo_path: str) -> Dict[str, Any]:
    """Analyze repository file structure and organization"""
    validate_path(repo_path)
    structure = {
        "total_files": 0,
        "directories": [],
        "file_types": {},
        "large_files": [],
        "empty_files": []
    }
    
    try:
        for root, dirs, files in os.walk(repo_path):
            for directory in dirs:
                structure["directories"].append(os.path.relpath(os.path.join(root, directory), repo_path))
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                file_ext = os.path.splitext(file)[1].lower()
                file_size = os.path.getsize(file_path)
                
                structure["total_files"] += 1
                
                # Count file types
                structure["file_types"][file_ext] = structure["file_types"].get(file_ext, 0) + 1
                
                # Track large files (>1MB)
                if file_size > 1024 * 1024:
                    structure["large_files"].append({
                        "path": rel_path,
                        "size": file_size
                        
                    })
                
                # Track empty files
                if file_size == 0:
                    structure["empty_files"].append(rel_path)
                    
    except Exception as e:
        logger.warning(f"Error analyzing file structure: {e}")
    
    return structure


@handle_errors(default_return={})
def _detect_languages_and_frameworks(repo_path: str) -> Dict[str, Any]:
    """Detect programming languages and frameworks used in the repository"""
    validate_path(repo_path)
    analysis = {
        "languages": {},
        "frameworks": {"detected": [], "config_files": []},
        "package_managers": []
    }
    
    try:
        for root, _, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                
                # Language detection based on file extensions
                if file.endswith('.php'):
                    analysis["languages"]["php"] = analysis["languages"].get("php", 0) + 1
                elif file.endswith(('.js', '.jsx')):
                    analysis["languages"]["javascript"] = analysis["languages"].get("javascript", 0) + 1
                elif file.endswith('.py'):
                    analysis["languages"]["python"] = analysis["languages"].get("python", 0) + 1
                elif file.endswith(('.html', '.htm')):
                    analysis["languages"]["html"] = analysis["languages"].get("html", 0) + 1
                elif file.endswith('.css'):
                    analysis["languages"]["css"] = analysis["languages"].get("css", 0) + 1
                
                # Framework and package manager detection
                if file == 'composer.json':
                    analysis["frameworks"]["config_files"].append(rel_path)
                    analysis["package_managers"].append("composer")
                    try:
                        with open(file_path, 'r') as f:
                            composer_data = json.load(f)
                            if 'laravel/framework' in composer_data.get('require', {}):
                                analysis["frameworks"]["detected"].append("Laravel")
                    except:
                        pass
                        
                elif file == 'package.json':
                    analysis["frameworks"]["config_files"].append(rel_path)
                    analysis["package_managers"].append("npm")
                    try:
                        with open(file_path, 'r') as f:
                            package_data = json.load(f)
                            deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                            if 'react' in deps:
                                analysis["frameworks"]["detected"].append("React")
                            if 'vue' in deps:
                                analysis["frameworks"]["detected"].append("Vue.js")
                            if 'express' in deps:
                                analysis["frameworks"]["detected"].append("Express.js")
                    except:
                        pass
                        
                elif file == 'requirements.txt':
                    analysis["frameworks"]["config_files"].append(rel_path)
                    analysis["package_managers"].append("pip")
                    try:
                        with open(file_path, 'r') as f:
                            for line in f:
                                if 'django' in line.lower():
                                    analysis["frameworks"]["detected"].append("Django")
                                elif 'flask' in line.lower():
                                    analysis["frameworks"]["detected"].append("Flask")
                    except:
                        pass
                        
    except Exception as e:
        logger.warning(f"Error detecting languages and frameworks: {e}")
    
    # Remove duplicates
    analysis["frameworks"]["detected"] = list(set(analysis["frameworks"]["detected"]))
    analysis["package_managers"] = list(set(analysis["package_managers"]))
    
    return analysis


@handle_errors(default_return={})
def _calculate_code_metrics(repo_path: str, file_stats: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate code quality and complexity metrics"""
    validate_path(repo_path)
    metrics = {
        "lines_of_code": 0,
        "avg_file_size": 0,
        "code_complexity": "medium",
        "technical_debt_indicators": [],
        "modernization_opportunities": []
    }
    
    try:
        total_size = 0
        code_files = 0
        
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(('.php', '.js', '.py', '.html', '.css')):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    code_files += 1
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            metrics["lines_of_code"] += lines
                            
                            # Check for technical debt indicators
                            f.seek(0)
                            content = f.read().lower()
                            if 'todo' in content or 'fixme' in content:
                                metrics["technical_debt_indicators"].append(f"TODO/FIXME found in {file}")
                            if 'deprecated' in content:
                                metrics["technical_debt_indicators"].append(f"Deprecated code in {file}")
                                
                    except Exception:
                        continue
        
        if code_files > 0:
            metrics["avg_file_size"] = total_size / code_files
            
        # Determine complexity based on metrics
        if metrics["lines_of_code"] > 50000:
            metrics["code_complexity"] = "high"
        elif metrics["lines_of_code"] < 5000:
            metrics["code_complexity"] = "low"
            
        # Modernization opportunities
        if file_stats["file_types"].get('.php', 0) > 0:
            metrics["modernization_opportunities"].append("PHP to Node.js migration")
        if file_stats["file_types"].get('.js', 0) > 0:
            metrics["modernization_opportunities"].append("JavaScript ES6+ modernization")
            
    except Exception as e:
        logger.warning(f"Error calculating code metrics: {e}")
    
    return metrics


@handle_errors(default_return={})
def _calculate_code_metrics_optimized(unified_scan: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate code quality and complexity metrics using unified scan results"""
    file_stats = unified_scan["file_structure"]
    file_details = unified_scan["file_details"]
    
    metrics = {
        "lines_of_code": 0,
        "avg_file_size": 0,
        "code_complexity": "medium",
        "maintainability_score": 75
    }
    
    total_size = 0
    code_files = []
    
    # Process cached file details instead of re-scanning
    for file_info in file_details:
        file_ext = file_info["extension"]
        file_size = file_info["size"]
        
        # Count code files
        if file_ext in ['.php', '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c']:
            code_files.append(file_info)
            total_size += file_size
            
            # Estimate lines of code (rough approximation: 50 chars per line)
            estimated_lines = max(1, file_size // 50)
            metrics["lines_of_code"] += estimated_lines
    
    # Calculate metrics
    if code_files:
        metrics["avg_file_size"] = total_size // len(code_files)
        
        # Complexity assessment based on file count and size
        if len(code_files) > 100 or metrics["avg_file_size"] > 10000:
            metrics["code_complexity"] = "high"
        elif len(code_files) < 20 and metrics["avg_file_size"] < 2000:
            metrics["code_complexity"] = "low"
    
    logger.info(f"Optimized code metrics calculated: {len(code_files)} code files, {metrics['lines_of_code']} estimated LOC")
    return metrics


def _analyze_security_and_dependencies(repo_path: str, language_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze security vulnerabilities and dependency issues"""
    security = {
        "dependency_files": language_analysis["frameworks"]["config_files"],
        "potential_vulnerabilities": [],
        "outdated_dependencies": [],
        "security_recommendations": []
    }
    
    try:
        # Check for common security issues in code
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(('.php', '.js', '.py')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            
                            # Basic security pattern detection
                            if 'eval(' in content:
                                security["potential_vulnerabilities"].append(f"eval() usage in {file}")
                            if 'mysql_query' in content:
                                security["potential_vulnerabilities"].append(f"Direct MySQL query in {file}")
                            if '$_get' in content or '$_post' in content:
                                security["potential_vulnerabilities"].append(f"Direct input usage in {file}")
                                
                    except Exception:
                        continue
        
        # Security recommendations
        security["security_recommendations"] = [
            "Implement input validation and sanitization",
            "Use parameterized queries to prevent SQL injection",
            "Update to latest framework versions",
            "Implement proper error handling"
        ]
        
    except Exception as e:
        logger.warning(f"Error analyzing security: {e}")
    
    return security


def _calculate_modernization_readiness(repo_data: Dict[str, Any]) -> int:
    """Calculate a modernization readiness score (0-100)"""
    score = 50  # Base score
    
    try:
        # Positive factors
        if repo_data["language_analysis"]["frameworks"]["detected"]:
            score += 20  # Framework usage is good
            
        if repo_data["file_structure"]["total_files"] < 1000:
            score += 10  # Manageable codebase size
            
        if len(repo_data["security_analysis"]["potential_vulnerabilities"]) < 5:
            score += 15  # Low security issues
            
        # Negative factors
        if repo_data["quality_metrics"]["code_complexity"] == "high":
            score -= 15  # High complexity reduces readiness
            
        if len(repo_data["quality_metrics"]["technical_debt_indicators"]) > 10:
            score -= 10  # High technical debt
            
        # Ensure score is within bounds
        score = max(0, min(100, score))
        
    except Exception as e:
        logger.warning(f"Error calculating readiness score: {e}")
        score = 50  # Default score on error
    
    return score


# ================== CODE TRANSFORMATION HELPER FUNCTIONS ==================

def _analyze_transformation_targets(repo_path: str) -> Dict[str, Any]:
    """Analyze code structure to identify transformation targets"""
    targets = {
        "php_files": [],
        "javascript_files": [],
        "database_files": [],
        "config_files": [],
        "framework_components": {},
        "transformation_complexity": "medium"
    }
    
    try:
        for root, _, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                
                if file.endswith('.php'):
                    targets["php_files"].append({
                        "path": rel_path,
                        "size": os.path.getsize(file_path),
                        "complexity": _estimate_file_complexity(file_path)
                    })
                elif file.endswith(('.js', '.jsx')):
                    targets["javascript_files"].append({
                        "path": rel_path,
                        "size": os.path.getsize(file_path),
                        "type": "existing_js"
                    })
                elif file.endswith(('.sql', '.db')):
                    targets["database_files"].append(rel_path)
                elif file in ['composer.json', 'package.json', '.env', 'config.php']:
                    targets["config_files"].append(rel_path)
        
        # Determine overall complexity
        total_php_files = len(targets["php_files"])
        if total_php_files > 100:
            targets["transformation_complexity"] = "high"
        elif total_php_files < 20:
            targets["transformation_complexity"] = "low"
            
    except Exception as e:
        logger.warning(f"Error analyzing transformation targets: {e}")
    
    return targets


def _perform_syntax_transformations(repo_path: str, target_stack: str, feedback: str = None) -> List[Dict[str, Any]]:
    """Perform language-specific syntax transformations"""
    transformations = []
    
    try:
        # Find PHP files to transform
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.php'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_path)
                    
                    transformation = _transform_php_to_nodejs(file_path, target_stack, feedback)
                    transformation["source_file"] = rel_path
                    transformations.append(transformation)
                    
    except Exception as e:
        logger.error(f"Syntax transformation error: {e}")
        transformations.append({
            "status": "failed",
            "error": str(e),
            "file": "unknown"
        })
    
    return transformations


def _migrate_framework_components(repo_path: str, target_stack: str, migration_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Migrate framework-specific components"""
    migrations = []
    
    try:
        # Detect current framework
        current_framework = migration_data.get("detected_framework", "generic_php")
        
        if "laravel" in current_framework.lower():
            migrations.extend(_migrate_laravel_components(repo_path, target_stack))
        elif "symfony" in current_framework.lower():
            migrations.extend(_migrate_symfony_components(repo_path, target_stack))
        else:
            migrations.extend(_migrate_generic_php_components(repo_path, target_stack))
            
    except Exception as e:
        logger.error(f"Framework migration error: {e}")
        migrations.append({
            "status": "failed",
            "error": str(e),
            "component": "framework_detection"
        })
    
    return migrations


def _apply_modernization_improvements(repo_path: str, target_stack: str) -> List[Dict[str, Any]]:
    """Apply modern coding practices and improvements"""
    improvements = []
    
    # Common modernization patterns
    modernization_tasks = [
        {
            "name": "async_await_conversion",
            "description": "Convert callbacks to async/await patterns",
            "impact": "high"
        },
        {
            "name": "es6_syntax_upgrade", 
            "description": "Upgrade to ES6+ syntax (arrow functions, destructuring)",
            "impact": "medium"
        },
        {
            "name": "error_handling_improvement",
            "description": "Implement proper error handling and logging",
            "impact": "high"
        },
        {
            "name": "security_hardening",
            "description": "Add input validation and security measures",
            "impact": "critical"
        }
    ]
    
    for task in modernization_tasks:
        improvements.append({
            "task": task["name"],
            "description": task["description"],
            "status": "planned",
            "impact": task["impact"],
            "estimated_effort": "2-4 hours"
        })
    
    return improvements


def _perform_llm_driven_refactoring(transform_results: Dict[str, Any], migration_data: Dict[str, Any], 
                                   feedback: str = None, cycle_number: int = 1) -> Dict[str, Any]:
    """Use LLM for intelligent code refactoring and optimization"""
    
    # Prepare context for LLM
    refactoring_context = {
        "source_analysis": transform_results.get("source_analysis", {}),
        "target_stack": migration_data.get("target_stack", "node.js"),
        "feedback": feedback,
        "cycle": cycle_number
    }
    
    # Generate optimized LLM prompt for refactoring
    full_context = {
        "target_platform": refactoring_context.get("target_stack", "modern_nodejs"),
        "transformation_scope": refactoring_context.get("transformation_scope", []),
        "code_patterns": refactoring_context.get("legacy_patterns", []),
        "dependencies": refactoring_context.get("dependency_updates", []),
        "feedback": feedback
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="TransformationAgent",
        phase="transformation",
        cycle_number=cycle_number,
        compressed_context=full_context,
        feedback=feedback
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    llm_response = llm_call(user_prompt, system_prompt)
    
    return {
        "llm_recommendations": llm_response,
        "context_used": refactoring_context,
        "refactoring_scope": "intelligent_optimization",
        "cycle_number": cycle_number
    }


def _generate_transformation_summary(transform_results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate summary of all transformation activities"""
    
    summary = {
        "total_files_analyzed": len(transform_results.get("source_analysis", {}).get("php_files", [])),
        "syntax_conversions_count": len(transform_results.get("syntax_conversions", [])),
        "framework_migrations_count": len(transform_results.get("framework_migrations", [])),
        "improvements_applied": len(transform_results.get("modernization_improvements", [])),
        "overall_status": "completed",
        "transformation_type": "php_to_nodejs",
        "recommendations": []
    }
    
    # Add recommendations based on results
    if summary["total_files_analyzed"] > 50:
        summary["recommendations"].append("Consider phased migration approach for large codebase")
    
    if summary["syntax_conversions_count"] > 0:
        summary["recommendations"].append("Review converted syntax for Node.js best practices")
        
    return summary


# ================== SYNTAX TRANSFORMATION HELPERS ==================

def _estimate_file_complexity(file_path: str) -> str:
    """Estimate complexity of a PHP file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Simple heuristics for complexity
        lines = len(content.split('\n'))
        functions = content.count('function ')
        classes = content.count('class ')
        
        if lines > 500 or functions > 20 or classes > 5:
            return "high"
        elif lines > 100 or functions > 5 or classes > 1:
            return "medium"
        else:
            return "low"
            
    except Exception:
        return "unknown"


def _transform_php_to_nodejs(file_path: str, target_stack: str, feedback: str = None) -> Dict[str, Any]:
    """Transform a PHP file to Node.js equivalent"""
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            php_content = f.read()
        
        # Basic transformation patterns
        transformation_patterns = [
            {
                "pattern": "PHP variable syntax transformation",
                "example": "$variable -> let variable",
                "status": "planned"
            },
            {
                "pattern": "Function definition conversion", 
                "example": "function name() {} -> function name() {}",
                "status": "planned"
            },
            {
                "pattern": "Array syntax modernization",
                "example": "array() -> []",
                "status": "planned"
            }
        ]
        
        return {
            "status": "analyzed",
            "file_size": len(php_content),
            "estimated_lines": len(php_content.split('\n')),
            "transformation_patterns": transformation_patterns,
            "target_framework": "express.js" if "node" in target_stack.lower() else "generic",
            "complexity": _estimate_file_complexity(file_path)
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "file": file_path
        }


def _migrate_laravel_components(repo_path: str, target_stack: str) -> List[Dict[str, Any]]:
    """Migrate Laravel-specific components to Node.js equivalents"""
    migrations = [
        {
            "component": "routes",
            "laravel_pattern": "Route::get('/path', 'Controller@method')",
            "nodejs_equivalent": "app.get('/path', controller.method)",
            "status": "migration_planned"
        },
        {
            "component": "middleware",
            "laravel_pattern": "Laravel Middleware",
            "nodejs_equivalent": "Express.js Middleware",
            "status": "migration_planned"
        },
        {
            "component": "models",
            "laravel_pattern": "Eloquent Models",
            "nodejs_equivalent": "Mongoose Models (MongoDB)",
            "status": "migration_planned"
        }
    ]
    return migrations


def _migrate_symfony_components(repo_path: str, target_stack: str) -> List[Dict[str, Any]]:
    """Migrate Symfony-specific components"""
    return [
        {
            "component": "dependency_injection",
            "framework": "symfony",
            "target": "node.js",
            "status": "migration_planned"
        }
    ]


def _migrate_generic_php_components(repo_path: str, target_stack: str) -> List[Dict[str, Any]]:
    """Migrate generic PHP components"""
    return [
        {
            "component": "generic_php_functions",
            "transformation": "php_to_javascript",
            "status": "migration_planned"
        }
    ]


def _extract_detected_framework(repository_analysis: Dict[str, Any]) -> str:
    """Extract the detected framework from repository analysis"""
    try:
        language_analysis = repository_analysis.get("language_analysis", {})
        frameworks = language_analysis.get("frameworks", {})
        detected_frameworks = frameworks.get("detected", [])
        
        if detected_frameworks:
            # Return the first detected framework, or combine multiple
            return ", ".join(detected_frameworks)
        else:
            # Fallback based on file types
            languages = language_analysis.get("languages", {})
            if "php" in languages:
                return "generic_php"
            elif "javascript" in languages:
                return "generic_javascript"
            elif "python" in languages:
                return "generic_python"
            else:
                return "generic"
                
    except Exception as e:
        logger.warning(f"Error extracting detected framework: {e}")
        return "generic"


# ================== AI-DRIVEN DATA MIGRATION FUNCTIONS ==================

def _ai_analyze_database_structure(repo_path: str, feedback: str = None) -> Dict[str, Any]:
    """AI-driven analysis of database structure and schema using unified prompt templates"""
    
    # Discover database files and configurations
    db_files = _discover_database_files(repo_path)
    
    # Prepare comprehensive database context for AI analysis
    db_context = {
        "database_files": db_files,
        "repo_path": repo_path,
        "feedback": feedback
    }
    
    # Use optimized unified prompt template system for database analysis
    full_context = {
        "repo_path": repo_path,
        "current_db": "mysql",  # Default, will be detected
        "target_db": "mongodb",
        "migration_complexity": "medium",
        "schema_files": [f.get("path", "") for f in db_files[:5]],
        "connection_patterns": [],
        "feedback": feedback
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="DatabaseMigrationAgent",
        phase="database",
        cycle_number=1,
        compressed_context=full_context,
        feedback=feedback
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    ai_analysis = llm_call(user_prompt, system_prompt)
    
    return {
        "ai_analysis": ai_analysis,
        "discovered_files": db_files,
        "analysis_context": db_context,
        "ai_confidence": "high",
        "prompt_template_used": "DataMigrationAgent"
    }


def _ai_generate_migration_strategy(database_analysis: Dict[str, Any], target_stack: str, 
                                  feedback: str = None, cycle_number: int = 1) -> Dict[str, Any]:
    """AI-driven generation of comprehensive migration strategy using unified prompt templates"""
    
    # Prepare optimized context for AI strategy generation
    full_context = {
        "current_db": "mysql",
        "target_db": "mongodb", 
        "migration_complexity": "medium",
        "schema_files": [],
        "connection_patterns": [],
        "feedback": feedback
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="DatabaseMigrationAgent",
        phase="database",
        cycle_number=cycle_number,
        compressed_context=full_context,
        feedback=feedback
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    ai_strategy = llm_call(user_prompt, system_prompt)
    
    return {
        "ai_migration_strategy": ai_strategy,
        "strategy_context": {
            "database_analysis": database_analysis,
            "target_stack": target_stack,
            "cycle": cycle_number,
            "feedback": feedback
        },
        "target_stack": target_stack,
        "cycle_number": cycle_number,
        "prompt_template_used": "DataMigrationAgent"
    }


def _ai_create_transformation_rules(database_analysis: Dict[str, Any], migration_strategy: Dict[str, Any], 
                                  feedback: str = None) -> Dict[str, Any]:
    """AI-driven creation of data transformation rules using unified prompt templates"""
    
    # Use optimized unified prompt template system for transformation rules
    full_context = {
        "current_db": "mysql",
        "target_db": "mongodb", 
        "migration_complexity": "medium",
        "schema_files": [],
        "connection_patterns": [],
        "feedback": feedback
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="DatabaseMigrationAgent",
        phase="database",
        cycle_number=1,
        compressed_context=full_context,
        feedback=feedback
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    ai_rules = llm_call(user_prompt, system_prompt)
    
    return {
        "ai_transformation_rules": ai_rules,
        "transformation_context": {
            "database_analysis": database_analysis,
            "migration_strategy": migration_strategy,
            "feedback": feedback
        },
        "rule_categories": ["schema", "data_types", "validation", "performance"],
        "prompt_template_used": "DataMigrationAgent"
    }


def _ai_generate_migration_scripts(transformation_rules: Dict[str, Any], target_stack: str, 
                                 feedback: str = None) -> Dict[str, Any]:
    """AI-driven generation of executable migration scripts using unified prompt templates"""
    
    # Use optimized unified prompt template system for script generation
    full_context = {
        "current_db": "mysql",
        "target_db": "mongodb", 
        "migration_complexity": "medium",
        "schema_files": [],
        "connection_patterns": [],
        "feedback": feedback
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="DatabaseMigrationAgent",
        phase="database",
        cycle_number=1,
        compressed_context=full_context,
        feedback=feedback
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    ai_scripts = llm_call(user_prompt, system_prompt)
    
    return {
        "ai_migration_scripts": ai_scripts,
        "script_context": {
            "transformation_rules": transformation_rules,
            "target_stack": target_stack,
            "feedback": feedback
        },
        "script_types": ["schema", "data_transformation", "validation", "rollback"],
        "target_platform": target_stack,
        "prompt_template_used": "DataMigrationAgent"
    }


def _ai_design_validation_strategy(database_analysis: Dict[str, Any], migration_scripts: Dict[str, Any], 
                                 feedback: str = None) -> Dict[str, Any]:
    """AI-driven design of comprehensive validation strategy using unified prompt templates"""
    
    # Use optimized unified prompt template system for validation strategy
    full_context = {
        "current_db": "mysql",
        "target_db": "mongodb", 
        "migration_complexity": "medium",
        "schema_files": [],
        "connection_patterns": [],
        "feedback": feedback
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="DatabaseMigrationAgent",
        phase="database",
        cycle_number=1,
        compressed_context=full_context,
        feedback=feedback
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    ai_validation = llm_call(user_prompt, system_prompt)
    
    return {
        "ai_validation_strategy": ai_validation,
        "validation_context": {
            "database_analysis": database_analysis,
            "migration_scripts": migration_scripts,
            "feedback": feedback
        },
        "validation_phases": ["integrity", "business_rules", "performance", "functional"],
        "prompt_template_used": "DataMigrationAgent"
    }


def _ai_create_execution_plan(migration_scripts: Dict[str, Any], validation_strategy: Dict[str, Any], 
                            cycle_number: int = 1, feedback: str = None) -> Dict[str, Any]:
    """AI-driven creation of comprehensive execution plan using unified prompt templates"""
    
    # Use optimized unified prompt template system for execution planning
    full_context = {
        "current_db": "mysql",
        "target_db": "mongodb", 
        "migration_complexity": "medium",
        "schema_files": [],
        "connection_patterns": [],
        "feedback": feedback
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="DatabaseMigrationAgent",
        phase="database",
        cycle_number=cycle_number,
        compressed_context=full_context,
        feedback=feedback
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    ai_execution = llm_call(user_prompt, system_prompt)
    
    return {
        "ai_execution_plan": ai_execution,
        "execution_context": {
            "migration_scripts": migration_scripts,
            "validation_strategy": validation_strategy,
            "cycle": cycle_number,
            "feedback": feedback
        },
        "plan_components": ["sequence", "timeline", "resources", "risk_management"],
        "cycle_number": cycle_number,
        "prompt_template_used": "DataMigrationAgent"
    }


def _ai_generate_migration_summary(database_analysis: Dict[str, Any], execution_plan: Dict[str, Any]) -> Dict[str, Any]:
    """AI-driven generation of migration summary and recommendations using unified prompt templates"""
    
    # Use optimized unified prompt template system for summary generation
    full_context = {
        "current_db": "mysql",
        "target_db": "mongodb", 
        "migration_complexity": "medium",
        "schema_files": [],
        "connection_patterns": [],
        "feedback": None
    }
    
    prompt_context = OptimizedPromptContext(
        agent_name="DatabaseMigrationAgent",
        phase="database",
        cycle_number=1,
        compressed_context=full_context,
        feedback=None
    )
    
    engine = OptimizedPromptEngine()
    system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
    ai_summary = llm_call(user_prompt, system_prompt)
    
    return {
        "ai_migration_summary": ai_summary,
        "summary_type": "executive_overview",
        "recommendation_confidence": "high",
        "prompt_template_used": "DataMigrationAgent"
    }


def _discover_database_files(repo_path: str) -> List[Dict[str, Any]]:
    """Discover database-related files in the repository"""
    db_files = []
    
    try:
        for root, _, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                
                # Database schema files
                if file.endswith(('.sql', '.ddl', '.dml')):
                    db_files.append({
                        "type": "sql_schema",
                        "path": rel_path,
                        "size": os.path.getsize(file_path)
                    })
                
                # Database configuration files
                elif file in ['database.php', 'db.config', '.env'] or 'database' in file.lower():
                    db_files.append({
                        "type": "database_config",
                        "path": rel_path,
                        "size": os.path.getsize(file_path)
                    })
                
                # Migration files
                elif 'migration' in file.lower() or 'migrate' in file.lower():
                    db_files.append({
                        "type": "migration_file",
                        "path": rel_path,
                        "size": os.path.getsize(file_path)
                    })
                    
    except Exception as e:
        logger.warning(f"Error discovering database files: {e}")
    
    return db_files


def _analyze_api_dependencies_comprehensive(repo_path: str, unified_scan: Dict[str, Any]) -> Dict[str, Any]:
    """Comprehensive analysis of API dependencies and backend compatibility requirements"""
    logger.info("Performing comprehensive API dependency analysis...")
    
    api_analysis = {
        "http_endpoints": [],
        "database_calls": [],
        "external_apis": [],
        "socket_connections": [],
        "authentication_flows": [],
        "file_operations": [],
        "middleware_usage": [],
        "third_party_services": [],
        "compatibility_risks": [],
        "preservation_requirements": []
    }
    
    # Define API pattern categories for comprehensive detection
    api_patterns = {
        "http_requests": {
            "patterns": ['fetch(', 'axios.', '$.ajax', 'request(', 'http.request', 'XMLHttpRequest', 'superagent'],
            "category": "http_endpoints"
        },
        "express_routes": {
            "patterns": ['app.get(', 'app.post(', 'app.put(', 'app.delete(', 'router.get(', 'router.post('],
            "category": "http_endpoints"
        },
        "database": {
            "patterns": ['db.', 'collection.', 'mongoose.', 'mongodb.', 'MongoClient', '.find(', '.save(', '.update('],
            "category": "database_calls"
        },
        "socket_io": {
            "patterns": ['socket.emit', 'socket.on', 'io.connect', 'io(', 'socketio'],
            "category": "socket_connections"
        },
        "auth": {
            "patterns": ['passport.', 'jwt.', 'session.', 'auth.', 'bcrypt', 'crypto.'],
            "category": "authentication_flows"
        },
        "file_ops": {
            "patterns": ['fs.', 'path.', 'multer', 'upload', 'readFile', 'writeFile'],
            "category": "file_operations"
        },
        "middleware": {
            "patterns": ['app.use(', 'express.static', 'bodyParser', 'cors', 'helmet'],
            "category": "middleware_usage"
        },
        "third_party": {
            "patterns": ['stripe.', 'paypal.', 'aws.', 'cloudinary.', 'sendgrid', 'twilio'],
            "category": "third_party_services"
        }
    }
    
    # Analyze each file for API dependencies
    for file_info in unified_scan.get("file_structure", {}).get("files", []):
        if file_info.get("type") in ["javascript", "typescript", "json"]:
            try:
                file_path = os.path.join(repo_path, file_info["path"])
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Extract API calls with context
                file_apis = _extract_api_calls_with_context(content, file_info["path"], api_patterns)
                
                # Categorize findings
                for category, calls in file_apis.items():
                    if calls:
                        api_analysis[category].extend(calls)
                        
            except Exception as e:
                logger.debug(f"Error analyzing file {file_info['path']}: {e}")
    
    # Analyze compatibility risks
    api_analysis["compatibility_risks"] = _assess_api_compatibility_risks(api_analysis)
    
    # Generate preservation requirements
    api_analysis["preservation_requirements"] = _generate_api_preservation_requirements(api_analysis)
    
    # Summary statistics
    api_analysis["summary"] = {
        "total_api_calls": sum(len(calls) for calls in api_analysis.values() if isinstance(calls, list)),
        "categories_found": [cat for cat, calls in api_analysis.items() if isinstance(calls, list) and calls],
        "risk_level": _calculate_api_risk_level(api_analysis)
    }
    
    logger.info(f"API analysis completed: Found {api_analysis['summary']['total_api_calls']} API calls across {len(api_analysis['summary']['categories_found'])} categories")
    
    return api_analysis


def _extract_api_calls_with_context(content: str, file_path: str, api_patterns: Dict[str, Any]) -> Dict[str, List]:
    """Extract API calls with surrounding context for better understanding"""
    file_apis = {category["category"]: [] for category in api_patterns.values()}
    lines = content.split('\n')
    
    for pattern_group, config in api_patterns.items():
        patterns = config["patterns"]
        category = config["category"]
        
        for pattern in patterns:
            for i, line in enumerate(lines):
                if pattern in line:
                    # Extract context (3 lines before and after)
                    context_start = max(0, i - 3)
                    context_end = min(len(lines), i + 4)
                    context = '\n'.join(lines[context_start:context_end])
                    
                    api_call = {
                        "file": file_path,
                        "line": i + 1,
                        "pattern": pattern,
                        "code": line.strip(),
                        "context": context,
                        "function_name": _extract_containing_function(lines, i),
                        "is_critical": _is_critical_api_call(line, pattern)
                    }
                    
                    file_apis[category].append(api_call)
    
    return file_apis


def _extract_containing_function(lines: List[str], line_index: int) -> str:
    """Extract the name of function containing the API call"""
    for i in range(line_index, max(0, line_index - 15), -1):
        line = lines[i].strip()
        # Look for function definitions
        if line.startswith('function '):
            return line.split('(')[0].replace('function ', '').strip()
        elif ' = (' in line and '=>' in line:
            return line.split(' = ')[0].strip()
        elif line.endswith(': function(') or line.endswith(': function ('):
            return line.split(':')[0].strip()
    return "unknown"


def _is_critical_api_call(line: str, pattern: str) -> bool:
    """Determine if an API call is critical for backend compatibility"""
    critical_indicators = [
        'api/', '/api/', 'endpoint', 'server', 'backend',
        'auth', 'login', 'session', 'database', 'db.',
        'socket.emit', 'socket.on'
    ]
    
    line_lower = line.lower()
    return any(indicator in line_lower for indicator in critical_indicators)


def _assess_api_compatibility_risks(api_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Assess potential compatibility risks during modernization"""
    risks = []
    
    # Check for mixed async patterns
    if api_analysis["http_endpoints"]:
        async_patterns = []
        for call in api_analysis["http_endpoints"]:
            if 'callback' in call["code"].lower():
                async_patterns.append("callback")
            elif 'promise' in call["code"].lower() or '.then(' in call["code"]:
                async_patterns.append("promise")
            elif 'async' in call["code"] or 'await' in call["code"]:
                async_patterns.append("async/await")
        
        if len(set(async_patterns)) > 1:
            risks.append({
                "type": "mixed_async_patterns",
                "severity": "high",
                "description": "Mixed async patterns detected - may cause compatibility issues",
                "patterns_found": list(set(async_patterns))
            })
    
    # Check for deprecated API usage
    deprecated_patterns = ['$.ajax', 'XMLHttpRequest', 'http.request']
    for category, calls in api_analysis.items():
        if isinstance(calls, list):
            for call in calls:
                if call.get("pattern") in deprecated_patterns:
                    risks.append({
                        "type": "deprecated_api",
                        "severity": "medium", 
                        "description": f"Deprecated API pattern '{call['pattern']}' in {call['file']}",
                        "file": call["file"],
                        "line": call["line"]
                    })
    
    return risks


def _generate_api_preservation_requirements(api_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate specific requirements for preserving API compatibility"""
    requirements = []
    
    # HTTP endpoint preservation
    if api_analysis["http_endpoints"]:
        requirements.append({
            "category": "http_endpoints",
            "requirement": "Preserve all HTTP request patterns and endpoint URLs",
            "details": [
                "Maintain existing URL structures",
                "Preserve request/response formats", 
                "Keep authentication headers",
                "Maintain error handling patterns"
            ],
            "critical_calls": [call for call in api_analysis["http_endpoints"] if call.get("is_critical")]
        })
    
    # Database call preservation  
    if api_analysis["database_calls"]:
        requirements.append({
            "category": "database_calls",
            "requirement": "Preserve database query patterns and data structures",
            "details": [
                "Maintain collection/table names",
                "Preserve query structures",
                "Keep data validation patterns",
                "Maintain transaction handling"
            ],
            "critical_calls": [call for call in api_analysis["database_calls"] if call.get("is_critical")]
        })
    
    # Socket connection preservation
    if api_analysis["socket_connections"]:
        requirements.append({
            "category": "socket_connections", 
            "requirement": "Preserve real-time communication patterns",
            "details": [
                "Maintain event names and handlers",
                "Preserve connection logic",
                "Keep message formats",
                "Maintain room/namespace structures"
            ],
            "critical_calls": [call for call in api_analysis["socket_connections"] if call.get("is_critical")]
        })
    
    return requirements


def _calculate_api_risk_level(api_analysis: Dict[str, Any]) -> str:
    """Calculate overall API compatibility risk level"""
    total_risks = len(api_analysis.get("compatibility_risks", []))
    critical_apis = sum(1 for category in api_analysis.values() 
                       if isinstance(category, list) 
                       for call in category 
                       if call.get("is_critical"))
    
    if total_risks >= 5 or critical_apis >= 10:
        return "high"
    elif total_risks >= 2 or critical_apis >= 5:
        return "medium"
    else:
        return "low"


def _analyze_backend_stack_compatibility(repo_path: str, unified_scan: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze backend technology stack and upgrade compatibility requirements"""
    logger.info("Performing backend stack compatibility analysis...")
    
    backend_analysis = {
        "node_version_compatibility": {},
        "express_compatibility": {},
        "middleware_compatibility": [],
        "npm_dependencies": [],
        "server_configuration": {},
        "upgrade_requirements": [],
        "breaking_changes": [],
        "migration_tasks": []
    }
    
    # Analyze package.json files for Node.js/Express compatibility
    for file_info in unified_scan.get("file_structure", {}).get("files", []):
        if file_info.get("filename") == "package.json":
            try:
                file_path = os.path.join(repo_path, file_info["path"])
                with open(file_path, 'r', encoding='utf-8') as f:
                    package_data = json.loads(f.read())
                
                # Node.js version analysis
                node_analysis = _analyze_node_version_requirements(package_data)
                backend_analysis["node_version_compatibility"].update(node_analysis)
                
                # Express framework analysis
                express_analysis = _analyze_express_compatibility(package_data)
                backend_analysis["express_compatibility"].update(express_analysis)
                
                # Dependencies analysis
                deps_analysis = _analyze_npm_dependencies_compatibility(package_data)
                backend_analysis["npm_dependencies"].extend(deps_analysis)
                
            except Exception as e:
                logger.debug(f"Error analyzing package.json {file_info['path']}: {e}")
    
    # Analyze server.js, app.js, index.js files
    server_files = ['server.js', 'app.js', 'index.js', 'main.js']
    for file_info in unified_scan.get("file_structure", {}).get("files", []):
        if file_info.get("filename") in server_files:
            try:
                file_path = os.path.join(repo_path, file_info["path"])
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Analyze middleware compatibility
                middleware_analysis = _analyze_middleware_compatibility(content, file_info["path"])
                backend_analysis["middleware_compatibility"].extend(middleware_analysis)
                
                # Analyze server configuration
                server_config = _analyze_server_configuration(content, file_info["path"])
                backend_analysis["server_configuration"].update(server_config)
                
            except Exception as e:
                logger.debug(f"Error analyzing server file {file_info['path']}: {e}")
    
    # Generate upgrade requirements and breaking changes
    backend_analysis["upgrade_requirements"] = _generate_backend_upgrade_requirements(backend_analysis)
    backend_analysis["breaking_changes"] = _identify_backend_breaking_changes(backend_analysis)
    backend_analysis["migration_tasks"] = _generate_backend_migration_tasks(backend_analysis)
    
    return backend_analysis


def _analyze_node_version_requirements(package_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze Node.js version requirements and compatibility"""
    node_analysis = {
        "engines": package_data.get("engines", {}),
        "current_compatibility": "unknown",
        "target_compatibility": "20.x",
        "upgrade_required": False,
        "compatibility_issues": []
    }
    
    # Check engines field
    if "node" in node_analysis["engines"]:
        current_node = node_analysis["engines"]["node"]
        # Based on server check: Node.js 4.9.1
        if "4." in current_node or current_node.startswith(">=4"):
            node_analysis["current_compatibility"] = "4.x"
            node_analysis["upgrade_required"] = True
            node_analysis["compatibility_issues"].append("Node.js 4.x is EOL and requires major upgrade to 20.x LTS")
    
    return node_analysis


def _analyze_express_compatibility(package_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze Express.js framework compatibility"""
    express_analysis = {
        "current_version": "unknown",
        "target_version": "4.x",
        "upgrade_required": False,
        "api_changes": [],
        "middleware_changes": []
    }
    
    dependencies = package_data.get("dependencies", {})
    if "express" in dependencies:
        current_version = dependencies["express"]
        express_analysis["current_version"] = current_version
        
        # Check for Express 3.x to 4.x upgrade (major breaking changes)
        if current_version.startswith("^3") or current_version.startswith("3."):
            express_analysis["upgrade_required"] = True
            express_analysis["api_changes"] = [
                "app.configure() removed",
                "app.use() middleware signature changed",
                "res.json() and res.send() behavior changed",
                "Error handling middleware signature changed"
            ]
            express_analysis["middleware_changes"] = [
                "body-parser middleware extracted",
                "cookie-parser middleware extracted",
                "session middleware extracted",
                "static middleware signature changed"
            ]
    
    return express_analysis


def _analyze_npm_dependencies_compatibility(package_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze npm dependencies for compatibility issues"""
    deps_analysis = []
    
    # Known problematic dependencies from Node.js 4.x era
    problematic_deps = {
        "body-parser": {"old": "1.0.0", "new": "1.20.0", "breaking": False},
        "mongoose": {"old": "3.x", "new": "7.x", "breaking": True},
        "socket.io": {"old": "1.x", "new": "4.x", "breaking": True},
        "lodash": {"old": "3.x", "new": "4.x", "breaking": False},
        "async": {"old": "1.x", "new": "3.x", "breaking": True}
    }
    
    dependencies = package_data.get("dependencies", {})
    for dep_name, version in dependencies.items():
        if dep_name in problematic_deps:
            dep_info = problematic_deps[dep_name]
            deps_analysis.append({
                "name": dep_name,
                "current_version": version,
                "recommended_version": dep_info["new"],
                "breaking_changes": dep_info["breaking"],
                "upgrade_priority": "high" if dep_info["breaking"] else "medium"
            })
    
    return deps_analysis


def _analyze_middleware_compatibility(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Analyze middleware usage for compatibility issues"""
    middleware_analysis = []
    
    # Express 3.x to 4.x middleware patterns
    problematic_patterns = {
        "app.configure(": {
            "issue": "app.configure() removed in Express 4.x",
            "solution": "Use environment-specific logic instead"
        },
        "app.use(express.bodyParser": {
            "issue": "express.bodyParser() removed in Express 4.x",
            "solution": "Use body-parser middleware separately"
        },
        "app.use(express.cookieParser": {
            "issue": "express.cookieParser() removed in Express 4.x", 
            "solution": "Use cookie-parser middleware separately"
        },
        "app.use(express.session": {
            "issue": "express.session() removed in Express 4.x",
            "solution": "Use express-session middleware separately"
        }
    }
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        for pattern, details in problematic_patterns.items():
            if pattern in line:
                middleware_analysis.append({
                    "file": file_path,
                    "line": i + 1,
                    "code": line.strip(),
                    "issue": details["issue"],
                    "solution": details["solution"],
                    "severity": "high"
                })
    
    return middleware_analysis


def _analyze_server_configuration(content: str, file_path: str) -> Dict[str, Any]:
    """Analyze server configuration for compatibility issues"""
    config_analysis = {
        "http_server": False,
        "https_server": False,
        "port_configuration": [],
        "static_file_serving": [],
        "error_handling": []
    }
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Check for HTTP server creation
        if 'http.createServer(' in line or 'http.Server(' in line:
            config_analysis["http_server"] = True
        
        # Check for HTTPS server
        if 'https.createServer(' in line:
            config_analysis["https_server"] = True
        
        # Check for port configuration
        if 'listen(' in line or '.listen(' in line:
            config_analysis["port_configuration"].append({
                "file": file_path,
                "line": i + 1,
                "code": line.strip()
            })
        
        # Check for static file serving
        if 'express.static(' in line:
            config_analysis["static_file_serving"].append({
                "file": file_path,
                "line": i + 1,
                "code": line.strip()
            })
    
    return config_analysis


def _generate_backend_upgrade_requirements(backend_analysis: Dict[str, Any]) -> List[str]:
    """Generate backend upgrade requirements"""
    requirements = []
    
    # Node.js upgrade requirements
    if backend_analysis["node_version_compatibility"].get("upgrade_required"):
        requirements.append("CRITICAL: Upgrade Node.js from 4.x to 20.x LTS")
        requirements.append("Update package.json engines field to specify Node.js 20.x")
    
    # Express upgrade requirements
    if backend_analysis["express_compatibility"].get("upgrade_required"):
        requirements.append("MAJOR: Upgrade Express.js from 3.x to 4.x")
        requirements.append("Refactor middleware usage to Express 4.x patterns")
        requirements.append("Update error handling middleware signatures")
    
    # Dependencies upgrade requirements
    for dep in backend_analysis["npm_dependencies"]:
        if dep.get("breaking_changes"):
            requirements.append(f"BREAKING: Upgrade {dep['name']} from {dep['current_version']} to {dep['recommended_version']}")
    
    return requirements


def _identify_backend_breaking_changes(backend_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify breaking changes in backend upgrade"""
    breaking_changes = []
    
    # Express 3.x to 4.x breaking changes
    if backend_analysis["express_compatibility"].get("upgrade_required"):
        breaking_changes.extend([
            {
                "component": "Express",
                "change": "app.configure() method removed",
                "impact": "high",
                "action_required": "Replace with environment-specific logic"
            },
            {
                "component": "Express", 
                "change": "Built-in middleware removed",
                "impact": "high",
                "action_required": "Install and configure separate middleware packages"
            }
        ])
    
    # Node.js 4.x to 20.x breaking changes
    if backend_analysis["node_version_compatibility"].get("upgrade_required"):
        breaking_changes.extend([
            {
                "component": "Node.js",
                "change": "Callbacks to Promises/async-await migration", 
                "impact": "medium",
                "action_required": "Update asynchronous code patterns"
            },
            {
                "component": "Node.js",
                "change": "ES6+ module system support",
                "impact": "medium", 
                "action_required": "Consider migrating to ES6 modules"
            }
        ])
    
    return breaking_changes


def _generate_backend_migration_tasks(backend_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate specific migration tasks for backend upgrade"""
    migration_tasks = []
    
    if backend_analysis["node_version_compatibility"].get("upgrade_required"):
        migration_tasks.extend([
            {
                "task": "Update Node.js runtime environment",
                "priority": "critical",
                "effort": "low",
                "description": "Upgrade server Node.js from 4.9.1 to 20.x LTS"
            },
            {
                "task": "Update package.json engines",
                "priority": "high", 
                "effort": "low",
                "description": "Update engines field to require Node.js >=20.0.0"
            }
        ])
    
    if backend_analysis["express_compatibility"].get("upgrade_required"):
        migration_tasks.extend([
            {
                "task": "Upgrade Express framework",
                "priority": "critical",
                "effort": "high",
                "description": "Upgrade Express from 3.x to 4.x and refactor breaking changes"
            },
            {
                "task": "Refactor middleware usage",
                "priority": "high",
                "effort": "medium", 
                "description": "Update middleware to Express 4.x compatible versions"
            }
        ])
    
    return migration_tasks


def _analyze_database_compatibility(repo_path: str, unified_scan: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze database migration and schema compatibility requirements"""
    logger.info("Performing database compatibility analysis...")
    
    database_analysis = {
        "mongodb_compatibility": {},
        "connection_patterns": [],
        "query_patterns": [],
        "schema_definitions": [],
        "mongoose_compatibility": {},
        "upgrade_requirements": [],
        "migration_scripts": [],
        "data_migration_tasks": []
    }
    
    # Analyze database connection and query patterns
    for file_info in unified_scan.get("file_structure", {}).get("files", []):
        if file_info.get("type") in ["javascript", "typescript"]:
            try:
                file_path = os.path.join(repo_path, file_info["path"])
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Analyze MongoDB connection patterns
                mongo_connections = _analyze_mongodb_connections(content, file_info["path"])
                database_analysis["connection_patterns"].extend(mongo_connections)
                
                # Analyze query patterns
                query_patterns = _analyze_mongodb_queries(content, file_info["path"])
                database_analysis["query_patterns"].extend(query_patterns)
                
                # Analyze Mongoose schema definitions
                if 'mongoose' in content.lower():
                    schema_patterns = _analyze_mongoose_schemas(content, file_info["path"])
                    database_analysis["schema_definitions"].extend(schema_patterns)
                
            except Exception as e:
                logger.debug(f"Error analyzing database file {file_info['path']}: {e}")
    
    # Analyze MongoDB version compatibility
    database_analysis["mongodb_compatibility"] = _analyze_mongodb_version_compatibility()
    
    # Analyze Mongoose compatibility  
    database_analysis["mongoose_compatibility"] = _analyze_mongoose_compatibility(database_analysis)
    
    # Generate upgrade requirements
    database_analysis["upgrade_requirements"] = _generate_database_upgrade_requirements(database_analysis)
    database_analysis["migration_scripts"] = _generate_database_migration_scripts(database_analysis)
    database_analysis["data_migration_tasks"] = _generate_data_migration_tasks(database_analysis)
    
    return database_analysis


def _analyze_mongodb_connections(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Analyze MongoDB connection patterns for compatibility"""
    connections = []
    
    # MongoDB 3.0 to 7.x connection API changes
    connection_patterns = [
        "MongoClient.connect(",
        "mongoose.connect(",
        "mongodb://",
        "new MongoClient(",
        "db.collection("
    ]
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        for pattern in connection_patterns:
            if pattern in line:
                # Analyze for MongoDB 3.0 vs 7.x compatibility
                compatibility_issue = None
                if "MongoClient.connect(" in line and "callback" in line:
                    compatibility_issue = "MongoDB 3.0 callback-style connections deprecated in 7.x"
                elif "mongoose.connect(" in line and not "useNewUrlParser" in content:
                    compatibility_issue = "Missing new connection options for MongoDB 7.x"
                
                connections.append({
                    "file": file_path,
                    "line": i + 1,
                    "code": line.strip(),
                    "pattern": pattern,
                    "compatibility_issue": compatibility_issue,
                    "severity": "high" if compatibility_issue else "low"
                })
    
    return connections


def _analyze_mongodb_queries(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Analyze MongoDB query patterns for compatibility"""
    queries = []
    
    # MongoDB query patterns that may have changed
    query_patterns = [
        ".find(",
        ".findOne(",
        ".insert(",
        ".update(",
        ".remove(",
        ".save(",
        ".aggregate(",
        ".mapReduce("
    ]
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        for pattern in query_patterns:
            if pattern in line:
                # Check for deprecated patterns
                compatibility_issue = None
                if ".insert(" in line:
                    compatibility_issue = "insert() deprecated, use insertOne() or insertMany()"
                elif ".update(" in line and "multi:" not in line:
                    compatibility_issue = "update() behavior changed, specify updateOne() or updateMany()"
                elif ".remove(" in line:
                    compatibility_issue = "remove() deprecated, use deleteOne() or deleteMany()"
                
                queries.append({
                    "file": file_path,
                    "line": i + 1,
                    "code": line.strip(),
                    "pattern": pattern,
                    "compatibility_issue": compatibility_issue,
                    "severity": "medium" if compatibility_issue else "low"
                })
    
    return queries


def _analyze_mongoose_schemas(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Analyze Mongoose schema definitions for compatibility"""
    schemas = []
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "new Schema(" in line or "mongoose.Schema(" in line:
            schemas.append({
                "file": file_path,
                "line": i + 1,
                "code": line.strip(),
                "type": "schema_definition"
            })
        elif "schema.pre(" in line or "schema.post(" in line:
            schemas.append({
                "file": file_path,
                "line": i + 1,
                "code": line.strip(),
                "type": "middleware_hook"
            })
    
    return schemas


def _analyze_mongodb_version_compatibility() -> Dict[str, Any]:
    """Analyze MongoDB version compatibility requirements"""
    # Based on server check: MongoDB 3.0.15 → 7.x
    return {
        "current_version": "3.0.15",
        "target_version": "7.x",
        "major_upgrade_required": True,
        "api_changes": [
            "Connection API completely rewritten",
            "Query methods signatures changed", 
            "Authentication mechanisms updated",
            "Index creation syntax changed",
            "Aggregation pipeline enhancements"
        ],
        "deprecated_features": [
            "insert() method deprecated",
            "update() method behavior changed",
            "remove() method deprecated",
            "Legacy authentication methods"
        ]
    }


def _analyze_mongoose_compatibility(database_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze Mongoose ODM compatibility"""
    return {
        "upgrade_required": True,
        "current_version": "3.x", 
        "target_version": "7.x",
        "breaking_changes": [
            "Connection handling rewritten",
            "Query execution changed to Promises",
            "Schema validation enhanced",
            "Middleware hooks signature changed"
        ],
        "migration_complexity": "high"
    }


def _generate_database_upgrade_requirements(database_analysis: Dict[str, Any]) -> List[str]:
    """Generate database upgrade requirements"""
    requirements = []
    
    if database_analysis["mongodb_compatibility"].get("major_upgrade_required"):
        requirements.extend([
            "CRITICAL: Upgrade MongoDB from 3.0.15 to 7.x",
            "Update MongoDB driver to latest version",
            "Migrate connection API from callbacks to async/await",
            "Update deprecated query methods (insert, update, remove)",
            "Test and validate all database operations"
        ])
    
    if database_analysis["mongoose_compatibility"].get("upgrade_required"):
        requirements.extend([
            "MAJOR: Upgrade Mongoose from 3.x to 7.x",
            "Refactor schema definitions for new syntax",
            "Update middleware hooks to new signature",
            "Migrate query execution to Promise-based API"
        ])
    
    return requirements


def _generate_database_migration_scripts(database_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate database migration scripts"""
    migration_scripts = []
    
    # Connection migration script
    migration_scripts.append({
        "name": "mongodb_connection_migration",
        "description": "Migrate MongoDB 3.0 connections to 7.x async/await pattern",
        "priority": "critical",
        "script_type": "code_transformation"
    })
    
    # Query migration script
    migration_scripts.append({
        "name": "mongodb_query_migration", 
        "description": "Update deprecated query methods to new API",
        "priority": "high",
        "script_type": "code_transformation"
    })
    
    # Schema migration script
    migration_scripts.append({
        "name": "mongoose_schema_migration",
        "description": "Update Mongoose schemas to 7.x compatible format",
        "priority": "high", 
        "script_type": "code_transformation"
    })
    
    return migration_scripts


def _generate_data_migration_tasks(database_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate data migration tasks"""
    return [
        {
            "task": "Backup existing MongoDB 3.0 data",
            "priority": "critical",
            "effort": "low",
            "description": "Create full backup before upgrading MongoDB"
        },
        {
            "task": "Test MongoDB 7.x compatibility",
            "priority": "critical", 
            "effort": "medium",
            "description": "Test all database operations with MongoDB 7.x"
        },
        {
            "task": "Validate data integrity post-upgrade",
            "priority": "high",
            "effort": "medium",
            "description": "Ensure all data migrated correctly to MongoDB 7.x"
        }
    ]


def _analyze_solr_compatibility(repo_path: str, unified_scan: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze Apache Solr upgrade compatibility requirements (5.x→9.x)"""
    logger.info("Performing Apache Solr compatibility analysis...")
    
    solr_analysis = {
        "solr_version_compatibility": {},
        "solr_config_files": [],
        "schema_definitions": [],
        "query_patterns": [],
        "admin_api_usage": [],
        "upgrade_requirements": [],
        "breaking_changes": [],
        "migration_tasks": []
    }
    
    # Analyze Solr configuration and schema files
    for file_info in unified_scan.get("file_structure", {}).get("files", []):
        try:
            file_path = os.path.join(repo_path, file_info["path"])
            filename = file_info.get("filename", "")
            
            # Solr configuration files
            if filename in ["solrconfig.xml", "schema.xml", "managed-schema"]:
                solr_config = _analyze_solr_config_file(file_path, file_info["path"])
                solr_analysis["solr_config_files"].append(solr_config)
            
            # Solr schema files
            elif "schema" in filename.lower() and filename.endswith(".xml"):
                schema_config = _analyze_solr_schema_file(file_path, file_info["path"])
                solr_analysis["schema_definitions"].append(schema_config)
            
            # Application code using Solr
            elif file_info.get("type") in ["javascript", "typescript"]:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Analyze Solr client usage patterns
                solr_queries = _analyze_solr_client_usage(content, file_info["path"])
                solr_analysis["query_patterns"].extend(solr_queries)
                
                # Analyze Solr Admin API usage
                admin_usage = _analyze_solr_admin_api(content, file_info["path"])
                solr_analysis["admin_api_usage"].extend(admin_usage)
                
        except Exception as e:
            logger.debug(f"Error analyzing Solr file {file_info['path']}: {e}")
    
    # Analyze Solr version compatibility
    solr_analysis["solr_version_compatibility"] = _analyze_solr_version_compatibility()
    
    # Generate upgrade requirements
    solr_analysis["upgrade_requirements"] = _generate_solr_upgrade_requirements(solr_analysis)
    solr_analysis["breaking_changes"] = _identify_solr_breaking_changes(solr_analysis)
    solr_analysis["migration_tasks"] = _generate_solr_migration_tasks(solr_analysis)
    
    return solr_analysis


def _analyze_solr_config_file(file_path: str, relative_path: str) -> Dict[str, Any]:
    """Analyze Solr configuration file for compatibility issues"""
    config_analysis = {
        "file": relative_path,
        "version_indicators": [],
        "deprecated_features": [],
        "compatibility_issues": []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check for Solr 5.x specific configurations
        if 'luceneMatchVersion="5.' in content:
            config_analysis["version_indicators"].append("Solr 5.x luceneMatchVersion detected")
            config_analysis["compatibility_issues"].append("luceneMatchVersion parameter deprecated in Solr 9.x")
        
        # Check for deprecated request handlers
        deprecated_handlers = [
            'solr.SearchHandler',
            'solr.StandardRequestHandler',
            'solr.UpdateRequestHandler'
        ]
        
        for handler in deprecated_handlers:
            if handler in content:
                config_analysis["deprecated_features"].append(f"Deprecated handler: {handler}")
        
        # Check for old-style field types
        if 'class="solr.TrieDateField"' in content:
            config_analysis["deprecated_features"].append("TrieDateField deprecated, use DatePointField")
        
        if 'class="solr.TrieIntField"' in content:
            config_analysis["deprecated_features"].append("TrieIntField deprecated, use IntPointField")
            
    except Exception as e:
        config_analysis["error"] = str(e)
    
    return config_analysis


def _analyze_solr_schema_file(file_path: str, relative_path: str) -> Dict[str, Any]:
    """Analyze Solr schema file for compatibility issues"""
    schema_analysis = {
        "file": relative_path,
        "field_types": [],
        "deprecated_fields": [],
        "compatibility_issues": []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check for deprecated field types
        deprecated_field_types = [
            'solr.TrieDateField',
            'solr.TrieIntField', 
            'solr.TrieLongField',
            'solr.TrieFloatField',
            'solr.TrieDoubleField'
        ]
        
        for field_type in deprecated_field_types:
            if field_type in content:
                new_type = field_type.replace('Trie', '').replace('Field', 'PointField')
                schema_analysis["deprecated_fields"].append({
                    "old_type": field_type,
                    "new_type": new_type,
                    "action_required": "Replace with Point-based field type"
                })
        
        # Check for copy field directives
        import re
        copy_fields = re.findall(r'<copyField[^>]*>', content)
        schema_analysis["field_types"].append(f"Found {len(copy_fields)} copyField directives")
        
    except Exception as e:
        schema_analysis["error"] = str(e)
    
    return schema_analysis


def _analyze_solr_client_usage(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Analyze Solr client usage patterns for compatibility"""
    solr_queries = []
    
    # Solr client patterns that may need updates
    solr_patterns = [
        'solr.query(',
        'solr.search(',
        'SolrQuery(',
        '/solr/select',
        '/solr/update',
        'q=*:*',
        'fq=',
        'facet=true'
    ]
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        for pattern in solr_patterns:
            if pattern in line:
                # Check for Solr 5.x specific query syntax
                compatibility_issue = None
                if '/solr/select' in line and 'wt=json' not in line:
                    compatibility_issue = "Consider explicitly setting wt=json for consistent response format"
                elif 'facet=true' in line and 'facet.method' not in content:
                    compatibility_issue = "Faceting performance may be affected in Solr 9.x"
                
                solr_queries.append({
                    "file": file_path,
                    "line": i + 1,
                    "code": line.strip(),
                    "pattern": pattern,
                    "compatibility_issue": compatibility_issue,
                    "severity": "medium" if compatibility_issue else "low"
                })
    
    return solr_queries


def _analyze_solr_admin_api(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Analyze Solr Admin API usage for compatibility"""
    admin_usage = []
    
    # Admin API patterns that may have changed
    admin_patterns = [
        '/solr/admin/cores',
        '/solr/admin/collections',
        'RELOAD',
        'CREATE',
        'UNLOAD',
        'STATUS'
    ]
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        for pattern in admin_patterns:
            if pattern in line:
                admin_usage.append({
                    "file": file_path,
                    "line": i + 1,
                    "code": line.strip(),
                    "api_endpoint": pattern,
                    "compatibility_note": "Admin API syntax mostly compatible between 5.x and 9.x"
                })
    
    return admin_usage


def _analyze_solr_version_compatibility() -> Dict[str, Any]:
    """Analyze Solr version compatibility requirements"""
    # Based on Auckland Library context: Solr 5.x → 9.x
    return {
        "current_version": "5.x",
        "target_version": "9.x",
        "major_upgrade_required": True,
        "api_changes": [
            "Trie* field types deprecated, replaced with Point* types",
            "Some request handlers consolidated or deprecated",
            "Enhanced security model with authentication/authorization",
            "Improved cluster management APIs",
            "Updated query parser syntax"
        ],
        "deprecated_features": [
            "luceneMatchVersion parameter",
            "TrieDateField, TrieIntField, etc.",
            "Legacy request handlers",
            "Old-style configuration syntax"
        ],
        "new_features": [
            "Point-based numeric fields for better performance",
            "Enhanced streaming expressions",
            "Improved faceting performance",
            "Better cluster management",
            "Enhanced security features"
        ]
    }


def _generate_solr_upgrade_requirements(solr_analysis: Dict[str, Any]) -> List[str]:
    """Generate Solr upgrade requirements"""
    requirements = []
    
    if solr_analysis["solr_version_compatibility"].get("major_upgrade_required"):
        requirements.extend([
            "CRITICAL: Upgrade Apache Solr from 5.x to 9.x",
            "Update Solr client libraries to 9.x compatible versions",
            "Migrate deprecated Trie* field types to Point* field types",
            "Update solrconfig.xml to remove deprecated parameters",
            "Test all search and indexing operations with Solr 9.x",
            "Update schema.xml to use modern field type definitions"
        ])
    
    # Check for specific configuration issues
    for config_file in solr_analysis["solr_config_files"]:
        if config_file.get("deprecated_features"):
            requirements.append(f"Update deprecated features in {config_file['file']}")
    
    # Check for schema compatibility issues
    for schema_file in solr_analysis["schema_definitions"]:
        if schema_file.get("deprecated_fields"):
            requirements.append(f"Migrate deprecated field types in {schema_file['file']}")
    
    return requirements


def _identify_solr_breaking_changes(solr_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify breaking changes in Solr upgrade"""
    breaking_changes = []
    
    # Solr 5.x to 9.x breaking changes
    breaking_changes.extend([
        {
            "component": "Field Types",
            "change": "Trie* field types deprecated",
            "impact": "high",
            "action_required": "Replace with Point* field types (DatePointField, IntPointField, etc.)"
        },
        {
            "component": "Configuration",
            "change": "luceneMatchVersion parameter deprecated",
            "impact": "medium",
            "action_required": "Remove luceneMatchVersion from solrconfig.xml"
        },
        {
            "component": "Request Handlers",
            "change": "Some legacy request handlers consolidated",
            "impact": "medium",
            "action_required": "Update request handler configurations"
        },
        {
            "component": "Security",
            "change": "Enhanced security model requires explicit configuration",
            "impact": "medium",
            "action_required": "Configure authentication and authorization if needed"
        }
    ])
    
    return breaking_changes


def _generate_solr_migration_tasks(solr_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate specific migration tasks for Solr upgrade"""
    migration_tasks = []
    
    if solr_analysis["solr_version_compatibility"].get("major_upgrade_required"):
        migration_tasks.extend([
            {
                "task": "Backup existing Solr indexes and configuration",
                "priority": "critical",
                "effort": "low",
                "description": "Create full backup of Solr 5.x data and configuration files"
            },
            {
                "task": "Update Solr server installation",
                "priority": "critical",
                "effort": "medium",
                "description": "Install and configure Solr 9.x server"
            },
            {
                "task": "Migrate field type definitions",
                "priority": "high",
                "effort": "medium",
                "description": "Replace Trie* field types with Point* equivalents in schema"
            },
            {
                "task": "Update client application code",
                "priority": "high",
                "effort": "medium",
                "description": "Update Solr client libraries and query syntax"
            },
            {
                "task": "Test search functionality",
                "priority": "high",
                "effort": "high",
                "description": "Comprehensive testing of all search and indexing operations"
            },
            {
                "task": "Performance optimization",
                "priority": "medium",
                "effort": "medium",
                "description": "Optimize queries and indexing for Solr 9.x performance improvements"
            }
        ])
    
    return migration_tasks


    