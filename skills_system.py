"""
Skills System - Dynamic Contextual Instruction Injection
Integrates with Prompt Engineering to inject skills based on triggers
"""

import yaml
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set
from enum import Enum
from datetime import datetime
import re


class SkillStatus(Enum):
    """Status of a skill in the system"""
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


@dataclass
class Skill:
    """Represents a single skill with metadata and instructions"""
    name: str  # Unique identifier (e.g., "persona-enforcer")
    version: str
    description: str
    target_agents: List[str]  # Which agents use this skill
    triggers: List[str]  # Keywords that activate skill (OR logic)
    priority: int  # Higher = preferred when multiple skills match
    max_tokens: int  # Token budget for this skill
    instructions: str  # The actual skill content/instructions
    status: SkillStatus = SkillStatus.ACTIVE
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def matches_trigger(self, user_prompt: str) -> bool:
        """Check if any trigger phrase appears in user prompt"""
        prompt_lower = user_prompt.lower()
        return any(trigger.lower() in prompt_lower for trigger in self.triggers)
    
    def to_context_string(self) -> str:
        """Convert skill to injectable context string for LLM prompt"""
        return f"""
## SKILL: {self.name}
**Purpose**: {self.description}
**Priority**: {self.priority}

{self.instructions}
"""
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'target_agents': self.target_agents,
            'triggers': self.triggers,
            'priority': self.priority,
            'max_tokens': self.max_tokens,
            'instructions': self.instructions,
            'status': self.status.value
        }


@dataclass
class SkillMatch:
    """Represents a matched skill that will be injected"""
    skill: Skill
    match_confidence: float  # 0-1, how well trigger matched
    injection_order: int  # Order in which to inject (by priority)


class SkillRegistry:
    """Registry for managing all skills across the organization"""
    
    def __init__(self, skills_directory: str = None):
        """
        Initialize skill registry
        
        Args:
            skills_directory: Path to directory containing skill YAML files
        """
        self.skills: Dict[str, Skill] = {}
        self.agent_skills: Dict[str, List[Skill]] = {}  # agent_id -> [skills]
        self.skills_directory = skills_directory or "./skills"
        self.max_skills_per_node = 3
        self.max_total_tokens = 1500
    
    def register_skill(self, skill: Skill) -> None:
        """Register a skill in the registry"""
        self.skills[skill.name] = skill
        
        # Index by agent
        for agent in skill.target_agents:
            if agent not in self.agent_skills:
                self.agent_skills[agent] = []
            self.agent_skills[agent].append(skill)
        
        # Sort by priority (descending)
        for agent in skill.target_agents:
            self.agent_skills[agent].sort(key=lambda s: s.priority, reverse=True)
    
    def load_skills_from_directory(self) -> int:
        """
        Load all skills from directory of YAML/Markdown files
        
        Returns:
            Number of skills loaded
        """
        if not os.path.exists(self.skills_directory):
            print(f"Skills directory not found: {self.skills_directory}")
            return 0
        
        loaded_count = 0
        for filename in os.listdir(self.skills_directory):
            if filename.endswith('.md') or filename.endswith('.yaml'):
                filepath = os.path.join(self.skills_directory, filename)
                try:
                    skill = self._load_skill_file(filepath)
                    if skill:
                        self.register_skill(skill)
                        loaded_count += 1
                except Exception as e:
                    print(f"Error loading skill from {filepath}: {e}")
        
        return loaded_count
    
    def _load_skill_file(self, filepath: str) -> Optional[Skill]:
        """Load a skill from a YAML/Markdown file with frontmatter"""
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Parse YAML frontmatter (between --- markers)
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    instructions = parts[2].strip()
                    
                    skill = Skill(
                        name=metadata.get('name'),
                        version=metadata.get('version', '1.0'),
                        description=metadata.get('description'),
                        target_agents=metadata.get('target_agents', []),
                        triggers=metadata.get('triggers', []),
                        priority=metadata.get('priority', 5),
                        max_tokens=metadata.get('max_tokens', 400),
                        instructions=instructions
                    )
                    return skill
                except Exception as e:
                    print(f"Error parsing frontmatter in {filepath}: {e}")
                    return None
        
        return None
    
    def find_applicable_skills(self, 
                              agent_id: str,
                              user_prompt: str,
                              max_skills: int = None) -> List[SkillMatch]:
        """
        Find skills that apply to a given prompt for an agent
        
        Args:
            agent_id: Target agent identifier
            user_prompt: User's prompt/request
            max_skills: Override max skills per node
            
        Returns:
            Sorted list of applicable skills
        """
        max_skills = max_skills or self.max_skills_per_node
        
        if agent_id not in self.agent_skills:
            return []
        
        matched = []
        for skill in self.agent_skills[agent_id]:
            if skill.status != SkillStatus.ACTIVE:
                continue
            
            if skill.matches_trigger(user_prompt):
                match_confidence = self._calculate_match_confidence(
                    skill, user_prompt
                )
                matched.append(SkillMatch(
                    skill=skill,
                    match_confidence=match_confidence,
                    injection_order=skill.priority
                ))
        
        # Sort by priority (descending), limit by max_skills
        matched.sort(key=lambda m: (m.skill.priority, m.match_confidence), 
                    reverse=True)
        
        return matched[:max_skills]
    
    @staticmethod
    def _calculate_match_confidence(skill: Skill, prompt: str) -> float:
        """Calculate how well a skill matches a prompt (0-1)"""
        prompt_lower = prompt.lower()
        matches = sum(1 for trigger in skill.triggers 
                     if trigger.lower() in prompt_lower)
        
        # More matches = higher confidence
        return min(matches / len(skill.triggers) if skill.triggers else 0.5, 1.0)
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Get a specific skill by name"""
        return self.skills.get(skill_name)
    
    def list_skills_for_agent(self, agent_id: str) -> List[Skill]:
        """Get all skills available to an agent"""
        return self.agent_skills.get(agent_id, [])
    
    def get_statistics(self) -> Dict:
        """Get registry statistics"""
        return {
            'total_skills': len(self.skills),
            'agents_with_skills': len(self.agent_skills),
            'skills_by_agent': {
                agent: len(skills) 
                for agent, skills in self.agent_skills.items()
            },
            'active_skills': sum(
                1 for skill in self.skills.values() 
                if skill.status == SkillStatus.ACTIVE
            )
        }


class SkillInjector:
    """Injects skills into prompts"""
    
    def __init__(self, registry: SkillRegistry):
        """
        Initialize injector with skill registry
        
        Args:
            registry: SkillRegistry instance
        """
        self.registry = registry
    
    def inject_skills_into_prompt(self,
                                 base_prompt: str,
                                 agent_id: str,
                                 user_prompt: str,
                                 max_tokens: int = None) -> str:
        """
        Inject applicable skills into a base prompt
        
        Args:
            base_prompt: Original prompt template
            agent_id: Target agent
            user_prompt: User's request (for trigger matching)
            max_tokens: Token budget for skills
            
        Returns:
            Enhanced prompt with skills injected
        """
        max_tokens = max_tokens or self.registry.max_total_tokens
        
        # Find applicable skills
        skill_matches = self.registry.find_applicable_skills(
            agent_id, 
            user_prompt
        )
        
        if not skill_matches:
            return base_prompt
        
        # Build skills context
        skills_context = self._build_skills_context(skill_matches, max_tokens)
        
        if not skills_context:
            return base_prompt
        
        # Inject into prompt
        enhanced_prompt = f"""{base_prompt}

### CONTEXTUAL SKILLS FOR THIS TASK
{skills_context}

---
"""
        
        return enhanced_prompt
    
    def _build_skills_context(self, 
                             skill_matches: List[SkillMatch],
                             max_tokens: int) -> str:
        """Build injectable skills context respecting token budget"""
        context_parts = []
        token_count = 0
        
        for match in skill_matches:
            skill_context = match.skill.to_context_string()
            skill_tokens = self._estimate_tokens(skill_context)
            
            if token_count + skill_tokens <= max_tokens:
                context_parts.append(skill_context)
                token_count += skill_tokens
            else:
                break  # Stop if we exceed token budget
        
        return "\n".join(context_parts)
    
    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Rough token estimate (4 chars ≈ 1 token)"""
        return len(text) // 4
    
    def explain_injected_skills(self, 
                               skill_matches: List[SkillMatch]) -> str:
        """Generate human-readable explanation of injected skills"""
        if not skill_matches:
            return "No skills were matched for injection."
        
        explanation = "**Injected Skills:**\n\n"
        for i, match in enumerate(skill_matches, 1):
            explanation += f"{i}. **{match.skill.name}** (Priority: {match.skill.priority}, Confidence: {match.match_confidence:.0%})\n"
            explanation += f"   - {match.skill.description}\n"
        
        return explanation


class AgentSkillConfig:
    """Configuration for a specific agent's skill setup"""
    
    def __init__(self, agent_id: str):
        """Initialize agent skill config"""
        self.agent_id = agent_id
        self.enabled_skills: Set[str] = set()
        self.disabled_skills: Set[str] = set()
        self.custom_skill_order: List[str] = []
        self.max_skills: Optional[int] = None
        self.max_tokens: Optional[int] = None
    
    def enable_skill(self, skill_name: str) -> None:
        """Enable a specific skill for this agent"""
        self.enabled_skills.add(skill_name)
        self.disabled_skills.discard(skill_name)
    
    def disable_skill(self, skill_name: str) -> None:
        """Disable a specific skill for this agent"""
        self.disabled_skills.add(skill_name)
        self.enabled_skills.discard(skill_name)
    
    def is_skill_enabled(self, skill_name: str) -> bool:
        """Check if a skill is enabled"""
        if skill_name in self.disabled_skills:
            return False
        if self.enabled_skills and skill_name not in self.enabled_skills:
            return False
        return True


def create_sample_skills() -> List[Skill]:
    """Create sample skills for demonstration"""
    
    skills = [
        Skill(
            name="persona-enforcer",
            version="1.0",
            description="Enforces tenant-specific brand tone from brand profile",
            target_agents=["blog_author", "social_promoter"],
            triggers=["brand", "voice", "tone", "style", "personality"],
            priority=15,
            max_tokens=300,
            instructions="""You MUST maintain the exact brand personality defined in the brand profile:
- Voice characteristics: Professional yet approachable
- Tone rules: Confident but humble, no jargon
- Avoid terms: innovative, revolutionary, game-changing
- Emphasize: practical value, proven results, team collaboration

Every sentence should feel authentic to this voice. If you deviate, rewrite."""
        ),
        
        Skill(
            name="seo-content-guidelines",
            version="1.0",
            description="Advanced SEO optimization with keyword placement and E-E-A-T",
            target_agents=["blog_author"],
            triggers=["seo", "search", "ranking", "keyword", "optimization"],
            priority=10,
            max_tokens=350,
            instructions="""Apply these SEO best practices:
1. **Primary Keyword**: Place in H1, first 100 words, and meta description
2. **E-E-A-T Signals**: Include expertise, experience, authority, trustworthiness
3. **Content Structure**: 
   - H1 title (primary keyword)
   - 2-3 H2 sections with variations
   - Short paragraphs (3-4 sentences max)
4. **Internal Links**: Link to 2-3 related content pieces
5. **Meta Description**: 155-160 chars, include primary keyword
6. **Read Time**: Target 5-8 minute read for blog posts"""
        ),
        
        Skill(
            name="social-platform-best-practices",
            version="1.0",
            description="Platform-specific engagement tactics and adaptation rules",
            target_agents=["social_promoter"],
            triggers=["social", "linkedin", "twitter", "instagram", "facebook", "platform"],
            priority=10,
            max_tokens=250,
            instructions="""Adapt content for each platform:

**LinkedIn**: Professional hook → Story/insight → CTA
- Start with bold claim or question
- Include data/metric if available
- Max 3 hashtags

**Twitter**: Punchy, witty, visual-forward
- First line hooks attention
- Optimal length: 125-150 chars
- Include emoji for personality

**Instagram**: Story-led, visual-focused, casual tone
- Behind-the-scenes angle preferred
- Use 6-8 relevant hashtags
- Encourage saves/shares not just likes

**Facebook**: Conversational, question-based
- Community feel
- Start with relatable problem
- Subtle CTA"""
        ),
        
        Skill(
            name="knowledge-retrieval-tool",
            version="1.0",
            description="Ray AI Search integration with tenant-to-data-store mapping",
            target_agents=["default_agent"],
            triggers=["search", "find", "look up", "document", "knowledge base", "database"],
            priority=10,
            max_tokens=200,
            instructions="""When user asks to search documents:
1. Extract key search terms from query
2. Query tenant's document store with: tenant_id + search terms
3. Filter results by relevance score (>0.7)
4. Return top 3 most relevant chunks with source attribution
5. If no results: "I couldn't find that in your documents, but here's what I know..."
6. Always cite source: [SOURCE: document_name]"""
        ),
        
        Skill(
            name="brand-voice-consistency",
            version="1.0",
            description="Maintains consistent brand voice across all content",
            target_agents=["blog_author", "social_promoter"],
            triggers=["brand", "consistent", "voice", "message", "copy"],
            priority=8,
            max_tokens=200,
            instructions="""Ensure content maintains our brand voice:
- Use conversational but professional language
- Avoid marketing jargon; be specific instead
- Focus on customer outcomes, not features
- Use "we" to show partnership mentality
- Include one specific example or metric per piece
- End with clear next step (CTA)"""
        )
    ]
    
    return skills
