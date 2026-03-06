"""
Prompt Engineering System for AI Growth Platform
Core module for managing, testing, and optimizing prompts
"""

import json
import yaml
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from enum import Enum


class PromptStatus(Enum):
    """Status of a prompt in its lifecycle"""
    DRAFT = "draft"
    TESTING = "testing"
    OPTIMIZING = "optimizing"
    PRODUCTION = "production"
    ARCHIVED = "archived"


@dataclass
class PromptMetrics:
    """Metrics for evaluating prompt performance"""
    clarity_score: float = 0.0  # 1-5 scale
    brand_alignment: float = 0.0  # 1-5 scale
    relevance_score: float = 0.0  # 1-5 scale
    tone_match: float = 0.0  # 1-5 scale
    format_compliance: bool = False
    hallucination_detected: bool = False
    user_satisfaction: Optional[float] = None  # 1-5 scale
    iteration_count: int = 0
    
    def average_quality_score(self) -> float:
        """Calculate average quality across all metrics"""
        scores = [self.clarity_score, self.brand_alignment, self.relevance_score, self.tone_match]
        return sum(scores) / len(scores) if scores else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PromptVersion:
    """Version control for a single prompt"""
    version_number: int
    prompt_text: str
    created_date: str
    created_by: str
    notes: str = ""
    metrics: Optional[PromptMetrics] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'version_number': self.version_number,
            'prompt_text': self.prompt_text,
            'created_date': self.created_date,
            'created_by': self.created_by,
            'notes': self.notes,
            'metrics': self.metrics.to_dict() if self.metrics else None
        }


@dataclass
class PromptTemplate:
    """Structured prompt with all components"""
    id: str  # Unique identifier
    name: str
    description: str
    use_case: str
    role: str
    task: str
    constraints: str
    format_spec: str
    examples: List[str] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)
    status: PromptStatus = PromptStatus.DRAFT
    versions: List[PromptVersion] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def build_prompt(self, **kwargs) -> str:
        """Build complete prompt by filling in variables"""
        prompt = f"""[ROLE]
{self.role}

[TASK]
{self._fill_variables(self.task, kwargs)}

[CONSTRAINTS]
{self._fill_variables(self.constraints, kwargs)}

[FORMAT]
{self._fill_variables(self.format_spec, kwargs)}"""
        
        if self.examples:
            prompt += f"\n\n[EXAMPLES]\n"
            for example in self.examples:
                prompt += f"{self._fill_variables(example, kwargs)}\n"
        
        return prompt
    
    @staticmethod
    def _fill_variables(text: str, variables: Dict[str, str]) -> str:
        """Replace [VARIABLE] placeholders with actual values"""
        result = text
        for key, value in variables.items():
            result = result.replace(f"[{key}]", value)
        # Replace any unfilled variables with placeholder message
        import re
        result = re.sub(r'\[[A-Z_]+\]', '[CUSTOMIZE_ME]', result)
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'use_case': self.use_case,
            'role': self.role,
            'task': self.task,
            'constraints': self.constraints,
            'format_spec': self.format_spec,
            'examples': self.examples,
            'variables': self.variables,
            'status': self.status.value,
            'tags': self.tags
        }


class PromptManager:
    """Main class for managing prompts across the organization"""
    
    def __init__(self):
        self.prompts: Dict[str, PromptTemplate] = {}
        self.templates: Dict[str, PromptTemplate] = {}
        self.evaluation_history: List[Dict[str, Any]] = []
    
    def create_prompt(self, 
                     template_id: str,
                     prompt_id: str,
                     custom_variables: Dict[str, str],
                     created_by: str = "system") -> str:
        """
        Create a complete prompt from template with custom variables
        
        Args:
            template_id: ID of the template to use
            prompt_id: Unique ID for this prompt instance
            custom_variables: Dictionary of variable values
            created_by: Who created this prompt
            
        Returns:
            Complete prompt text ready to use
        """
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")
        
        template = self.templates[template_id]
        complete_prompt = template.build_prompt(**custom_variables)
        
        # Store version
        version = PromptVersion(
            version_number=1,
            prompt_text=complete_prompt,
            created_date=datetime.now().isoformat(),
            created_by=created_by
        )
        
        # Create new prompt from template
        new_prompt = PromptTemplate(
            id=prompt_id,
            name=template.name,
            description=template.description,
            use_case=template.use_case,
            role=template.role,
            task=template.task,
            constraints=template.constraints,
            format_spec=template.format_spec,
            examples=template.examples,
            status=PromptStatus.DRAFT,
            versions=[version]
        )
        
        self.prompts[prompt_id] = new_prompt
        return complete_prompt
    
    def register_template(self, template: PromptTemplate) -> None:
        """Register a new prompt template"""
        self.templates[template.id] = template
    
    def get_prompt(self, prompt_id: str) -> Optional[PromptTemplate]:
        """Retrieve a prompt by ID"""
        return self.prompts.get(prompt_id)
    
    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """Retrieve a template by ID"""
        return self.templates.get(template_id)
    
    def update_prompt(self, 
                     prompt_id: str, 
                     new_prompt_text: str,
                     updated_by: str = "system",
                     notes: str = "") -> bool:
        """
        Update a prompt with a new version
        
        Args:
            prompt_id: ID of prompt to update
            new_prompt_text: New prompt text
            updated_by: Who made the update
            notes: Notes about the change
            
        Returns:
            True if successful
        """
        if prompt_id not in self.prompts:
            raise ValueError(f"Prompt {prompt_id} not found")
        
        prompt = self.prompts[prompt_id]
        new_version_number = len(prompt.versions) + 1
        
        new_version = PromptVersion(
            version_number=new_version_number,
            prompt_text=new_prompt_text,
            created_date=datetime.now().isoformat(),
            created_by=updated_by,
            notes=notes
        )
        
        prompt.versions.append(new_version)
        return True
    
    def record_evaluation(self, 
                         prompt_id: str,
                         metrics: PromptMetrics,
                         output_sample: str,
                         evaluator_notes: str = "") -> None:
        """
        Record evaluation metrics for a prompt
        
        Args:
            prompt_id: ID of evaluated prompt
            metrics: PromptMetrics object with scores
            output_sample: Sample output from this prompt
            evaluator_notes: Qualitative feedback
        """
        evaluation = {
            'prompt_id': prompt_id,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics.to_dict(),
            'output_sample': output_sample,
            'notes': evaluator_notes
        }
        
        self.evaluation_history.append(evaluation)
        
        # Update prompt's latest metrics
        if prompt_id in self.prompts:
            prompt = self.prompts[prompt_id]
            latest_version = prompt.versions[-1]
            latest_version.metrics = metrics
    
    def get_evaluation_history(self, prompt_id: str) -> List[Dict[str, Any]]:
        """Get all evaluations for a prompt"""
        return [e for e in self.evaluation_history if e['prompt_id'] == prompt_id]
    
    def list_prompts_by_status(self, status: PromptStatus) -> List[PromptTemplate]:
        """Get all prompts with a specific status"""
        return [p for p in self.prompts.values() if p.status == status]
    
    def export_prompt(self, prompt_id: str, format: str = "json") -> str:
        """
        Export a prompt and its history
        
        Args:
            prompt_id: ID of prompt to export
            format: 'json', 'yaml', or 'text'
            
        Returns:
            Exported prompt in specified format
        """
        if prompt_id not in self.prompts:
            raise ValueError(f"Prompt {prompt_id} not found")
        
        prompt = self.prompts[prompt_id]
        latest_version = prompt.versions[-1]
        
        data = {
            'prompt_id': prompt.id,
            'name': prompt.name,
            'status': prompt.status.value,
            'current_version': latest_version.version_number,
            'prompt_text': latest_version.prompt_text,
            'metrics': latest_version.metrics.to_dict() if latest_version.metrics else None,
            'version_history': [v.to_dict() for v in prompt.versions]
        }
        
        if format == "json":
            return json.dumps(data, indent=2)
        elif format == "yaml":
            return yaml.dump(data, default_flow_style=False)
        else:
            return latest_version.prompt_text
    
    def create_ab_test(self, 
                      prompt_id_a: str,
                      prompt_id_b: str,
                      test_name: str) -> Dict[str, Any]:
        """
        Set up A/B test for two prompt variations
        
        Returns:
            Test configuration
        """
        test_config = {
            'test_name': test_name,
            'created_date': datetime.now().isoformat(),
            'prompt_a': {
                'id': prompt_id_a,
                'version': len(self.prompts[prompt_id_a].versions)
            },
            'prompt_b': {
                'id': prompt_id_b,
                'version': len(self.prompts[prompt_id_b].versions)
            },
            'results': {
                'a_evaluations': [],
                'b_evaluations': []
            }
        }
        return test_config
    
    def generate_report(self, prompt_id: str) -> str:
        """
        Generate a comprehensive report on prompt performance
        
        Args:
            prompt_id: ID of prompt to report on
            
        Returns:
            Formatted report string
        """
        if prompt_id not in self.prompts:
            raise ValueError(f"Prompt {prompt_id} not found")
        
        prompt = self.prompts[prompt_id]
        evaluations = self.get_evaluation_history(prompt_id)
        
        report = f"""
=== PROMPT PERFORMANCE REPORT ===
Prompt ID: {prompt.id}
Name: {prompt.name}
Status: {prompt.status.value}
Version Count: {len(prompt.versions)}

LATEST METRICS:
"""
        if prompt.versions[-1].metrics:
            metrics = prompt.versions[-1].metrics
            report += f"""  Clarity Score: {metrics.clarity_score}/5
  Brand Alignment: {metrics.brand_alignment}/5
  Relevance Score: {metrics.relevance_score}/5
  Tone Match: {metrics.tone_match}/5
  Average Quality: {metrics.average_quality_score():.2f}/5
  Format Compliant: {metrics.format_compliance}
  Hallucinations Detected: {metrics.hallucination_detected}
  Iteration Count: {metrics.iteration_count}
"""
        
        report += f"""
EVALUATION HISTORY: {len(evaluations)} evaluations recorded
"""
        
        if evaluations:
            avg_quality = sum(e['metrics']['clarity_score'] + e['metrics']['brand_alignment'] + 
                           e['metrics']['relevance_score'] + e['metrics']['tone_match']) / (len(evaluations) * 4)
            report += f"  Average Quality Trend: {avg_quality:.2f}/5\n"
        
        return report


# Utility functions for common operations

def load_templates_from_yaml(yaml_file: str) -> List[PromptTemplate]:
    """Load templates from YAML file"""
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    templates = []
    for template_id, template_data in data.get('templates', {}).items():
        template = PromptTemplate(
            id=template_id,
            name=template_data.get('name', ''),
            description=template_data.get('description', ''),
            use_case=template_data.get('use_cases', []),
            role=template_data.get('role', ''),
            task=template_data.get('task', ''),
            constraints=template_data.get('constraints', ''),
            format_spec=template_data.get('format', ''),
            examples=template_data.get('examples', []),
            variables=template_data.get('variables', {})
        )
        templates.append(template)
    
    return templates


def compare_prompts(prompt_a: PromptTemplate, prompt_b: PromptTemplate) -> Dict[str, Any]:
    """Compare two prompts for A/B testing"""
    return {
        'prompt_a_id': prompt_a.id,
        'prompt_b_id': prompt_b.id,
        'differences': {
            'role_differs': prompt_a.role != prompt_b.role,
            'task_differs': prompt_a.task != prompt_b.task,
            'constraints_differ': prompt_a.constraints != prompt_b.constraints,
            'format_differs': prompt_a.format_spec != prompt_b.format_spec
        }
    }
