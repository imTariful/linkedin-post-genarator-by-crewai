"""
Main Crew AI workflow for Instagram Content Creation
"""
from crewai import Crew, Process
from agents import (
    create_research_agent, 
    create_content_writer_agent, 
    create_reviewer_agent, 
    create_image_prompt_agent,
    create_research_task,
    create_writing_task,
    create_review_task,
    create_image_prompt_task
)
from image_generator import ImageGenerator
from config import NUM_IMAGES
import json
import os
from datetime import datetime

class InstagramContentCrew:
    """Main class for managing the Instagram content creation workflow"""
    
    def __init__(self):
        self.research_agent = create_research_agent()
        self.writer_agent = create_content_writer_agent()
        self.reviewer_agent = create_reviewer_agent()
        self.image_prompt_agent = create_image_prompt_agent()
        self.image_generator = ImageGenerator()
        
    def create_content(self, topic: str, save_images: bool = True) -> dict:
        """
        Create complete Instagram content for a given topic
        
        Args:
            topic: The topic to create content about
            save_images: Whether to save generated images to disk
            
        Returns:
            Dictionary containing all generated content
        """
        print(f"Starting Instagram content creation for topic: '{topic}'")
        
        # Create tasks
        research_task = create_research_task(topic, self.research_agent)
        writing_task = create_writing_task(self.writer_agent)
        review_task = create_review_task(self.reviewer_agent)
        image_prompt_task = create_image_prompt_task(topic, self.image_prompt_agent)
        
        # Update task contexts
        writing_task.context = [research_task]
        review_task.context = [writing_task]
        
        # Create and run the crew
        crew = Crew(
            agents=[
                self.research_agent,
                self.writer_agent, 
                self.reviewer_agent,
                self.image_prompt_agent
            ],
            tasks=[
                research_task,
                writing_task,
                review_task,
                image_prompt_task
            ],
            process=Process.sequential,
            verbose=True
        )
        
        print("Running content creation workflow...")
        result = crew.kickoff()
        
        # Extract results from each task
        research_result = str(research_task.output)
        writing_result = str(writing_task.output)
        review_result = str(review_task.output)
        image_prompts_result = str(image_prompt_task.output)
        
        print("Generating images...")
        
        # Parse image prompts from the result
        image_prompts = self._parse_image_prompts(image_prompts_result, topic)
        
        # Generate images
        generated_images = self.image_generator.generate_images(
            image_prompts, 
            num_images=1  # 1 image per prompt
        )
        
        # Save images if requested
        saved_image_paths = []
        if save_images and generated_images:
            saved_image_paths = self.image_generator.save_images(generated_images)
            print(f"Saved {len(saved_image_paths)} images to disk")
        
        # Compile final result
        final_result = {
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "research": research_result,
            "content": {
                "short_caption": self._extract_short_caption(review_result),
                "long_caption": self._extract_long_caption(review_result),
                "hashtags": self._extract_hashtags(review_result)
            },
            "image_prompts": image_prompts,
            "generated_images": generated_images,
            "saved_image_paths": saved_image_paths
        }
        
        # Save result to file
        self._save_result(final_result, topic)
        
        print("Instagram content creation completed!")
        return final_result
    
    def _parse_image_prompts(self, image_prompts_result: str, topic: str) -> list:
        """Parse image prompts from the agent output, with fallbacks using topic"""
        # This is a simple parser - in practice, you might want more sophisticated parsing
        lines = image_prompts_result.split('\n')
        prompts = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 20:  # Basic filtering
                # Remove numbering and bullet points
                clean_line = line.lstrip('0123456789.-• ').strip()
                if clean_line:
                    prompts.append(clean_line)
        
        # If we don't have enough prompts, create some fallbacks
        if len(prompts) < 3:
            prompts.extend([
                f"Professional Instagram post about {topic}, modern design, high quality",
                f"Engaging social media visual for {topic}, vibrant colors, square format",
                f"Creative illustration representing {topic}, clean background, Instagram ready"
            ])
        
        return prompts[:3]  # Return max 3 prompts
    
    def _extract_short_caption(self, content: str) -> str:
        """Extract short caption from the content"""
        # Look for patterns that indicate short caption
        lines = content.split('\n')
        for line in lines:
            if 'SHORT CAPTION' in line.upper() or 'SHORT:' in line.upper():
                # Find the next non-empty line
                idx = lines.index(line)
                for i in range(idx + 1, len(lines)):
                    if lines[i].strip():
                        return lines[i].strip()
        return "Check the full content for short caption"
    
    def _extract_long_caption(self, content: str) -> str:
        """Extract long caption from the content"""
        # Look for patterns that indicate long caption
        lines = content.split('\n')
        for line in lines:
            if 'LONG CAPTION' in line.upper() or 'LONG:' in line.upper():
                # Find the next non-empty line
                idx = lines.index(line)
                caption_lines = []
                for i in range(idx + 1, len(lines)):
                    if lines[i].strip() and not lines[i].strip().startswith('#'):
                        caption_lines.append(lines[i].strip())
                    elif lines[i].strip().startswith('#') and caption_lines:
                        break
                return '\n'.join(caption_lines)
        return content  # Return full content if we can't parse
    
    def _extract_hashtags(self, content: str) -> list:
        """Extract hashtags from the content"""
        hashtags = []
        lines = content.split('\n')
        
        for line in lines:
            if '#' in line:
                # Extract hashtags from the line
                words = line.split()
                for word in words:
                    if word.startswith('#') and len(word) > 1:
                        hashtags.append(word)
        
        return hashtags[:30]  # Limit to 30 hashtags
    
    def _save_result(self, result: dict, topic: str):
        """Save the result to a JSON file"""
        # Create results directory
        os.makedirs("results", exist_ok=True)
        
        # Create filename
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/instagram_content_{safe_topic}_{timestamp}.json"
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to: {filename}")

def main():
    """Main function to run the Instagram content creation system"""
    print("Instagram Content Creation Multi-Agent System")
    print("=" * 50)
    
    # Example topics
    example_topics = [
        "The Future of Electric Cars",
        "AI in Healthcare", 
        "Digital Nomad Lifestyle",
        "Sustainable Fashion",
        "Remote Work Productivity"
    ]
    
    print("Available example topics:")
    for i, topic in enumerate(example_topics, 1):
        print(f"{i}. {topic}")
    
    # Get user input
    try:
        choice = input("\nEnter topic number (1-5) or type your own topic: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(example_topics):
            topic = example_topics[int(choice) - 1]
        else:
            topic = choice if choice else example_topics[0]
        
        print(f"\nSelected topic: {topic}")
        
        # Create and run the crew
        crew = InstagramContentCrew()
        result = crew.create_content(topic)
        
        # Display results
        print("\n" + "="*50)
        print("FINAL INSTAGRAM CONTENT")
        print("="*50)
        
        print(f"\nSHORT CAPTION:")
        print(result['content']['short_caption'])
        
        print(f"\nLONG CAPTION:")
        print(result['content']['long_caption'])
        
        print(f"\nHASHTAGS:")
        print(' '.join(result['content']['hashtags']))
        
        print(f"\nIMAGE PROMPTS:")
        for i, prompt in enumerate(result['image_prompts'], 1):
            print(f"{i}. {prompt}")
        
        if result['saved_image_paths']:
            print(f"\nSAVED IMAGES:")
            for path in result['saved_image_paths']:
                print(f"  - {path}")
        
        print(f"\nContent creation completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check your API keys and try again")

if __name__ == "__main__":
    main()
