#!/usr/bin/env python3
"""
Prompt Usage Examples for Auckland Library Multi-Agent Framework

Demonstrates how to effectively use the prompt template system in various scenarios.
"""

import asyncio
from prompt_templates import PromptTemplateEngine, PromptContext
from util import llm_call

async def example_basic_usage():
    """Example 1: Basic prompt generation for CodeUnderstandingAgent"""
    
    print("=== Example 1: Basic Prompt Generation ===")
    
    # Create basic context
    context = PromptContext(
        agent_name="CodeUnderstandingAgent",
        phase="analysis",
        project_config={
            "project_name": "Auckland Library System",
            "legacy_repo_path": "/path/to/legacy/library/system",
            "target_stack": "Node.js + MongoDB + Solr",
            "client": "Jing Sun"
        }
    )
    
    # Generate prompts
    engine = PromptTemplateEngine()
    system_prompt, user_prompt = engine.generate_prompt("CodeUnderstandingAgent", context)
    
    print("Generated System Prompt:")
    print(system_prompt[:200] + "...")
    print("\nGenerated User Prompt:")
    print(user_prompt[:300] + "...")
    
    # Call LLM (placeholder)
    response = await llm_call(system_prompt, user_prompt, "CodeUnderstandingAgent")
    print(f"\nLLM Response: {response}")

async def example_iterative_improvement():
    """Example 2: Iterative improvement with feedback"""
    
    print("\n=== Example 2: Iterative Improvement Cycle ===")
    
    # Simulate feedback from previous cycle
    feedback = {
        "failed_areas": ["Integration testing", "Performance testing"],
        "recommendations": [
            "Fix API integration issues",
            "Optimize error handling and resource management"
        ],
        "priority_fixes": [
            "Address failing integration tests",
            "Reduce error rate in load testing"
        ],
        "next_cycle_focus": ["API stability", "Performance optimization"]
    }
    
    # Previous results context
    previous_results = {
        "migration_strategy": "incremental_modernization",
        "code_transformation": {
            "files_modified": 23,
            "status": "partially_successful"
        }
    }
    
    # Create context for Cycle 2
    context = PromptContext(
        agent_name="CodemodAgent",
        phase="execution",
        cycle_number=2,
        feedback=feedback,
        previous_results=previous_results,
        project_config={
            "target_stack": "Node.js + MongoDB + Solr"
        }
    )
    
    # Generate cycle-aware prompts
    engine = PromptTemplateEngine()
    system_prompt, user_prompt = engine.generate_prompt("CodemodAgent", context)
    
    print("Feedback-Enhanced User Prompt:")
    print(user_prompt[:500] + "...")
    
    # Call LLM with feedback context
    response = await llm_call(system_prompt, user_prompt, "CodemodAgent")
    print(f"\nCycle 2 Response: {response}")

async def example_validation_with_criteria():
    """Example 3: Validation agent with comprehensive criteria"""
    
    print("\n=== Example 3: Validation with Criteria ===")
    
    # Mock execution results
    execution_results = {
        "code_transformation": {
            "files_modified": 25,
            "build_status": "successful",
            "test_coverage": "87.3%"
        },
        "data_migration": {
            "records_migrated": 125000,
            "data_integrity": "100%",
            "performance_improvement": "35%"
        }
    }
    
    context = PromptContext(
        agent_name="ValidationAgent",
        phase="validation",
        cycle_number=1,
        previous_results=execution_results,
        target_format="json"
    )
    
    engine = PromptTemplateEngine()
    system_prompt, user_prompt = engine.generate_prompt("ValidationAgent", context)
    
    print("Validation User Prompt (showing criteria section):")
    # Extract criteria section
    criteria_start = user_prompt.find("VALIDATION CRITERIA")
    if criteria_start != -1:
        criteria_section = user_prompt[criteria_start:criteria_start + 800]
        print(criteria_section + "...")
    
    response = await llm_call(system_prompt, user_prompt, "ValidationAgent")
    print(f"\nValidation Response: {response}")

async def example_documentation_comprehensive():
    """Example 4: Comprehensive documentation generation"""
    
    print("\n=== Example 4: Comprehensive Documentation ===")
    
    # Complete workflow results
    all_results = {
        "analysis": {
            "repository_analysis": "completed",
            "modernization_readiness": 75
        },
        "planning": {
            "migration_strategy": "incremental_approach",
            "timeline": "8-10 weeks"
        },
        "execution": {
            "cycles_completed": 2,
            "final_status": "accepted"
        },
        "validation": {
            "overall_score": 94.2,
            "acceptance_criteria_met": True
        }
    }
    
    context = PromptContext(
        agent_name="DocumentationAgent",
        phase="documentation",
        previous_results=all_results,
        project_config={
            "project_name": "Auckland Library System Modernization",
            "client": "Jing Sun"
        }
    )
    
    engine = PromptTemplateEngine()
    system_prompt, user_prompt = engine.generate_prompt("DocumentationAgent", context)
    
    print("Documentation Scope (from user prompt):")
    scope_start = user_prompt.find("DOCUMENTATION SCOPE:")
    if scope_start != -1:
        scope_section = user_prompt[scope_start:scope_start + 600]
        print(scope_section + "...")
    
    response = await llm_call(system_prompt, user_prompt, "DocumentationAgent")
    print(f"\nDocumentation Response: {response}")

async def example_custom_context():
    """Example 5: Custom context handling"""
    
    print("\n=== Example 5: Custom Context Handling ===")
    
    class CustomPromptEngine(PromptTemplateEngine):
        """Extended engine with custom context handling"""
        
        def _generate_context_instructions(self, context: PromptContext) -> str:
            instructions = super()._generate_context_instructions(context)
            
            # Add custom Auckland Library specific instructions
            if context.agent_name == "ModernizationPlannerAgent":
                library_instructions = """
AUCKLAND LIBRARY SPECIFIC REQUIREMENTS:
- Maintain 99.9% uptime during business hours (9 AM - 6 PM)
- Preserve patron privacy and data security (GDPR compliance)
- Ensure compatibility with existing RFID book tracking system
- Minimize disruption to daily checkout/return operations
- Support for both staff and patron self-service terminals"""
                instructions += library_instructions
            
            return instructions
    
    # Use custom engine
    custom_engine = CustomPromptEngine()
    
    context = PromptContext(
        agent_name="ModernizationPlannerAgent",
        phase="planning",
        project_config={
            "project_name": "Auckland Library System",
            "client": "Jing Sun"
        }
    )
    
    system_prompt, user_prompt = custom_engine.generate_prompt("ModernizationPlannerAgent", context)
    
    print("Custom Context Instructions:")
    instructions_start = user_prompt.find("AUCKLAND LIBRARY SPECIFIC")
    if instructions_start != -1:
        custom_section = user_prompt[instructions_start:instructions_start + 400]
        print(custom_section + "...")

async def example_prompt_optimization():
    """Example 6: Prompt optimization techniques"""
    
    print("\n=== Example 6: Prompt Optimization Techniques ===")
    
    # Demonstrate different target formats
    formats = ["json", "xml", "yaml"]
    
    for format_type in formats:
        context = PromptContext(
            agent_name="CodeUnderstandingAgent",
            phase="analysis",
            target_format=format_type,
            project_config={"legacy_repo_path": "/test/repo"}
        )
        
        engine = PromptTemplateEngine()
        _, user_prompt = engine.generate_prompt("CodeUnderstandingAgent", context)
        
        # Extract format instruction
        format_start = user_prompt.find("OUTPUT FORMAT:")
        if format_start != -1:
            format_section = user_prompt[format_start:format_start + 200]
            print(f"\n{format_type.upper()} Format Instructions:")
            print(format_section)

def show_prompt_statistics():
    """Example 7: Prompt statistics and analysis"""
    
    print("\n=== Example 7: Prompt Statistics ===")
    
    engine = PromptTemplateEngine()
    
    # Analyze all agent templates
    for agent_name in engine.templates.keys():
        context = PromptContext(
            agent_name=agent_name,
            phase="test",
            project_config={"legacy_repo_path": "/test"}
        )
        
        system_prompt, user_prompt = engine.generate_prompt(agent_name, context)
        
        print(f"\n{agent_name}:")
        print(f"  System Prompt: {len(system_prompt)} characters")
        print(f"  User Prompt: {len(user_prompt)} characters")
        print(f"  Total: {len(system_prompt) + len(user_prompt)} characters")
        
        # Count key components
        competencies = system_prompt.count("COMPETENCIES")
        frameworks = system_prompt.count("FRAMEWORK")
        standards = system_prompt.count("STANDARDS")
        
        print(f"  Components: {competencies} competencies, {frameworks} frameworks, {standards} standards")

async def main():
    """Run all examples"""
    
    print("🎯 Auckland Library Multi-Agent Prompt Engineering Examples")
    print("=" * 80)
    
    try:
        await example_basic_usage()
        await example_iterative_improvement()
        await example_validation_with_criteria()
        await example_documentation_comprehensive()
        await example_custom_context()
        await example_prompt_optimization()
        show_prompt_statistics()
        
        print("\n" + "=" * 80)
        print("✅ All examples completed successfully!")
        print("💡 These examples demonstrate the flexibility and power of the prompt template system.")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())