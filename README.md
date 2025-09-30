# Instagram Content Creation Multi-Agent System

A sophisticated Multi-Agent System built with Crew AI that automates the end-to-end Instagram content creation pipeline. The system uses Google Gemini as the primary LLM and integrates with external image generation APIs.

## 🎯 Features

- **4 Specialized Agents**: Research, Content Writer, Reviewer, and Image Prompt Generator
- **Google Gemini Integration**: Uses Google's Gemini 1.5 Flash model for all AI operations
- **External Image Generation**: Supports Nano Banana, Segmind, and Stability AI APIs
- **Complete Instagram Package**: Generates captions, hashtags, and images
- **Automated Workflow**: Sequential agent collaboration for optimal results

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd crew

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file with your API keys:

```env
# Google Gemini API Key (Required)
GOOGLE_API_KEY=your_google_api_key_here

# Image Generation API (Choose one)
NANO_BANANA_API_KEY=your_nano_banana_api_key_here
SEGMIND_API_KEY=your_segmind_api_key_here
STABILITY_API_KEY=your_stability_api_key_here
```

### 3. Run the System

```bash
# Run the main application
python instagram_crew.py

# Or run a quick test
python test_system.py
```

## 🤖 Agent Architecture

### 1. Research Agent
- **Role**: Research Specialist
- **Goal**: Gather comprehensive information about the given topic
- **Output**: Detailed research summary with key facts and insights

### 2. Content Writer Agent
- **Role**: Instagram Content Writer
- **Goal**: Create compelling Instagram captions and hashtags
- **Output**: Short caption, long caption, and hashtag strategy

### 3. Reviewer Agent
- **Role**: Content Reviewer and Editor
- **Goal**: Polish content for grammar, tone, and engagement
- **Output**: Final polished Instagram content

### 4. Image Prompt Generator Agent
- **Role**: Visual Content Strategist
- **Goal**: Create detailed image prompts for visual content
- **Output**: 3 optimized image prompts for Instagram

## 📱 Generated Content

The system produces a complete Instagram content package:

- **Short Caption**: Under 150 characters, hook + key message + CTA
- **Long Caption**: Under 2200 characters, detailed story + insights
- **Hashtags**: Up to 30 relevant hashtags (trending + niche + branded)
- **Image Prompts**: 3 detailed prompts for visual content generation
- **Generated Images**: Actual images created using external APIs

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Image Generation Settings
IMAGE_GENERATION_API = "nano_banana"  # Options: "nano_banana", "segmind", "stability"
NUM_IMAGES = 3  # Number of images to generate

# Instagram Content Settings
MAX_CAPTION_LENGTH = 2200  # Instagram caption limit
HASHTAG_LIMIT = 30  # Maximum number of hashtags
```

## 🌐 Supported Image APIs

### Nano Banana
- High-quality image generation
- Fast processing
- Good for social media content

### Segmind
- Stable Diffusion XL models
- Base64 encoded output
- Professional quality

### Stability AI
- Industry-standard API
- Multiple model options
- High-resolution output

## 📁 Project Structure

```
crew/
├── agents.py              # Agent definitions and tasks
├── config.py              # Configuration settings
├── image_generator.py     # Image generation API integration
├── instagram_crew.py      # Main workflow and execution
├── test_system.py         # Test script
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
└── README.md             # This file
```

## 🧪 Testing

Run the test script to verify everything is working:

```bash
python test_system.py
```

This will:
- Test agent initialization
- Run a sample content creation workflow
- Verify API connections
- Display sample output

## 📊 Example Output

```
🎯 Selected topic: The Future of Electric Cars

📝 SHORT CAPTION:
🚗 The future is electric! Discover how EVs are revolutionizing transportation. What's your take? #ElectricCars #Future

📝 LONG CAPTION:
The automotive industry is undergoing a massive transformation, and electric vehicles are leading the charge! 🚗⚡

From Tesla's groundbreaking innovations to traditional automakers' electrification efforts, we're witnessing a revolution on wheels. The numbers speak for themselves:
• Global EV sales increased 40% in 2023
• Charging infrastructure is expanding rapidly
• Battery technology is improving exponentially

But it's not just about the cars - it's about creating a sustainable future for our planet. Every electric vehicle on the road is a step toward cleaner air and reduced carbon emissions.

What excites you most about the electric vehicle revolution? Share your thoughts below! 👇

#ElectricCars #EV #SustainableTransport #Tesla #FutureOfMobility #CleanEnergy #GreenTech #Innovation #Automotive #ClimateAction

🎨 IMAGE PROMPTS:
1. Futuristic electric car concept on a sleek highway at sunset, neon lights, high-tech atmosphere, Instagram square format
2. Close-up of electric car charging station with glowing blue energy, modern city background, professional photography style
3. Split-screen showing traditional gas station vs modern EV charging hub, clean minimalist design, social media ready
```

## 🔑 API Keys Setup

### Google Gemini API
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### Image Generation APIs

#### Nano Banana
1. Visit [Nano Banana](https://nanobanana.ai/)
2. Sign up and get your API key
3. Add to `.env` file

#### Segmind
1. Go to [Segmind](https://segmind.com/)
2. Create account and get API key
3. Add to `.env` file

#### Stability AI
1. Visit [Stability AI Platform](https://platform.stability.ai/)
2. Sign up and generate API key
3. Add to `.env` file

## 🚨 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure all required API keys are set in `.env` file
   - Check key validity and permissions

2. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Image Generation Fails**
   - Verify image API keys are correct
   - Check API rate limits and quotas
   - Try different image generation service

4. **Content Quality Issues**
   - Adjust agent prompts in `agents.py`
   - Modify temperature settings in `config.py`
   - Review and refine task descriptions

## 📈 Future Enhancements

- [ ] Support for video content generation
- [ ] Multi-language content creation
- [ ] Brand voice customization
- [ ] Content scheduling integration
- [ ] Performance analytics
- [ ] A/B testing capabilities

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the system!

## 📄 License

This project is for educational purposes. Please ensure you comply with the terms of service of all integrated APIs.
