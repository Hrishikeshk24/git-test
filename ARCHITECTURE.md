# Integrated Architecture: Prompt Engineering + Skills System

## System Overview

Your AI Growth Platform combines two complementary systems:

1. **Prompt Engineering System** - Static, reusable prompt templates
2. **Skills System** - Dynamic, runtime-injected contextual instructions

Together they create a powerful prompt composition engine.

```
┌─────────────────────────────────────────────────────────────────┐
│              User Request / Prompt                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │  Skill Trigger Matching       │
         │  (Registry.find_applicable)   │
         └───────────┬───────────────────┘
                     │
     ┌───────────────┴───────────────┐
     │                               │
     ▼                               ▼
┌──────────────┐          ┌─────────────────┐
│ Base Prompt  │          │ Matched Skills  │
│ Template     │          │ (by priority)   │
└──────┬───────┘          └────────┬────────┘
       │                           │
       └─────────────┬─────────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │ Skill Injector       │
         │ (merge + token budget)
         └──────────┬───────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │ Enhanced Prompt      │
         │ (with skills injected)
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
         │ Output               │
         │ (brand-compliant,    │
         │  skill-enhanced)     │
         └──────────────────────┘
```

---

## Core Components

### 1. Prompt Manager (Existing)
**Responsibility**: Static prompt lifecycle management

```python
PromptManager
├── Templates (YAML-based)
├── Version Control
├── Evaluation Tracking
└── Export/Reporting
```

**Use Cases**:
- Marketing copy templates
- Content strategy outlines
- Email sequences
- Social media frameworks

---

### 2. Skills System (New)
**Responsibility**: Dynamic contextual instruction injection

```python
SkillRegistry
├── Skill Registration
├── Agent Mapping
└── Trigger Matching

SkillInjector
├── Match Finding
├── Context Building
└── Token Management

Skill
├── Metadata
├── Target Agents
├── Triggers
└── Instructions
```

**Use Cases**:
- Brand voice enforcement
- SEO guidelines injection
- Platform-specific tactics
- Knowledge base integration
- Compliance rules

---

## Integration Architecture

### Workflow: Request → Prompt → Skills → LLM

#### Step 1: User Makes Request
```
User: "Write an SEO-optimized blog post about our brand equity"
```

#### Step 2: Select Prompt Template
```python
from prompt_manager import PromptManager

manager = PromptManager()
prompt_template = manager.create_prompt(
    template_id="marketing_copy",
    prompt_id="blog_001",
    custom_variables={
        'CHANNEL': 'Blog Post',
        'PERSONA': 'Marketing Directors',
        'CTA': 'Learn More'
    }
)
```

Output:
```
[ROLE]
You are a senior marketing copywriter...

[TASK]
Write SEO-optimized blog post...

[CONSTRAINTS]
- Professional tone
- 2000 words
- Include metrics
...

[FORMAT]
Markdown with H2 sections

[EXAMPLES]
Example of strong blog post...
```

#### Step 3: Detect Applicable Skills
```python
from skills_system import SkillRegistry, SkillInjector

registry = SkillRegistry()
registry.load_skills_from_directory()

injector = SkillInjector(registry)

# System automatically detects:
# - "SEO-optimized" → triggers "seo-content-guidelines" skill
# - "blog" → triggers "persona-enforcer" skill
# - "brand equity" → triggers "brand-voice-consistency" skill

matched_skills = registry.find_applicable_skills(
    agent_id="blog_author",
    user_prompt=user_request
)
```

#### Step 4: Inject Skills
```python
enhanced_prompt = injector.inject_skills_into_prompt(
    base_prompt=prompt_template,
    agent_id="blog_author",
    user_prompt=user_request,
    max_tokens=1500
)
```

Output:
```
[ROLE]
You are a senior marketing copywriter...

[TASK]
Write SEO-optimized blog post...

[CONSTRAINTS]
- Professional tone
- 2000 words
...

[FORMAT]
Markdown with H2 sections

### CONTEXTUAL SKILLS FOR THIS TASK

## SKILL: seo-content-guidelines
... [SEO instructions injected] ...

## SKILL: persona-enforcer
... [Brand voice instructions injected] ...

## SKILL: brand-voice-consistency
... [Additional voice guidelines] ...
```

#### Step 5: Call LLM
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=2048,
    messages=[
        {"role": "user", "content": enhanced_prompt}
    ]
)

output = response.content[0].text
```

#### Step 6: Evaluate Output
```python
from prompt_evaluator import PromptEvaluator

evaluator = PromptEvaluator()
evaluation = evaluator.evaluate_output(output)

# Checks against:
# - Template constraints
# - Skill requirements
# - Brand guidelines
# - SEO best practices
```

---

## Data Models

### Prompt Model
```python
PromptTemplate
├── id: str
├── name: str
├── role: str
├── task: str
├── constraints: str
├── format_spec: str
├── examples: List[str]
├── variables: Dict[str, str]
├── status: PromptStatus
└── versions: List[PromptVersion]
```

### Skill Model
```python
Skill
├── name: str (unique identifier)
├── version: str
├── description: str
├── target_agents: List[str]  # Which agents use this
├── triggers: List[str]        # Keywords that activate
├── priority: int              # Higher = preferred
├── max_tokens: int            # Budget for this skill
├── instructions: str          # Content to inject
└── status: SkillStatus
```

### Combined Flow
```
User Prompt
    ↓
[Agent ID] → [Template Lookup]
    ↓
[Base Prompt]
    ↓
[Skill Matching] ← [User Prompt + Triggers]
    ↓
[Skill Injection] → [Respecting Token Budget]
    ↓
[Enhanced Prompt]
    ↓
[LLM Call]
    ↓
[Output]
    ↓
[Evaluation] ← [Prompt Metrics + Skills Compliance]
```

---

## Agent Mapping

Each agent has skills that support its domain:

| Agent | Prompt Templates | Available Skills | Typical Flow |
|-------|-----------------|-----------------|--------------|
| `blog_author` | marketing_copy, content_strategy | persona-enforcer, seo-guidelines, brand-voice | Blog post request → prompt + 3 skills |
| `social_promoter` | marketing_copy, social_media_voice | social-platform-best-practices, brand-voice | Social post request → prompt + 2 skills |
| `default_agent` (RAG) | customer_success_messaging | knowledge-retrieval-tool, context-synthesizer | Q&A request → prompt + 1 skill |
| `valuation_logic` | intelligence_analysis | competitive-analysis-methodology | Analysis request → prompt + 1 skill |

---

## Configuration Hierarchy

```
Skills & Prompts

├── Organization Level
│   ├── Global Skills Registry
│   ├── Global Prompt Templates
│   └── Brand Guidelines (shared)
│
├── Agent Level
│   ├── Agent Skills (blog_author, social_promoter, etc.)
│   ├── Agent-Specific Templates
│   └── Agent Skill Overrides
│
├── Tenant Level
│   ├── Tenant Brand Profile
│   ├── Tenant Skills (optional custom)
│   └── Tenant Template Variations
│
└── Session Level
    ├── User Preferences
    ├── Dynamic Triggers
    └── Real-time Skill Selection
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- ✅ Prompt Engineering System (done)
- ✅ Skills System (done)
- Skills Registry + YAML loader
- Integration examples

### Phase 2: Integration (Week 2)
- Update PromptManager to work with SkillInjector
- Build agent-skill mappings
- Create sample skill files
- Integration tests

### Phase 3: Production (Week 3+)
- Load skills from directory at startup
- Hot-reload endpoint for skill updates
- Monitoring and metrics
- Performance optimization

---

## Code Examples

### Example 1: Basic Integration
```python
from prompt_manager import PromptManager
from skills_system import SkillRegistry, SkillInjector
from prompt_evaluator import PromptEvaluator

# Initialize systems
manager = PromptManager()
registry = SkillRegistry("./skills")
injector = SkillInjector(registry)
evaluator = PromptEvaluator()

# Load scenarios
registry.load_skills_from_directory()

# Prompt generation
prompt = manager.create_prompt(
    template_id="marketing_copy",
    prompt_id="blog_001",
    custom_variables={'CHANNEL': 'Blog', 'PERSONA': 'CMO'}
)

# Skill injection
user_request = "Write SEO-optimized blog about competitive advantage"
enhanced_prompt = injector.inject_skills_into_prompt(
    base_prompt=prompt,
    agent_id="blog_author",
    user_prompt=user_request
)

# LLM call
output = llm_api(enhanced_prompt)

# Evaluation
evaluation = evaluator.evaluate_output(output)
manager.record_evaluation("blog_001", evaluation['metrics'], output)
```

### Example 2: Dynamic Skill Selection
```python
# User makes 3 different requests to blog_author

# Request 1: "Write a blog post"
skills_1 = registry.find_applicable_skills("blog_author", "Write a blog post")
# Matches: brand-voice-consistency (priority 8)
# Expected: 1 skill injected

# Request 2: "Write an SEO-optimized blog post"
skills_2 = registry.find_applicable_skills("blog_author", 
    "Write an SEO-optimized blog post")
# Matches: persona-enforcer (15), seo-content-guidelines (10), 
#          brand-voice-consistency (8)
# Expected: 3 skills injected (max_skills_per_node = 3)

# Request 3: "Write a blog about our competitive advantage with SEO"
skills_3 = registry.find_applicable_skills("blog_author",
    "Write a blog about our competitive advantage with SEO")
# Same as above, same 3 skills by priority
```

### Example 3: Token Budget Management
```python
# Skills are injected respecting token budget

skill_matches = [
    SkillMatch(seo_skill, confidence=0.95, priority=10),      # 350 tokens
    SkillMatch(persona_skill, confidence=0.8, priority=15),   # 300 tokens
    SkillMatch(voice_skill, confidence=0.75, priority=8)      # 200 tokens
]

# With max_total_tokens = 1500:
enhanced = injector.inject_skills_into_prompt(
    prompt, "blog_author", user_request, max_tokens=1500
)
# Result: All 3 skills = 850 tokens total (within budget)

# With max_total_tokens = 400:
enhanced = injector.inject_skills_into_prompt(
    prompt, "blog_author", user_request, max_tokens=400
)
# Result: persona_skill + seo_skill (650 tokens > 400)
# Actually: Only persona_skill (300 tokens), 
#          seo breaks budget, stops injection
```

---

## File Structure

```
ai-growth-platform/
├── prompt_engineering/
│   ├── PROMPT_ENGINEERING_METHODOLOGY.md
│   ├── IMPLEMENTATION_GUIDE.md
│   ├── prompt_templates.yaml
│   ├── prompt_manager.py
│   ├── prompt_evaluator.py
│   └── examples.py
│
├── skills_system/
│   ├── ARCHITECTURE.md (this file)
│   ├── skills_system.py
│   ├── skills/
│   │   ├── persona-enforcer.md
│   │   ├── seo-content-guidelines.md
│   │   ├── social-platform-best-practices.md
│   │   ├── brand-voice-consistency.md
│   │   ├── knowledge-retrieval-tool.md
│   │   └── [more skills...]
│   ├── agents/
│   │   ├── blog_author.yaml
│   │   ├── social_promoter.yaml
│   │   └── [more agents...]
│   └── examples_with_skills.py
│
└── integration/
    ├── ai_application.py (main entry point)
    ├── config.yaml
    └── [other integration code...]
```

---

## Workflow Diagram

```
REQUEST FLOW:
┌──────────────────────┐
│ User Request         │
│ "Write SEO blog"     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Route to Agent       │
│ blog_author          │
└──────────┬───────────┘
           │
           ├─────────────────────────┐
           │                         │
           ▼                         ▼
    ┌─────────────┐         ┌────────────────┐
    │ Prompt      │         │ Skills         │
    │ Template    │         │ Registry       │
    │ Lookup      │         │ (Trigger Match)
    └──────┬──────┘         └────────┬───────┘
           │                        │
           │    [Base Template]     │ [Matched Skills]
           └────────┬───────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Skill Injector  │
           │ (merge + budget)
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Enhanced Prompt │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ LLM (Claude)    │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Output          │
           │ (SEO'd, branded,
           │  compliant)     │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Evaluator       │
           │ Score & record  │
           └─────────────────┘
```

---

## Key Integration Points

### 1. **Unified Configuration**
```yaml
# config.yaml
agents:
  blog_author:
    templates:
      - marketing_copy
      - content_strategy
    skills:
      - persona-enforcer
      - seo-content-guidelines
      - brand-voice-consistency
    max_skills_per_node: 3
    max_total_tokens: 1500
```

### 2. **Shared Evaluation Metrics**
- Prompt templates define structural requirements
- Skills define contextual requirements
- Evaluator checks both simultaneously

### 3. **Version Tracking**
- Templates have versions
- Skills have versions
- Track output quality across versions of both

### 4. **Hot-reload Capability**
```python
# POST /v1/admin/reload-skills
@app.post("/admin/reload-skills")
def reload_skills():
    registry.load_skills_from_directory()
    return {"status": "reloaded", "stats": registry.get_statistics()}
```

---

## Benefits of Integration

| Aspect | Prompt Templates | Skills | Combined |
|--------|-----------------|--------|----------|
| **Structure** | Predefined prompt format | Dynamic contextual rules | Balanced structure + flexibility |
| **Reusability** | High (templates across prompts) | High (skills across agents) | Highest (component reuse) |
| **Maintainability** | Easy (version control) | Easy (YAML-based) | Very easy (both tracked) |
| **Customization** | Via variables | Via triggers + agent config | Granular control at all levels |
| **Scalability** | Linear with templates | Linear with skills | Exponential (combinations) |
| **A/B Testing** | Compare template versions | Compare skill matching | Compare entire compositions |

---

## Monitoring & Analytics

Track metrics across both systems:

```python
analytics = {
    'prompt_metrics': {
        'templates_used': ['marketing_copy', 'content_strategy'],
        'average_quality_score': 4.2,
        'versions_tried': 3
    },
    'skill_metrics': {
        'skills_matched': 3,
        'total_skills_injected': 2,  # Due to token budget
        'top_triggered_skills': ['persona-enforcer', 'seo-guidelines'],
        'average_trigger_confidence': 0.87
    },
    'combined_metrics': {
        'time_to_production': '2 iterations',
        'satisfaction_score': 4.5,
        'skill_impact': '+0.8 quality points'
    }
}
```

---

## Conclusion

The integrated architecture provides:
- **Predictability** through prompt templates
- **Intelligence** through skill injection  
- **Flexibility** through dynamic matching
- **Scale** through component reuse

Start with prompt templates, add skills as needed, and let them work together to create superior outputs.
