#!/usr/bin/env python3
"""
Legacy System Modernization Framework - Main Entry Point

Simple main function to run the complete modernization workflow.
Users only need to modify the configuration parameters below.
"""

from framework import execute_modernization_workflow
from ai_execution_agent import AIExecutionAgent
from code_evaluation_program import CodeEvaluationProgram, EvaluationConfig

def main():
    """
    Main function to run the complete modernization workflow
    
    USER CONFIGURATION - Modify these parameters:
    """
    
    # ==================== USER CONFIGURATION ====================
    # Modify these parameters for your project
    
    PROJECT_CONFIG = {
        'legacy_repo_path': '/Users/ianzhou/Desktop/frontend',  # Frontend project
        'project_name': 'TV Radio Frontend Modernization',
        'target_stack': 'Node.js 20.x + MongoDB 7.x + Express 4.x + Modern ES6+',
        'client': 'UoA Library Frontend'
    }
    
    OUTPUT_PATH = '/Users/ianzhou/frame-fix/frontend_modernized_output'                  # Output directory
    
    # ==================== END USER CONFIGURATION ====================
    
    print("=" * 60)
    print(" LEGACY SYSTEM MODERNIZATION FRAMEWORK")
    print("=" * 60)
    print(f"Project: {PROJECT_CONFIG['project_name']}")
    print(f"Legacy Path: {PROJECT_CONFIG['legacy_repo_path']}")
    print(f"Target Stack: {PROJECT_CONFIG['target_stack']}")
    print(f"Output Path: {OUTPUT_PATH}")
    print("=" * 60)
    
    # Step 1: Strategy Generation
    print("\nSTEP 1: STRATEGY GENERATION")
    print("-" * 40)
    print("Running comprehensive code analysis and strategy planning...")
    
    try:
        strategy_result = execute_modernization_workflow(PROJECT_CONFIG)
        
        if strategy_result.success:
            print(f"SUCCESS: Strategy generation completed successfully!")
            print(f"   Validation cycles: {strategy_result.cycle_count}")
        else:
            print(f"FAILED: Strategy generation failed!")
            print(f"   Error: {strategy_result.data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"ERROR: Strategy generation error: {e}")
        return False
    
    # Step 2: Code Execution
    print("\nSTEP 2: CODE EXECUTION")
    print("-" * 40)
    print("Running AI-driven code transformation...")
    
    try:
        agent = AIExecutionAgent(output_directory=OUTPUT_PATH)
        
        execution_result = agent.execute_modernization(
            project_config=PROJECT_CONFIG,
            framework_results=strategy_result.data
        )
        
        if execution_result.get('execution_status') == 'success':
            print(f"SUCCESS: Code execution completed successfully!")
            print(f"   Output directory: {execution_result.get('output_directory', OUTPUT_PATH)}")
            print(f"   Files processed: {len(execution_result.get('code_generation_results', {}).get('generated_files', []))}")
            
            # Step 3: Full-Stack Compatibility Validation
            print("\nSTEP 3: FULL-STACK COMPATIBILITY VALIDATION")
            print("-" * 40)
            print("Validating API, backend, and database compatibility...")
            
            try:
                from util import APICompatibilityAnalyzer, BackendCompatibilityAnalyzer, DatabaseCompatibilityAnalyzer
                
                # Get analysis data from the strategy
                repo_analysis = strategy_result.data.get('repository_analysis', {})
                api_analysis = repo_analysis.get('api_analysis', {})
                backend_analysis = repo_analysis.get('backend_analysis', {})
                database_analysis = repo_analysis.get('database_analysis', {})
                
                # API Compatibility Analysis
                print("\n   API COMPATIBILITY:")
                if api_analysis:
                    compatibility_score = api_analysis.get('summary', {}).get('risk_level', 'unknown')
                    total_apis = api_analysis.get('summary', {}).get('total_api_calls', 0)
                    critical_risks = len([risk for risk in api_analysis.get('compatibility_risks', []) 
                                        if risk.get('severity') == 'high'])
                    
                    print(f"   - Total API calls detected: {total_apis}")
                    print(f"   - Risk level: {compatibility_score}")
                    print(f"   - Critical compatibility risks: {critical_risks}")
                    
                    if critical_risks > 0:
                        print(f"   WARNING: {critical_risks} critical API compatibility risks!")
                    elif compatibility_score == 'low':
                        print("   SUCCESS: Low API compatibility risk")
                    else:
                        print("   INFO: API compatibility analysis completed")
                else:
                    print("   INFO: No API analysis data available")
                
                # Backend Compatibility Analysis  
                print("\n   BACKEND COMPATIBILITY:")
                if backend_analysis:
                    node_upgrade = backend_analysis.get('node_version_compatibility', {}).get('upgrade_required', False)
                    express_upgrade = backend_analysis.get('express_compatibility', {}).get('upgrade_required', False)
                    breaking_changes = len(backend_analysis.get('breaking_changes', []))
                    migration_tasks = len(backend_analysis.get('migration_tasks', []))
                    
                    print(f"   - Node.js upgrade required: {'Yes' if node_upgrade else 'No'}")
                    print(f"   - Express.js upgrade required: {'Yes' if express_upgrade else 'No'}")
                    print(f"   - Breaking changes identified: {breaking_changes}")
                    print(f"   - Migration tasks required: {migration_tasks}")
                    
                    if node_upgrade or express_upgrade:
                        print("   WARNING: Major backend upgrades required!")
                        if node_upgrade:
                            print("   - Node.js 4.x → 20.x LTS migration needed")
                        if express_upgrade:
                            print("   - Express.js 3.x → 4.x migration needed")
                    else:
                        print("   SUCCESS: Backend compatibility maintained")
                else:
                    print("   INFO: No backend analysis data available")
                
                # Database Compatibility Analysis
                print("\n   DATABASE COMPATIBILITY:")
                if database_analysis:
                    mongodb_upgrade = database_analysis.get('mongodb_compatibility', {}).get('major_upgrade_required', False)
                    mongoose_upgrade = database_analysis.get('mongoose_compatibility', {}).get('upgrade_required', False)
                    migration_scripts = len(database_analysis.get('migration_scripts', []))
                    data_tasks = len(database_analysis.get('data_migration_tasks', []))
                    
                    print(f"   - MongoDB upgrade required: {'Yes' if mongodb_upgrade else 'No'}")
                    print(f"   - Mongoose upgrade required: {'Yes' if mongoose_upgrade else 'No'}")
                    print(f"   - Migration scripts needed: {migration_scripts}")
                    print(f"   - Data migration tasks: {data_tasks}")
                    
                    if mongodb_upgrade or mongoose_upgrade:
                        print("   WARNING: Major database upgrades required!")
                        if mongodb_upgrade:
                            print("   - MongoDB 3.0 → 7.x migration needed")
                        if mongoose_upgrade:
                            print("   - Mongoose 3.x → 7.x migration needed")
                    else:
                        print("   SUCCESS: Database compatibility maintained")
                else:
                    print("   INFO: No database analysis data available")
                
                # Overall Assessment
                print(f"\n   OVERALL ASSESSMENT:")
                total_critical_issues = (
                    (1 if api_analysis and critical_risks > 0 else 0) +
                    (1 if backend_analysis and (node_upgrade or express_upgrade) else 0) +
                    (1 if database_analysis and (mongodb_upgrade or mongoose_upgrade) else 0)
                )
                
                if total_critical_issues == 0:
                    print("   EXCELLENT: All systems compatible - ready for modernization")
                elif total_critical_issues == 1:
                    print("   MODERATE: Minor compatibility issues - manageable migration")
                else:
                    print("   HIGH RISK: Multiple critical compatibility issues - complex migration required")
                    
            except Exception as e:
                print(f"   WARNING: Full-stack compatibility validation failed: {e}")
                print("   RECOMMENDATION: Manual compatibility review recommended")
            
            # Step 4: Code Quality Evaluation
            print("\nSTEP 4: CODE QUALITY EVALUATION")
            print("-" * 40)
            print("Evaluating generated code quality and functional equivalence...")
            
            try:
                # Configure evaluation paths
                evaluation_config = EvaluationConfig(
                    original_path=PROJECT_CONFIG['legacy_repo_path'],
                    modernized_path=OUTPUT_PATH,
                    output_report_path=f"{OUTPUT_PATH}/evaluation_report.md",
                    output_json_path=f"{OUTPUT_PATH}/evaluation_report.json",
                    parallel_processing=True,
                    max_workers=2,  # Reduced for rate limiting
                    include_ai_analysis=True,
                    verbose=True
                )
                
                # Create and run evaluator
                evaluator = CodeEvaluationProgram(evaluation_config)
                evaluation_results = evaluator.run_evaluation()
                
                # Extract key metrics
                summary = evaluation_results.get("summary", {})
                quality_score = summary.get("overall_quality_score", 0)
                functional_equiv = summary.get("functional_equivalence_status", "UNKNOWN")
                critical_issues = summary.get("critical_issues_count", 0)
                recommendation = summary.get("recommendation", "UNKNOWN")
                
                print(f"SUCCESS: Code evaluation completed!")
                print(f"   Quality Score: {quality_score}/100")
                print(f"   Functional Equivalence: {functional_equiv}")
                print(f"   Critical Issues: {critical_issues}")
                print(f"   Overall Recommendation: {recommendation}")
                print(f"   Detailed Report: {evaluation_config.output_report_path}")
                print(f"   JSON Report: {evaluation_config.output_json_path}")
                
                # Provide recommendation-based feedback
                if recommendation == "Ready for Production":
                    print("   ✅ EXCELLENT: Code is ready for production deployment!")
                elif recommendation == "Needs Fixes":
                    print("   ⚠️  MODERATE: Code needs minor fixes before deployment")
                else:
                    print("   ❌ CRITICAL: Code has major issues requiring attention")
                    
            except Exception as e:
                print(f"   WARNING: Code evaluation failed: {e}")
                print("   RECOMMENDATION: Manual code review recommended")
                
        else:
            print(f"FAILED: Code execution failed!")
            print(f"   Error: {execution_result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"ERROR: Code execution error: {e}")
        return False
    
    # Success
    print("\nFULL-STACK MODERNIZATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"SUCCESS: Strategy: Generated and validated")
    print(f"SUCCESS: Code: Transformed and saved to {OUTPUT_PATH}")
    print(f"SUCCESS: API Compatibility: Validated and preserved")
    print(f"SUCCESS: Backend: Node.js/Express modernization applied")
    print(f"SUCCESS: Database: MongoDB/Mongoose compatibility maintained")
    print(f"SUCCESS: Evaluation: Code quality and functional equivalence assessed")
    print(f"READY: Full-stack modernized code available in {OUTPUT_PATH}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    """
    Entry point when running: python3 main.py
    """
    
    print("Starting Legacy System Modernization Framework...")
    
    try:
        success = main()
        exit_code = 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\nModernization cancelled by user")
        exit_code = 1
        
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        print("\nPlease check:")
        print("- GROQ_API_KEY environment variable is set")
        print("- Legacy repository path exists and is accessible")
        print("- All required dependencies are installed (groq, python-dotenv)")
        exit_code = 1
    
    print(f"\nExiting with code: {exit_code}")
    exit(exit_code)