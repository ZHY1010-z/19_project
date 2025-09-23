#!/usr/bin/env python3
"""
Utility functions for Auckland Library Multi-Agent Modernization Framework

Reusable components for workflow orchestration, validation, and agent communication.
"""

import asyncio
import json
import logging
import time
import os
from typing import Dict, Any, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# AI API Setup
try:
    from anthropic import Anthropic
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) if os.getenv("ANTHROPIC_API_KEY") else None
except ImportError:
    anthropic_client = None

try:
    import openai
    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
except ImportError:
    openai_client = None

# Import prompt template system
try:
    from prompt_templates import PromptTemplateEngine, PromptContext, get_analysis_prompt
    PROMPT_TEMPLATES_AVAILABLE = True
except ImportError:
    PROMPT_TEMPLATES_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

# Configuration Constants
class WorkflowConfig:
    """Central configuration for workflow parameters"""
    MAX_CYCLES = 3
    ACCEPTANCE_THRESHOLD = 90.0
    DEFAULT_TIMEOUT = 60.0
    PARALLEL_WORKERS = 2
    
    # Validation Thresholds
    MIN_INTEGRATION_PASS_RATE = 95.0
    MAX_PERFORMANCE_ERROR_RATE = 1.0
    MIN_CODE_COVERAGE = 85.0
    MIN_OVERALL_SCORE = 85.0

class WorkflowPhase(Enum):
    """Workflow execution phases"""
    ANALYSIS = "analysis"
    PLANNING = "planning"
    EXECUTION = "execution"
    VALIDATION = "validation"
    DOCUMENTATION = "documentation"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ValidationCriteria:
    """Validation criteria structure"""
    integration_pass_rate: float
    performance_error_rate: float
    security_passed: bool
    code_coverage: float
    overall_score: float
    
    def is_acceptable(self, config: WorkflowConfig = None) -> bool:
        """Check if validation criteria meet acceptance standards"""
        config = config or WorkflowConfig()
        
        checks = [
            self.integration_pass_rate >= config.MIN_INTEGRATION_PASS_RATE,
            self.performance_error_rate <= config.MAX_PERFORMANCE_ERROR_RATE,
            self.security_passed,
            self.code_coverage >= config.MIN_CODE_COVERAGE,
            self.overall_score >= config.MIN_OVERALL_SCORE
        ]
        
        passed_checks = sum(checks)
        total_checks = len(checks)
        pass_rate = (passed_checks / total_checks) * 100
        
        return pass_rate >= config.ACCEPTANCE_THRESHOLD

@dataclass
class AgentResult:
    """Standardized result structure for agent operations"""
    agent_name: str
    phase: WorkflowPhase
    status: str
    data: Dict[str, Any]
    execution_time: float
    error_message: Optional[str] = None
    cycle_number: Optional[int] = None

class Timer:
    """Context manager for timing operations"""
    
    def __init__(self, operation_name: str = "Operation"):
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        logger.info(f"{self.operation_name} completed in {duration:.2f}s")
    
    @property
    def duration(self) -> float:
        """Get operation duration"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0

async def llm_call(system_prompt: str, user_prompt: str, agent_name: str = "", model: str = "claude-3-sonnet") -> str:
    """
    Simple LLM call function with API support
    
    Args:
        system_prompt: System instructions for the LLM
        user_prompt: User query/request for the LLM
        agent_name: Name of the calling agent for logging
        model: Model identifier (placeholder for future use)
    
    Returns:
        LLM response string
    """
    logger.info(f"[{agent_name}] LLM Call to {model}")
    
    try:
        # Try Anthropic Claude first
        if anthropic_client:
            response = await asyncio.to_thread(
                anthropic_client.messages.create,
                model="claude-3-sonnet-20240229",  # Default model, can be parameterized later
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            logger.info(f"[{agent_name}] Anthropic API call successful")
            return response.content[0].text
        
        # Try OpenAI if Anthropic not available
        elif openai_client:
            response = await openai_client.chat.completions.create(
                model="gpt-4",  # Default model, can be parameterized later
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=4000
            )
            logger.info(f"[{agent_name}] OpenAI API call successful")
            return response.choices[0].message.content
        
        else:
            # Fallback when no API available
            logger.warning(f"No API keys available, using fallback for {agent_name}")
            return await _fallback_response(system_prompt, user_prompt, agent_name, model)
    
    except Exception as e:
        logger.error(f"API call failed for {agent_name}: {e}")
        return await _fallback_response(system_prompt, user_prompt, agent_name, model)


async def _fallback_response(system_prompt: str, user_prompt: str, agent_name: str, model: str) -> str:
    """
    Fallback response when no API is available
    
    Args:
        system_prompt: System instructions
        user_prompt: User query
        agent_name: Agent identifier
        model: Model name
    
    Returns:
        Simulated response
    """
    logger.info(f"[{agent_name}] Using fallback mode - no API available")
    
    # Simulate processing time based on prompt complexity
    system_length = len(system_prompt)
    user_length = len(user_prompt)
    processing_time = min(2.0, 0.3 + (system_length + user_length) / 10000)
    await asyncio.sleep(processing_time)
    
    # Generate context-aware fallback responses
    if "analysis" in user_prompt.lower():
        return f"""{{\n  "repository_analysis": {{\n    "status": "analyzed",\n    "agent": "{agent_name}",\n    "model": "{model}"\n  }}\n}}"""
    elif "planning" in user_prompt.lower():
        return f"""{{\n  "migration_strategy": {{\n    "status": "planned",\n    "agent": "{agent_name}",\n    "model": "{model}"\n  }}\n}}"""
    elif "transformation" in user_prompt.lower():
        return f"""{{\n  "transformation_results": {{\n    "status": "transformed",\n    "agent": "{agent_name}",\n    "model": "{model}"\n  }}\n}}"""
    elif "migration" in user_prompt.lower():
        return f"""{{\n  "migration_results": {{\n    "status": "migrated",\n    "agent": "{agent_name}",\n    "model": "{model}"\n  }}\n}}"""
    elif "validation" in user_prompt.lower():
        return f"""{{\n  "validation_results": {{\n    "status": "validated",\n    "overall_score": 94.2,\n    "agent": "{agent_name}",\n    "model": "{model}"\n  }}\n}}"""
    elif "documentation" in user_prompt.lower():
        return f"""{{\n  "documentation_results": {{\n    "status": "documented",\n    "agent": "{agent_name}",\n    "model": "{model}"\n  }}\n}}"""
    else:
        return f"""{{\n  "task_result": {{\n    "status": "completed",\n    "agent": "{agent_name}",\n    "model": "{model}"\n  }}\n}}"""

def extract_json_from_response(response: str) -> Dict[str, Any]:
    """
    Extract JSON content from LLM response
    
    Handles responses that may be wrapped in markdown code blocks or contain
    additional text around the JSON content.
    
    Args:
        response: Raw LLM response string
    
    Returns:
        Parsed JSON data as dictionary
    
    Raises:
        ValueError: If no valid JSON is found in the response
    """
    try:
        # Try direct JSON parsing first
        return json.loads(response)
    except json.JSONDecodeError:
        pass
    
    # Try extracting from markdown code blocks
    if "```json" in response:
        json_start = response.find("```json") + 7
        json_end = response.find("```", json_start)
        if json_end != -1:
            json_content = response[json_start:json_end].strip()
            try:
                return json.loads(json_content)
            except json.JSONDecodeError:
                pass
    
    # Try extracting JSON-like content with regex or heuristics
    import re
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, response, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    raise ValueError(f"No valid JSON found in response: {response[:200]}...")

async def run_parallel_tasks(tasks: List[Callable], max_workers: int = None) -> List[Any]:
    """
    Execute multiple tasks in parallel
    
    Args:
        tasks: List of callable tasks to execute
        max_workers: Maximum number of parallel workers
    
    Returns:
        List of task results in the same order as input tasks
    """
    max_workers = max_workers or WorkflowConfig.PARALLEL_WORKERS
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task) for task in tasks]
        results = [future.result() for future in futures]
    
    return results

def generate_feedback(validation_results: Dict[str, Any], criteria: ValidationCriteria) -> Dict[str, Any]:
    """
    Generate structured feedback for failed validations
    
    Args:
        validation_results: Raw validation test results
        criteria: Validation criteria object
    
    Returns:
        Structured feedback dictionary
    """
    feedback = {
        "failed_areas": [],
        "recommendations": [],
        "priority_fixes": [],
        "next_cycle_focus": []
    }
    
    # Analyze each criteria area
    if criteria.integration_pass_rate < WorkflowConfig.MIN_INTEGRATION_PASS_RATE:
        feedback["failed_areas"].append("Integration testing")
        feedback["recommendations"].append("Fix API integration issues and endpoint compatibility")
        feedback["priority_fixes"].append("Address failing integration tests")
        feedback["next_cycle_focus"].append("API stability and error handling")
    
    if criteria.performance_error_rate > WorkflowConfig.MAX_PERFORMANCE_ERROR_RATE:
        feedback["failed_areas"].append("Performance testing")
        feedback["recommendations"].append("Optimize error handling and resource management")
        feedback["priority_fixes"].append("Reduce error rate in load testing")
        feedback["next_cycle_focus"].append("Performance optimization")
    
    if not criteria.security_passed:
        feedback["failed_areas"].append("Security validation")
        feedback["recommendations"].append("Address security vulnerabilities and implement proper validation")
        feedback["priority_fixes"].append("Fix security issues immediately")
        feedback["next_cycle_focus"].append("Security hardening")
    
    if criteria.code_coverage < WorkflowConfig.MIN_CODE_COVERAGE:
        feedback["failed_areas"].append("Code coverage")
        feedback["recommendations"].append("Add comprehensive test cases for uncovered code")
        feedback["priority_fixes"].append("Increase test coverage")
        feedback["next_cycle_focus"].append("Test completeness")
    
    if criteria.overall_score < WorkflowConfig.MIN_OVERALL_SCORE:
        feedback["failed_areas"].append("Overall code quality")
        feedback["recommendations"].append("Improve code quality metrics and technical debt")
        feedback["priority_fixes"].append("Address code quality issues")
        feedback["next_cycle_focus"].append("Code quality improvement")
    
    return feedback

def log_phase_transition(from_phase: WorkflowPhase, to_phase: WorkflowPhase, context: str = ""):
    """Log workflow phase transitions with context"""
    logger.info(f"Phase transition: {from_phase.value.upper()} -> {to_phase.value.upper()}")
    if context:
        logger.info(f"Context: {context}")

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

class WorkflowState:
    """Manages workflow execution state"""
    
    def __init__(self, workflow_id: str, config: Dict[str, Any]):
        self.workflow_id = workflow_id
        self.config = config
        self.current_phase = WorkflowPhase.ANALYSIS
        self.phase_results = {}
        self.cycle_count = 0
        self.start_time = time.time()
        self.feedback_history = []
        
    def update_phase(self, phase: WorkflowPhase, results: Dict[str, Any] = None):
        """Update current phase and store results"""
        previous_phase = self.current_phase
        self.current_phase = phase
        
        if results:
            self.phase_results[phase.value] = results
        
        log_phase_transition(previous_phase, phase)
    
    def add_feedback(self, feedback: Dict[str, Any]):
        """Add feedback to history"""
        feedback["cycle"] = self.cycle_count
        feedback["timestamp"] = time.time()
        self.feedback_history.append(feedback)
    
    def get_execution_time(self) -> float:
        """Get total workflow execution time"""
        return time.time() - self.start_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization"""
        return {
            "workflow_id": self.workflow_id,
            "config": self.config,
            "current_phase": self.current_phase.value,
            "phase_results": self.phase_results,
            "cycle_count": self.cycle_count,
            "execution_time": self.get_execution_time(),
            "feedback_history": self.feedback_history
        }

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

# Agent Interface Definitions for Extensibility
class AgentInterface:
    """Base interface for all agent implementations"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentResult:
        """
        Execute agent task with standardized interface
        
        Args:
            input_data: Task input data
            context: Additional context (cycle number, feedback, etc.)
        
        Returns:
            Standardized AgentResult
        """
        raise NotImplementedError("Agent execute method must be implemented")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data format"""
        return isinstance(input_data, dict)
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "type": self.__class__.__name__
        }