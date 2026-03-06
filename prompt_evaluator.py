"""
Evaluator module for assessing prompt quality and outputs
Implements metrics and rubrics for objective evaluation
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple, List
from enum import Enum
import json


class EvaluationCategory(Enum):
    """Categories for evaluating prompt quality"""
    CLARITY = "clarity"
    BRAND_ALIGNMENT = "brand_alignment"
    TONE_MATCH = "tone_match"
    RELEVANCE = "relevance"
    FORMAT_COMPLIANCE = "format_compliance"
    HALLUCINATION = "hallucination"


@dataclass
class EvaluationRubric:
    """Rubric for evaluating a specific category"""
    category: EvaluationCategory
    description: str
    scale: int  # typically 1-5
    criteria: Dict[int, str]  # score -> description
    
    def get_score_description(self, score: int) -> str:
        """Get description for a score"""
        return self.criteria.get(score, "Unknown score")


class PromptEvaluator:
    """Evaluates prompts and their outputs against quality standards"""
    
    def __init__(self, brand_guidelines: Dict[str, Any] = None, 
                 target_audience: Dict[str, str] = None):
        """
        Initialize evaluator with brand and audience context
        
        Args:
            brand_guidelines: Brand voice, tone, style guidelines
            target_audience: Description of target audience
        """
        self.brand_guidelines = brand_guidelines or {}
        self.target_audience = target_audience or {}
        self.rubrics = self._create_default_rubrics()
    
    def _create_default_rubrics(self) -> Dict[EvaluationCategory, EvaluationRubric]:
        """Create default evaluation rubrics"""
        return {
            EvaluationCategory.CLARITY: EvaluationRubric(
                category=EvaluationCategory.CLARITY,
                description="How clear and unambiguous is the output?",
                scale=5,
                criteria={
                    5: "Extremely clear, no ambiguity, easy to understand",
                    4: "Clear with minor ambiguities",
                    3: "Mostly clear with some confusing sections",
                    2: "Unclear with significant confusing sections",
                    1: "Very unclear, hard to understand"
                }
            ),
            EvaluationCategory.BRAND_ALIGNMENT: EvaluationRubric(
                category=EvaluationCategory.BRAND_ALIGNMENT,
                description="Does output match brand voice and guidelines?",
                scale=5,
                criteria={
                    5: "Perfect brand alignment, authentic voice",
                    4: "Strong alignment with minor deviations",
                    3: "Acceptable alignment with some inconsistencies",
                    2: "Weak alignment, notable deviations",
                    1: "No brand alignment, misses voice entirely"
                }
            ),
            EvaluationCategory.TONE_MATCH: EvaluationRubric(
                category=EvaluationCategory.TONE_MATCH,
                description="Does tone match requirements and context?",
                scale=5,
                criteria={
                    5: "Perfect tone match, contextually appropriate",
                    4: "Mostly appropriate tone with minor issues",
                    3: "Acceptable tone with some awkwardness",
                    2: "Notable tone mismatches",
                    1: "Wrong tone entirely"
                }
            ),
            EvaluationCategory.RELEVANCE: EvaluationRubric(
                category=EvaluationCategory.RELEVANCE,
                description="Is output relevant to target audience and use case?",
                scale=5,
                criteria={
                    5: "Highly relevant, addresses audience specifically",
                    4: "Relevant with good audience understanding",
                    3: "Somewhat relevant, generic in places",
                    2: "Limited relevance to target audience",
                    1: "Not relevant to audience or use case"
                }
            ),
            EvaluationCategory.FORMAT_COMPLIANCE: EvaluationRubric(
                category=EvaluationCategory.FORMAT_COMPLIANCE,
                description="Does output match specified format requirements?",
                scale=5,
                criteria={
                    5: "Perfect format compliance, all elements present",
                    4: "Good compliance with minor format issues",
                    3: "Acceptable compliance with some missing elements",
                    2: "Poor compliance, missing key elements",
                    1: "Format requirements not met"
                }
            ),
            EvaluationCategory.HALLUCINATION: EvaluationRubric(
                category=EvaluationCategory.HALLUCINATION,
                description="Does output contain false or fabricated information?",
                scale=2,
                criteria={
                    2: "No hallucinations detected",
                    1: "Hallucinations present"
                }
            )
        }
    
    def evaluate_output(self, 
                       output: str,
                       prompt: str = None,
                       category_weights: Dict[EvaluationCategory, float] = None) -> Dict[str, Any]:
        """
        Evaluate output quality across multiple categories
        
        Args:
            output: The output text to evaluate
            prompt: The original prompt (for context)
            category_weights: Custom weights for categories (normalized to sum to 1)
            
        Returns:
            Dictionary with scores and overall rating
        """
        scores = {}
        
        # Score each category (in real implementation, would integrate with LLM judge or human review)
        for category, rubric in self.rubrics.items():
            score = self._score_category(category, output, prompt)
            scores[category.value] = score
        
        # Calculate weighted average
        weights = category_weights or self._default_weights()
        weighted_score = sum(scores.get(cat.value, 0) * weight 
                           for cat, weight in weights.items())
        
        return {
            'category_scores': scores,
            'weighted_score': weighted_score,
            'overall_rating': self._get_rating(weighted_score),
            'rubrics': {cat.value: {
                'description': rubric.description,
                'score_description': rubric.get_score_description(scores.get(cat.value, 0))
            } for cat, rubric in self.rubrics.items()}
        }
    
    def _score_category(self, category: EvaluationCategory, output: str, prompt: str = None) -> int:
        """
        Score a specific evaluation category
        
        In production, this would integrate with:
        - Claude/GPT as a metric judge
        - Human evaluator input
        - Automated checks
        """
        # Placeholder implementation - replace with actual evaluation logic
        # For now, returns dummy scores for demonstration
        
        if category == EvaluationCategory.FORMAT_COMPLIANCE:
            # Check for JSON, list structure, etc.
            if output.startswith('{') or output.startswith('['):
                return 5
            return 3
        elif category == EvaluationCategory.HALLUCINATION:
            # Check for obvious false/fabricated info
            suspicious_phrases = ['definitely', '100%', 'always', 'never']
            if any(phrase in output.lower() for phrase in suspicious_phrases):
                return 1
            return 2
        else:
            # Default scoring - would be replaced with real evaluation
            return 4
    
    def _default_weights(self) -> Dict[EvaluationCategory, float]:
        """Default weights for category scores"""
        return {
            EvaluationCategory.CLARITY: 0.2,
            EvaluationCategory.BRAND_ALIGNMENT: 0.25,
            EvaluationCategory.TONE_MATCH: 0.2,
            EvaluationCategory.RELEVANCE: 0.2,
            EvaluationCategory.FORMAT_COMPLIANCE: 0.1,
            EvaluationCategory.HALLUCINATION: 0.05  # Presence of hallucination is heavily penalized
        }
    
    @staticmethod
    def _get_rating(score: float) -> str:
        """Convert numeric score to rating"""
        if score >= 4.5:
            return "Excellent"
        elif score >= 3.5:
            return "Good"
        elif score >= 2.5:
            return "Acceptable"
        elif score >= 1.5:
            return "Poor"
        else:
            return "Unacceptable"
    
    def compare_outputs(self, 
                       output_a: str, 
                       output_b: str,
                       prompt: str = None) -> Dict[str, Any]:
        """
        Compare two outputs side-by-side
        
        Returns:
            Comparison data including winner and per-category performance
        """
        eval_a = self.evaluate_output(output_a, prompt)
        eval_b = self.evaluate_output(output_b, prompt)
        
        return {
            'output_a': {
                'score': eval_a['weighted_score'],
                'rating': eval_a['overall_rating'],
                'category_scores': eval_a['category_scores']
            },
            'output_b': {
                'score': eval_b['weighted_score'],
                'rating': eval_b['overall_rating'],
                'category_scores': eval_b['category_scores']
            },
            'winner': 'A' if eval_a['weighted_score'] > eval_b['weighted_score'] else 'B',
            'score_difference': abs(eval_a['weighted_score'] - eval_b['weighted_score']),
            'category_winners': self._category_comparison(eval_a, eval_b)
        }
    
    @staticmethod
    def _category_comparison(eval_a: Dict, eval_b: Dict) -> Dict[str, str]:
        """Determine category winners"""
        winners = {}
        for category, score_a in eval_a['category_scores'].items():
            score_b = eval_b['category_scores'].get(category, 0)
            if score_a > score_b:
                winners[category] = 'A'
            elif score_b > score_a:
                winners[category] = 'B'
            else:
                winners[category] = 'Tie'
        return winners
    
    def create_evaluation_checklist(self) -> str:
        """Generate a checklist for manual evaluation"""
        checklist = "PROMPT EVALUATION CHECKLIST\n" + "=" * 50 + "\n\n"
        
        for category, rubric in self.rubrics.items():
            checklist += f"\n{category.value.upper()}\n"
            checklist += f"Description: {rubric.description}\n"
            checklist += "Scoring:\n"
            for score, description in sorted(rubric.criteria.items(), reverse=True):
                checklist += f"  [{score}] {description}\n"
            checklist += "\n"
        
        return checklist
    
    def generate_feedback(self, evaluation: Dict[str, Any]) -> str:
        """Generate human-readable feedback from evaluation"""
        feedback = f"""
EVALUATION RESULTS
Overall Score: {evaluation['weighted_score']:.2f}/5
Rating: {evaluation['overall_rating']}

CATEGORY BREAKDOWN:
"""
        for category, rubric in evaluation['rubrics'].items():
            feedback += f"\n{category.upper()}:"
            feedback += f"\n  Score: {evaluation['category_scores'].get(category, 0)}/5"
            feedback += f"\n  Assessment: {rubric['score_description']}\n"
        
        return feedback


class BrandGuidelinesChecker:
    """Checks output against brand guidelines"""
    
    def __init__(self, brand_guidelines: Dict[str, Any]):
        """
        Initialize with brand guidelines
        
        Args:
            brand_guidelines: Dictionary of brand rules, tone, style
        """
        self.guidelines = brand_guidelines
        self.violations = []
    
    def check_tone(self, output: str, required_tone: str) -> Tuple[bool, List[str]]:
        """Check if output matches required tone"""
        violations = []
        
        tone_rules = {
            'professional': ['seriously', 'damn', 'cute'],  # avoid these
            'casual': ['hereby', 'pursuant'],  # avoid these
            'expert': ['i think', 'maybe', 'perhaps']  # avoid these
        }
        
        if required_tone in tone_rules:
            for word in tone_rules[required_tone]:
                if word.lower() in output.lower():
                    violations.append(f"Tone violation: '{word}' doesn't match '{required_tone}' tone")
        
        is_compliant = len(violations) == 0
        return is_compliant, violations
    
    def check_brand_terms(self, output: str, required_terms: List[str] = None,
                         forbidden_terms: List[str] = None) -> Tuple[bool, List[str]]:
        """Check for required and forbidden terms"""
        violations = []
        
        if required_terms:
            for term in required_terms:
                if term.lower() not in output.lower():
                    violations.append(f"Missing required term: '{term}'")
        
        if forbidden_terms:
            for term in forbidden_terms:
                if term.lower() in output.lower():
                    violations.append(f"Forbidden term detected: '{term}'")
        
        is_compliant = len(violations) == 0
        return is_compliant, violations
    
    def check_length(self, output: str, min_chars: int = None, 
                    max_chars: int = None) -> Tuple[bool, List[str]]:
        """Check length constraints"""
        violations = []
        length = len(output)
        
        if min_chars and length < min_chars:
            violations.append(f"Output too short: {length} chars, minimum {min_chars}")
        
        if max_chars and length > max_chars:
            violations.append(f"Output too long: {length} chars, maximum {max_chars}")
        
        is_compliant = len(violations) == 0
        return is_compliant, violations
