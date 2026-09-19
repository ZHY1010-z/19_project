#!/usr/bin/env python3
"""
AI-Driven Execution Agent for Auckland Library Modernization Framework

This agent integrates with framework.py results to perform actual AI-driven code modernization
rather than using hardcoded templates. It leverages the comprehensive analysis from the 
framework and uses prompt_templates_1.py for consistent AI interactions.
"""

import os
import json
import logging
import re
import time
import subprocess
from typing import Dict, Any, List, Optional
import shutil
from datetime import datetime

# Import framework components
from framework import analyze_code
from util import llm_call, ASTAnalyzer, DependencyAnalyzer, QualityAnalyzer
# Import optimized prompt templates
from prompt_templates_optimized_full import (
    OptimizedPromptEngine, OptimizedPromptContext,
    get_transformation_prompt as get_execution_prompt
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIExecutionAgent:
    """
    AI-driven execution agent that integrates with framework.py results
    to perform actual code modernization using LLM-driven transformations.
    """
    
    # Safe dependency upgrade mappings with compatibility checks
    SAFE_DEPENDENCY_UPGRADES = {
        'express': {
            'from_version': '^3.0.0',
            'to_version': '^4.18.2',
            'breaking_changes': True,
            'notes': 'Middleware and routing system changed'
        },
        'mongodb': {
            'from_version': '^2.0.0', 
            'to_version': '^4.17.1',
            'breaking_changes': True,
            'notes': 'Connection API and methods completely changed'
        },
        'socket.io': {
            'from_version': '^1.0.0',
            'to_version': '^4.7.2', 
            'breaking_changes': True,
            'notes': 'Complete API rewrite'
        },
        'body-parser': {
            'from_version': '^1.0.0',
            'to_version': '^1.20.2',
            'breaking_changes': False,
            'notes': 'Minor API updates'
        },
        'lodash': {
            'from_version': '^4.17.19',
            'to_version': '^4.17.21',
            'breaking_changes': False,
            'notes': 'Security updates only'
        },
        'handlebars': {
            'from_version': '^4.7.6',
            'to_version': '^4.7.8',
            'breaking_changes': False,
            'notes': 'Security and bug fixes'
        }
    }
    
    def __init__(self, output_directory: str = None):
        """
        Initialize the AI Execution Agent
        
        Args:
            output_directory: Directory to save modernized code (default: create timestamped folder)
        """
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_directory = output_directory or f"modernized_output_{self.timestamp}"
        
        # Ensure output directory exists
        os.makedirs(self.output_directory, exist_ok=True)
        
        # Initialize analyzers for quality validation
        self.ast_analyzer = ASTAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        self.quality_analyzer = QualityAnalyzer()
        
        logger.info(f"AI Execution Agent initialized. Output directory: {self.output_directory}")
    
    def execute_modernization(self, project_config: Dict[str, Any], 
                            framework_results: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute complete AI-driven modernization based on framework analysis
        
        Args:
            project_config: Project configuration with legacy_repo_path, target_stack, etc.
            framework_results: Pre-computed framework analysis results (optional)
            
        Returns:
            Comprehensive execution results including generated code and metrics
        """
        try:
            logger.info("Starting AI-driven modernization execution...")
            
            # Step 1: Get framework analysis if not provided
            if not framework_results:
                logger.info("Running framework analysis...")
                framework_results = analyze_code(project_config)
                
                if "error" in framework_results:
                    return {"error": f"Framework analysis failed: {framework_results['error']}"}
            
            # Use compressed data for execution to reduce token consumption
            compressed_results = framework_results.get("compressed_for_execution", framework_results)
            logger.info("Using compressed framework results for token optimization")
            
            # Step 2: Extract migration strategy from compressed results
            migration_plan = self._extract_migration_strategy(compressed_results)
            
            # Step 3: Execute AI-driven code generation with compressed data
            code_generation_results = self._execute_code_generation(
                project_config, compressed_results, migration_plan
            )
            
            # Step 4: Validate generated code quality
            validation_results = self._validate_generated_code(
                project_config["legacy_repo_path"], code_generation_results
            )
            
            # Step 5: AI-driven compatibility fixing (NEW)
            compatibility_results = {"status": "skipped"}
            if code_generation_results.get("ai_generation_success"):
                logger.info("Starting post-generation AI-driven compatibility fixing...")
                compatibility_results = self._ai_compatibility_fixing_workflow()
            
            # Step 6: Generate execution summary using compressed data
            execution_summary = self._generate_execution_summary(
                compressed_results, code_generation_results, validation_results, compatibility_results
            )
            
            logger.info("AI-driven modernization execution completed successfully")
            
            return {
                "execution_status": "success",
                "framework_integration": True,
                "framework_results": framework_results,
                "migration_strategy": migration_plan,
                "code_generation": code_generation_results,
                "validation_results": validation_results,
                "compatibility_results": compatibility_results,
                "execution_summary": execution_summary,
                "output_directory": self.output_directory,
                "timestamp": self.timestamp
            }
            
        except Exception as e:
            logger.error(f"AI execution failed: {str(e)}")
            return {
                "execution_status": "failed",
                "error": str(e),
                "timestamp": self.timestamp
            }
    
    def _extract_migration_strategy(self, framework_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract actionable migration strategy from framework analysis"""
        
        migration_strategy = {
            "priority_areas": [],
            "transformation_targets": [],
            "security_fixes": [],
            "dependency_updates": [],
            "architectural_changes": []
        }
        
        try:
            # Extract from static analysis summary
            static_summary = framework_results.get("static_analysis_summary", {})
            
            # Identify high-priority transformation areas
            if static_summary.get("code_smells_detected", 0) > 100:
                migration_strategy["priority_areas"].append("code_quality_improvement")
            
            if static_summary.get("circular_dependencies", 0) > 0:
                migration_strategy["priority_areas"].append("dependency_refactoring")
                
            # Extract specific recommendations
            recommendations = framework_results.get("recommendations", [])
            for rec in recommendations:
                if "security" in rec.lower() or "vulnerability" in rec.lower():
                    migration_strategy["security_fixes"].append(rec)
                elif "dependency" in rec.lower() or "package" in rec.lower():
                    migration_strategy["dependency_updates"].append(rec)
                elif "pattern" in rec.lower() or "refactor" in rec.lower():
                    migration_strategy["transformation_targets"].append(rec)
                elif "architecture" in rec.lower():
                    migration_strategy["architectural_changes"].append(rec)
            
            # Extract modernization readiness insights
            readiness_score = framework_results.get("modernization_readiness_score", 0)
            migration_strategy["complexity_level"] = "high" if readiness_score < 50 else "medium" if readiness_score < 75 else "low"
            
            logger.info(f"Extracted migration strategy with {len(migration_strategy['priority_areas'])} priority areas")
            
        except Exception as e:
            logger.warning(f"Error extracting migration strategy: {e}")
            
        return migration_strategy
    
    def _execute_code_generation(self, project_config: Dict[str, Any], 
                               framework_results: Dict[str, Any],
                               migration_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI-driven code generation using framework analysis"""
        
        logger.info("Starting AI-driven code generation...")
        
        try:
            # Prepare optimized prompt context with compressed framework results
            full_context = {
                "target_platform": project_config.get("target_platform", "modern_nodejs"),
                "transformation_scope": migration_strategy.get("scope", []),
                "code_patterns": migration_strategy.get("patterns", []),
                "dependencies": migration_strategy.get("dependencies", [])
            }
            
            prompt_context = OptimizedPromptContext(
                agent_name="TransformationAgent",
                phase="transformation",
                cycle_number=1,
                compressed_context=full_context,
                project_config=project_config
            )
            
            # Get optimized execution prompt
            engine = OptimizedPromptEngine()
            system_prompt, user_prompt = engine.get_optimized_prompt(prompt_context)
            
            # Call LLM for AI-driven code generation with optimized prompts
            logger.info("Requesting AI-driven code transformation with optimized prompts...")
            ai_response = llm_call(user_prompt, system_prompt)
            
            # Process AI response and generate actual files
            generated_files = self._process_ai_code_generation(
                ai_response, project_config["legacy_repo_path"], migration_strategy
            )
            
            return {
                "ai_generation_success": True,
                "ai_response": ai_response,
                "generated_files": generated_files,
                "files_created": len(generated_files),
                "generation_strategy": migration_strategy,
                "prompt_context_used": "ExecutionAgent"
            }
            
        except Exception as e:
            import traceback
            logger.error(f"Code generation failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "ai_generation_success": False,
                "error": str(e),
                "files_created": 0
            }
    
    def _process_ai_code_generation(self, ai_response: str, legacy_repo_path: str, 
                                  migration_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process AI response and generate actual modernized code files"""
        
        generated_files = []
        
        try:
            # Copy original structure to output directory
            self._copy_legacy_structure(legacy_repo_path)
            
            # Parse AI response for code generation instructions
            # This is a simplified implementation - in practice, you'd want more sophisticated parsing
            files_to_modernize = self._identify_files_for_modernization(legacy_repo_path, migration_strategy)
            
            for file_info in files_to_modernize:
                try:
                    logger.info(f"Processing file: {file_info.get('relative_path', 'unknown')}")
                    modernized_content = self._generate_modernized_file_content(
                        file_info, ai_response, migration_strategy
                    )
                    
                    if modernized_content:
                        output_path = os.path.join(self.output_directory, file_info["relative_path"])
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(modernized_content)
                        
                        generated_files.append({
                            "original_path": file_info["full_path"],
                            "output_path": output_path,
                            "relative_path": file_info["relative_path"],
                            "modernization_applied": True,
                            "file_size": len(modernized_content)
                        })
                        
                        logger.info(f"Generated modernized file: {file_info['relative_path']}")
                
                except Exception as e:
                    logger.warning(f"Failed to modernize {file_info['relative_path']}: {e}")
                    # Copy original file as fallback
                    output_path = os.path.join(self.output_directory, file_info["relative_path"])
                    shutil.copy2(file_info["full_path"], output_path)
                    
                    generated_files.append({
                        "original_path": file_info["full_path"],
                        "output_path": output_path,
                        "relative_path": file_info["relative_path"],
                        "modernization_applied": False,
                        "error": str(e)
                    })
            
        except Exception as e:
            logger.error(f"Error processing AI code generation: {e}")
        
        return generated_files
    
    def _copy_legacy_structure(self, legacy_repo_path: str):
        """Copy legacy repository structure to output directory"""
        try:
            # Copy non-code files (package.json, config files, etc.)
            for root, dirs, files in os.walk(legacy_repo_path):
                # Skip node_modules and other common build directories
                dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist', 'build']]
                
                for file in files:
                    source_path = os.path.join(root, file)
                    rel_path = os.path.relpath(source_path, legacy_repo_path)
                    dest_path = os.path.join(self.output_directory, rel_path)
                    
                    # Only copy files that won't be modernized
                    file_type = self._get_file_type_for_modernization(file)
                    if not file_type:  # File doesn't need modernization
                        # Skip hidden files that aren't meant for modernization
                        if file.startswith('.') and not file.startswith('.env'):
                            continue
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.copy2(source_path, dest_path)
                        
        except Exception as e:
            logger.warning(f"Error copying legacy structure: {e}")
    
    def _identify_files_for_modernization(self, legacy_repo_path: str, 
                                        migration_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify files that need modernization (code, config, and documentation files)"""
        
        files_to_modernize = []
        
        try:
            for root, dirs, files in os.walk(legacy_repo_path):
                # Skip node_modules and other build directories
                dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist', 'build']]
                
                for file in files:
                    file_type = self._get_file_type_for_modernization(file)
                    
                    if file_type:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, legacy_repo_path)
                        
                        files_to_modernize.append({
                            "full_path": full_path,
                            "relative_path": rel_path,
                            "filename": file,
                            "file_type": file_type,
                            "priority": self._calculate_modernization_priority(full_path)
                        })
            
            # Sort by priority (highest first)
            files_to_modernize.sort(key=lambda x: x["priority"], reverse=True)
            
            logger.info(f"Identified {len(files_to_modernize)} files for modernization")
            
        except Exception as e:
            logger.error(f"Error identifying files for modernization: {e}")
        
        return files_to_modernize
    
    def _get_file_type_for_modernization(self, filename: str) -> Optional[str]:
        """Determine if file should be modernized and return its type"""
        from pathlib import Path
        
        file_ext = Path(filename).suffix.lower()
        
        # JavaScript/TypeScript code files
        if file_ext in {'.js', '.ts', '.jsx', '.tsx'}:
            return 'code'
        
        # JSON configuration files
        if file_ext == '.json':
            return 'json_config'
        
        # YAML configuration files  
        if file_ext in {'.yml', '.yaml'}:
            return 'yaml_config'
        
        # Environment files
        if filename == '.env' or filename.startswith('.env.'):
            return 'env_config'
        
        # Special configuration files (by exact name)
        special_configs = {
            'Dockerfile': 'docker_config',
            '.gitignore': 'git_config',
            '.dockerignore': 'docker_config',
            '.npmignore': 'npm_config',
            'README.md': 'documentation',
            'package-lock.json': 'json_config'
        }
        
        if filename in special_configs:
            return special_configs[filename]
        
        # JavaScript config files
        js_configs = {
            'webpack.config.js', 'babel.config.js', 'jest.config.js',
            '.eslintrc.js', 'rollup.config.js', 'vite.config.js'
        }
        
        if filename in js_configs:
            return 'js_config'
        
        return None
    
    def _calculate_modernization_priority(self, file_path: str) -> int:
        """Calculate modernization priority for a file based on file type and content"""
        priority = 1
        
        filename = os.path.basename(file_path)
        file_type = self._get_file_type_for_modernization(filename)
        
        try:
            # Set base priority by file type and importance
            if filename == 'package.json':
                priority += 10  # Highest priority - dependencies must be modernized first
            elif file_type == 'json_config':
                priority += 5   # Other config files are important
            elif filename in ['app.js', 'index.js', 'server.js', 'main.js']:
                priority += 8   # Main entry files are very important
            elif file_type == 'code':
                # Only analyze content for code files to avoid binary/JSON parsing issues
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Higher priority for files with legacy patterns
                    if 'callback' in content and 'function(' in content:
                        priority += 3  # Callback patterns need modernization
                    
                    if 'require(' in content and not 'import ' in content:
                        priority += 2  # CommonJS to ES6 modules
                    
                    if 'var ' in content:
                        priority += 2  # var to let/const
                    
                    # Framework-specific priorities
                    if 'express' in content.lower():
                        priority += 3  # Express.js files are important
                    
                    if 'mongodb' in content.lower() or 'mongoose' in content.lower():
                        priority += 3  # Database-related files
                        
                except (UnicodeDecodeError, IOError):
                    # File might be binary or unreadable, keep base priority
                    pass
            elif file_type in ['yaml_config', 'env_config']:
                priority += 3   # Other config files
            elif file_type == 'documentation':
                priority += 1   # Documentation is lower priority
                
        except Exception as e:
            logger.warning(f"Error calculating priority for {file_path}: {e}")
        
        return priority
    
    def _generate_modernized_file_content(self, file_info: Dict[str, Any], 
                                        ai_response: str, 
                                        migration_strategy: Dict[str, Any]) -> Optional[str]:
        """Generate modernized content for a specific file using AI guidance"""
        
        try:
            # Read original file content
            with open(file_info["full_path"], 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Prepare optimized specific modernization context for this file
            full_context = {
                "target_platform": "modern_nodejs",
                "transformation_scope": ["file_modernization"],
                "code_patterns": [f"modernize_{file_info.get('type', 'js')}_file"],
                "dependencies": migration_strategy.get("dependencies", []),
                "file_content": original_content  # Complete file content
            }
            
            file_context = OptimizedPromptContext(
                agent_name="TransformationAgent",
                phase="transformation",
                cycle_number=1,
                compressed_context=full_context
            )
            
            # Generate optimized file-specific modernization prompt
            engine = OptimizedPromptEngine()
            system_prompt, user_prompt = engine.get_optimized_prompt(file_context)
            
            # Generate file-type specific prompt
            file_specific_prompt = self._get_file_specific_prompt(file_info, original_content)
            
            # Combine prompts for comprehensive modernization
            combined_prompt = f"{user_prompt}\n\n{file_specific_prompt}"
            
            # Call LLM for file-specific modernization
            raw_response = llm_call(combined_prompt, system_prompt)
            
            # Clean and post-process the AI response
            modernized_content = self._clean_ai_response(raw_response, file_info['relative_path'])
            
            # Special post-processing for package.json - fix any invalid versions
            if file_info.get('filename') == 'package.json' and modernized_content:
                modernized_content = self._fix_package_json_versions(modernized_content)
            
            # Validate response based on file type
            if modernized_content and self._validate_modernized_content(modernized_content, file_info):
                # Advanced validation for code quality and compatibility
                filename = file_info.get('filename', file_info['relative_path'])
                file_type = file_info.get('file_type', 'code')
                validation_issues = self._validate_generated_code_advanced(modernized_content, filename, file_type)
                
                if validation_issues:
                    logger.warning(f"Validation issues found in {filename}: {validation_issues}")
                    # Log issues but still return content - let user decide if they want to fix
                    for issue in validation_issues:
                        logger.warning(f"  - {issue}")
                
                return modernized_content
            else:
                logger.warning(f"AI response doesn't look like valid content for {file_info['relative_path']}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating modernized content for {file_info['relative_path']}: {e}")
            return None
    
    def _get_file_specific_prompt(self, file_info: Dict[str, Any], original_content: str) -> str:
        """Generate file-type specific modernization prompt"""
        file_type = file_info.get('file_type', 'code')
        filename = file_info['filename']
        relative_path = file_info['relative_path']
        
        if file_type == 'json_config':
            if filename == 'package.json':
                # Pre-validate dependency versions for initial generation
                try:
                    validated_deps = self._get_validated_dependencies(original_content)
                    validated_deps_json = json.dumps(validated_deps, indent=2) if validated_deps else "No existing dependencies found"
                except:
                    validated_deps_json = "Could not validate existing dependencies"
                
                return f"""
PACKAGE.JSON MODERNIZATION REQUEST:

File: {relative_path}
Original Content:
```json
{original_content}
```

VALIDATED DEPENDENCY VERSIONS (use these EXACT versions):
{validated_deps_json}

**CRITICAL: YOU MUST USE ONLY THE VERSIONS LISTED ABOVE**
- Do NOT make up version numbers like "1.0.0" for packages
- Do NOT use placeholder versions
- If a package is not in the validated list, DON'T include it
- EVERY dependency version MUST come from the validated list above
- Use the EXACT version strings provided (including ^ prefix)

CRITICAL DEPENDENCY UPGRADE REQUIREMENTS:
1. ONLY use dependency versions from the VALIDATED list above - NO EXCEPTIONS
2. NEVER use fake versions like "^1.0.0" - only use validated versions
3. Check for breaking changes before major version upgrades
4. Express: 3.x→4.x requires middleware and routing changes
5. MongoDB: 2.x→4.x→6.x requires connection API changes
6. Socket.io: 1.x→4.x requires complete syntax updates
7. Add "type": "module" for ES6 module support
8. Replace deprecated 'request' package with 'axios'

MODERNIZATION TASKS:
1. Update dependencies using ONLY validated versions above
2. Add security dependencies (helmet, cors, dotenv) with validated versions
3. Add devDependencies (nodemon, eslint, jest) with validated versions
4. Add modern npm scripts (dev, test, lint, build)
5. Set engines field for Node.js >=16.0.0
6. Add "type": "module" for ES6 modules
7. Remove deprecated dependencies (request, etc.)

**CRITICAL: RESPOND WITH ONLY VALID JSON - NO TEXT BEFORE OR AFTER**
- Your ENTIRE response must be ONLY the JSON object
- Start IMMEDIATELY with the opening brace
- End IMMEDIATELY with the closing brace
- NO explanatory text like "Here is..." or "I've modernized..."
- NO markdown formatting like ```json
- NO transformation plans, notes, or commentary after the JSON
- NO asterisks (**), headers, or explanatory sections
- EVERY version number MUST come from the VALIDATED list above
- NO fake or placeholder versions allowed
- The JSON must be parseable immediately with JSON.parse()

EXAMPLE OF CORRECT FORMAT (your entire response starts and ends with braces):
{{"name": "example", "version": "1.0.0", "dependencies": {{}}}}

RESPOND WITH COMPLETE MODERNIZED PACKAGE.JSON:
"""
            else:
                return f"""
JSON CONFIGURATION MODERNIZATION REQUEST:

File: {relative_path}
Original Content:
```json
{original_content}
```

MODERNIZATION TASKS:
1. Update configuration syntax to modern standards
2. Add missing recommended options
3. Ensure compatibility with latest tool versions
4. Add security-related configurations
5. Optimize for modern development workflow
6. Fix any deprecated configuration options

**IMPORTANT: OUTPUT ONLY PURE JSON. NO EXPLANATORY TEXT.**
Please provide ONLY the complete modernized JSON content with proper formatting:
"""
        
        elif file_type == 'yaml_config':
            return f"""
YAML CONFIGURATION MODERNIZATION REQUEST:

File: {relative_path}
Original Content:
```yaml
{original_content}
```

MODERNIZATION TASKS:
1. Update to latest YAML syntax standards
2. Modernize service versions and configurations
3. Add security best practices
4. Optimize for current deployment patterns
5. Add missing recommended configurations
6. Update deprecated options to current alternatives

**IMPORTANT: OUTPUT ONLY PURE YAML. NO EXPLANATORY TEXT.**
Please provide ONLY the complete modernized YAML content:
"""
        
        elif file_type == 'env_config':
            return f"""
ENVIRONMENT CONFIGURATION MODERNIZATION REQUEST:

File: {relative_path}
Original Content:
```
{original_content}
```

MODERNIZATION TASKS:
1. Add missing essential environment variables
2. Improve security by suggesting better default values
3. Add comments for clarity
4. Organize variables by category
5. Add modern Node.js environment variables
6. Ensure all sensitive data uses environment variables

**IMPORTANT: OUTPUT ONLY PURE .ENV FORMAT. NO EXPLANATORY TEXT.**
Please provide ONLY the complete modernized .env content:
"""
        
        elif file_type == 'documentation':
            return f"""
DOCUMENTATION MODERNIZATION REQUEST:

File: {relative_path}
Original Content:
```markdown
{original_content}
```

MODERNIZATION TASKS:
1. Update installation and setup instructions for modern Node.js
2. Add modern npm script usage examples
3. Update dependency information
4. Add security best practices section
5. Improve formatting and structure
6. Add modern development workflow instructions

**IMPORTANT: OUTPUT ONLY PURE MARKDOWN. NO EXPLANATORY TEXT.**
Please provide ONLY the complete modernized documentation content:
"""
        
        else:
            # Default to JavaScript/TypeScript code file prompt
            return f"""
JAVASCRIPT MODERNIZATION REQUEST:

File: {relative_path}
Priority Level: {file_info.get('priority', 1)}

Original Content:
```javascript
{original_content}
```

CRITICAL BEHAVIOR PRESERVATION:
- Maintain ALL endpoints, routes, and functions from original file
- Keep IDENTICAL response formats (don't wrap arrays in objects, preserve exact structure)
- Preserve exact API behavior - only modernize syntax, not functionality
- Don't add validation, error handling, or features not present in original
- Keep all route handlers with same logic flow

CRITICAL ES6 CONVERSION REQUIREMENTS:
1. Convert ALL require() statements to ES6 import statements consistently
2. Convert ALL module.exports to export default or named exports 
3. Replace __dirname with path.dirname(fileURLToPath(import.meta.url))
4. Convert var declarations to const/let appropriately
5. Convert callback patterns to async/await
6. Add proper error handling with try/catch
7. Update deprecated API calls to modern equivalents
8. NEVER mix require() and import in the same file
9. NEVER use TypeScript syntax in .js files
10. Ensure syntactically valid JavaScript output

DEPRECATED PACKAGE HANDLING:
- The 'request' package is DEPRECATED and archived - NEVER include it in modernized code
- If 'request' is imported but NOT used anywhere in the code, completely REMOVE the import
- If 'request' is actually used in the code, replace ALL usages with 'axios' (modern alternative)
- Replace request.get() with axios.get(), request.post() with axios.post(), etc.
- Note: axios returns response.data directly, while request returns the full response body
- If you see ANY of these deprecated packages, remove or replace them:
  * 'request' → use 'axios' instead
  * 'async' (if only used for async.waterfall/series) → use native async/await
  * Old callback-based packages → use their modern promise-based equivalents

MODERNIZATION TASKS:
- Consistent ES6 module system throughout
- Modern async/await patterns
- Proper const/let usage
- Enhanced error handling
- Security best practices
- Performance optimizations

**CRITICAL OUTPUT REQUIREMENTS:**
- Output COMPLETE file - never truncate or cut short
- Include ALL functions, exports, and code sections
- If content is large, prioritize main functionality first
- End with clear completion marker: "// MODERNIZATION COMPLETE"

**IMPORTANT: ONLY OUTPUT PURE JAVASCRIPT CODE. NO EXPLANATORY TEXT.**
- Do NOT include any explanatory text like "Here is the modernized version..."
- Do NOT include numbered lists of transformations
- Do NOT include any commentary outside of JavaScript comments
- Start directly with import statements or actual JavaScript code
- ALL explanations must be JavaScript comments (// or /* */) if needed

Please provide ONLY the complete modernized JavaScript content with consistent ES6 module syntax:
"""
    
    def _validate_modernized_content(self, content: str, file_info: Dict[str, Any]) -> bool:
        """Validate modernized content based on file type"""
        file_type = file_info.get('file_type', 'code')
        filename = file_info['filename']
        
        if not content.strip():
            return False
        
        if file_type == 'json_config':
            # Validate JSON format
            try:
                import json
                # Clean content first - remove any explanatory text
                cleaned_content = self._clean_json_content(content)
                data = json.loads(cleaned_content)
                
                # Check for essential package.json fields
                if filename == 'package.json':
                    # More lenient validation - just need a name field
                    has_name = 'name' in data
                    logger.info(f"Package.json validation: name field present = {has_name}")
                    return has_name
                return True
            except json.JSONDecodeError as e:
                logger.warning(f"JSON decode error for {filename}: {e}")
                logger.debug(f"Content that failed: {content}")
                return False
            except Exception as e:
                logger.warning(f"JSON validation error for {filename}: {e}")
                return False
        
        elif file_type == 'yaml_config':
            # Basic YAML validation
            return ':' in content and not content.startswith('{')
        
        elif file_type == 'env_config':
            # Environment file validation
            return '=' in content or content.startswith('#')
        
        elif file_type == 'documentation':
            # Documentation validation
            return len(content) > 50  # Minimum reasonable length
        
        else:
            # JavaScript/TypeScript code validation
            return (
                'function' in content or 
                'const' in content or 
                'import' in content or
                'export' in content or
                'module.exports' in content
            )
    
    def _validate_es6_consistency(self, content: str, filename: str) -> List[str]:
        """Detect mixed module system issues"""
        issues = []
        has_require = 'require(' in content
        has_import = 'import ' in content or 'export ' in content
        
        if has_require and has_import:
            issues.append(f"Mixed module systems detected in {filename}: both require() and import/export found")
        
        if '__dirname' in content and has_import:
            issues.append(f"__dirname used in ES6 module {filename}: should use import.meta.url instead")
        
        if 'module.exports' in content and has_import:
            issues.append(f"module.exports mixed with ES6 exports in {filename}")
            
        return issues
    
    def _validate_typescript_syntax(self, content: str, filename: str) -> List[str]:
        """Detect TypeScript syntax in JavaScript files"""
        issues = []
        
        if filename.endswith('.js'):
            ts_patterns = [
                ': string', ': number', ': boolean', ': any', 
                'interface ', 'type ', ': Promise<', ': Array<',
                '?: ', 'readonly ', 'private ', 'protected ', 'public '
            ]
            
            for pattern in ts_patterns:
                if pattern in content:
                    issues.append(f"TypeScript syntax '{pattern}' found in JavaScript file {filename}")
                    break
        
        return issues
    
    def _validate_npm_package_version(self, package_name: str, version: str) -> bool:
        """Validate if a specific npm package version exists"""
        try:
            # Use npm view command to check if version exists
            result = subprocess.run(
                ['npm', 'view', f'{package_name}@{version}', 'name'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning(f"Could not validate {package_name}@{version}")
            return False
    
    def _get_latest_compatible_version(self, package_name: str, major_version: str = None) -> str:
        """Get the latest compatible version for a package"""
        try:
            if major_version:
                # Get latest version within major version
                cmd = ['npm', 'view', f'{package_name}@^{major_version}', 'version']
            else:
                # Get absolute latest version
                cmd = ['npm', 'view', package_name, 'version']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # Extract just the version number, not the full output
                output = result.stdout.strip()
                # Handle cases where output might have multiple lines or extra info
                lines = output.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('@') and not line.startswith('npm'):
                        # Extract version number (handles formats like "package@1.2.3 '1.2.3'")
                        import re
                        version_match = re.search(r"(\d+\.\d+\.\d+)", line)
                        if version_match:
                            return version_match.group(1)
                return output.split('\n')[0].strip()  # Fallback to first line
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Fallback to known safe versions (updated 2024-2025)
        safe_versions = {
            'express': '4.18.2',
            'body-parser': '1.20.2',
            'mongodb': '6.3.0',
            'mongoose': '8.1.0',
            'handlebars': '4.7.8',
            'winston': '3.11.0',
            'socket.io': '4.6.1',
            'axios': '1.6.5',
            'async': '3.2.5',
            'moment': '2.30.1',
            'uuid': '9.0.1',
            'minimist': '1.2.8',
            'helmet': '7.1.0',
            'cors': '2.8.5',
            'dotenv': '16.3.1',
            'nodemon': '3.0.3',
            'eslint': '8.56.0',
            'jest': '29.7.0',
            'winston-logstash': '1.2.1'
        }
        return safe_versions.get(package_name, '1.0.0')

    def _validate_dependency_compatibility(self, package_content: str) -> List[str]:
        """Check dependency version compatibility with npm registry validation"""
        issues = []
        
        try:
            import json
            pkg = json.loads(package_content)
            deps = pkg.get('dependencies', {})
            
            # Validate each dependency version exists
            for pkg_name, version in deps.items():
                clean_version = version.replace('^', '').replace('~', '').replace('>=', '')
                if not self._validate_npm_package_version(pkg_name, clean_version):
                    # Get correct version
                    correct_version = self._get_latest_compatible_version(pkg_name, clean_version.split('.')[0])
                    issues.append(f"Invalid version {pkg_name}@{version}, should use ^{correct_version}")
            
            # Check known breaking upgrades using class mapping table
            for pkg_name, upgrade_info in self.SAFE_DEPENDENCY_UPGRADES.items():
                if pkg_name in deps:
                    version = deps[pkg_name]
                    if upgrade_info['breaking_changes'] and version.startswith(upgrade_info['to_version'][:2]):
                        issues.append(f"Breaking change upgrade detected: {pkg_name} {upgrade_info['notes']}")
            
            # Check if ES6 module support is included
            if 'type' not in pkg:
                issues.append("Missing 'type': 'module' for ES6 module support")
            elif pkg.get('type') != 'module':
                issues.append("Should set 'type': 'module' for ES6 module compatibility")
                
            # Check Node.js version requirements
            engines = pkg.get('engines', {})
            if 'node' not in engines:
                issues.append("Missing Node.js version requirement in engines field")
            elif not engines['node'].replace('>=', '').replace('^', '').startswith(('16', '18', '20')):
                issues.append("Node.js version should be >=16.0.0 for modern ES6 support")
                        
        except Exception as e:
            issues.append(f"Could not validate package.json dependencies: {str(e)}")
        
        return issues
    
    def _validate_generated_code_advanced(self, content: str, filename: str, file_type: str) -> List[str]:
        """Comprehensive validation of generated code"""
        all_issues = []
        
        # ES6 module consistency check
        all_issues.extend(self._validate_es6_consistency(content, filename))
        
        # TypeScript syntax check
        all_issues.extend(self._validate_typescript_syntax(content, filename))
        
        # Dependency compatibility check (package.json only)
        if file_type == 'json_config' and 'package.json' in filename:
            all_issues.extend(self._validate_dependency_compatibility(content))
        
        # API compatibility validation for JavaScript/TypeScript files
        if file_type in ['javascript', 'typescript', 'code'] and filename.endswith(('.js', '.ts', '.jsx', '.tsx')):
            all_issues.extend(self._validate_api_compatibility(content, filename))
        
        # Backend modernization validation
        if file_type in ['javascript', 'typescript', 'code'] and filename.endswith(('.js', '.ts')):
            all_issues.extend(self._validate_backend_modernization(content, filename))
        
        # Database compatibility validation
        if file_type in ['javascript', 'typescript', 'code'] and filename.endswith(('.js', '.ts')):
            all_issues.extend(self._validate_database_compatibility(content, filename))
        
        return all_issues
    
    def _validate_api_compatibility(self, content: str, filename: str) -> List[str]:
        """Validate that generated code maintains API compatibility"""
        issues = []
        
        # Log which file is being validated
        logger.debug(f"Validating API compatibility for: {filename}")
        
        # Critical API patterns that must be preserved
        critical_patterns = {
            'database': ['db.', 'collection.', 'mongoose.', 'MongoClient', '.find(', '.save(', '.update('],
            'http_routes': ['app.get(', 'app.post(', 'app.put(', 'app.delete(', 'router.'],
            'auth': ['passport.', 'jwt.', 'session.', 'auth.', 'bcrypt'],
            'socket': ['socket.emit', 'socket.on', 'io.connect', 'io('],
            'middleware': ['app.use(', 'express.static', 'bodyParser', 'cors']
        }
        
        # Check for modified API endpoints
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Look for potential API endpoint modifications using critical_patterns
            if any(pattern in line for pattern in critical_patterns['http_routes']):
                # Extract the route pattern
                route_match = re.search(r'app\.\w+\(\s*[\'"`]([^\'"`]+)[\'"`]', line)
                if route_match:
                    route = route_match.group(1)
                    # Check for suspicious route modifications
                    if '/api/' in route and ('v2/' in route or 'new/' in route):
                        issues.append(f"Potential API route modification detected at line {i+1}: {line.strip()}")
            
            # Check for database connection changes using critical_patterns
            if any(pattern in line for pattern in critical_patterns['database'][:2]):  # MongoClient, mongoose
                # Look for changed connection strings or patterns
                if 'mongodb://localhost:' not in line and 'process.env.' not in line:
                    issues.append(f"Database connection may have been modified at line {i+1}: {line.strip()}")
            
            # Check for socket event name changes using critical_patterns
            if any(pattern in line for pattern in critical_patterns['socket'][:2]):  # socket.emit, socket.on
                # Extract event name
                event_match = re.search(r'socket\.emit\(\s*[\'"`]([^\'"`]+)[\'"`]', line)
                if event_match:
                    event_name = event_match.group(1)
                    # Check for suspicious event name patterns
                    if any(suspicious in event_name.lower() for suspicious in ['new', 'v2', 'updated', 'modern']):
                        issues.append(f"Socket event name may have been modified at line {i+1}: {event_name}")
        
        # Check for missing critical middleware
        has_cors = 'cors' in content.lower()
        has_body_parser = 'bodyparser' in content.lower() or 'body-parser' in content.lower()
        has_express_json = 'express.json()' in content
        
        if not (has_body_parser or has_express_json):
            issues.append("Missing body parsing middleware - may break API requests")
            
        if not has_cors:
            issues.append("CORS middleware may be missing - could cause cross-origin issues")
        
        # Check for authentication middleware preservation
        if 'passport' in content.lower() and 'passport.initialize()' not in content:
            issues.append("Passport authentication may not be properly initialized")
        
        return issues
    
    def _validate_backend_modernization(self, content: str, filename: str) -> List[str]:
        """Validate backend modernization compliance (Node.js 4.x→20.x, Express 3.x→4.x)"""
        issues = []
        
        # Log which file is being validated
        logger.debug(f"Validating backend modernization for: {filename}")
        
        # Node.js modernization checks
        lines = content.split('\n')
        
        # Check for Node.js 4.x patterns that need modernization
        for i, line in enumerate(lines):
            # Check for callback patterns that should be async/await
            if 'function(' in line and 'callback' in line and 'async' not in line:
                issues.append(f"Callback pattern detected at line {i+1} - consider migrating to async/await: {line.strip()}")
            
            # Check for deprecated Express 3.x patterns
            if 'app.configure(' in line:
                issues.append(f"CRITICAL: app.configure() removed in Express 4.x at line {i+1}: {line.strip()}")
            
            if 'express.bodyParser(' in line:
                issues.append(f"CRITICAL: express.bodyParser() removed in Express 4.x at line {i+1}: {line.strip()}")
            
            if 'express.cookieParser(' in line:
                issues.append(f"CRITICAL: express.cookieParser() removed in Express 4.x at line {i+1}: {line.strip()}")
            
            if 'express.session(' in line:
                issues.append(f"CRITICAL: express.session() removed in Express 4.x at line {i+1}: {line.strip()}")
            
            # Check for proper Express 4.x middleware usage
            if 'app.use(' in line and 'bodyParser' in line and not 'body-parser' in content:
                issues.append(f"Missing body-parser module import for Express 4.x at line {i+1}")
        
        # Check for proper error handling middleware in Express 4.x
        has_error_middleware = False
        for line in lines:
            if 'function(err, req, res, next)' in line or 'function (err, req, res, next)' in line:
                has_error_middleware = True
                break
        
        if 'express' in content.lower() and not has_error_middleware:
            issues.append("Missing Express 4.x compatible error handling middleware")
        
        # Check for Node.js version compatibility in package.json references
        if '"engines"' in content and '"node"' in content:
            if '"4.' in content or '">=4' in content:
                issues.append("package.json engines field requires Node.js 20.x LTS upgrade")
        
        return issues
    
    def _validate_database_compatibility(self, content: str, filename: str) -> List[str]:
        """Validate database compatibility (MongoDB 3.0→7.x, Mongoose 3.x→7.x)"""
        issues = []
        
        # Log which file is being validated
        logger.debug(f"Validating database compatibility for: {filename}")
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # MongoDB 3.0 to 7.x compatibility checks
            if 'MongoClient.connect(' in line and 'callback' in line:
                issues.append(f"MongoDB 3.0 callback-style connection deprecated at line {i+1} - use async/await: {line.strip()}")
            
            # Check for deprecated MongoDB query methods
            if '.insert(' in line and 'insertOne' not in line and 'insertMany' not in line:
                issues.append(f"Deprecated MongoDB insert() at line {i+1} - use insertOne() or insertMany(): {line.strip()}")
            
            if '.update(' in line and 'updateOne' not in line and 'updateMany' not in line:
                issues.append(f"Deprecated MongoDB update() at line {i+1} - use updateOne() or updateMany(): {line.strip()}")
            
            if '.remove(' in line and 'deleteOne' not in line and 'deleteMany' not in line:
                issues.append(f"Deprecated MongoDB remove() at line {i+1} - use deleteOne() or deleteMany(): {line.strip()}")
            
            # Mongoose 3.x to 7.x compatibility checks
            if 'mongoose.connect(' in line:
                # Check for new connection options
                if 'useNewUrlParser' not in content:
                    issues.append(f"Missing useNewUrlParser option for MongoDB 7.x at line {i+1}")
                if 'useUnifiedTopology' not in content:
                    issues.append(f"Missing useUnifiedTopology option for MongoDB 7.x at line {i+1}")
            
            # Check for Mongoose schema compatibility
            if 'new Schema(' in line or 'mongoose.Schema(' in line:
                # Check for deprecated schema options
                if 'safe:' in line:
                    issues.append(f"Deprecated Mongoose 'safe' option at line {i+1} - use 'writeConcern': {line.strip()}")
            
            # Check for Mongoose middleware hooks compatibility
            if 'schema.pre(' in line or 'schema.post(' in line:
                if 'function(' in line and 'next' in line and 'async' not in line:
                    issues.append(f"Mongoose middleware at line {i+1} should use async/await for Mongoose 7.x: {line.strip()}")
        
        # Check for proper MongoDB connection string format
        if 'mongodb://' in content:
            # Look for legacy connection patterns
            for line in lines:
                if 'mongodb://' in line and 'localhost' in line and ':27017' not in line:
                    issues.append("MongoDB connection string may need explicit port specification for 7.x")
                    break
        
        return issues
    
    def _clean_json_content(self, content: str) -> str:
        """Clean JSON content by removing explanatory text and fixing common issues"""
        import re
        
        # First, try to extract just the JSON object using regex
        # Look for the main JSON structure starting with { and ending with }
        json_match = re.search(r'^\s*(\{[\s\S]*?\})\s*$', content, re.MULTILINE)
        if json_match:
            potential_json = json_match.group(1)
            # Verify it's valid JSON
            try:
                json.loads(potential_json)
                return potential_json
            except:
                pass
        
        # Fallback: Remove common explanatory prefixes and suffixes
        lines = content.split('\n')
        cleaned_lines = []
        json_started = False
        brace_count = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Skip lines with markdown-style headers or explanations
            if stripped.startswith('**') or stripped.startswith('#') or stripped.startswith('TRANSFORMATION'):
                continue
            
            # Skip explanatory text before JSON starts
            if not json_started:
                if stripped.startswith('{'):
                    json_started = True
                    cleaned_lines.append(line)
                    brace_count += stripped.count('{') - stripped.count('}')
                elif stripped.startswith('"') and ':' in stripped:
                    # Might be JSON without opening brace, add it
                    json_started = True
                    cleaned_lines.append('{')
                    cleaned_lines.append(line)
                    brace_count = 1 + stripped.count('{') - stripped.count('}')
                continue
            
            # Once JSON started, include lines until JSON ends
            cleaned_lines.append(line)
            brace_count += stripped.count('{') - stripped.count('}')
            
            # Stop when JSON is complete (brace_count reaches 0)
            if brace_count <= 0:
                break
        
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Final cleanup: remove any trailing artifacts after the closing brace
        if '}' in cleaned_content:
            # Find the last closing brace and cut everything after it
            last_brace_index = cleaned_content.rfind('}')
            cleaned_content = cleaned_content[:last_brace_index + 1]
        
        return cleaned_content.strip()
    
    
    def _fix_package_json_versions(self, package_json_str: str) -> str:
        """Fix invalid package versions in package.json with known good versions"""
        try:
            pkg = json.loads(package_json_str)
            fixed = False
            
            # Known good versions mapping (updated 2024-2025)
            known_versions = {
                'express': '^4.18.2',
                'body-parser': '^1.20.2',
                'mongodb': '^6.3.0',
                'mongoose': '^8.1.0',
                'handlebars': '^4.7.8',
                'winston': '^3.11.0',
                'socket.io': '^4.6.1',
                'axios': '^1.6.5',
                'async': '^3.2.5',
                'moment': '^2.30.1',
                'uuid': '^9.0.1',
                'minimist': '^1.2.8',
                'helmet': '^7.1.0',
                'cors': '^2.8.5',
                'dotenv': '^16.3.1',
                'nodemon': '^3.0.3',
                'eslint': '^8.56.0',
                'jest': '^29.7.0'
            }
            
            # Fix dependencies
            if 'dependencies' in pkg:
                for dep_name, dep_version in list(pkg['dependencies'].items()):
                    # Check if version looks fake (e.g., ^1.0.0, 1.0.0)
                    clean_ver = dep_version.replace('^', '').replace('~', '')
                    if clean_ver == '1.0.0' or clean_ver.startswith('1.0.'):
                        # Replace with known good version
                        if dep_name in known_versions:
                            logger.info(f"Fixing invalid version for {dep_name}: {dep_version} -> {known_versions[dep_name]}")
                            pkg['dependencies'][dep_name] = known_versions[dep_name]
                            fixed = True
                    # Also fix if we have a better known version
                    elif dep_name in known_versions and dep_name != 'request':
                        pkg['dependencies'][dep_name] = known_versions[dep_name]
                        fixed = True
                
                # Remove deprecated 'request' package and replace with axios
                if 'request' in pkg['dependencies']:
                    logger.info("Removing deprecated 'request' package, replacing with 'axios'")
                    del pkg['dependencies']['request']
                    pkg['dependencies']['axios'] = known_versions['axios']
                    fixed = True
            
            # Fix devDependencies
            if 'devDependencies' in pkg:
                for dep_name, dep_version in list(pkg['devDependencies'].items()):
                    clean_ver = dep_version.replace('^', '').replace('~', '')
                    if clean_ver == '1.0.0' or clean_ver.startswith('1.0.'):
                        if dep_name in known_versions:
                            logger.info(f"Fixing invalid dev version for {dep_name}: {dep_version} -> {known_versions[dep_name]}")
                            pkg['devDependencies'][dep_name] = known_versions[dep_name]
                            fixed = True
            
            # Ensure type: module for ES6
            if 'type' not in pkg or pkg['type'] != 'module':
                pkg['type'] = 'module'
                fixed = True
            
            if fixed:
                logger.info("Fixed package.json with validated versions")
            
            return json.dumps(pkg, indent=2)
        except Exception as e:
            logger.warning(f"Could not fix package.json versions: {e}")
            return package_json_str
    
    def _clean_ai_response(self, raw_response: str, file_path: str) -> str:
        """Clean and post-process AI response based on file type"""
        
        if not raw_response:
            return ""
        
        # Remove markdown code blocks
        content = raw_response.strip()
        
        # Remove AI completion markers and status indicators
        ai_markers_to_remove = [
            '**TRANSFORMATION_COMPLETE**',
            '**COMPLETE**',
            '**DONE**',
            '**END**',
            '**FINISHED**',
            '[COMPLETE]',
            '[DONE]',
            '[END]',
            '<!-- TRANSFORMATION_COMPLETE -->',
            '// TRANSFORMATION_COMPLETE',
            '# TRANSFORMATION_COMPLETE',
            'TRANSFORMATION_COMPLETE',
            '**Code generation complete**',
            '**Modernization complete**',
            '**Transformation finished**'
        ]
        
        for marker in ai_markers_to_remove:
            content = content.replace(marker, '')
        
        # Remove lines that contain only markers or status text
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped_line = line.strip()
            # Skip lines that are only AI status indicators
            if (stripped_line.startswith('**') and stripped_line.endswith('**') and 
                any(word in stripped_line.lower() for word in ['complete', 'done', 'finished', 'end', 'transformation'])):
                continue
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines).strip()
        
        # Detect file type from path
        from pathlib import Path
        file_ext = Path(file_path).suffix.lower()
        filename = Path(file_path).name
        
        # Remove code block markers based on file type
        if file_ext == '.json' or filename.endswith('.json'):
            # JSON files
            if content.startswith('```json'):
                content = content[7:]
            elif content.startswith('```'):
                content = content[3:]
        elif file_ext in {'.yml', '.yaml'}:
            # YAML files
            if content.startswith('```yaml'):
                content = content[7:]
            elif content.startswith('```yml'):
                content = content[6:]
            elif content.startswith('```'):
                content = content[3:]
        elif file_ext == '.md':
            # Markdown files
            if content.startswith('```markdown'):
                content = content[11:]
            elif content.startswith('```md'):
                content = content[5:]
            elif content.startswith('```'):
                content = content[3:]
        else:
            # JavaScript/TypeScript and other code files
            if content.startswith('```javascript'):
                content = content[13:]
            elif content.startswith('```js'):
                content = content[5:]
            elif content.startswith('```typescript'):
                content = content[13:]
            elif content.startswith('```ts'):
                content = content[5:]
            elif content.startswith('```'):
                content = content[3:]
        
        if content.endswith('```'):
            content = content[:-3]
        
        content = content.strip()
        
        # Fix common import/require mixing issues
        lines = content.split('\n')
        cleaned_lines = []
        additional_imports = []  # Collect imports that need to be moved to top
        
        for i, line in enumerate(lines):
            # Fix broken import statements like "import argv from 'minimist')(process.argv.slice(2));"
            if 'import' in line and ')(' in line:
                # Split into proper import and separate statement
                if 'minimist' in line:
                    cleaned_lines.append("import minimist from 'minimist';")
                    cleaned_lines.append("const argv = minimist(process.argv.slice(2));")
                    continue
            
            # Detect import statements inside functions (ES6 doesn't allow this)
            if line.strip().startswith('import ') and i > 0:
                # Check if we're inside a function by looking for function declarations before this line
                function_context = any('function' in prev_line or '=>' in prev_line or '= (' in prev_line 
                                     for prev_line in lines[max(0, i-10):i])
                if function_context:
                    # Move import to top and replace with comment
                    additional_imports.append(line.strip())
                    cleaned_lines.append(f'// {line.strip()} // Moved to top-level imports')
                    continue
            
            # Convert mixed require/import usage - choose ES6 imports consistently
            if line.strip().startswith('const fs = require('):
                additional_imports.append("import fs from 'fs';")
                continue
            
            # Fix require.extensions usage (not compatible with ES6 modules)
            if 'require.extensions[' in line:
                # Comment out or replace with ES6 module equivalent
                cleaned_lines.append('// ' + line + ' // Note: require.extensions not available in ES6 modules')
                continue
            
            # Convert var to const/let appropriately
            if line.strip().startswith('var '):
                # Simple heuristic: if it's reassigned later, use let; otherwise const
                var_name = line.split()[1].split('=')[0].strip()
                if any(f'{var_name} =' in future_line for future_line in lines[i+1:]):
                    cleaned_lines.append(line.replace('var ', 'let ', 1))
                else:
                    cleaned_lines.append(line.replace('var ', 'const ', 1))
                continue
            
            cleaned_lines.append(line)
        
        # Reconstruct content with additional imports at the top
        if additional_imports:
            # Find where existing imports end
            import_end_index = 0
            for i, line in enumerate(cleaned_lines):
                if line.strip().startswith('import '):
                    import_end_index = i + 1
                elif line.strip() and not line.strip().startswith('//'):
                    break
            
            # Insert additional imports after existing ones
            for imp in additional_imports:
                if imp not in '\n'.join(cleaned_lines[:import_end_index]):  # Avoid duplicates
                    cleaned_lines.insert(import_end_index, imp)
                    import_end_index += 1
        
        content = '\n'.join(cleaned_lines)
        
        # Remove any remaining markdown artifacts
        content = content.replace('```javascript', '').replace('```js', '').replace('```', '')
        
        # Ensure proper module format consistency
        if 'import ' in content and 'require(' in content:
            logger.warning(f"Mixed module systems detected in {file_path}, cleaning up...")
            # Convert remaining require() to imports where possible, but handle dynamic requires differently
            import re
            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Convert static require() statements to imports
                if 'const ' in line and ' = require(' in line and '`' not in line:
                    # Static require - convert to import
                    match = re.match(r'(\s*)const (\w+) = require\([\'\"](.*?)[\'\"].*?\);?', line)
                    if match:
                        indent, var_name, module_path = match.groups()
                        # Add import at top and replace line with comment
                        additional_imports.append(f"import {var_name} from '{module_path}';")
                        lines[i] = f"{indent}// import {var_name} from '{module_path}'; // Moved to top-level imports"
                
                # Dynamic require() with template literals - replace with dynamic import
                elif 'require(' in line and '`' in line:
                    # Dynamic require - convert to dynamic import()
                    lines[i] = re.sub(r'require\(([^)]+)\)', r'await import(\1)', line)
                    # Also need to make the function async
                    if 'const ' in line and ' = ' in line:
                        lines[i] = lines[i].replace('const ', 'const ') + ' // Note: converted to dynamic import'
            
            content = '\n'.join(lines)
            
            # Re-add any new imports to top
            if additional_imports:
                content_lines = content.split('\n')
                import_end_index = 0
                for i, line in enumerate(content_lines):
                    if line.strip().startswith('import '):
                        import_end_index = i + 1
                    elif line.strip() and not line.strip().startswith('//'):
                        break
                
                for imp in additional_imports:
                    if imp not in '\n'.join(content_lines[:import_end_index]):
                        content_lines.insert(import_end_index, imp)
                        import_end_index += 1
                
                content = '\n'.join(content_lines)
        
        # Validate JSON files after cleaning
        if file_ext == '.json' or filename.endswith('.json'):
            try:
                import json
                json.loads(content)
                logger.debug(f"JSON validation passed for {file_path}")
            except json.JSONDecodeError as e:
                logger.warning(f"JSON validation failed for {file_path}: {e}")
                # Try to fix common JSON issues
                content = self._fix_json_syntax(content)
                try:
                    json.loads(content)
                    logger.info(f"JSON syntax fixed for {file_path}")
                except json.JSONDecodeError:
                    logger.error(f"Could not fix JSON syntax for {file_path}")
        
        logger.debug(f"Cleaned AI response for {file_path}: {len(content)} characters")
        return content
    
    def _fix_json_syntax(self, content: str) -> str:
        """Fix common JSON syntax issues"""
        # Remove trailing commas before closing brackets/braces
        import re
        content = re.sub(r',(\s*[}\]])', r'\1', content)
        
        # Fix unquoted keys
        content = re.sub(r'(\w+)(\s*:)', r'"\1"\2', content)
        
        # Remove any remaining markdown artifacts
        content = content.replace('```json', '').replace('```', '').strip()
        
        return content
    
    def _validate_generated_code(self, legacy_repo_path: str, 
                               code_generation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the quality of generated modernized code"""
        
        logger.info("Validating generated code quality...")
        
        validation_results = {
            "validation_success": True,
            "quality_metrics": {},
            "comparison_metrics": {},
            "issues_found": [],
            "recommendations": []
        }
        
        try:
            # Analyze modernized code quality
            if code_generation_results.get("ai_generation_success"):
                modernized_analysis = self._analyze_modernized_code()
                validation_results["quality_metrics"] = modernized_analysis
                
                # Compare with original code
                original_analysis = self._analyze_original_code(legacy_repo_path)
                validation_results["comparison_metrics"] = self._compare_code_quality(
                    original_analysis, modernized_analysis
                )
                
                # Generate recommendations
                validation_results["recommendations"] = self._generate_quality_recommendations(
                    modernized_analysis
                )
            
        except Exception as e:
            logger.error(f"Code validation failed: {e}")
            validation_results["validation_success"] = False
            validation_results["error"] = str(e)
        
        return validation_results
    
    def _get_quality_score(self, quality_results: Dict[str, Any]) -> float:
        """Safely extract quality score from quality results"""
        try:
            quality_scores = quality_results.get("quality_scores")
            if quality_scores is None:
                return 0.0
            
            # Handle QualityScore object (has overall_score attribute)
            if hasattr(quality_scores, 'overall_score'):
                return float(quality_scores.overall_score)
            
            # Handle dict (legacy format)
            elif isinstance(quality_scores, dict):
                return float(quality_scores.get("overall_score", 0))
            
            # Default fallback
            return 0.0
        except Exception as e:
            logger.warning(f"Error extracting quality score: {e}")
            return 0.0
    
    def _analyze_modernized_code(self) -> Dict[str, Any]:
        """Analyze the quality of modernized code in output directory"""
        try:
            # Use existing analyzers on the modernized code
            ast_results = self.ast_analyzer.analyze_repository(self.output_directory)
            quality_results = self.quality_analyzer.analyze_repository_quality(self.output_directory)
            
            return {
                "files_analyzed": ast_results.get("files_analyzed", 0),
                "functions_found": ast_results.get("total_functions", 0),
                "classes_found": ast_results.get("total_classes", 0),
                "code_smells": quality_results.get("total_code_smells", 0),
                "quality_score": self._get_quality_score(quality_results)
            }
        except Exception as e:
            logger.warning(f"Error analyzing modernized code: {e}")
            return {}
    
    def _analyze_original_code(self, legacy_repo_path: str) -> Dict[str, Any]:
        """Analyze the quality of original legacy code"""
        try:
            ast_results = self.ast_analyzer.analyze_repository(legacy_repo_path)
            quality_results = self.quality_analyzer.analyze_repository_quality(legacy_repo_path)
            
            return {
                "files_analyzed": ast_results.get("files_analyzed", 0),
                "functions_found": ast_results.get("total_functions", 0),
                "classes_found": ast_results.get("total_classes", 0),
                "code_smells": quality_results.get("total_code_smells", 0),
                "quality_score": self._get_quality_score(quality_results)
            }
        except Exception as e:
            logger.warning(f"Error analyzing original code: {e}")
            return {}
    
    def _compare_code_quality(self, original: Dict[str, Any], 
                            modernized: Dict[str, Any]) -> Dict[str, Any]:
        """Compare code quality metrics between original and modernized versions"""
        
        comparison = {}
        
        try:
            metrics = ["code_smells", "quality_score", "functions_found", "classes_found"]
            
            for metric in metrics:
                orig_val = original.get(metric, 0)
                mod_val = modernized.get(metric, 0)
                
                if metric == "code_smells":
                    # Lower is better for code smells
                    improvement = orig_val - mod_val
                    improvement_pct = (improvement / orig_val * 100) if orig_val > 0 else 0
                elif metric == "quality_score":
                    # Higher is better for quality score
                    improvement = mod_val - orig_val
                    improvement_pct = (improvement / orig_val * 100) if orig_val > 0 else 0
                else:
                    # Neutral comparison for counts
                    improvement = mod_val - orig_val
                    improvement_pct = (improvement / orig_val * 100) if orig_val > 0 else 0
                
                comparison[metric] = {
                    "original": orig_val,
                    "modernized": mod_val,
                    "improvement": improvement,
                    "improvement_percentage": improvement_pct
                }
        
        except Exception as e:
            logger.warning(f"Error comparing code quality: {e}")
        
        return comparison
    
    def _generate_quality_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on code quality analysis"""
        
        recommendations = []
        
        try:
            quality_score = analysis.get("quality_score", 0)
            code_smells = analysis.get("code_smells", 0)
            
            if quality_score < 70:
                recommendations.append("Consider additional refactoring to improve overall code quality")
            
            if code_smells > 50:
                recommendations.append("Focus on resolving remaining code smells for better maintainability")
            
            recommendations.append("Run comprehensive testing to ensure functional equivalence")
            recommendations.append("Consider implementing TypeScript for enhanced type safety")
            recommendations.append("Add comprehensive error handling and logging")
            
        except Exception as e:
            logger.warning(f"Error generating recommendations: {e}")
        
        return recommendations
    
    def _generate_execution_summary(self, framework_results: Dict[str, Any],
                                  code_generation: Dict[str, Any],
                                  validation: Dict[str, Any],
                                  compatibility: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate comprehensive execution summary"""
        
        summary = {
            "execution_timestamp": self.timestamp,
            "framework_integration": "successful",
            "total_files_processed": code_generation.get("files_created", 0),
            "ai_generation_status": "successful" if code_generation.get("ai_generation_success") else "failed",
            "validation_status": "successful" if validation.get("validation_success") else "failed",
            "output_location": self.output_directory,
            "key_achievements": [],
            "next_steps": []
        }
        
        try:
            # Extract key achievements
            if code_generation.get("ai_generation_success"):
                summary["key_achievements"].append(f"Successfully modernized {code_generation.get('files_created', 0)} files")
            
            if validation.get("validation_success"):
                comparison = validation.get("comparison_metrics", {})
                code_smell_improvement = comparison.get("code_smells", {}).get("improvement", 0)
                if code_smell_improvement > 0:
                    summary["key_achievements"].append(f"Reduced code smells by {code_smell_improvement}")
            
            # Framework integration achievements
            readiness_score = framework_results.get("modernization_readiness_score", 0)
            summary["key_achievements"].append(f"Framework analysis completed with {readiness_score:.1f}/100 readiness score")
            
            # Generate next steps
            summary["next_steps"].extend([
                "Run comprehensive integration testing",
                "Deploy to staging environment for validation", 
                "Conduct user acceptance testing",
                "Plan production deployment strategy"
            ])
            
            if validation.get("recommendations"):
                summary["next_steps"].extend(validation["recommendations"][:3])
                
        except Exception as e:
            logger.warning(f"Error generating execution summary: {e}")
        
        return summary

    # ==================== AI-DRIVEN COMPATIBILITY FIXING METHODS ====================
    
    def _ai_compatibility_fixing_workflow(self) -> Dict[str, Any]:
        """Main workflow for AI-driven compatibility fixing"""
        
        logger.info("Starting AI-driven compatibility fixing workflow...")
        
        workflow_results = {
            "status": "started",
            "total_iterations": 0,
            "fixes_applied": [],
            "final_validation": {},
            "success": False
        }
        
        try:
            # Run iterative AI fixing with max 5 iterations
            fix_results = self._iterative_ai_fixing(max_iterations=5)
            workflow_results.update(fix_results)
            
            logger.info(f"Compatibility fixing workflow completed: {workflow_results['status']}")
            
        except Exception as e:
            logger.error(f"Compatibility fixing workflow failed: {e}")
            workflow_results["status"] = "failed"
            workflow_results["error"] = str(e)
        
        return workflow_results
    
    def _iterative_ai_fixing(self, max_iterations: int = 5) -> Dict[str, Any]:
        """Iterative AI-driven fixing until code is runnable"""
        
        results = {
            "status": "unknown",
            "total_iterations": 0,
            "fixes_applied": [],
            "final_validation": {},
            "success": False
        }
        
        iteration = 0
        all_fixes = []
        previous_issue_count = float('inf')
        stagnant_iterations = 0
        
        while iteration < max_iterations:
            logger.info(f"AI compatibility fixing iteration {iteration + 1}/{max_iterations}")
            
            # Step 1: Validate current state
            validation = self._ai_validate_runtime_compatibility()
            current_issue_count = len(validation.get("issues", []))
            
            if not validation.get("has_issues", True):
                logger.info(f"Code is compatible after {iteration} iterations")
                results["status"] = "success"
                results["success"] = True
                break
            
            # Check for improvement
            if current_issue_count < previous_issue_count:
                logger.info(f"Progress: Issues reduced from {previous_issue_count} to {current_issue_count}")
                stagnant_iterations = 0
            elif current_issue_count == previous_issue_count:
                stagnant_iterations += 1
                logger.warning(f"No progress: Issues remain at {current_issue_count} (stagnant for {stagnant_iterations} iterations)")
                
                # Early exit if no progress for 2 iterations
                if stagnant_iterations >= 2:
                    logger.info("Stopping early due to lack of progress")
                    results["status"] = "stagnant"
                    break
            
            # Step 2: AI-driven fixing
            fixes = self._ai_driven_compatibility_fixing(validation)
            all_fixes.extend(fixes.get("fixes_applied", []))
            
            logger.info(f"Iteration {iteration + 1}: Applied {len(fixes.get('fixes_applied', []))} fixes")
            previous_issue_count = current_issue_count
            iteration += 1
        
        results["total_iterations"] = iteration
        results["fixes_applied"] = all_fixes
        results["final_validation"] = self._ai_validate_runtime_compatibility()
        
        if not results["success"]:
            results["status"] = "max_iterations_reached" if iteration >= max_iterations else "failed"
        
        return results
    
    def _ai_validate_runtime_compatibility(self) -> Dict[str, Any]:
        """AI-driven validation of runtime compatibility"""
        
        logger.info("Validating runtime compatibility...")
        
        validation_results = {
            "has_issues": False,
            "issues": [],
            "validation_time": time.time()
        }
        
        try:
            # Check syntax errors
            syntax_errors = self._check_syntax_errors()
            if syntax_errors:
                validation_results["has_issues"] = True
                validation_results["issues"].extend(syntax_errors)
            
            # Check import/export errors  
            import_errors = self._check_import_errors()
            if import_errors:
                validation_results["has_issues"] = True
                validation_results["issues"].extend(import_errors)
            
            # Check dependency issues
            dependency_errors = self._check_dependency_issues()
            if dependency_errors:
                validation_results["has_issues"] = True
                validation_results["issues"].extend(dependency_errors)
            
            # AI analysis of issues if any found
            if validation_results["has_issues"]:
                ai_analysis = self._ai_analyze_compatibility_issues(validation_results["issues"])
                validation_results["ai_analysis"] = ai_analysis
            
            logger.info(f"Runtime validation completed: {len(validation_results['issues'])} issues found")
            
        except Exception as e:
            logger.error(f"Runtime validation failed: {e}")
            validation_results["has_issues"] = True
            validation_results["validation_error"] = str(e)
        
        return validation_results
    
    def _check_syntax_errors(self) -> List[Dict[str, str]]:
        """Check for syntax errors in JavaScript files"""
        
        syntax_errors = []
        
        # Find main JavaScript files to check
        main_files = ['app-media.js', 'app.js', 'index.js', 'main.js']
        
        for filename in main_files:
            file_path = os.path.join(self.output_directory, filename)
            if os.path.exists(file_path):
                try:
                    result = subprocess.run(
                        ['node', '--check', file_path],
                        cwd=self.output_directory,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode != 0:
                        syntax_errors.append({
                            "type": "syntax_error",
                            "file": filename,
                            "error": result.stderr.strip(),
                            "severity": "high"
                        })
                        
                except Exception as e:
                    syntax_errors.append({
                        "type": "syntax_check_failed",
                        "file": filename,
                        "error": str(e),
                        "severity": "medium"
                    })
        
        return syntax_errors
    
    def _check_import_errors(self) -> List[Dict[str, str]]:
        """Check for import/export errors"""
        
        import_errors = []
        
        try:
            # Create a simple test to check imports
            test_script = '''
try {
    const modules = ['./logger.js', './config.js', './metrics.js'];
    for (const mod of modules) {
        try {
            await import(mod);
        } catch (err) {
            console.log(`IMPORT_ERROR:${mod}:${err.message}`);
        }
    }
} catch (err) {
    console.log(`GENERAL_ERROR:${err.message}`);
}
'''
            
            test_file = os.path.join(self.output_directory, 'test_imports.mjs')
            with open(test_file, 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(
                ['node', 'test_imports.mjs'],
                cwd=self.output_directory,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse import errors from output
            for line in result.stdout.split('\n'):
                if line.startswith('IMPORT_ERROR:'):
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        import_errors.append({
                            "type": "import_error",
                            "file": parts[1],
                            "error": parts[2],
                            "severity": "high"
                        })
            
            # Clean up test file
            if os.path.exists(test_file):
                os.remove(test_file)
                
        except Exception as e:
            import_errors.append({
                "type": "import_check_failed",
                "file": "test_imports.mjs",
                "error": str(e),
                "severity": "medium"
            })
        
        return import_errors
    
    def _check_dependency_issues(self) -> List[Dict[str, str]]:
        """Check for dependency-related issues"""
        
        dependency_errors = []
        
        try:
            # Check if package.json exists
            package_json_path = os.path.join(self.output_directory, "package.json")
            if not os.path.exists(package_json_path):
                dependency_errors.append({
                    "type": "missing_package_json",
                    "file": "package.json",
                    "error": "package.json file is missing",
                    "severity": "high"
                })
                return dependency_errors
            
            # Check npm dependencies
            result = subprocess.run(
                ['npm', 'install', '--dry-run'],
                cwd=self.output_directory,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                dependency_errors.append({
                    "type": "dependency_resolution",
                    "file": "package.json",
                    "error": result.stderr.strip(),
                    "severity": "high"
                })
                
        except Exception as e:
            dependency_errors.append({
                "type": "dependency_check_failed",
                "file": "package.json", 
                "error": str(e),
                "severity": "medium"
            })
        
        return dependency_errors
    
    def _ai_analyze_compatibility_issues(self, issues: List[Dict[str, str]]) -> Dict[str, Any]:
        """AI analysis of compatibility issues"""
        
        if not issues:
            return {"analysis": "No issues to analyze"}
        
        try:
            issues_summary = json.dumps(issues, indent=2)
            
            prompt = f"""
Analyze these JavaScript/Node.js modernization compatibility issues and provide fix strategies:

ISSUES FOUND:
{issues_summary}

For each issue, provide:
1. Root cause analysis
2. Specific fix strategy
3. Risk assessment (low/medium/high)
4. Priority level (1-5, where 1 is highest priority)

Focus on ES6 module issues, API compatibility, and dependency problems.
Return analysis as JSON with structured recommendations.
"""
            
            ai_response = llm_call(prompt)
            
            # Try to parse as JSON, fallback to text
            try:
                return json.loads(ai_response)
            except:
                return {"analysis": ai_response, "format": "text"}
                
        except Exception as e:
            logger.warning(f"AI issue analysis failed: {e}")
            return {"analysis": f"AI analysis failed: {e}"}
    
    def _ai_driven_compatibility_fixing(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """AI-driven fixing of compatibility issues"""
        
        logger.info("Starting AI-driven compatibility fixing...")
        
        fix_results = {
            "fixes_applied": [],
            "total_fixes": 0,
            "success": True
        }
        
        issues = validation_results.get("issues", [])
        if not issues:
            logger.info("No issues to fix")
            return fix_results
        
        try:
            # Group issues by type for more efficient fixing
            issues_by_type = {}
            for issue in issues:
                issue_type = issue.get("type", "unknown")
                if issue_type not in issues_by_type:
                    issues_by_type[issue_type] = []
                issues_by_type[issue_type].append(issue)
            
            # Fix issues by type
            for issue_type, type_issues in issues_by_type.items():
                type_fixes = self._ai_fix_issues_by_type(issue_type, type_issues)
                fix_results["fixes_applied"].extend(type_fixes)
            
            fix_results["total_fixes"] = len(fix_results["fixes_applied"])
            logger.info(f"Applied {fix_results['total_fixes']} compatibility fixes")
            
        except Exception as e:
            logger.error(f"AI compatibility fixing failed: {e}")
            fix_results["success"] = False
            fix_results["error"] = str(e)
        
        return fix_results
    
    def _ai_fix_issues_by_type(self, issue_type: str, issues: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Fix issues of a specific type using AI"""
        
        fixes_applied = []
        
        try:
            if issue_type == "import_error":
                fixes_applied.extend(self._ai_fix_import_issues(issues))
            elif issue_type == "syntax_error":
                fixes_applied.extend(self._ai_fix_syntax_issues(issues))
            elif issue_type == "dependency_resolution":
                fixes_applied.extend(self._ai_fix_dependency_issues(issues))
            elif issue_type == "dependency_check_failed":
                fixes_applied.extend(self._ai_fix_dependency_check_issues(issues))
            else:
                logger.warning(f"Unknown issue type: {issue_type}")
                
        except Exception as e:
            logger.error(f"Failed to fix {issue_type} issues: {e}")
        
        return fixes_applied
    
    def _ai_fix_import_issues(self, issues: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """AI-driven fixing of import/export issues"""
        
        fixes = []
        
        for issue in issues:
            try:
                file_path = os.path.join(self.output_directory, issue["file"])
                if not os.path.exists(file_path):
                    continue
                
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Skip files that are already pure ES6 modules
                has_require = 'require(' in content
                has_module_exports = 'module.exports' in content
                has_import = 'import ' in content
                has_export = 'export ' in content
                
                if (has_import or has_export) and not (has_require or has_module_exports):
                    logger.info(f"Skipping {issue['file']} - already pure ES6 module")
                    continue
                
                # AI prompt for fixing import issues
                prompt = f"""
Fix this ES6 module import/export issue in JavaScript:

ERROR: {issue["error"]}
FILE: {issue["file"]}

CURRENT FILE CONTENT:
{content}

**CRITICAL: RETURN ONLY THE COMPLETE CORRECTED FILE CONTENT**
- NO explanations, NO markdown code blocks, NO commentary
- Start directly with the first line of JavaScript code
- End with the last line of JavaScript code
- The response must be EXACTLY what should be written to the file
- NO text like "Here's the corrected version:" or "Explanation:"
- NO ```javascript``` blocks

Focus on:
1. Fixing import/export syntax
2. Correcting module paths  
3. Ensuring ES6 module compatibility

RESPOND WITH PURE JAVASCRIPT ONLY:
"""
                
                fixed_content = llm_call(prompt)
                
                # Clean AI response to extract pure code
                cleaned_content = self._extract_pure_code_from_ai_response(fixed_content, file_path)
                
                if cleaned_content:
                    # Apply the fix
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)
                    
                    fixes.append({
                        "type": "import_fix",
                        "file": issue["file"],
                        "description": f"Fixed import/export issue: {issue['error']}"
                    })
                    
                    logger.info(f"Applied import fix to {issue['file']}")
                else:
                    logger.warning(f"Failed to extract clean code from AI response for {issue['file']}")
                
            except Exception as e:
                logger.warning(f"Failed to fix import issue in {issue.get('file', 'unknown')}: {e}")
        
        return fixes
    
    def _ai_fix_syntax_issues(self, issues: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """AI-driven fixing of syntax issues"""
        
        fixes = []
        
        for issue in issues:
            try:
                file_path = os.path.join(self.output_directory, issue["file"])
                if not os.path.exists(file_path):
                    continue
                
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # AI prompt for fixing syntax issues
                prompt = f"""
Fix this JavaScript syntax error:

ERROR: {issue["error"]}
FILE: {issue["file"]}

CURRENT FILE CONTENT:
{content}

**CRITICAL: RETURN ONLY THE COMPLETE CORRECTED FILE CONTENT**
- NO explanations, NO markdown code blocks, NO commentary
- Start directly with the first line of JavaScript code
- End with the last line of JavaScript code
- The response must be EXACTLY what should be written to the file
- NO text like "Here's the corrected version:" or "Explanation:"
- NO ```javascript``` blocks

Focus on:
1. Correct JavaScript/ES6 syntax
2. Proper function declarations
3. Correct object/array syntax

RESPOND WITH PURE JAVASCRIPT ONLY:
"""
                
                fixed_content = llm_call(prompt)
                
                # Apply the fix
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                fixes.append({
                    "type": "syntax_fix",
                    "file": issue["file"],
                    "description": f"Fixed syntax error: {issue['error']}"
                })
                
                logger.info(f"Applied syntax fix to {issue['file']}")
                
            except Exception as e:
                logger.warning(f"Failed to fix syntax issue in {issue.get('file', 'unknown')}: {e}")
        
        return fixes
    
    def _ai_fix_dependency_check_issues(self, issues: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Fix dependency check failures by updating package.json and installing packages"""
        
        fixes = []
        
        try:
            # Find package.json in output directory
            package_json_path = os.path.join(self.output_directory, "package.json")
            
            if not os.path.exists(package_json_path):
                logger.warning("package.json not found, cannot fix dependency issues")
                return fixes
            
            # Read current package.json
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_content = f.read()
            
            # Apply automatic version fixing
            logger.info("Applying automatic dependency version fixes...")
            fixed_package = self._fix_package_json_versions(package_content)
            
            # Write fixed package.json
            with open(package_json_path, 'w', encoding='utf-8') as f:
                f.write(fixed_package)
            
            logger.info("Updated package.json with correct dependency versions")
            
            # Run npm install to install/update packages
            try:
                result = subprocess.run(
                    ['npm', 'install'],
                    cwd=self.output_directory,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    logger.info("Successfully installed dependencies")
                    fixes.append({
                        "type": "dependency_install",
                        "file": "package.json",
                        "description": "Fixed dependency versions and installed packages"
                    })
                else:
                    logger.warning(f"npm install failed: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                logger.warning("npm install timed out")
            except FileNotFoundError:
                logger.warning("npm not found - cannot install dependencies automatically")
            
            # Mark all dependency issues as addressed
            for issue in issues:
                fixes.append({
                    "type": "dependency_check",
                    "file": issue.get("file", "package.json"),
                    "description": f"Addressed: {issue.get('error', 'dependency issue')}"
                })
            
        except Exception as e:
            logger.error(f"Failed to fix dependency check issues: {e}")
        
        return fixes
    
    def _get_validated_dependencies(self, package_content: str) -> Dict[str, Dict[str, str]]:
        """Get validated versions for all dependencies including recommended additions"""
        validated_deps = {
            "dependencies": {},
            "devDependencies": {}
        }
        
        # Recommended modern dependencies with validated versions (updated 2024-2025)
        recommended_deps = {
            "body-parser": "^1.20.2",
            "express": "^4.18.2", 
            "helmet": "^7.1.0",
            "cors": "^2.8.5",
            "dotenv": "^16.3.1",
            "mongoose": "^8.1.0",
            "mongodb": "^6.3.0",
            "winston": "^3.11.0",
            "socket.io": "^4.6.1",
            "axios": "^1.6.5",
            "moment": "^2.30.1",
            "uuid": "^9.0.1",
            "minimist": "^1.2.8",
            "async": "^3.2.5",
            "handlebars": "^4.7.8"
        }
        
        recommended_dev_deps = {
            "nodemon": "^3.0.3",
            "eslint": "^8.56.0",
            "jest": "^29.7.0"
        }
        
        # List of deprecated/archived packages to remove
        deprecated_packages = {
            'request': 'axios',  # request is deprecated, use axios
            # Add more deprecated packages here as needed
        }
        
        try:
            pkg = json.loads(package_content)
            existing_deps = pkg.get('dependencies', {})
            
            # Remove deprecated packages and log replacements
            for deprecated_pkg, replacement in deprecated_packages.items():
                if deprecated_pkg in existing_deps:
                    logger.warning(f"Removing deprecated package '{deprecated_pkg}' - use '{replacement}' instead")
                    del existing_deps[deprecated_pkg]
                    # Ensure replacement is added if not present
                    if replacement not in existing_deps and replacement in recommended_deps:
                        existing_deps[replacement] = recommended_deps[replacement]
            
            # Validate existing dependencies
            for pkg_name, version in existing_deps.items():
                clean_version = version.replace('^', '').replace('~', '').replace('>=', '')
                
                # Check if current version exists
                if self._validate_npm_package_version(pkg_name, clean_version):
                    validated_deps["dependencies"][pkg_name] = version  # Keep original
                else:
                    # Get correct version - don't use major version constraint for invalid versions
                    correct_version = self._get_latest_compatible_version(pkg_name)
                    validated_deps["dependencies"][pkg_name] = f"^{correct_version}"
                    logger.info(f"Corrected {pkg_name}: {version} -> ^{correct_version}")
            
            # Add recommended dependencies (validate them too)
            for pkg_name, version in recommended_deps.items():
                if pkg_name not in validated_deps["dependencies"]:
                    clean_version = version.replace('^', '')
                    if self._validate_npm_package_version(pkg_name, clean_version):
                        validated_deps["dependencies"][pkg_name] = version
                    else:
                        correct_version = self._get_latest_compatible_version(pkg_name)
                        validated_deps["dependencies"][pkg_name] = f"^{correct_version}"
            
            # Add recommended dev dependencies
            for pkg_name, version in recommended_dev_deps.items():
                clean_version = version.replace('^', '')
                if self._validate_npm_package_version(pkg_name, clean_version):
                    validated_deps["devDependencies"][pkg_name] = version
                else:
                    correct_version = self._get_latest_compatible_version(pkg_name)
                    validated_deps["devDependencies"][pkg_name] = f"^{correct_version}"
                
        except Exception as e:
            logger.warning(f"Error validating dependencies: {e}")
            # Fallback to basic set
            validated_deps["dependencies"] = recommended_deps
            validated_deps["devDependencies"] = recommended_dev_deps
        
        return validated_deps

    def _ai_fix_dependency_issues(self, issues: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """AI-driven fixing of dependency issues with validated versions"""
        
        fixes = []
        
        for issue in issues:
            try:
                package_json_path = os.path.join(self.output_directory, "package.json")
                if not os.path.exists(package_json_path):
                    continue
                
                # Read package.json
                with open(package_json_path, 'r') as f:
                    package_content = f.read()
                
                # Pre-validate and get correct versions for dependencies
                validated_deps = self._get_validated_dependencies(package_content)
                
                # AI prompt for fixing dependency issues with validated versions
                prompt = f"""
Fix this Node.js dependency issue using ONLY VALIDATED VERSIONS:

ERROR: {issue["error"]}

CURRENT PACKAGE.JSON:
{package_content}

VALIDATED DEPENDENCY VERSIONS (use these EXACT versions):
{json.dumps(validated_deps, indent=2)}

**CRITICAL: RETURN ONLY VALID JSON CONTENT**
- NO explanations, NO markdown code blocks, NO commentary
- Start directly with opening brace {{
- End with closing brace }}
- The response must be EXACTLY what should be written to package.json
- NO text like "Here's the corrected version:" or "Explanation:"
- NO ```json``` blocks
- MUST be valid JSON that passes JSON.parse()
- ONLY use dependency versions from the VALIDATED list above

Focus on:
1. Use ONLY the validated dependency versions provided
2. Compatible version ranges from validated list
3. Removing conflicting dependencies

RESPOND WITH PURE JSON ONLY:
"""
                
                fixed_content = llm_call(prompt)
                
                # Validate JSON before applying
                try:
                    json.loads(fixed_content)
                    
                    # Apply the fix
                    with open(package_json_path, 'w') as f:
                        f.write(fixed_content)
                    
                    fixes.append({
                        "type": "dependency_fix",
                        "file": "package.json",
                        "description": f"Fixed dependency issue: {issue['error']}"
                    })
                    
                    logger.info("Applied dependency fix to package.json")
                    
                except json.JSONDecodeError:
                    logger.warning("AI-generated package.json is not valid JSON, skipping fix")
                
            except Exception as e:
                logger.warning(f"Failed to fix dependency issue: {e}")
        
        return fixes

    def _extract_pure_code_from_ai_response(self, ai_response: str, file_path: str) -> str:
        """Extract pure code from AI response that may contain explanations"""
        
        if not ai_response or not ai_response.strip():
            return ""
        
        content = ai_response.strip()
        
        # Remove markdown code blocks
        if content.startswith('```'):
            lines = content.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]  # Remove opening ```
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]  # Remove closing ```
            content = '\n'.join(lines)
        
        # Remove explanation text patterns
        lines = content.split('\n')
        cleaned_lines = []
        code_started = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip common explanation patterns
            if stripped.startswith('Here\'s') or stripped.startswith('Explanation:') or stripped.startswith('The corrected'):
                continue
                
            # Look for actual code start
            if not code_started:
                if (stripped.startswith('import ') or 
                    stripped.startswith('const ') or 
                    stripped.startswith('function ') or
                    stripped.startswith('export ') or
                    stripped.startswith('{') or
                    stripped.startswith('//')):
                    code_started = True
                    cleaned_lines.append(line)
                continue
            else:
                # Once code started, include all lines unless they're clearly explanation
                if not (stripped.startswith('Explanation:') or 
                       stripped.startswith('The main changes') or
                       stripped.startswith('1.') or stripped.startswith('2.') or stripped.startswith('3.')):
                    cleaned_lines.append(line)
        
        cleaned_content = '\n'.join(cleaned_lines).strip()
        
        # Validate that we have meaningful content
        if len(cleaned_content) < 10:
            logger.warning(f"Extracted content too short for {file_path}")
            return ""
        
        return cleaned_content


def execute_ai_modernization(project_config: Dict[str, Any], 
                           output_directory: str = None) -> Dict[str, Any]:
    """
    Convenience function to execute AI-driven modernization
    
    Args:
        project_config: Project configuration dict with legacy_repo_path, target_stack, etc.
        output_directory: Optional output directory for modernized code
        
    Returns:
        Comprehensive execution results
    """
    agent = AIExecutionAgent(output_directory)
    return agent.execute_modernization(project_config)


if __name__ == "__main__":
    # Example usage for testing
    test_config = {
        "project_name": "Auckland Library Media System",
        "legacy_repo_path": "/Users/ianzhou/Desktop/frontend",
        "target_stack": "Node.js + MongoDB + Solr",
        "client": "Auckland University Library"
    }
    
    logger.info("Testing AI Execution Agent...")
    results = execute_ai_modernization(test_config)
    
    if results.get("execution_status") == "success":
        logger.info(f"AI modernization completed successfully!")
        logger.info(f"Modernized code saved to: {results.get('output_directory')}")
        logger.info(f"Files processed: {results.get('code_generation', {}).get('files_created', 0)}")
        
        # Show compatibility results
        compatibility = results.get("compatibility_results", {})
        if compatibility.get("status") == "success":
            logger.info(f"Compatibility fixes applied: {compatibility.get('total_iterations', 0)} iterations")
        elif compatibility.get("status") != "skipped":
            logger.warning(f"Compatibility fixing: {compatibility.get('status', 'unknown')}")
    else:
        logger.error(f"AI modernization failed: {results.get('error', 'Unknown error')}")