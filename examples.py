"""
Example Usage of Prompt Engineering System
Demonstrates how to use prompt_manager and prompt_evaluator
for building and optimizing prompts in the AI Growth Platform
"""

from prompt_manager import (
    PromptManager, PromptTemplate, PromptStatus, PromptMetrics, 
    load_templates_from_yaml, compare_prompts
)
from prompt_evaluator import (
    PromptEvaluator, EvaluationCategory, BrandGuidelinesChecker
)


def example_1_create_and_manage_prompt():
    """Example 1: Create a prompt from template and manage versions"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Creating and Managing Prompts")
    print("="*60)
    
    # Initialize manager
    manager = PromptManager()
    
    # Create a prompt template
    marketing_copy_template = PromptTemplate(
        id="marketing_copy_v1",
        name="High-Converting Marketing Copy",
        description="Generate compelling copy for various marketing channels",
        use_case="Marketing and branding",
        role="You are a senior marketing copywriter specializing in B2B SaaS with 10+ years experience.",
        task="Write compelling marketing copy for [CHANNEL] that appeals to [PERSONA] and drives [CTA].",
        constraints="""- Tone: Professional yet approachable
- Length: [LENGTH] characters max
- Must include measurable benefit
- Avoid jargon""",
        format_spec="Output copy only, ready to use, no explanation needed",
        examples=[
            "Example: 'Our platform handles 10x more data in half the time. Try it free today.'"
        ],
        variables={
            'CHANNEL': 'LinkedIn, Email, Landing Page, etc.',
            'PERSONA': 'Target audience (e.g., CFOs, Marketing Directors)',
            'CTA': 'Desired action (Schedule demo, Sign up, etc.)',
            'LENGTH': 'Character limit'
        }
    )
    
    # Register the template
    manager.register_template(marketing_copy_template)
    print(f"✓ Registered template: {marketing_copy_template.name}")
    
    # Create a prompt from template
    variables = {
        'CHANNEL': 'LinkedIn Post',
        'PERSONA': 'VP of Marketing at B2B SaaS companies',
        'CTA': 'Schedule product demo',
        'LENGTH': '280'
    }
    
    prompt_text = manager.create_prompt(
        template_id="marketing_copy_v1",
        prompt_id="linkedin_post_001",
        custom_variables=variables,
        created_by="demo_user"
    )
    
    print(f"✓ Created prompt: linkedin_post_001")
    print("\nGenerated Prompt:")
    print("-" * 40)
    print(prompt_text)
    print("-" * 40)
    
    return manager


def example_2_evaluate_outputs(manager: PromptManager):
    """Example 2: Evaluate prompt outputs"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Evaluating Prompt Outputs")
    print("="*60)
    
    # Initialize evaluator with brand context
    brand_guidelines = {
        'voice': 'Professional yet approachable',
        'tone': 'Confident but not arrogant',
        'key_terms': ['intelligent', 'efficient', 'proven'],
        'avoid_terms': ['innovative', 'revolutionary', 'game-changing']
    }
    
    evaluator = PromptEvaluator(brand_guidelines=brand_guidelines)
    
    # Sample outputs to evaluate
    output_a = """Join 500+ marketing teams scaling their growth 10x faster.
Our AI handles months of brand strategy in hours.
See the difference. Book a demo today."""
    
    output_b = """Struggling with brand messaging across channels?
Our platform intelligently aligns your brand voice, proven to reduce 
messaging development time by 60%.
Schedule your demo now."""
    
    print("Evaluating Output A...")
    eval_a = evaluator.evaluate_output(output_a)
    print(f"Score: {eval_a['weighted_score']:.2f}/5 ({eval_a['overall_rating']})")
    print("\nCategory Scores:")
    for category, score in eval_a['category_scores'].items():
        print(f"  {category}: {score}/5")
    
    print("\n" + "-"*40)
    print("Evaluating Output B...")
    eval_b = evaluator.evaluate_output(output_b)
    print(f"Score: {eval_b['weighted_score']:.2f}/5 ({eval_b['overall_rating']})")
    print("\nCategory Scores:")
    for category, score in eval_b['category_scores'].items():
        print(f"  {category}: {score}/5")
    
    # Compare outputs
    print("\n" + "-"*40)
    print("A/B Test Comparison:")
    comparison = evaluator.compare_outputs(output_a, output_b)
    print(f"Winner: Output {comparison['winner']}")
    print(f"Score Difference: {comparison['score_difference']:.2f} points")
    print("\nCategory Winners:")
    for category, winner in comparison['category_winners'].items():
        print(f"  {category}: {winner}")
    
    return evaluator


def example_3_brand_compliance(evaluator: PromptEvaluator):
    """Example 3: Check brand compliance"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Brand Compliance Checking")
    print("="*60)
    
    brand_guidelines = {
        'voice': 'Professional yet approachable',
        'tone': 'expert',
        'required_terms': ['intelligent', 'proven', 'scalable'],
        'forbidden_terms': ['innovative', 'revolutionary', 'cutting-edge'],
        'min_length': 50,
        'max_length': 300
    }
    
    checker = BrandGuidelinesChecker(brand_guidelines)
    
    test_output = """Our intelligent platform has proven results for scaling 
brand operations. Join leading teams who trust us with their messaging."""
    
    print("Testing Output Against Brand Guidelines:")
    print(f"Output: {test_output}\n")
    
    # Check tone
    is_tone_compliant, tone_violations = checker.check_tone(test_output, 'expert')
    print(f"Tone Compliance: {'✓ Pass' if is_tone_compliant else '✗ Fail'}")
    if tone_violations:
        for violation in tone_violations:
            print(f"  - {violation}")
    
    # Check required terms
    is_terms_compliant, term_violations = checker.check_brand_terms(
        test_output, 
        required_terms=['intelligent', 'proven'],
        forbidden_terms=['innovative']
    )
    print(f"Brand Terms Compliance: {'✓ Pass' if is_terms_compliant else '✗ Fail'}")
    if term_violations:
        for violation in term_violations:
            print(f"  - {violation}")
    
    # Check length
    is_length_compliant, length_violations = checker.check_length(
        test_output,
        min_length=50,
        max_length=300
    )
    print(f"Length Compliance: {'✓ Pass' if is_length_compliant else '✗ Fail'}")
    if length_violations:
        for violation in length_violations:
            print(f"  - {violation}")


def example_4_iteration_workflow(manager: PromptManager):
    """Example 4: Iterating and optimizing prompts"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Iterative Prompt Optimization")
    print("="*60)
    
    prompt_id = "linkedin_post_001"
    
    # Original prompt (version 1 - already created)
    print(f"Current versions for {prompt_id}:")
    prompt = manager.get_prompt(prompt_id)
    print(f"  Version {len(prompt.versions)}: Created by {prompt.versions[-1].created_by}")
    
    # Update prompt with improvements (version 2)
    improved_prompt = """ITERATION 1 - REFINED CONSTRAINTS:

[ROLE]
You are a senior marketing copywriter specializing in B2B SaaS with 10+ years experience.

[TASK]
Write LinkedIn post copy that appeals to VP of Marketing at B2B SaaS companies
and drives them to schedule a product demo.

[CONSTRAINTS]
- Tone: Professional yet approachable, confident
- Length: 280 characters maximum
- Must include specific ROI or time metric
- Start with audience pain point
- Avoid overused terms: innovative, revolutionary, game-changing
- Include social proof element

[FORMAT]
Post copy only, ready to publish, include hook in first line

[EXAMPLES]
"Scaling brand messaging across 5+ channels? 
Most teams waste 40 hours/month aligning messaging.
Our platform does it in hours. See how →"""
    
    manager.update_prompt(
        prompt_id=prompt_id,
        new_prompt_text=improved_prompt,
        updated_by="optimization_user",
        notes="Added specific metrics, pain point focus, and social proof element"
    )
    print(f"\n✓ Updated to Version 2")
    print("  Notes: Added specific metrics, pain point focus, and social proof element")
    
    # Record evaluation metrics for the improvement
    improved_metrics = PromptMetrics(
        clarity_score=5.0,
        brand_alignment=4.5,
        relevance_score=5.0,
        tone_match=4.5,
        format_compliance=True,
        hallucination_detected=False,
        iteration_count=2
    )
    
    manager.record_evaluation(
        prompt_id=prompt_id,
        metrics=improved_metrics,
        output_sample="Scaling brand messaging across channels? We cut that from 40hrs to 1hr.",
        evaluator_notes="Significant improvement. Pain point makes it more relevant."
    )
    
    print(f"✓ Recorded evaluation metrics: {improved_metrics.average_quality_score():.2f}/5")
    
    # Generate performance report
    report = manager.generate_report(prompt_id)
    print("\nPerformance Report:")
    print(report)


def example_5_ab_testing(manager: PromptManager, evaluator: PromptEvaluator):
    """Example 5: A/B testing different prompt variations"""
    print("\n" + "="*60)
    print("EXAMPLE 5: A/B Testing Prompt Variations")
    print("="*60)
    
    # Create version A and B for testing
    version_a_variables = {
        'CHANNEL': 'LinkedIn Post',
        'PERSONA': 'VP of Marketing at B2B SaaS',
        'CTA': 'Schedule product demo',
        'LENGTH': '280'
    }
    
    version_b_variables = {
        'CHANNEL': 'LinkedIn Post',
        'PERSONA': 'VP of Marketing at B2B SaaS',
        'CTA': 'Click to learn more',
        'LENGTH': '280'
    }
    
    # Simulated outputs from each version
    output_a = """40 hours every month spent aligning brand voice?
Our platform uses AI to intelligently scale messaging across channels.
Proven by 500+ teams. Schedule demo →"""
    
    output_b = """Scale your brand messaging faster than your competition.
Watch your team deliver consistent brand voice in hours, not weeks.
AI-powered, proven, and designed for growth teams. Learn more →"""
    
    print("Test Setup:")
    print("Version A: Focus on time/hours metric")
    print("Version B: Focus on competitive advantage")
    print()
    
    # Compare outputs
    comparison = evaluator.compare_outputs(output_a, output_b)
    
    print(f"Version A Score: {comparison['output_a']['score']:.2f}/5")
    print(f"Version B Score: {comparison['output_b']['score']:.2f}/5")
    print(f"\nWinner: Version {comparison['winner']} by {comparison['score_difference']:.2f} points")
    
    print("\nDetailed Comparison:")
    for category, winner in comparison['category_winners'].items():
        print(f"  {category}: Version {winner}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("PROMPT ENGINEERING SYSTEM - USAGE EXAMPLES")
    print("AI Growth Platform - Branding & Marketing")
    print("="*60)
    
    # Example 1: Create and manage prompts
    manager = example_1_create_and_manage_prompt()
    
    # Example 2: Evaluate outputs
    evaluator = example_2_evaluate_outputs(manager)
    
    # Example 3: Brand compliance
    example_3_brand_compliance(evaluator)
    
    # Example 4: Iteration workflow
    example_4_iteration_workflow(manager)
    
    # Example 5: A/B testing
    example_5_ab_testing(manager, evaluator)
    
    print("\n" + "="*60)
    print("✓ All examples completed successfully!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Customize prompt templates with your brand guidelines")
    print("2. Integrate with your LLM/AI backend")
    print("3. Implement human evaluation workflows")
    print("4. Set up monitoring and analytics")
    print("5. Establish prompt review and approval process")


if __name__ == "__main__":
    main()
