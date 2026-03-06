"""
Integrated Examples: Prompt Engineering + Skills System
Demonstrates how to use both systems together for AI-powered content creation
"""

from prompt_manager import PromptManager, PromptTemplate, PromptMetrics
from skills_system import (
    SkillRegistry, SkillInjector, Skill, create_sample_skills
)
from prompt_evaluator import PromptEvaluator, BrandGuidelinesChecker


def example_1_skills_injection_workflow():
    """Example 1: Basic workflow with prompt and skills injection"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Prompt + Skills Injection Workflow")
    print("="*70)
    
    # Initialize systems
    manager = PromptManager()
    registry = SkillRegistry()
    injector = SkillInjector(registry)
    
    # Register sample skills
    for skill in create_sample_skills():
        registry.register_skill(skill)
    
    print(f"✓ Registered {len(registry.skills)} skills")
    print(f"✓ Skills available for {len(registry.agent_skills)} agents\n")
    
    # Create base prompt from template
    marketing_template = PromptTemplate(
        id="marketing_copy_blog",
        name="Blog Post Marketing Copy",
        description="Generate compelling blog post content",
        use_case="Content marketing",
        role="You are an expert content strategist specializing in B2B marketing.",
        task="Write a compelling blog post about [TOPIC] targeting [AUDIENCE].",
        constraints="""- Professional yet approachable tone
- Include specific metrics or examples
- Clear, scannable structure with multiple sections
- 2000+ words
- Include data-driven insights""",
        format_spec="""Markdown format with:
- H1 title
- 3-4 H2 sections
- Short paragraphs (3-4 sentences max)
- Meta description (155-160 chars)""",
        examples=[
            "Title: How to Scale Your Brand Messaging Across 10+ Channels\nSections: The Challenge, Why Tools Fail, Better Approach, Implementation, Results"
        ],
        variables={
            'TOPIC': 'Main topic for blog post',
            'AUDIENCE': 'Target reader (e.g., VP of Marketing, CMO)'
        }
    )
    
    manager.register_template(marketing_template)
    
    # User makes request
    user_request = "Write an SEO-optimized blog post about scaling brand messaging for marketing directors"
    print(f"User Request: {user_request}\n")
    
    # Step 1: Create base prompt
    variables = {
        'TOPIC': 'Scaling Brand Messaging Across Channels',
        'AUDIENCE': 'VP of Marketing, Marketing Directors'
    }
    
    base_prompt = manager.create_prompt(
        template_id="marketing_copy_blog",
        prompt_id="blog_scaling_001",
        custom_variables=variables,
        created_by="integration_example"
    )
    
    print("Step 1: Generated Base Prompt")
    print("-" * 70)
    print(base_prompt[:500] + "...\n")
    
    # Step 2: Find applicable skills
    matched_skills = registry.find_applicable_skills(
        agent_id="blog_author",
        user_prompt=user_request
    )
    
    print(f"Step 2: Skill Matching Results")
    print("-" * 70)
    print(f"Matched {len(matched_skills)} skills (priority order):\n")
    for i, match in enumerate(matched_skills, 1):
        print(f"{i}. {match.skill.name}")
        print(f"   Priority: {match.skill.priority}")
        print(f"   Match Confidence: {match.match_confidence:.0%}")
        print(f"   Description: {match.skill.description}\n")
    
    # Step 3: Inject skills into prompt
    enhanced_prompt = injector.inject_skills_into_prompt(
        base_prompt=base_prompt,
        agent_id="blog_author",
        user_prompt=user_request,
        max_tokens=1500
    )
    
    print(f"Step 3: Enhanced Prompt with Injected Skills")
    print("-" * 70)
    # Show the injected portion
    if "### CONTEXTUAL SKILLS" in enhanced_prompt:
        skills_section = enhanced_prompt.split("### CONTEXTUAL SKILLS")[1]
        print("### CONTEXTUAL SKILLS FOR THIS TASK")
        print(skills_section[:600] + "...\n")
    
    # Step 4: Show what would be sent to LLM
    print(f"Step 4: Ready for LLM")
    print("-" * 70)
    print("✓ Base prompt structure established")
    print(f"✓ {len(matched_skills)} skills injected")
    print(f"✓ Total tokens estimated: ~{len(enhanced_prompt)//4}")
    print("✓ Ready to send to LLM (Claude/GPT-4)\n")


def example_2_dynamic_skill_selection():
    """Example 2: Different requests trigger different skills"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Dynamic Skill Selection for Different Requests")
    print("="*70)
    
    registry = SkillRegistry()
    for skill in create_sample_skills():
        registry.register_skill(skill)
    
    # Test different user requests
    test_requests = [
        ("Write a blog post", "blog_author"),
        ("Write an SEO-optimized blog for CMOs", "blog_author"),
        ("Create social media posts for LinkedIn", "social_promoter"),
        ("Promote our latest blog on all platforms", "social_promoter"),
        ("Search our documents for revenue data", "default_agent")
    ]
    
    print("\nTesting skill matching for various requests:\n")
    
    for user_request, agent_id in test_requests:
        matches = registry.find_applicable_skills(agent_id, user_request)
        
        print(f"REQUEST: \"{user_request}\"")
        print(f"AGENT: {agent_id}")
        print(f"SKILLS MATCHED: {len(matches)}")
        
        if matches:
            for i, match in enumerate(matches, 1):
                print(f"  {i}. {match.skill.name} (priority {match.skill.priority})")
        else:
            print("  (No skills matched)")
        print()


def example_3_token_budget_management():
    """Example 3: Skills respecting token budget constraints"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Token Budget Management")
    print("="*70)
    
    registry = SkillRegistry()
    injector = SkillInjector(registry)
    
    # Create skills with different token requirements
    test_skills = [
        Skill(
            name="skill_a",
            version="1.0",
            description="High-priority skill",
            target_agents=["test_agent"],
            triggers=["test"],
            priority=15,
            max_tokens=500,
            instructions="A" * 2000  # ~500 tokens
        ),
        Skill(
            name="skill_b",
            version="1.0",
            description="Medium-priority skill",
            target_agents=["test_agent"],
            triggers=["test"],
            priority=10,
            max_tokens=400,
            instructions="B" * 1600  # ~400 tokens
        ),
        Skill(
            name="skill_c",
            version="1.0",
            description="Lower-priority skill",
            target_agents=["test_agent"],
            triggers=["test"],
            priority=5,
            max_tokens=300,
            instructions="C" * 1200  # ~300 tokens
        )
    ]
    
    for skill in test_skills:
        registry.register_skill(skill)
    
    # Test with different token budgets
    base_prompt = "This is a test prompt."
    test_budgets = [400, 900, 1500, 3000]
    
    print("\nMatching skills against available token budgets:\n")
    
    for budget in test_budgets:
        matches = registry.find_applicable_skills("test_agent", "test")
        
        # Simulate injection with budget
        injected_tokens = 0
        injected_count = 0
        
        for match in matches:
            skill_tokens = match.skill.max_tokens
            if injected_tokens + skill_tokens <= budget:
                injected_tokens += skill_tokens
                injected_count += 1
            else:
                break
        
        print(f"Budget: {budget} tokens")
        print(f"  Skills that fit: {injected_count}/{len(matches)}")
        print(f"  Actual tokens used: {injected_tokens}")
        
        if injected_count > 0:
            for i in range(injected_count):
                print(f"    ✓ {matches[i].skill.name}")
        
        remaining = len(matches) - injected_count
        if remaining > 0:
            print(f"    ✗ {remaining} skills dropped (budget exceeded)")
        print()


def example_4_agent_specific_configuration():
    """Example 4: Agent-specific skill configuration"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Agent-Specific Skill Configuration")
    print("="*70)
    
    registry = SkillRegistry()
    for skill in create_sample_skills():
        registry.register_skill(skill)
    
    # Show agent configurations
    agents = [
        ("blog_author", "Content creation for blog posts"),
        ("social_promoter", "Social media post generation"),
        ("default_agent", "General Q&A and RAG")
    ]
    
    print("\nAgent Skill Configurations:\n")
    
    for agent_id, description in agents:
        available_skills = registry.list_skills_for_agent(agent_id)
        
        print(f"Agent: {agent_id}")
        print(f"Purpose: {description}")
        print(f"Available Skills: {len(available_skills)}")
        
        if available_skills:
            # Sort by priority
            sorted_skills = sorted(available_skills, 
                                  key=lambda s: s.priority, 
                                  reverse=True)
            for skill in sorted_skills[:5]:  # Show top 5
                print(f"  • {skill.name} (priority {skill.priority})")
        print()


def example_5_registry_statistics():
    """Example 5: Skills registry statistics and monitoring"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Registry Statistics & Monitoring")
    print("="*70)
    
    registry = SkillRegistry()
    for skill in create_sample_skills():
        registry.register_skill(skill)
    
    stats = registry.get_statistics()
    
    print("\nSkills Registry Statistics:\n")
    print(f"Total Skills: {stats['total_skills']}")
    print(f"Total Agents: {stats['agents_with_skills']}")
    print(f"Active Skills: {stats['active_skills']}")
    
    print("\nSkills per Agent:")
    for agent, count in sorted(stats['skills_by_agent'].items()):
        print(f"  • {agent}: {count} skills")


def example_6_integrated_workflow():
    """Example 6: Complete integrated workflow"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Complete Integrated Workflow")
    print("="*70)
    
    # Initialize all systems
    manager = PromptManager()
    registry = SkillRegistry()
    injector = SkillInjector(registry)
    evaluator = PromptEvaluator()
    
    # Register skills
    for skill in create_sample_skills():
        registry.register_skill(skill)
    
    # Register prompt template
    template = PromptTemplate(
        id="social_post",
        name="Social Media Post",
        role="You are a social media strategist.",
        task="Write a social media post for [PLATFORM] about [TOPIC].",
        constraints="Professional, engaging, on-brand",
        format_spec="Platform-optimized post text",
        examples=["Example post..."],
        variables={'PLATFORM': 'LinkedIn or Twitter', 'TOPIC': 'Company news'}
    )
    manager.register_template(template)
    
    # User request
    user_request = "Create a LinkedIn post about our new AI platform for marketing"
    print(f"User Request: {user_request}\n")
    
    # Workflow steps
    print("WORKFLOW EXECUTION:\n")
    
    # 1. Create prompt
    print("1️⃣  Creating base prompt from template...")
    prompt = manager.create_prompt(
        template_id="social_post",
        prompt_id="linkedin_001",
        custom_variables={
            'PLATFORM': 'LinkedIn',
            'TOPIC': 'New AI platform announcement'
        },
        created_by="workflow"
    )
    print("   ✓ Prompt created\n")
    
    # 2. Match skills
    print("2️⃣  Matching applicable skills...")
    skills = registry.find_applicable_skills("social_promoter", user_request)
    print(f"   ✓ Found {len(skills)} matching skills\n")
    
    # 3. Inject skills
    print("3️⃣  Injecting skills into prompt...")
    enhanced_prompt = injector.inject_skills_into_prompt(
        base_prompt=prompt,
        agent_id="social_promoter",
        user_prompt=user_request,
        max_tokens=1500
    )
    print("   ✓ Skills injected, prompt enhanced\n")
    
    # 4. Show what goes to LLM
    print("4️⃣  Ready for LLM...")
    print(f"   • Prompt length: {len(enhanced_prompt)} chars")
    print(f"   • Estimated tokens: ~{len(enhanced_prompt)//4}")
    print(f"   • Skills injected: {len(skills)}")
    print("   • Ready to call Claude/GPT-4\n")
    
    # 5. Simulate LLM output
    print("5️⃣  [Simulated LLM Response]")
    simulated_output = """
🚀 We just launched something we've been working on for months.

Our new platform helps marketing teams scale their brand voice instantly.
Instead of rewriting copy 5 times across 5 channels, we do it once—intelligently.

The result? Our customers save 20+ hours per week on messaging.
And the output is more consistent than ever.

This is how modern teams build at scale.

Ready to see it work? → [demo link]

#MarketingAI #BrandStrategy #MarketingAutomation
"""
    print(f"   {simulated_output}\n")
    
    # 6. Evaluate output
    print("6️⃣  Evaluating output...")
    evaluation = evaluator.evaluate_output(simulated_output)
    print(f"   • Quality Score: {evaluation['weighted_score']:.2f}/5")
    print(f"   • Rating: {evaluation['overall_rating']}")
    print("   ✓ Evaluation complete\n")
    
    # 7. Record metrics
    print("7️⃣  Recording metrics...")
    metrics = PromptMetrics(
        clarity_score=4.5,
        brand_alignment=4.8,
        relevance_score=4.6,
        tone_match=4.7,
        format_compliance=True,
        hallucination_detected=False,
        iteration_count=1
    )
    manager.record_evaluation(
        "linkedin_001",
        metrics,
        simulated_output,
        "First iteration, excellent quality. Skills worked great together."
    )
    print("   ✓ Metrics recorded\n")
    
    print("✅ WORKFLOW COMPLETE\n")


def main():
    """Run all integrated examples"""
    print("\n" + "="*70)
    print("INTEGRATED SYSTEM EXAMPLES: PROMPTS + SKILLS")
    print("="*70)
    
    example_1_skills_injection_workflow()
    example_2_dynamic_skill_selection()
    example_3_token_budget_management()
    example_4_agent_specific_configuration()
    example_5_registry_statistics()
    example_6_integrated_workflow()
    
    print("\n" + "="*70)
    print("✅ All integrated examples completed!")
    print("="*70)
    print("\nKey Takeaways:")
    print("1. Prompts provide structure; skills add intelligence")
    print("2. Skills match dynamically based on user request")
    print("3. Token budgets prevent prompt bloat")
    print("4. Agent configuration controls which skills apply")
    print("5. Both systems feed into evaluation and improvement")
    print("\nNext Steps:")
    print("- Load skills from YAML directory at startup")
    print("- Integrate with your LLM API")
    print("- Set up monitoring dashboard")
    print("- Create custom skills for your workflows")


if __name__ == "__main__":
    main()
