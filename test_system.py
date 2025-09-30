"""
Test script for the Instagram Content Creation Multi-Agent System
"""
import os
from instagram_crew import InstagramContentCrew
from config import GOOGLE_API_KEY

def test_system():
    """Test the system with a sample topic"""
    
    # Check if API key is set
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key in the .env file")
        return
    
    print("Testing Instagram Content Creation System")
    print("=" * 50)
    
    # Test topic
    test_topic = "Importance of AI in coding"
    
    try:
        # Create crew instance
        crew = InstagramContentCrew()
        
        # Run content creation
        print(f"Testing with topic: '{test_topic}'")
        result = crew.create_content(test_topic, save_images=False)  # Don't save images for test
        
        # Display results
        print("\nTest completed successfully!")
        print("\nResults Summary:")
        print(f"  - Topic: {result['topic']}")
        print(f"  - Research completed: {'Yes' if result['research'] else 'No'}")
        print(f"  - Content created: {'Yes' if result['content'] else 'No'}")
        print(f"  - Image prompts generated: {len(result['image_prompts'])}")
        print(f"  - Images generated: {len(result['generated_images'])}")
        
        print("\nSample Content:")
        print(f"Short Caption: {result['content']['short_caption'][:100]}...")
        print(f"Hashtags: {len(result['content']['hashtags'])} hashtags generated")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your Google API key is correct")
        print("2. Ensure you have internet connection")
        print("3. Verify all dependencies are installed")

if __name__ == "__main__":
    test_system()
