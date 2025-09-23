# Prompt Engineering Guide for Auckland Library Multi-Agent Framework

## Overview

This guide provides comprehensive instructions for creating effective prompts in the Auckland Library multi-agent modernization system. The framework uses a sophisticated prompt template system that adapts to context, feedback, and iterative improvement cycles.

## Prompt Architecture

### 1. **Dual-Prompt Structure**

Each agent uses a **System Prompt** + **User Prompt** combination:

- **System Prompt**: Defines the agent's role, competencies, and behavioral guidelines
- **User Prompt**: Provides specific task context, data, and instructions

### 2. **Context-Aware Generation**

Prompts are dynamically generated based on:
- Agent type and capabilities
- Current workflow phase
- Cycle number (for iterative improvement)
- Previous results and feedback
- Project configuration

## Agent-Specific Prompt Strategies

### **CodeUnderstandingAgent**

**Purpose**: Legacy system analysis and modernization readiness assessment

**Key Prompt Elements**:
```
CORE COMPETENCIES:
- Legacy codebase analysis and architecture assessment
- Technology stack identification and compatibility evaluation
- Dependency mapping and security vulnerability detection

ANALYSIS FRAMEWORK:
1. Repository Structure Analysis
2. Technology Stack Assessment
3. Dependency and Security Analysis
4. Architecture Pattern Recognition
5. Modernization Feasibility Evaluation
```

**Context Integration**:
- Repository path and target stack from project config
- Specific focus on Auckland Library requirements
- Quantitative metrics and actionable insights

### **ModernizationPlannerAgent**

**Purpose**: Migration strategy development and risk assessment

**Key Prompt Elements**:
```
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
```

**Context Integration**:
- Previous analysis results as input
- Security vulnerability data
- Library-specific business considerations

### **CodemodAgent**

**Purpose**: Automated code transformation and modernization

**Key Prompt Elements**:
```
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
```

**Context Integration**:
- Migration plan as guidance
- Previous cycle feedback for iterative improvement
- Specific technology targets (Node.js, TypeScript)

### **DataMigrationAgent**

**Purpose**: Database and search system migration

**Key Prompt Elements**:
```
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
```

**Context Integration**:
- Source and target system specifications
- Library catalog data requirements
- Performance benchmarks and constraints

### **ValidationAgent**

**Purpose**: Comprehensive system testing and quality assurance

**Key Prompt Elements**:
```
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
```

**Context Integration**:
- Code and data transformation results
- 17-point validation criteria checklist
- Library-specific business logic requirements

### **DocumentationAgent**

**Purpose**: Comprehensive project documentation and knowledge transfer

**Key Prompt Elements**:
```
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
```

**Context Integration**:
- All previous phase results
- Validation outcomes and quality metrics
- Library staff training requirements

## Context-Aware Features

### **1. Feedback Integration**

When validation fails, subsequent cycles receive targeted feedback:

```python
PREVIOUS CYCLE FEEDBACK:
- Failed Areas: Integration testing, Performance testing
- Recommendations: Fix API integration issues, Optimize error handling
- Priority Fixes: Address failing integration tests, Reduce error rate
```

### **2. Iterative Improvement**

Prompts adapt based on cycle number:

```python
CYCLE 2 CONTEXT:
- This is an iterative improvement cycle
- Previous validation identified areas for improvement
- Focus on addressing specific feedback points
- Maintain successful elements from previous cycle
```

### **3. Results Chaining**

Each agent receives relevant results from previous phases:

```python
PROJECT CONTEXT:
- Analysis Results: {repository_analysis}
- Security Assessment: {vulnerability_scan}
- Migration Plan: {migration_strategy}
```

## Best Practices

### **1. Specificity and Context**

✅ **Good**: "Convert 18 callback functions to async/await in the authentication module"
❌ **Bad**: "Modernize the code"

### **2. Quantitative Targets**

✅ **Good**: "Achieve ≥95% integration test pass rate with ≤200ms response time"
❌ **Bad**: "Make sure tests pass and performance is good"

### **3. Domain Expertise**

✅ **Good**: "Preserve library catalog search algorithms and patron data handling logic"
❌ **Bad**: "Don't break existing functionality"

### **4. Output Format Specification**

✅ **Good**: "Provide response in valid JSON format with all required fields"
❌ **Bad**: "Give me the results"

### **5. Actionable Instructions**

✅ **Good**: "Identify specific blockers with recommended solutions and estimated complexity"
❌ **Bad**: "Tell me what's wrong"

## Usage Examples

### **Basic Usage**

```python
from prompt_templates import PromptTemplateEngine, PromptContext

# Create context
context = PromptContext(
    agent_name="CodeUnderstandingAgent",
    phase="analysis",
    project_config={
        "legacy_repo_path": "/path/to/repo",
        "target_stack": "Node.js + MongoDB + Solr"
    }
)

# Generate prompts
engine = PromptTemplateEngine()
system_prompt, user_prompt = engine.generate_prompt("CodeUnderstandingAgent", context)
```

### **Iterative Improvement Usage**

```python
# Cycle 2 with feedback
context = PromptContext(
    agent_name="CodemodAgent",
    phase="execution",
    cycle_number=2,
    feedback={
        "failed_areas": ["Integration testing"],
        "recommendations": ["Fix API integration issues"],
        "priority_fixes": ["Address failing integration tests"]
    },
    previous_results=previous_cycle_results
)

system_prompt, user_prompt = engine.generate_prompt("CodemodAgent", context)
```

### **Integration with Framework**

```python
# In your agent implementation
async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentResult:
    # Create prompt context
    prompt_context = PromptContext(
        agent_name=self.name,
        phase=WorkflowPhase.ANALYSIS,
        project_config=input_data,
        cycle_number=context.get("cycle_number") if context else None,
        feedback=context.get("feedback") if context else None
    )
    
    # Generate optimized prompts
    system_prompt, user_prompt = get_analysis_prompt(prompt_context)
    
    # Call LLM with optimized prompts
    llm_response = await llm_call(system_prompt, user_prompt, self.name)
```

## Prompt Optimization Checklist

### **Before Implementation**
- [ ] Clear role definition and competencies
- [ ] Specific analysis framework or approach
- [ ] Quality standards and success criteria
- [ ] Output format specification
- [ ] Context integration points

### **During Testing**
- [ ] Prompt generates consistent, high-quality responses
- [ ] Context variables are properly substituted
- [ ] Feedback integration works correctly
- [ ] Output format is parseable and actionable
- [ ] Domain-specific requirements are addressed

### **After Deployment**
- [ ] Monitor response quality and consistency
- [ ] Track feedback effectiveness
- [ ] Measure improvement across cycles
- [ ] Update templates based on real-world performance
- [ ] Document lessons learned and best practices

## Advanced Features

### **1. Template Customization**

You can extend the template system for specific use cases:

```python
class CustomPromptEngine(PromptTemplateEngine):
    def _initialize_templates(self):
        templates = super()._initialize_templates()
        # Add custom templates or modify existing ones
        return templates
```

### **2. Context Handlers**

Create custom context processing:

```python
def _generate_custom_context(self, context: PromptContext) -> str:
    # Custom context processing logic
    return context_string
```

### **3. Multi-Model Support**

Templates can be adapted for different LLM models:

```python
context = PromptContext(
    agent_name="CodeUnderstandingAgent",
    phase="analysis",
    target_format="json",  # or "xml", "yaml"
    # ... other context
)
```

## Troubleshooting

### **Common Issues**

1. **Inconsistent Output Format**
   - Ensure output format is clearly specified
   - Add examples of expected JSON structure
   - Validate format in post-processing

2. **Missing Context Integration**
   - Check that all required variables are in prompt_variables
   - Verify context data is properly passed
   - Debug with logging context values

3. **Poor Feedback Integration**
   - Ensure feedback is structured and specific
   - Test feedback generation logic
   - Validate feedback context formatting

4. **Template Variable Errors**
   - Check for missing variables in _build_prompt_variables
   - Ensure proper error handling for missing data
   - Use default values for optional variables

This prompt engineering system provides a robust foundation for high-quality, context-aware LLM interactions in your multi-agent framework.