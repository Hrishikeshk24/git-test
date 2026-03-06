# Quick Start: Prompt Engineering + Skills System

**Get your integrated system running in 15 minutes.**

## What You'll Build

A two-layer prompt composition system:
1. **Prompt Templates** → Structural framework (who, what, how format)
2. **Skills System** → Contextual enhancements (trigger-based instructions)

Together = Maximum flexibility with minimal duplication.

---

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install pyyaml
```

### 2. Create Directory Structure
```bash
mkdir -p skills/
```

### 3. Copy Sample Files
From this repository:
- Keep `prompt_manager.py`
- Keep `skills_system.py`
- Keep `prompt_evaluator.py`
- Copy `prompt_templates.yaml`
- Copy `skills/persona-enforcer.md`
- Copy `skills/seo-content-guidelines.md`

### 4. Run Integrated Example
```bash
python examples_integrated.py
```

You should see 6 examples showing how both systems work together.

---

## How It Works (30 seconds)

### Basic Flow
```python
from prompt_manager import PromptManager
from skills_system import SkillRegistry, SkillInjector

# 1. Load systems
manager = PromptManager()
registry = SkillRegistry("./skills/")
injector = SkillInjector(registry)
registry.load_skills_from_directory()

# 2. Create base prompt
prompt = manager.create_prompt(
    template_id="marketing_copy",
    prompt_id="blog_001",
    custom_variables={'CHANNEL': 'Blog', 'PERSONA': 'CMO'}
)

# 3. Inject matching skills
enhanced = injector.inject_skills_into_prompt(
    base_prompt=prompt,
    agent_id="blog_author",
    user_prompt=user_request,
    max_tokens=1500
)

# 4. Send to LLM
output = claude_api(enhanced)
```

---

## Key Concepts

### Prompts (Templates)
- **Static** prompt structures
- **Reusable** across projects
- **Customizable** via variables
- **Versioned** for tracking

**Use for:** Marketing copy, content strategies, email sequences

### Skills
- **Dynamic** instruction injection
- **Trigger-based** (keyword matching)
- **Priority-ordered** (best match first)
- **Token-budgeted** (don't bloat prompts)

**Use for:** Brand enforcement, SEO rules, platform guidelines, compliance

### Together
- Templates = *How* to structure requests
- Skills = *What* rules to follow
- Combined = Production-grade prompts

---

## Quick Examples

### Example 1: SEO Blog Post
```python
# Request
user_request = "Write SEO-optimized blog post about brand strategy"

# Template provides base structure
prompt = manager.create_prompt(
    template_id="marketing_copy",
    custom_variables={'CHANNEL': 'Blog', ...}
)

# Skills auto-inject based on triggers
# - "SEO" → seo-content-guidelines skill
# - "blog" → persona-enforcer skill
# - "brand" → brand-voice-consistency skill

enhanced = injector.inject_skills_into_prompt(
    prompt, "blog_author", user_request
)

# Send to LLM - gets structure + 3 skill enhancements
output = llm_api(enhanced)
```

### Example 2: LinkedIn Post
```python
user_request = "Create LinkedIn post about our new product"

# Template
prompt = manager.create_prompt(
    template_id="marketing_copy",
    custom_variables={'CHANNEL': 'LinkedIn', ...}
)

# Matching skills
# - "LinkedIn" → social-platform-best-practices
# - "product" → brand-voice-consistency

enhanced = injector.inject_skills_into_prompt(
    prompt, "social_promoter", user_request
)

output = llm_api(enhanced)
```

---

## File Structure
```
your-project/
├── prompt_manager.py
├── skills_system.py
├── prompt_evaluator.py
├── prompt_templates.yaml
├── skills/
│   ├── persona-enforcer.md
│   ├── seo-content-guidelines.md
│   ├── social-platform-best-practices.md
│   └── [more skills...]
├── examples_integrated.py
└── your_app.py (your code)
```

---

## Creating Your Own Skills

### Skill File Format
Create `skills/my-skill.md`:
```yaml
---
name: my-skill
version: "1.0"
description: What this skill does
target_agents:
  - blog_author
  - social_promoter
triggers:
  - "keyword1"
  - "keyword2"
priority: 10
max_tokens: 300
---

# My Skill Title

Instructions and guidelines for the LLM...

- Point 1
- Point 2
- Point 3

Examples and patterns...
```

Then load it:
```python
registry.load_skills_from_directory()  # Auto-loads all .md files
```

---

## Integration Checklist

- [ ] Install pyyaml
- [ ] Create skills/ directory
- [ ] Copy sample skill files
- [ ] Run `examples_integrated.py`
- [ ] Customize `prompt_templates.yaml` for your content
- [ ] Update skill triggers for your keywords
- [ ] Create your first skill
- [ ] Integrate with your LLM API
- [ ] Run through evaluation framework
- [ ] Track metrics and iterate

---

## Next Steps

1. **Customize for Your Brand** (30 min)
   - Edit `prompt_templates.yaml`
   - Update brand voice in skills
   - Add your personas

2. **Create Your First Skills** (1 hour)
   - Identify pattern across prompts
   - Extract as a skill
   - Test with 2-3 requests

3. **Integrate with Your LLM** (1-2 hours)
   - Connect to Claude/OpenAI API
   - Handle streaming responses
   - Set up error handling

4. **Add Evaluation** (30 min)
   - Import PromptEvaluator
   - Score outputs
   - Track metrics over time

5. **Scale & Monitor** (ongoing)
   - Expand skill library
   - Track performance
   - A/B test variations
   - Refresh quarterly

---

## Common Questions

**Q: Should I use templates or skills?**  
A: Both! Templates for structure, skills for rules. They work together.

**Q: How many skills per prompt?**  
A: 2-3 typically. Too many dilutes focus. Token budget limits this.

**Q: What about latency?**  
A: Skill matching is instant (substring search). Token injection is minimal overhead.

**Q: Can I use just prompts without skills?**  
A: Yes! Skills are optional. Start with templates, add skills when patterns emerge.

**Q: How do I version skills?**  
A: Use `version` field in YAML. Load specific versions by name.

**Q: Can skills override each other?**  
A: No, they're additive. Design skills to complement each other.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skills not loading | Check skills/ directory exists and files have .md extension |
| Wrong skills matched | Review triggers - use specific keywords, not generic terms |
| Prompt too long | Reduce max_tokens or disable lower-priority skills |
| Inconsistent outputs | Add more specific constraints to skill instructions |
| Token budget exceeded | Reduce max_skills_per_node or skill max_tokens |

---

## For More Details

- **Methodology**: See `PROMPT_ENGINEERING_METHODOLOGY.md`
- **Integration Design**: See `ARCHITECTURE.md`
- **Full Implementation**: See `IMPLEMENTATION_GUIDE.md`
- **Code Examples**: Run `examples_integrated.py`, `examples.py`
- **API Reference**: See docstrings in Python modules

---

**You're ready! Start with example 1, then build your own. Questions? Check ARCHITECTURE.md for deeper dives.**
