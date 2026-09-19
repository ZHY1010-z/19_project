#!/usr/bin/env python3
"""
Optimized Prompt Templates - Keep all functionality, reduce tokens by 80%
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class PromptType(Enum):
    ANALYSIS = "analysis"
    PLANNING = "planning"
    TRANSFORMATION = "transformation"
    MIGRATION = "migration"
    VALIDATION = "validation"
    DOCUMENTATION = "documentation"

@dataclass
class OptimizedPromptContext:
    """Streamlined context for prompt generation"""
    agent_name: str
    phase: str
    cycle_number: Optional[int] = None
    project_config: Optional[Dict[str, Any]] = None
    compressed_context: Optional[Dict[str, Any]] = None  # Use compressed context instead of full data
    feedback: Optional[str] = None
    target_format: str = "json"

class OptimizedPromptEngine:
    """Token-efficient prompt engine preserving all analysis capabilities"""
    
    def __init__(self):
        self.system_prompts = self._init_system_prompts()
        self.user_templates = self._init_user_templates()
    
    def _init_system_prompts(self) -> Dict[str, str]:
        """Concise system prompts - reduced from 1000+ to ~200 tokens each"""
        return {
            "CodeUnderstandingAgent": """Expert legacy code analyst. Analyze codebase for modernization.
Skills: AST analysis, dependency mapping, security assessment, architecture evaluation.
Output: Structured JSON with key findings, security issues, modernization priorities.""",

            "StrategicPlanningAgent": """Migration strategy specialist. Create practical modernization plans.
Skills: Risk assessment, timeline estimation, resource planning, technology selection.
Output: Actionable migration strategy with phases, priorities, effort estimates.""",

            "ValidationAgent": """Strategy validation expert. Assess migration plan feasibility.
Skills: Risk analysis, compatibility checking, constraint validation.
Output: Validation results with approval/rejection and improvement suggestions.""",

            "DocumentationAgent": """Technical documentation specialist. Generate clear implementation guides.
Skills: Strategy documentation, step-by-step guides, requirement specifications.
Output: Comprehensive documentation for development teams.""",

            "TransformationAgent": """Code transformation expert. Modernize legacy patterns.
Skills: Refactoring, pattern updates, dependency upgrades, security improvements.
Output: ONLY pure code content without explanations, markers, or status indicators."""
        }
    
    def _init_user_templates(self) -> Dict[str, str]:
        """Compressed user prompt templates"""
        return {
            "analysis": """LEGACY CODE ANALYSIS
Project: {repo_path}
Target: {target_platform}

CODE CONTEXT:
{compressed_data}

ANALYZE:
1. Technology stack & versions
2. Security vulnerabilities (severity levels)
3. Architecture patterns & complexity 
4. Modernization readiness score (0-10)
5. Critical migration blockers

OUTPUT: JSON with analysis results""",

            "planning": """MIGRATION STRATEGY PLANNING
Project Analysis: {compressed_data}
Target: {target_platform}

PLAN:
1. Migration approach (incremental/full/hybrid)
2. Phase breakdown with priorities
3. Effort estimation (hours)
4. Risk assessment & mitigation
5. Success criteria

OUTPUT: JSON migration strategy""",

            "validation": """STRATEGY VALIDATION
Current Strategy: {strategy_summary}
Project Context: {compressed_data}
{feedback_context}

VALIDATE:
1. Technical feasibility
2. Risk acceptability  
3. Resource requirements
4. Timeline realism
5. Success probability

CRITICAL: You must provide a clear decision using one of these keywords:
- APPROVED/ACCEPTABLE/FEASIBLE for good strategies
- REJECTED/UNACCEPTABLE/INFEASIBLE for problematic strategies

OUTPUT: JSON with clear decision (use keywords above)""",

            "documentation": """STRATEGY DOCUMENTATION
Project: {project_summary}
Strategy: {migration_approach}
Key Points: {key_recommendations}

DOCUMENT:
1. Executive summary
2. Implementation phases
3. Technical requirements
4. Risk mitigation plans
5. Success metrics

OUTPUT: Structured documentation""",

            "transformation": """CODE TRANSFORMATION GUIDANCE
Target: {target_tech}
Scope: {transformation_scope}
Patterns: {code_patterns}

RECOMMEND:
1. Priority transformation areas
2. Modern pattern replacements
3. Dependency upgrade path
4. Security improvements
5. Testing strategy

CRITICAL: Output COMPLETE code. Never truncate.
If approaching limit, prioritize main functionality.
Output ONLY valid code content without any additional text, markers, or comments.
Never include completion markers, status indicators, or explanatory text.

OUTPUT: Pure code content only""",

            "database_migration": """DATABASE MIGRATION ANALYSIS
Current: {current_db} → Target: {target_db}
Complexity: {migration_complexity}
Schema Files: {schema_files}

ANALYZE:
1. Migration strategy
2. Schema conversion approach
3. Data integrity risks
4. Performance impact
5. Rollback procedures

OUTPUT: JSON database migration plan""",

            "migration_execution": """MIGRATION EXECUTION PLAN
Type: {migration_type}
Priority Files: {priority_files}
Dependencies: {dependencies_order}

PLAN:
1. Execution sequence
2. Testing checkpoints
3. Rollback triggers
4. Monitoring requirements
5. Success validation

OUTPUT: JSON execution plan"""
        }
    
    def get_optimized_prompt(self, context: OptimizedPromptContext) -> Tuple[str, str]:
        """Generate optimized prompt pair with minimal tokens"""
        
        # Get system prompt
        system_prompt = self.system_prompts.get(
            context.agent_name, 
            "Expert analyst. Provide structured analysis in JSON format."
        )
        
        # Determine template based on phase
        template_key = self._map_phase_to_template(context.phase)
        user_template = self.user_templates.get(template_key, self.user_templates["analysis"])
        
        # Fill template with compressed data
        user_prompt = self._fill_template(user_template, context)
        
        return system_prompt, user_prompt
    
    def _map_phase_to_template(self, phase: str) -> str:
        """Map phase to appropriate template"""
        phase_mapping = {
            "analysis": "analysis",
            "planning": "planning", 
            "strategy_planning": "planning",
            "validation": "validation",
            "strategy_validation": "validation",
            "documentation": "documentation",
            "strategy_documentation": "documentation", 
            "transformation": "transformation",
            "database": "database_migration",
            "migration": "migration_execution"
        }
        return phase_mapping.get(phase, "analysis")
    
    def _fill_template(self, template: str, context: OptimizedPromptContext) -> str:
        """Fill template with compressed context data"""
        
        # Extract compressed data
        compressed = context.compressed_context or {}
        
        # Create template variables
        variables = {
            "repo_path": context.project_config.get("repository_path", "") if context.project_config else "",
            "target_platform": context.project_config.get("target_platform", "modern_nodejs") if context.project_config else "modern_nodejs",
            "compressed_data": self._format_compressed_data(compressed),
            "feedback_context": f"\nFeedback: {context.feedback}" if context.feedback else "",
            
            # Planning specific
            "strategy_summary": compressed.get("strategy_summary", ""),
            "project_summary": compressed.get("project_summary", ""),
            "migration_approach": compressed.get("migration_approach", ""),
            "key_recommendations": ", ".join(compressed.get("key_recommendations", [])),
            
            # Transformation specific  
            "target_tech": compressed.get("target_tech", "modern_nodejs"),
            "transformation_scope": ", ".join(compressed.get("transformation_scope", [])),
            "code_patterns": ", ".join(compressed.get("code_patterns", [])),
            
            # Database specific
            "current_db": compressed.get("current_db", ""),
            "target_db": compressed.get("target_db", ""),
            "migration_complexity": compressed.get("migration_complexity", ""),
            "schema_files": ", ".join(compressed.get("schema_files", [])),
            
            # Migration specific
            "migration_type": compressed.get("migration_type", ""),
            "priority_files": ", ".join(compressed.get("priority_files", [])),
            "dependencies_order": ", ".join(compressed.get("dependencies_order", []))
        }
        
        # Fill template, handle missing keys gracefully
        try:
            return template.format(**variables)
        except KeyError as e:
            # If key is missing, replace with empty string
            for key in variables:
                template = template.replace("{" + key + "}", variables[key])
            return template
    
    def _format_compressed_data(self, context_data: Dict[str, Any]) -> str:
        """Format context data for prompt inclusion"""
        
        if not context_data:
            return "No analysis data available"
        
        # Format different types of context data
        formatted_parts = []
        
        # Extract from repository analysis if available
        repo_analysis = context_data.get("repository_analysis", {})
        
        # Languages
        if "programming_languages" in repo_analysis:
            langs = repo_analysis["programming_languages"]
            langs_str = ", ".join([f"{k}({v})" for k, v in langs.items()])
            formatted_parts.append(f"Languages: {langs_str}")
        elif "langs" in context_data:  # Fallback to compressed format
            langs_str = ", ".join([f"{k}({v})" for k, v in context_data["langs"].items()])
            formatted_parts.append(f"Languages: {langs_str}")
        
        # Frameworks
        if "frameworks_detected" in repo_analysis:
            fw_str = ", ".join(repo_analysis["frameworks_detected"])
            formatted_parts.append(f"Frameworks: {fw_str}")
        elif "frameworks" in context_data:  # Fallback to compressed format
            fw_str = ", ".join(context_data["frameworks"])
            formatted_parts.append(f"Frameworks: {fw_str}")
        
        # File statistics
        if "total_files" in repo_analysis:
            formatted_parts.append(f"Files: {repo_analysis.get('total_files', 0)} total")
        elif "files" in context_data:  # Fallback to compressed format
            files = context_data["files"]
            formatted_parts.append(f"Files: {files.get('total', 0)} total, {files.get('js', 0)} JS")
        
        # Security issues (if available)
        if "security_analysis" in repo_analysis:
            sec = repo_analysis["security_analysis"]
            if sec and isinstance(sec, dict):
                sec_count = len(sec.get("issues", []))
                if sec_count > 0:
                    formatted_parts.append(f"Security: {sec_count} issues")
        elif "sec_issues" in context_data:  # Fallback to compressed format
            sec = context_data["sec_issues"]
            if sec:
                sec_str = ", ".join([f"{k}:{v}" for k, v in sec.items()])
                formatted_parts.append(f"Security: {sec_str}")
        
        # Add other relevant information from context
        if "modernization_readiness" in context_data:
            formatted_parts.append(f"Modernization Readiness: {context_data['modernization_readiness']}")
        
        return " | ".join(formatted_parts) if formatted_parts else str(context_data)[:200]

# Backward compatibility functions for existing framework.py
def get_analysis_prompt(context) -> Tuple[str, str]:
    """Backward compatible analysis prompt generation"""
    engine = OptimizedPromptEngine()
    
    # Convert old context to new format
    optimized_context = _convert_legacy_context(context, "analysis")
    
    return engine.get_optimized_prompt(optimized_context)

def get_planning_prompt(context) -> Tuple[str, str]:
    """Backward compatible planning prompt generation"""
    engine = OptimizedPromptEngine()
    optimized_context = _convert_legacy_context(context, "planning")
    return engine.get_optimized_prompt(optimized_context)

def get_validation_prompt(context) -> Tuple[str, str]:
    """Backward compatible validation prompt generation"""
    engine = OptimizedPromptEngine()
    optimized_context = _convert_legacy_context(context, "validation")
    return engine.get_optimized_prompt(optimized_context)

def get_documentation_prompt(context) -> Tuple[str, str]:
    """Backward compatible documentation prompt generation"""
    engine = OptimizedPromptEngine()
    optimized_context = _convert_legacy_context(context, "documentation")
    return engine.get_optimized_prompt(optimized_context)

def get_transformation_prompt(context) -> Tuple[str, str]:
    """Backward compatible transformation prompt generation"""
    engine = OptimizedPromptEngine()
    optimized_context = _convert_legacy_context(context, "transformation")
    return engine.get_optimized_prompt(optimized_context)

def get_migration_prompt(context) -> Tuple[str, str]:
    """Backward compatible migration prompt generation"""
    engine = OptimizedPromptEngine()
    optimized_context = _convert_legacy_context(context, "migration")
    return engine.get_optimized_prompt(optimized_context)

def _convert_legacy_context(legacy_context, phase: str) -> OptimizedPromptContext:
    """Convert legacy PromptContext to OptimizedPromptContext"""
    
    # Extract full context data
    full_context_data = {}
    
    if hasattr(legacy_context, 'repo_analysis'):
        full_context_data["repository_analysis"] = legacy_context.repo_analysis
    
    if hasattr(legacy_context, 'previous_results'):
        full_context_data.update(legacy_context.previous_results or {})
    
    return OptimizedPromptContext(
        agent_name=getattr(legacy_context, 'agent_name', 'CodeUnderstandingAgent'),
        phase=getattr(legacy_context, 'phase', phase),
        cycle_number=getattr(legacy_context, 'cycle_number', None),
        project_config=getattr(legacy_context, 'project_config', None),
        compressed_context=full_context_data,
        feedback=getattr(legacy_context, 'feedback', None)
    )

if __name__ == "__main__":
    # Test the optimized templates
    
    sample_context = {
        "repository_analysis": {
            "programming_languages": {"javascript": 45, "python": 12},
            "frameworks_detected": ["express", "mongoose"], 
            "total_files": 156
        }
    }
    
    context = OptimizedPromptContext(
        agent_name="CodeUnderstandingAgent",
        phase="analysis",
        compressed_context=sample_context,
        project_config={"repository_path": "/test/repo", "target_platform": "modern_nodejs"}
    )
    
    engine = OptimizedPromptEngine()
    system, user = engine.get_optimized_prompt(context)
    
    print("System Prompt Length:", len(system))
    print("User Prompt Length:", len(user))
    print("\nUser Prompt:")
    print(user)