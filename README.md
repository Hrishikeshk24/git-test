# AI Growth Platform: Prompt Engineering + Skills System
## Integrated Framework for Intelligent Content Generation

A comprehensive, production-ready system combining **Prompt Engineering** (templates) with **Skills System** (dynamic instruction injection) for building, testing, and optimizing AI-powered marketing and branding applications.

---

## 📋 What's Included

### Getting Started
- **[QUICK_START.md](QUICK_START.md)** - ⚡ 15-minute setup guide
- **[README.md](README.md)** - Overview and feature tour (this file)

### Core Documentation
- **[PROMPT_ENGINEERING_METHODOLOGY.md](PROMPT_ENGINEERING_METHODOLOGY.md)** - Framework & principles
  - 4-stage lifecycle
  - Prompt design framework
  - Best practices for marketing/branding
  - A/B testing strategies

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Integrated system design ⭐ NEW
  - How prompts + skills work together
  - Data models and workflows
  - Integration examples
  - Configuration hierarchy

- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Step-by-step guide
  - Setup and customization
  - 4-phase implementation roadmap
  - LLM integration examples
  - Troubleshooting

### Templates & Resources
- **[prompt_templates.yaml](prompt_templates.yaml)** - Prompt templates for:
  - Brand positioning
  - Marketing copy
  - Content strategy
  - Customer messaging
  - Social media content
  - Email campaigns

- **[skills/](skills/)** - Reusable skill instruction blocks ⭐ NEW
  - `persona-enforcer.md` - Brand voice enforcement
  - `seo-content-guidelines.md` - SEO optimization rules
  - `social-platform-best-practices.md` - Platform-specific tactics
  - [Add your own...]

### Python Implementation
- **[prompt_manager.py](prompt_manager.py)** - Template-based prompt management
- **[skills_system.py](skills_system.py)** - Dynamic skill injection ⭐ NEW
- **[prompt_evaluator.py](prompt_evaluator.py)** - Quality evaluation & scoring
- **[examples.py](examples.py)** - Prompt system examples
- **[examples_integrated.py](examples_integrated.py)** - Combined system examples ⭐ NEW

---

## 🚀 Quick Start (5 Minutes)

### 1. Review the Methodology
```bash
# Read the core framework
cat PROMPT_ENGINEERING_METHODOLOGY.md
```

### 2. Understand the Structure
The system uses a simple framework for all prompts:
```
[ROLE] + [TASK] + [CONSTRAINTS] + [FORMAT] + [EXAMPLES]
```

### 3. Customize Templates
Edit `prompt_templates.yaml` and add your:
- Brand voice characteristics
- Target audience personas
- Company-specific examples
- Industry terminology

### 4. Run Examples
```bash
# Install requirements
pip install -r requirements.txt

# Run the examples
python examples.py
```

### 5. Integrate with Your LLM
```python
from prompt_manager import PromptManager
from prompt_evaluator import PromptEvaluator

manager = PromptManager()
evaluator = PromptEvaluator()

# Create prompt from template
prompt = manager.create_prompt(
    template_id="brand_positioning",
    prompt_id="my_prompt_001",
    custom_variables={'COMPANY_TYPE': 'B2B SaaS'},
    created_by="your_name"
)

# Use with your LLM (e.g., Claude, GPT-4)
# output = your_llm_api(prompt)

# Evaluate the output
evaluation = evaluator.evaluate_output(output)
print(f"Score: {evaluation['weighted_score']}/5")
```

---

## 📁 Project Structure

```
prompt-engineering/
├── PROMPT_ENGINEERING_METHODOLOGY.md    # Core framework & principles
├── IMPLEMENTATION_GUIDE.md               # Step-by-step implementation
├── prompt_templates.yaml                 # Reusable templates
├── prompt_manager.py                     # Prompt lifecycle management
├── prompt_evaluator.py                   # Quality evaluation system
├── examples.py                           # Working code examples
├── requirements.txt                      # Python dependencies
└── README.md                             # This file
```

---

## 🎯 Key Features

### Prompt Management
- **Template-Based Creation**: Use YAML templates with variables
- **Version Control**: Track all versions and changes
- **Status Tracking**: DRAFT → TESTING → OPTIMIZING → PRODUCTION
- **Export Options**: JSON, YAML, or plain text formats

### Quality Evaluation
- **Multi-Category Scoring**: 6 evaluation dimensions
  - Clarity (1-5)
  - Brand Alignment (1-5)
  - Tone Match (1-5)
  - Relevance (1-5)
  - Format Compliance (Pass/Fail)
  - Hallucination Detection (Pass/Fail)

- **A/B Testing**: Compare outputs from different prompt variations
- **Weighted Scoring**: Customizable weights for each category
- **Performance Reports**: Track metrics over time

### Brand Compliance
- **Tone Validation**: Check against required tone
- **Term Checking**: Required terms, forbidden terms
- **Length Validation**: Min/max character limits
- **Compliance Reports**: Clear violation explanations

---

## 💡 Use Cases

### 1. Brand Positioning
Create differentiated positioning statements that clearly communicate unique value:
```
→ Use: brand_positioning_statement template
→ Outputs: Clear 1-2 sentence differentiators
→ Typical iterations: 2-3 to perfection
```

### 2. Marketing Copy
Generate high-converting copy for various channels and audiences:
```
→ Use: marketing_copy_generation template
→ Outputs: LinkedIn posts, email subject lines, landing page copy
→ Typical iterations: 3-4 to find winning variation
```

### 3. Content Strategy
Develop multi-month content plans aligned with brand positioning:
```
→ Use: content_strategy template
→ Outputs: Content pillars, calendar, metrics, resource plan
→ Typical iterations: 2-3 to solidify strategy
```

### 4. Customer Messaging
Create lifecycle messaging for onboarding, engagement, retention:
```
→ Use: customer_success_messaging template
→ Outputs: Email sequences, in-app guidance, support responses
→ Typical iterations: 2-3 per sequence
```

### 5. Social Media Voice
Maintain consistent brand voice across platforms:
```
→ Use: social_media_voice template
→ Outputs: Platform-specific posts, tone samples
→ Typical iterations: 1-2 once voice is dialed in
```

---

## 📊 Methodology Overview

### The 4-Stage Prompt Engineering Lifecycle

```
IDEATION
  ↓ What are we trying to accomplish?
DESIGN
  ↓ Structure the prompt with all components
TESTING
  ↓ Generate outputs and evaluate them
OPTIMIZATION
  ↓ Refine based on results and repeat
PRODUCTION
  ↓ Deploy with monitoring and refresh cycles
```

### Key Principles

1. **Clarity & Specificity**
   - Define exact task and output format
   - Include relevant context and constraints
   - Specify tone, style, and audience

2. **Consistency**
   - Use templates for similar prompts
   - Maintain uniform structure
   - Enable predictable A/B testing

3. **Measurability**
   - Define success metrics upfront
   - Track performance over time
   - Enable objective comparisons

4. **Contextual Awareness**
   - Include brand guidelines
   - Reference target audience
   - Consider use case specifics

---

## 🛠️ Python API Quick Reference

### PromptManager
```python
from prompt_manager import PromptManager, PromptTemplate

# Initialize
manager = PromptManager()

# Register template
manager.register_template(my_template)

# Create prompt from template
prompt = manager.create_prompt(
    template_id="template_id",
    prompt_id="unique_id",
    custom_variables={'VAR': 'value'},
    created_by="username"
)

# Update prompt (create new version)
manager.update_prompt(
    prompt_id="id",
    new_prompt_text="Updated prompt...",
    notes="Version 2 improvements"
)

# Record evaluation
manager.record_evaluation(prompt_id, metrics, output_sample)

# Get reports
report = manager.generate_report(prompt_id)
```

### PromptEvaluator
```python
from prompt_evaluator import PromptEvaluator

# Initialize with brand context
evaluator = PromptEvaluator(brand_guidelines={...})

# Evaluate single output
evaluation = evaluator.evaluate_output(output)

# Compare two outputs
comparison = evaluator.compare_outputs(output_a, output_b)

# Check brand compliance
checker = BrandGuidelinesChecker({...})
is_compliant, violations = checker.check_tone(output, 'professional')
```

---

## 🔄 Workflow Example

### Typical Iteration Workflow

```python
# 1. Create initial prompt from template
prompt_v1 = manager.create_prompt(
    template_id="marketing_copy",
    prompt_id="campaign_001",
    custom_variables={'CHANNEL': 'LinkedIn', 'PERSONA': 'CMO'}
)

# 2. Generate sample output with LLM
output_v1 = llm_api(prompt_v1)

# 3. Evaluate output
eval_v1 = evaluator.evaluate_output(output_v1, prompt_v1)
# Score: 3.2/5 - needs improvement

# 4. Identify issue: Missing specific benefit
# 5. Refine prompt with improvement
prompt_v2 = """
[Updated prompt with specific ROI metric in constraints]
"""

# 6. Update in manager
manager.update_prompt(
    prompt_id="campaign_001",
    new_prompt_text=prompt_v2,
    notes="V2: Added specific ROI metric to constraints"
)

# 7. Generate and evaluate again
output_v2 = llm_api(prompt_v2)
eval_v2 = evaluator.evaluate_output(output_v2, prompt_v2)
# Score: 4.3/5 - much better!

# 8. Record successful metrics
manager.record_evaluation(
    "campaign_001",
    metrics_from_eval,
    output_v2,
    "Significant improvement with ROI metric"
)

# 9. A/B test variations
comparison = evaluator.compare_outputs(output_v1, output_v2)
# Winner: V2 by 1.1 points
```

---

## 📈 Getting Started Roadmap

| Phase | Timeline | Tasks |
|-------|----------|-------|
| **Setup** | 1 day | Review methodology, install deps, customize templates |
| **Pilot** | 1 week | Create 2-3 prompts, manual testing, document learnings |
| **Evaluate** | 1 week | Set up metrics, A/B test, refine based on results |
| **Scale** | 2+ weeks | Expand templates, integrate LLM, automate workflows |
| **Monitor** | Ongoing | Track performance, refresh prompts, continuous improvement |

---

## 🎓 Learning Resources

### In This Repository
1. **PROMPT_ENGINEERING_METHODOLOGY.md** - Start here for concepts
2. **prompt_templates.yaml** - Study the template structures
3. **examples.py** - See working code patterns
4. **IMPLEMENTATION_GUIDE.md** - Follow step-by-step guide

### Best Practices Checklist
- [ ] Define success metrics before creating prompt
- [ ] Include 1-2 high-quality examples
- [ ] Tighten constraints based on testing
- [ ] Version control all changes
- [ ] A/B test important variations
- [ ] Monitor performance over time
- [ ] Refresh prompts quarterly

---

## 🔄 Integration Examples

### With Anthropic's Claude
```python
import anthropic
from prompt_manager import PromptManager

client = anthropic.Anthropic()
manager = PromptManager()

prompt = manager.create_prompt(...)

response = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

output = response.content[0].text
```

### With OpenAI's GPT-4
```python
import openai
from prompt_manager import PromptManager

manager = PromptManager()
prompt = manager.create_prompt(...)

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

output = response.choices[0].message.content
```

---

## 📞 Support & Troubleshooting

### Common Issues & Solutions

**Q: How many iterations until a prompt is "perfect"?**
A: Usually 2-4 cycles. First iteration establishes baseline, iterations 2-3 refine specifics, iteration 4 handles edge cases.

**Q: Should I template everything?**
A: Not necessarily. Template high-volume, high-impact prompts (marketing copy, positioning). One-offs can use basic structure.

**Q: How do I handle brand evolution?**
A: Update templates quarterly with new brand guidelines. Flag and refresh existing prompts. Track metrics before/after.

**Q: Can I use this without an LLM API?**
A: Yes! The system works for manual prompt development too. Just skip the LLM integration step.

---

## 📝 Next Steps

1. **Start Here**: Read [PROMPT_ENGINEERING_METHODOLOGY.md](PROMPT_ENGINEERING_METHODOLOGY.md)
2. **Customize**: Edit [prompt_templates.yaml](prompt_templates.yaml) with your brand
3. **Learn**: Run `python examples.py` to see everything in action
4. **Implement**: Follow [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
5. **Integrate**: Connect to your LLM using the integration examples
6. **Scale**: Expand templates and workflows for your team

---

## 📄 License

This prompt engineering methodology and system is provided as-is for use in your AI applications. Customize and extend as needed.

---

## 🎯 Key Takeaways

✅ **Structure matters** - Well-organized prompts consistently outperform ad-hoc requests  
✅ **Test iteratively** - Plan for 2-3 refinement cycles  
✅ **Measure objectively** - Use consistent evaluation rubrics  
✅ **Document everything** - Track what works and why  
✅ **Keep evolving** - Refresh prompts as your brand and audience changes  

---

**Ready to build amazing prompts? Start with the methodology guide and customize your first template today!**
