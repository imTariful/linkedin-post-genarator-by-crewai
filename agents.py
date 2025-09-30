"""
Crew AI Agents for Instagram Content Creation
"""
from crewai import Agent, Task
from crewai.llm import LLM
from config import GOOGLE_API_KEY, MAX_CAPTION_LENGTH, HASHTAG_LIMIT

# Initialize Google Gemini LLM using CrewAI's LLM class
llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=GOOGLE_API_KEY,
    temperature=0.7
)

def create_research_agent():
    """Create the Research Agent"""
    return Agent(
        role="Research Specialist",
        goal="Gather comprehensive, accurate, and up-to-date information about the given topic",
        backstory="""You are an expert researcher with a keen eye for detail and a passion for finding 
        the most relevant and engaging information. You excel at identifying key trends, statistics, 
        and insights that would resonate with Instagram audiences. You always verify your sources 
        and provide well-structured, factual content.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_content_writer_agent():
    """Create the Content Writer Agent"""
    return Agent(
        role="Instagram Content Writer",
        goal="Create compelling, engaging Instagram captions that drive engagement and resonate with the target audience",
        backstory="""You are a creative content writer specializing in Instagram marketing. You understand 
        the nuances of social media engagement, know how to craft captions that stop the scroll, and 
        create content that encourages likes, comments, and shares. You're skilled at writing both 
        short punchy captions and longer, more detailed posts that tell a story.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_reviewer_agent():
    """Create the Reviewer Agent"""
    return Agent(
        role="Content Reviewer and Editor",
        goal="Review, edit, and polish content to ensure it meets high standards for grammar, clarity, tone, and engagement",
        backstory="""You are a meticulous editor with years of experience in content marketing and social media. 
        You have an eagle eye for grammar, tone, and engagement optimization. You ensure every piece of content 
        is polished, professional, and perfectly tailored for its intended audience. You're also skilled at 
        maintaining brand voice and ensuring content aligns with marketing objectives.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_image_prompt_agent():
    """Create the Image Prompt Generator Agent"""
    return Agent(
        role="Visual Content Strategist",
        goal="Create detailed, compelling image prompts that will generate visually stunning and relevant images for Instagram",
        backstory="""You are a visual content strategist with deep understanding of visual storytelling and 
        Instagram aesthetics. You know how to craft detailed prompts that will generate images that are 
        not only beautiful but also perfectly aligned with the content and brand message. You understand 
        composition, lighting, mood, and style that works well on social media platforms.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_research_task(topic: str, research_agent: Agent):
    """Create the research task"""
    return Task(
        description=f"""
        Research the topic: "{topic}"
        
        Your research should include:
        1. Key facts and statistics about the topic
        2. Current trends and developments
        3. Interesting insights or perspectives
        4. Relevant examples or case studies
        5. Data points that would be engaging for Instagram audiences
        
        Focus on information that would be:
        - Visually interesting
        - Shareable and engaging
        - Relevant to current conversations
        - Easy to understand in social media format
        
        Provide a comprehensive research summary with clear sections and bullet points.
        """,
        agent=research_agent,
        expected_output="A detailed research summary with key facts, trends, and insights about the topic, formatted for easy consumption by content creators."
    )

def create_writing_task(writer_agent: Agent):
    """Create the content writing task"""
    return Task(
        description="""
        Using the research provided, create Instagram content including:
        
        1. SHORT CAPTION (under 150 characters):
           - Hook that grabs attention
           - Key message or insight
           - Call-to-action
        
        2. LONG CAPTION (under 2200 characters):
           - Engaging opening line
           - Story or detailed explanation
           - Key points from research
           - Call-to-action
           - Relevant hashtags (up to 30)
        
        3. HASHTAG STRATEGY:
           - 5-10 trending hashtags
           - 5-10 niche-specific hashtags
           - 5-10 branded or general hashtags
        
        Make sure the content is:
        - Engaging and shareable
        - Easy to read and understand
        - Optimized for Instagram's algorithm
        - Includes clear calls-to-action
        - Uses emojis appropriately
        """,
        agent=writer_agent,
        expected_output="Complete Instagram content package with short caption, long caption, and hashtag strategy."
    )

def create_review_task(reviewer_agent: Agent):
    """Create the content review task"""
    return Task(
        description="""
        Review and edit the Instagram content provided. Focus on:
        
        1. GRAMMAR AND CLARITY:
           - Fix any grammatical errors
           - Improve sentence structure
           - Ensure clarity and flow
        
        2. TONE AND VOICE:
           - Ensure consistent, engaging tone
           - Check for brand voice alignment
           - Optimize for Instagram audience
        
        3. ENGAGEMENT OPTIMIZATION:
           - Strengthen hooks and openings
           - Improve calls-to-action
           - Optimize hashtag selection
           - Ensure content is shareable
        
        4. LENGTH AND FORMAT:
           - Verify caption lengths are appropriate
           - Check hashtag count (max 30)
           - Ensure proper formatting
        
        Provide the final polished content with any improvements made.
        """,
        agent=reviewer_agent,
        expected_output="Final polished Instagram content with all improvements applied."
    )

def create_image_prompt_task(topic: str, image_prompt_agent: Agent):
    """Create the image prompt generation task"""
    return Task(
        description=f"""
        Create 3 detailed image prompts for the topic: "{topic}"
        
        Each prompt should be:
        1. VISUALLY COMPELLING: Create images that would stop users from scrolling
        2. INSTAGRAM-OPTIMIZED: Square format, high contrast, engaging composition
        3. TOPIC-RELEVANT: Directly related to the content and message
        4. DETAILED: Include specific visual elements, lighting, mood, style
        5. DIVERSE: Each prompt should offer a different visual perspective
        
        Consider these elements for each prompt:
        - Main subject and composition
        - Lighting and mood
        - Color palette
        - Style (photography, illustration, etc.)
        - Background and setting
        - Text overlay possibilities
        - Instagram aesthetic appeal
        
        Format each prompt as a detailed description that could be used with any text-to-image AI.
        """,
        agent=image_prompt_agent,
        expected_output="Three detailed image prompts optimized for Instagram content, each offering a unique visual perspective on the topic."
    )
