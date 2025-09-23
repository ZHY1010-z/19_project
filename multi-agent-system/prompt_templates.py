#!/usr/bin/env python3
"""
Prompt Templates and Engineering System for Auckland Library Multi-Agent Framework

Provides structured, optimized prompts for each agent with context-aware generation.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class PromptType(Enum):
    """Types of prompts for different purposes"""
    ANALYSIS = "analysis"
    PLANNING = "planning"
    TRANSFORMATION = "transformation"
    MIGRATION = "migration"
    VALIDATION = "validation"
    DOCUMENTATION = "documentation"
    FEEDBACK = "feedback"

@dataclass
class PromptContext:
    """Context information for prompt generation"""
    agent_name: str
    phase: str
    cycle_number: Optional[int] = None
    project_config: Optional[Dict[str, Any]] = None
    previous_results: Optional[Dict[str, Any]] = None
    feedback: Optional[Dict[str, Any]] = None
    target_format: str = "json"

class PromptTemplateEngine:
    """Advanced prompt template engine with context-aware generation"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.context_handlers = self._initialize_context_handlers()
    
    def _initialize_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize all prompt templates"""
        return {
            "CodeUnderstandingAgent": {
                "system": """You are an expert software architect and legacy system analyst specializing in modernization projects.

CORE COMPETENCIES:
- Legacy codebase analysis and architecture assessment
- Technology stack identification and compatibility evaluation
- Dependency mapping and security vulnerability detection
- Code complexity measurement and maintainability scoring
- Modernization readiness assessment

ANALYSIS FRAMEWORK:
1. Repository Structure Analysis
2. Technology Stack Assessment
3. Dependency and Security Analysis
4. Architecture Pattern Recognition
5. Modernization Feasibility Evaluation

OUTPUT REQUIREMENTS:
- Provide detailed, actionable insights
- Use quantitative metrics where possible
- Identify specific blockers and recommendations
- Format response as valid JSON matching expected schema
- Focus on Auckland Library's specific modernization needs""",
                
                "user": """LEGACY SYSTEM MODERNIZATION ANALYSIS

PROJECT CONTEXT:
- Client: Auckland Library
- Source System: {legacy_repo_path}
- Target Stack: {target_stack}
- Project Goal: {project_goal}

ANALYSIS SCOPE:
1. Repository Structure and File Organization
2. Programming Languages and Framework Versions
3. Dependencies, Libraries, and Security Vulnerabilities
4. Architecture Patterns and Design Quality
5. Database Schema and Data Models
6. API Endpoints and Integration Points
7. Test Coverage and Documentation Quality
8. Performance Bottlenecks and Scalability Issues

SPECIFIC FOCUS AREAS:
- Legacy callback patterns vs modern async/await
- Outdated framework versions requiring updates
- Security vulnerabilities in dependencies
- Database migration complexity (MySQL → MongoDB)
- Search system upgrade requirements (Solr 8.11 → 9.2)
- Library-specific business logic preservation

DELIVERABLES:
Provide comprehensive analysis in JSON format including:
- Repository metrics and language distribution
- Framework detection with version compatibility
- Security vulnerability assessment
- Modernization readiness score (0-100)
- Specific recommendations and blockers
- Estimated complexity and timeline impact

{context_specific_instructions}"""
            },
            
            "ModernizationPlannerAgent": {
                "system": """You are a senior technical project manager and migration strategy expert specializing in large-scale system modernization.

CORE COMPETENCIES:
- Migration strategy design and risk assessment
- Resource planning and timeline estimation
- Security vulnerability analysis and remediation planning
- Stakeholder management and approval workflows
- Technology adoption and change management

PLANNING FRAMEWORK:
1. Strategic Migration Approach Selection
2. Risk Assessment and Mitigation Planning
3. Resource Allocation and Timeline Development
4. Security Enhancement Strategy
5. Stakeholder Communication and Approval Workflow

DECISION CRITERIA:
- Minimize system downtime and user disruption
- Preserve critical business functionality
- Enhance security and performance
- Optimize resource utilization
- Ensure knowledge transfer and team readiness""",
                
                "user": """MIGRATION STRATEGY DEVELOPMENT

PROJECT CONTEXT:
- Client: Auckland Library
- Current Analysis: {analysis_summary}
- Security Assessment: {vulnerability_summary}
- Target Architecture: {target_stack}
- Timeline Constraints: {timeline_constraints}

STRATEGY REQUIREMENTS:
1. Incremental Migration Approach
   - Phase breakdown with dependencies
   - Rollback strategies for each phase
   - Testing and validation checkpoints

2. Risk Assessment Matrix
   - Technical risks (complexity, compatibility, performance)
   - Business risks (downtime, data loss, user impact)
   - Mitigation strategies with contingency plans

3. Resource Planning
   - Team composition and skill requirements
   - Infrastructure and tooling needs
   - Training and knowledge transfer plans

4. Security Enhancement Strategy
   - Vulnerability remediation priorities
   - Modern security practices implementation
   - Compliance and audit considerations

5. Stakeholder Management
   - Communication plan and approval gates
   - User training and change management
   - Success metrics and monitoring

LIBRARY-SPECIFIC CONSIDERATIONS:
- Catalog data integrity during migration
- Search functionality continuity
- Patron account and borrowing history preservation
- Staff workflow minimal disruption
- Integration with library management systems

{context_specific_instructions}"""
            },
            
            "CodemodAgent": {
                "system": """You are an expert software engineer specializing in automated code transformation and modernization.

CORE COMPETENCIES:
- Legacy code pattern recognition and modernization
- Framework and dependency upgrades
- Automated refactoring and code transformation
- Build system integration and optimization
- Test automation and quality assurance

TRANSFORMATION APPROACH:
1. Pattern-based code modernization
2. Dependency and framework updates
3. Code quality and performance optimization
4. Build and deployment pipeline enhancement
5. Automated testing and validation

QUALITY STANDARDS:
- Maintain functional equivalence
- Improve code maintainability and readability
- Enhance performance and security
- Ensure comprehensive test coverage
- Follow modern development best practices""",
                
                "user": """CODE TRANSFORMATION EXECUTION

PROJECT CONTEXT:
- Migration Plan: {migration_strategy}
- Current Cycle: {cycle_number}
- Target Stack: Node.js + MongoDB + Solr
{feedback_context}

TRANSFORMATION SCOPE:
1. Framework Modernization
   - Express.js version upgrade and configuration
   - React component modernization
   - TypeScript integration and type definitions

2. Code Pattern Updates
   - Callback to async/await conversion
   - Promise-based API implementation
   - Modern ES6+ syntax adoption
   - Error handling improvement

3. Dependency Management
   - Package version updates with compatibility checking
   - Security vulnerability patching
   - Unused dependency cleanup
   - Modern alternative replacements

4. Build System Enhancement
   - Webpack/Vite configuration optimization
   - Development workflow improvement
   - Production build optimization
   - Testing framework integration

5. Code Quality Improvements
   - ESLint and Prettier configuration
   - Code splitting and modularity
   - Performance optimization
   - Documentation and comments

LIBRARY-SPECIFIC REQUIREMENTS:
- Preserve catalog search algorithms
- Maintain patron data handling logic
- Ensure API backward compatibility
- Optimize database query patterns

{context_specific_instructions}"""
            },
            
            "DataMigrationAgent": {
                "system": """You are a database migration specialist and search system expert focusing on large-scale data transformations.

CORE COMPETENCIES:
- Database schema design and migration
- ETL pipeline development and optimization
- Search engine configuration and tuning
- Data integrity validation and quality assurance
- Performance optimization and scalability planning

MIGRATION FRAMEWORK:
1. Schema Analysis and Transformation Design
2. ETL Pipeline Development and Testing
3. Data Integrity Validation and Quality Control
4. Search Index Rebuilding and Optimization
5. Performance Testing and Rollback Planning

DATA QUALITY STANDARDS:
- 100% data integrity preservation
- Zero data loss tolerance
- Comprehensive validation checkpoints
- Performance benchmarking and optimization
- Rollback capability maintenance""",
                
                "user": """DATABASE AND SEARCH MIGRATION

PROJECT CONTEXT:
- Migration Plan: {migration_strategy}
- Current Cycle: {cycle_number}
- Source: MySQL 5.7 + Solr 8.11
- Target: MongoDB 6.0 + Solr 9.2
{feedback_context}

MIGRATION SCOPE:
1. Database Schema Transformation
   - MySQL to MongoDB schema mapping
   - Relational to document model conversion
   - Index strategy and performance optimization
   - Data type conversion and validation

2. Data Migration Pipeline
   - ETL process design and implementation
   - Batch processing and incremental updates
   - Data validation and quality checks
   - Error handling and recovery mechanisms

3. Search System Upgrade
   - Solr 8.11 to 9.2 migration path
   - Index schema redesign and optimization
   - Search relevance tuning for library catalog
   - Performance benchmarking and optimization

4. Library-Specific Data Handling
   - Book catalog and metadata preservation
   - Patron records and borrowing history
   - Digital asset and file attachment migration
   - Search facets and filtering optimization

5. Quality Assurance
   - Data integrity verification
   - Performance regression testing
   - Search accuracy validation
   - Backup and rollback verification

CRITICAL SUCCESS FACTORS:
- Zero data loss during migration
- Minimal search downtime
- Preserved search relevance and accuracy
- Optimized query performance

{context_specific_instructions}"""
            },
            
            "ValidationAgent": {
                "system": """You are a comprehensive quality assurance engineer and system validation expert specializing in enterprise software testing.

CORE COMPETENCIES:
- Integration and end-to-end testing
- Performance and load testing
- Security vulnerability assessment
- Code quality and coverage analysis
- Business logic validation and compliance

VALIDATION FRAMEWORK:
1. Functional Testing (Integration, Unit, E2E)
2. Performance Testing (Load, Stress, Scalability)
3. Security Testing (Vulnerability, Penetration, Compliance)
4. Code Quality Assessment (Coverage, Complexity, Maintainability)
5. Business Logic Validation (Workflows, Data Integrity, Compliance)

ACCEPTANCE CRITERIA:
- Integration Testing: ≥95% pass rate
- Performance Testing: ≤1% error rate, ≤200ms response time
- Security Testing: Zero critical vulnerabilities
- Code Coverage: ≥85% for new/modified code
- Business Logic: 100% critical workflow functionality""",
                
                "user": """COMPREHENSIVE SYSTEM VALIDATION

PROJECT CONTEXT:
- Code Transformation Results: {code_results_summary}
- Data Migration Results: {data_results_summary}
- Current Cycle: {cycle_number}
- Target System: Node.js + MongoDB + Solr

VALIDATION SCOPE:
1. Functional Validation
   - API endpoint integration testing
   - Database CRUD operation validation
   - Search functionality accuracy testing
   - User authentication and authorization
   - Business workflow end-to-end testing

2. Performance Validation
   - Load testing with 1000+ concurrent users
   - Database query performance benchmarking
   - Search response time optimization
   - Memory usage and resource utilization
   - Scalability and bottleneck identification

3. Security Validation
   - Vulnerability scanning and assessment
   - Authentication mechanism testing
   - Authorization and access control validation
   - Input validation and injection prevention
   - Data encryption and privacy compliance

4. Code Quality Assessment
   - Test coverage analysis and reporting
   - Code complexity and maintainability metrics
   - Linting and style guide compliance
   - Technical debt assessment
   - Documentation quality evaluation

5. Library-Specific Business Logic
   - Catalog search accuracy and relevance
   - Patron account management functionality
   - Book borrowing and return workflows
   - Fine calculation and payment processing
   - Report generation and data export

VALIDATION CRITERIA (17-Point Checklist):
- Integration test pass rate ≥95%
- Unit test pass rate ≥90%
- E2E test pass rate ≥95%
- Load test error rate ≤1%
- 95th percentile response time ≤200ms
- Database query performance ≤100ms average
- Zero critical/high security vulnerabilities
- All authentication flows functional
- Proper access controls implemented
- SQL injection/XSS protection verified
- Code coverage ≥85%
- Linting score ≥90/100
- Cyclomatic complexity ≤10 per function
- Technical debt ratio ≤30%
- Data integrity 100% for critical operations
- All library workflows functional
- Search performance within thresholds

{context_specific_instructions}"""
            },
            
            "DocumentationAgent": {
                "system": """You are a technical documentation specialist and knowledge management expert focusing on comprehensive project documentation.

CORE COMPETENCIES:
- Technical documentation architecture and design
- User guide and training material development
- API documentation and developer resources
- Process documentation and workflow mapping
- Knowledge transfer and change management

DOCUMENTATION FRAMEWORK:
1. Technical Documentation (Architecture, APIs, Database)
2. User Documentation (Guides, Training, Troubleshooting)
3. Process Documentation (Migration, Operations, Maintenance)
4. Knowledge Transfer (Handover, Training, Support)
5. Compliance Documentation (Audit, Security, Regulatory)

QUALITY STANDARDS:
- Clear, actionable, and comprehensive content
- Multiple audience targeting and accessibility
- Version control and maintenance procedures
- Integration with development workflows
- Measurable training and adoption outcomes""",
                
                "user": """COMPREHENSIVE PROJECT DOCUMENTATION

PROJECT CONTEXT:
- Execution Results: {execution_summary}
- Validation Outcomes: {validation_summary}
- Project: Auckland Library Legacy System Modernization
- Technology Stack: Node.js + MongoDB + Solr

DOCUMENTATION SCOPE:
1. Technical Documentation
   - System architecture diagrams and documentation
   - API documentation with OpenAPI 3.0 specification
   - Database schema documentation and data dictionary
   - Deployment guides and environment configuration
   - Infrastructure and DevOps documentation

2. User Documentation
   - Staff training materials and quick-start guides
   - Feature comparison matrix (old vs new system)
   - Troubleshooting guides and FAQ
   - Video tutorials and interactive walkthroughs
   - User interface changes and workflow updates

3. Administrative Documentation
   - System configuration and user management
   - Backup and disaster recovery procedures
   - Monitoring and maintenance schedules
   - Security policies and compliance guides
   - Performance tuning and optimization guides

4. Process Documentation
   - Migration timeline and milestone documentation
   - Lessons learned and best practices
   - Issue tracking and resolution procedures
   - Change management and approval workflows
   - Quality assurance and testing procedures

5. Knowledge Transfer Materials
   - Technical handover documentation
   - Training schedules and learning paths
   - Support contact information and escalation
   - Transition timeline and responsibility matrix
   - Post-implementation support procedures

LIBRARY-SPECIFIC FOCUS:
- Library staff workflow changes and adaptations
- Patron-facing feature updates and improvements
- Integration with existing library management systems
- Compliance with library industry standards
- Accessibility and usability considerations

{context_specific_instructions}"""
            }
        }
    
    def _initialize_context_handlers(self) -> Dict[str, callable]:
        """Initialize context-specific instruction handlers"""
        return {
            "feedback_aware": self._generate_feedback_context,
            "cycle_aware": self._generate_cycle_context,
            "results_aware": self._generate_results_context,
            "config_aware": self._generate_config_context
        }
    
    def generate_prompt(self, agent_name: str, context: PromptContext) -> tuple[str, str]:
        """
        Generate optimized system and user prompts for specific agent and context
        
        Args:
            agent_name: Name of the agent requesting the prompt
            context: Context information for prompt generation
            
        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        if agent_name not in self.templates:
            raise ValueError(f"No templates found for agent: {agent_name}")
        
        template = self.templates[agent_name]
        
        # Generate context-specific instructions
        context_instructions = self._generate_context_instructions(context)
        
        # Build user prompt with context
        user_prompt_vars = self._build_prompt_variables(context)
        user_prompt_vars["context_specific_instructions"] = context_instructions
        
        # Format prompts
        system_prompt = template["system"]
        user_prompt = template["user"].format(**user_prompt_vars)
        
        return system_prompt, user_prompt
    
    def _generate_context_instructions(self, context: PromptContext) -> str:
        """Generate context-specific instructions"""
        instructions = []
        
        # Cycle-specific instructions
        if context.cycle_number and context.cycle_number > 1:
            instructions.append(f"CYCLE {context.cycle_number} CONTEXT:")
            instructions.append("- This is an iterative improvement cycle")
            instructions.append("- Previous validation identified areas for improvement")
            instructions.append("- Focus on addressing specific feedback points")
            instructions.append("- Maintain successful elements from previous cycle")
        
        # Feedback-aware instructions
        if context.feedback:
            instructions.append("\nFEEDBACK INTEGRATION:")
            for area in context.feedback.get("failed_areas", []):
                instructions.append(f"- Address failures in: {area}")
            for rec in context.feedback.get("recommendations", []):
                instructions.append(f"- Implement: {rec}")
        
        # Results-aware instructions
        if context.previous_results:
            instructions.append("\nPREVIOUS RESULTS CONTEXT:")
            instructions.append("- Build upon successful outcomes from previous phases")
            instructions.append("- Maintain consistency with established patterns")
            instructions.append("- Leverage existing analysis and insights")
        
        # Format-specific instructions
        instructions.append(f"\nOUTPUT FORMAT:")
        instructions.append(f"- Provide response in valid {context.target_format.upper()} format")
        instructions.append("- Include all required fields and proper data types")
        instructions.append("- Ensure response is parseable and actionable")
        
        return "\n".join(instructions) if instructions else ""
    
    def _build_prompt_variables(self, context: PromptContext) -> Dict[str, str]:
        """Build variable dictionary for prompt formatting"""
        variables = {
            "agent_name": context.agent_name,
            "phase": context.phase,
            "cycle_number": str(context.cycle_number or 1),
            "target_format": context.target_format,
            "legacy_repo_path": "",
            "target_stack": "Node.js + MongoDB + Solr",
            "project_goal": "Legacy system modernization for Auckland Library",
            "timeline_constraints": "8-12 weeks implementation timeline",
            "analysis_summary": "",
            "vulnerability_summary": "",
            "migration_strategy": "",
            "code_results_summary": "",
            "data_results_summary": "",
            "execution_summary": "",
            "validation_summary": "",
            "feedback_context": ""
        }
        
        # Override with context-specific values
        if context.project_config:
            variables.update({
                "legacy_repo_path": context.project_config.get("legacy_repo_path", ""),
                "target_stack": context.project_config.get("target_stack", "Node.js + MongoDB + Solr"),
                "project_goal": f"Modernization of {context.project_config.get('project_name', 'Legacy System')}"
            })
        
        # Add previous results context
        if context.previous_results:
            variables.update({
                "analysis_summary": str(context.previous_results.get("repository_analysis", "")),
                "vulnerability_summary": str(context.previous_results.get("security_assessment", "")),
                "migration_strategy": str(context.previous_results.get("migration_strategy", "")),
                "code_results_summary": str(context.previous_results.get("code_transformation", "")),
                "data_results_summary": str(context.previous_results.get("data_migration", "")),
                "execution_summary": str(context.previous_results.get("execution_results", "")),
                "validation_summary": str(context.previous_results.get("validation_result", ""))
            })
        
        # Add feedback context
        if context.feedback:
            feedback_text = f"\nPREVIOUS CYCLE FEEDBACK:\n"
            feedback_text += f"Failed Areas: {', '.join(context.feedback.get('failed_areas', []))}\n"
            feedback_text += f"Recommendations: {', '.join(context.feedback.get('recommendations', []))}\n"
            feedback_text += f"Priority Fixes: {', '.join(context.feedback.get('priority_fixes', []))}\n"
            variables["feedback_context"] = feedback_text
        
        return variables
    
    def _generate_feedback_context(self, context: PromptContext) -> str:
        """Generate feedback-specific context"""
        if not context.feedback:
            return ""
        
        return f"""
PREVIOUS CYCLE FEEDBACK:
- Failed Areas: {', '.join(context.feedback.get('failed_areas', []))}
- Recommendations: {', '.join(context.feedback.get('recommendations', []))}
- Priority Fixes: {', '.join(context.feedback.get('priority_fixes', []))}
"""
    
    def _generate_cycle_context(self, context: PromptContext) -> str:
        """Generate cycle-specific context"""
        if not context.cycle_number or context.cycle_number == 1:
            return "Initial implementation cycle - focus on comprehensive execution."
        
        return f"""
CYCLE {context.cycle_number} CONTEXT:
- This is an iterative improvement cycle
- Previous cycles identified areas for enhancement
- Focus on specific issues while maintaining successful elements
"""
    
    def _generate_results_context(self, context: PromptContext) -> str:
        """Generate results-aware context"""
        if not context.previous_results:
            return ""
        
        return """
PREVIOUS RESULTS INTEGRATION:
- Build upon successful outcomes from previous phases
- Maintain consistency with established patterns
- Leverage existing analysis and insights
"""
    
    def _generate_config_context(self, context: PromptContext) -> str:
        """Generate configuration-specific context"""
        if not context.project_config:
            return ""
        
        config = context.project_config
        return f"""
PROJECT CONFIGURATION:
- Project: {config.get('project_name', 'Unknown')}
- Repository: {config.get('legacy_repo_path', 'Unknown')}
- Target: {config.get('target_stack', 'Unknown')}
- Client: {config.get('client', 'Unknown')}
"""

# Convenience functions for framework integration
def get_analysis_prompt(context: PromptContext) -> tuple[str, str]:
    """Get optimized prompts for CodeUnderstandingAgent"""
    engine = PromptTemplateEngine()
    return engine.generate_prompt("CodeUnderstandingAgent", context)

def get_planning_prompt(context: PromptContext) -> tuple[str, str]:
    """Get optimized prompts for ModernizationPlannerAgent"""
    engine = PromptTemplateEngine()
    return engine.generate_prompt("ModernizationPlannerAgent", context)

def get_transformation_prompt(context: PromptContext) -> tuple[str, str]:
    """Get optimized prompts for CodemodAgent"""
    engine = PromptTemplateEngine()
    return engine.generate_prompt("CodemodAgent", context)

def get_migration_prompt(context: PromptContext) -> tuple[str, str]:
    """Get optimized prompts for DataMigrationAgent"""
    engine = PromptTemplateEngine()
    return engine.generate_prompt("DataMigrationAgent", context)

def get_validation_prompt(context: PromptContext) -> tuple[str, str]:
    """Get optimized prompts for ValidationAgent"""
    engine = PromptTemplateEngine()
    return engine.generate_prompt("ValidationAgent", context)

def get_documentation_prompt(context: PromptContext) -> tuple[str, str]:
    """Get optimized prompts for DocumentationAgent"""
    engine = PromptTemplateEngine()
    return engine.generate_prompt("DocumentationAgent", context)