# Implementation Guide: Prompt Engineering for AI Growth Platform

## Quick Start (5 Minutes)

### 1. Review Core Methodology
Start with [PROMPT_ENGINEERING_METHODOLOGY.md](PROMPT_ENGINEERING_METHODOLOGY.md) to understand:
- The 4-stage prompt engineering lifecycle
- Prompt design framework (ROLE + TASK + CONSTRAINTS + FORMAT + EXAMPLES)
- Best practices for marketing and branding

### 2. Customize Prompt Templates
Edit [prompt_templates.yaml](prompt_templates.yaml) to:
- Replace placeholder variables with your brand specifics
- Add your brand voice characteristics
- Define your target personas
- Include industry-specific examples

### 3. Run Examples
```bash
python examples.py
```

This demonstrates:
- Creating prompts from templates
- Evaluating outputs
- Brand compliance checking
- A/B testing variations
- Iteration workflows

---

## Architecture Overview

The system integrates **Prompt Engineering** with **Skills System** for maximum flexibility:

```
┌────────────────────────────────────────────────────────────┐
│              User Request / Task                             │
└──────────────────────┬─────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌────────────────┐          ┌──────────────────┐
│ Prompt Manager │          │ Skills Registry  │
│                │          │                  │
│ • Templates    │          │ • Skill Loading  │
│ • Variables    │          │ • Trigger Match  │
│ • Versioning   │          │ • Priority Sort  │
└────────┬───────┘          └────────┬─────────┘
         │                           │
    [Base Prompt]            [Matched Skills]
         │                           │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │ Skill Injector       │
         │ (merge + tk budgets) │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Enhanced Prompt      │
         │ (wit contextual      │
         │  instructions)       │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ LLM API              │
         │ (Claude/GPT-4)       │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ Prompt Evaluator     │
         │ (score & validate)   │
         └──────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed integrated system design.

---

## Implementation Steps

### Phase 1: Setup (Day 1)

#### 1.1 Install Dependencies
```bash
pip install pyyaml
```

#### 1.2 Define Brand Guidelines
Create `brand_guidelines.json`:
```json
{
  "voice_characteristics": {
    "professionalism": "Professional yet approachable",
    "expertise": "Data-driven and evidence-based",
    "personality": "Confident but humble"
  },
  "key_terms": ["intelligent", "scalable", "proven"],
  "forbidden_terms": ["revolutionary", "innovative", "game-changing"],
  "tone_examples": [
    "We help teams scale their brand presence.",
    "Join 500+ companies using our platform."
  ]
}
```

#### 1.3 Customize Templates
Update `prompt_templates.yaml` with your specific:
- Brand voice characteristics
- Target personas (with demographics, pain points, goals)
- Key differentiators
- Industry-specific content

---

## Phase 0.5: Skills System Integration (Optional but Recommended)

**New Feature**: Dynamic skill injection system augments prompts with contextual instructions at runtime.

### Overview

Skills are reusable instruction blocks that automatically inject into prompts based on triggers:

```
User Request with keyword "SEO"
    ↓
Skill Registry detects "seo" trigger  
    ↓
"seo-content-guidelines" skill matched
    ↓
Skill injected into prompt before LLM call
    ↓
LLM generates SEO-optimized output
```

### 0.5.1 Create Skills Directory
```bash
mkdir -p skills/
```

### 0.5.2 Add Your First Skill File

Create `skills/persona-enforcer.md`:
```yaml
---
name: persona-enforcer
version: "1.0"
description: Enforce brand voice in all content
target_agents:
  - blog_author
  - social_promoter
triggers:
  - "brand"
  - "voice"
  - "tone"
  - "personality"
priority: 15
max_tokens: 300
---

# Persona Enforcer Skill

You MUST maintain exact brand personality:
- Professional yet approachable tone
- Data-driven language
- Lead with customer outcomes
- Forbidden terms: innovative, revolutionary, game-changing

If you deviate, rewrite immediately...
```

### 0.5.3 Integrate Skills Into Code

```python
from skills_system import SkillRegistry, SkillInjector

# Initialize
registry = SkillRegistry("./skills/")
injector = SkillInjector(registry)

# Load all skills from directory
registry.load_skills_from_directory()

# When creating prompt:
prompt = manager.create_prompt(...)  # Base prompt

# Inject skills
user_request = "Write an SEO blog about brand strategy"
enhanced_prompt = injector.inject_skills_into_prompt(
    base_prompt=prompt,
    agent_id="blog_author",      # Which agent
    user_prompt=user_request,     # For trigger matching
    max_tokens=1500               # Token budget
)

# Send enhanced_prompt to LLM
output = llm_api(enhanced_prompt)
```

### 0.5.4 Create an Agent Configuration

Create `agents/blog_author.yaml`:
```yaml
agent_id: blog_author
name: Content Author
description: Creates blog posts and long-form content

skills:
  - persona-enforcer
  - seo-content-guidelines
  - brand-voice-consistency

config:
  max_skills_per_node: 3
  max_total_tokens: 1500
  
prompts:
  - marketing_copy
  - content_strategy
```

### 0.5.5 Skills vs Templates: When to Use Each

| Aspect | **Prompt Templates** | **Skills** |
|--------|--------|--------|
| **Purpose** | Define prompt structure | Add contextual instructions |
| **When to Use** | High-volume, fixed formats | Cross-cutting concerns |
| **Examples** | Marketing copy, email sequences | Brand enforcement, SEO rules, platform guidelines |
| **Frequency** | Used for every request | Triggered by keywords in request |
| **Customization** | Via variables | Via triggers and agent config |
| **Token Cost** | Always included | Only if triggered |

**Combination = Power:**
```
Template provides: Structure + base instructions
Skills provide: Contextual tweaks + specialized guidance  
Together: Flexible yet consistent output
```

---

#### 2.1 Select 2-3 High-Impact Use Cases
Start with the prompts that will give immediate business value:
1. Brand positioning statements
2. LinkedIn copy for outreach
3. Email campaign sequences

#### 2.2 Create Base Prompts
Using the PromptManager:
```python
from prompt_manager import PromptManager, PromptTemplate

# Initialize
manager = PromptManager()

# Register your templates
template = PromptTemplate(
    id="brand_positioning",
    name="Brand Positioning",
    role="You are a brand strategist...",
    task="Create positioning for [COMPANY_TYPE]",
    constraints="Professional tone, 2 paragraphs max...",
    format_spec="Plain text with explanation",
    examples=["Example positioning statement..."],
    variables={'COMPANY_TYPE': 'SaaS company'}
)
manager.register_template(template)

# Generate prompt
prompt = manager.create_prompt(
    template_id="brand_positioning",
    prompt_id="acme_positioning_001",
    custom_variables={'COMPANY_TYPE': 'Data Analytics Platform'},
    created_by="your_name"
)
```

#### 2.3 Manual Testing & Iteration
1. Use prompts with your LLM (Claude, GPT-4, etc.)
2. Evaluate outputs manually
3. Record what works and what doesn't
4. Refine prompt based on learnings

### Phase 3: Evaluation Framework (Week 2)

#### 3.1 Set Up Evaluation Process
Define metrics for your use case:

```python
from prompt_evaluator import PromptEvaluator, PromptMetrics

evaluator = PromptEvaluator(
    brand_guidelines={
        'voice': 'Professional yet approachable',
        'tone': 'expert'
    }
)

# Record evaluation
metrics = PromptMetrics(
    clarity_score=4.5,
    brand_alignment=5.0,
    relevance_score=4.0,
    tone_match=4.5,
    format_compliance=True,
    hallucination_detected=False
)

manager.record_evaluation(
    prompt_id="acme_positioning_001",
    metrics=metrics,
    output_sample="Generated positioning text...",
    evaluator_notes="Strong but could be more specific to target audience"
)
```

#### 3.2 Implement A/B Testing
Compare prompt variations:

```python
# Create variation
manager.update_prompt(
    prompt_id="acme_positioning_001",
    new_prompt_text="Improved prompt with pain point focus...",
    notes="V2: Added target pain point in constraints"
)

# Compare outputs
comparison = evaluator.compare_outputs(output_a, output_b)
# Returns: {winner, score_difference, category_winners}
```

#### 3.3 Document Learnings
Track what improves prompts:
- Specific constraints vs. general ones
- Examples style and quality
- Tone and voice specifications
- Audience context

### Phase 4: Scale (Week 3+)

#### 4.1 Expand Template Library
Build templates for:
- Customer testimonial frameworks
- Case study structures
- Whitepaper outlines
- Social media content by platform
- Each email in a sequence

#### 4.2 Automate Workflows
```python
# Workflow example
class PromptWorkflow:
    def __init__(self, manager, evaluator):
        self.manager = manager
        self.evaluator = evaluator
    
    def generate_and_evaluate(self, template_id, variables, llm_func):
        # Generate prompt
        prompt = self.manager.create_prompt(template_id, **variables)
        
        # Call LLM
        output = llm_func(prompt)
        
        # Evaluate
        evaluation = self.evaluator.evaluate_output(output, prompt)
        
        # Record
        if evaluation['weighted_score'] >= 4.0:
            self.manager.record_evaluation(
                prompt_id=variables.get('prompt_id'),
                metrics=self._build_metrics(evaluation),
                output_sample=output
            )
        
        return output, evaluation
```

#### 4.3 Production Monitoring
```python
# Track performance over time
def monitor_prompt_usage(manager, prompt_id, outputs):
    history = manager.get_evaluation_history(prompt_id)
    
    # Check for degradation
    recent_scores = [e['metrics']['average_quality_score'] 
                     for e in history[-10:]]
    
    if sum(recent_scores)/len(recent_scores) < 3.5:
        print(f"⚠️  Prompt {prompt_id} quality degraded - review needed")
        
        # Trigger review workflow
        return trigger_prompt_refresh(prompt_id)
```

---

## Key Files & Their Purposes

| File | Purpose | When to Use |
|------|---------|------------|
| `PROMPT_ENGINEERING_METHODOLOGY.md` | Core framework and principles | Reference guide, team training |
| `prompt_templates.yaml` | Reusable prompt templates | Creating new prompts, A/B testing |
| `prompt_manager.py` | Manage prompt lifecycle | Production code, create/version/evaluate |
| `prompt_evaluator.py` | Evaluate and score outputs | Quality assurance, A/B testing |
| `examples.py` | Usage examples | Learning, integration examples |

---

## Best Practices Checklist

### Before Create Any Prompt
- [ ] Define success metrics
- [ ] Identify target audience specifics
- [ ] Document brand voice requirements
- [ ] List any constraints or guardrails
- [ ] Provide 1-2 examples of desired output

### During Prompt Refinement
- [ ] Test with 3-5 sample inputs
- [ ] Evaluate against all metrics
- [ ] Check for brand compliance
- [ ] Verify tone consistency
- [ ] Look for hallucinations or false claims

### For Production Prompts
- [ ] Version control with changelog
- [ ] Document decision rationale
- [ ] Set up monitoring metrics
- [ ] Plan refresh cycle (quarterly)
- [ ] Have fallback/escalation process

---

## Integration with Your LLM

### Example: Using with Anthropic's Claude

```python
import anthropic
from prompt_manager import PromptManager

manager = PromptManager()
client = anthropic.Anthropic()

# Get prompt
prompt = manager.create_prompt(
    template_id="brand_positioning",
    prompt_id="client_123",
    custom_variables={'COMPANY_TYPE': 'B2B SaaS'}
)

# Call API
message = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

output = message.content[0].text

# Evaluate
evaluator = PromptEvaluator()
evaluation = evaluator.evaluate_output(output, prompt)

# Record
manager.record_evaluation(
    prompt_id="client_123",
    metrics=metrics,
    output_sample=output
)
```

### Example: Using with OpenAI's GPT-4

```python
import openai
from prompt_manager import PromptManager

# Similar pattern, different API
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a brand expert..."},
        {"role": "user", "content": prompt}
    ]
)
```

---

## Troubleshooting

### Problem: Outputs not matching brand voice
**Solution:**
1. Review brand_guidelines in evaluator
2. Add more specific tone examples to prompt
3. Check for conflicting constraints
4. Test with simplified constraints first

### Problem: Inconsistent quality across variations
**Solution:**
1. Add more specific examples (few-shot learning)
2. Tighten format specifications
3. Include explicit tone and audience in each section
4. Reduce number of variables (simplify prompt)

### Problem: Prompts hallucinating or making false claims
**Solution:**
1. Add explicit instruction: "Only include verifiable facts"
2. Include examples of good fact-checking
3. Add constraint: "If uncertain, include [CITE_NEEDED]"
4. Reduce creative freedom constraints

### Problem: Scaling prompts to new audiences
**Solution:**
1. Create separate templates per audience segment
2. Include audience-specific examples
3. Test with representative audience samples
4. Track performance separately per audience

---

## Metrics & Measurement

### Quality Metrics (Per Output)
- **Clarity**: Can target audience understand this?
- **Brand Alignment**: Is this authentically our voice?
- **Relevance**: Is this useful for the target?
- **Tone Match**: Does it match requirements?
- **Format Compliance**: Does it match the spec?

### Business Metrics (Over Time)
- **Engagement Rate**: Clicks, shares, responses
- **Conversion Rate**: Leads generated, demos booked
- **Time to Production**: Hours from prompt to publishable output
- **Reuse Rate**: Percentage needing edits before publication
- **Team Satisfaction**: Evaluator ratings (1-5 scale)

### Prompt Metrics (Tracking)
- **Iteration Count**: How many versions needed?
- **First-Pass Quality**: Score on first output
- **Improvement Trajectory**: Quality trend over versions
- **Performance Degradation**: Score decline over time

---

## Next Steps

1. **Customize Templates** (1-2 hours)
   - Edit `prompt_templates.yaml` with your brand
   - Add specific examples from your industry
   - Define your personas

2. **Run Examples** (30 minutes)
   - Execute `python examples.py`
   - Understand the workflow
   - Modify for your use case

3. **Pilot Prompts** (1 week)
   - Pick 2-3 high-impact prompts
   - Create, test, iterate
   - Document learnings

4. **Integrate with LLM** (1-2 weeks)
   - Connect to your API (OpenAI, Anthropic, etc.)
   - Build evaluation workflow
   - Set up monitoring

5. **Scale & Optimize** (Ongoing)
   - Expand template library
   - A/B test variations
   - Monitor and refresh prompts

---

## Support & Resources

### In This Repository
- **PROMPT_ENGINEERING_METHODOLOGY.md**: Complete framework
- **prompt_templates.yaml**: Template library  
- **Python modules**: prompt_manager.py, prompt_evaluator.py
- **examples.py**: Working code examples

### External Resources
- OpenAI Prompt Engineering Best Practices
- Anthropic's Claude Prompt Examples
- Brex's Prompt Engineering Guide
- Your organization's brand guidelines

### Getting Help
1. Check the methodology guide for conceptual questions
2. Review examples.py for code patterns
3. Look at prompt_templates.yaml for template examples
4. Use Python docstrings for module documentation

---

## Version History

**v1.0** (Current)
- Core prompt management system
- Evaluation framework
- Template library for marketing use cases
- Implementation guide and examples

---

## Future Enhancements

Planned additions for v2.0:
- [ ] Integration with popular LLM APIs
- [ ] Web dashboard for prompt management
- [ ] Advanced A/B testing with statistical significance
- [ ] Automated prompt optimization using AI
- [ ] Team collaboration features
- [ ] Prompt analytics and insights
- [ ] Integration with marketing automation tools
- [ ] Voice and tone classifier
- [ ] Automated compliance checking

---

**Start with the methodology guide, customize your templates, run the examples, then integrate with your LLM. You'll have a production-ready prompt engineering system in a few days!**
