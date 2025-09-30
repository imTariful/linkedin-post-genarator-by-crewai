"""
Image generation module using external APIs
"""
import requests
import base64
import json
from typing import List, Dict
import random
from config import NANO_BANANA_API_KEY, SEGMIND_API_KEY, STABILITY_API_KEY, IMAGE_GENERATION_API

class ImageGenerator:
    """Handles image generation using various external APIs"""
    
    def __init__(self, api_type: str = IMAGE_GENERATION_API):
        self.api_type = api_type
        self.api_key = self._get_api_key()
    
    def _get_api_key(self) -> str:
        """Get the appropriate API key based on the selected service"""
        if self.api_type == "nano_banana":
            return NANO_BANANA_API_KEY
        elif self.api_type == "segmind":
            return SEGMIND_API_KEY
        elif self.api_type == "stability":
            return STABILITY_API_KEY
        elif self.api_type == "pollinations":
            # Pollinations is a free, keyless image generation service
            return ""
        else:
            raise ValueError(f"Unsupported API type: {self.api_type}")
    
    def generate_images(self, prompts: List[str], num_images: int = 3) -> List[Dict]:
        """
        Generate images from text prompts
        
        Args:
            prompts: List of text prompts for image generation
            num_images: Number of images to generate per prompt
            
        Returns:
            List of dictionaries containing image data and metadata
        """
        if self.api_type == "nano_banana":
            return self._generate_nano_banana(prompts, num_images)
        elif self.api_type == "segmind":
            return self._generate_segmind(prompts, num_images)
        elif self.api_type == "stability":
            return self._generate_stability(prompts, num_images)
        elif self.api_type == "pollinations":
            return self._generate_pollinations(prompts, num_images)
        else:
            raise ValueError(f"Unsupported API type: {self.api_type}")

    def _generate_pollinations(self, prompts: List[str], num_images: int) -> List[Dict]:
        """Generate images using Pollinations (free, keyless) by returning image URLs.

        Docs: https://pollinations.ai/ – images are served directly via URL.
        """
        from urllib.parse import quote

        images: List[Dict] = []
        base_url = "https://image.pollinations.ai/prompt/"

        for prompt in prompts:
            # Generate multiple image URLs with different seeds for variety
            for _ in range(max(1, num_images)):
                seed = random.randint(1, 10_000_000)
                query_suffix = f"?width=1024&height=1024&enhance=true&seed={seed}"
                url = f"{base_url}{quote(prompt)}{query_suffix}"
                images.append({
                    "prompt": prompt,
                    "url": url,
                    "api": "pollinations"
                })

        return images
    
    def _generate_nano_banana(self, prompts: List[str], num_images: int) -> List[Dict]:
        """Generate images using Nano Banana API"""
        images = []
        
        for prompt in prompts:
            try:
                url = "https://api.nanobanana.ai/v1/images/generations"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "nano-banana-v1",
                    "prompt": prompt,
                    "n": num_images,
                    "size": "1024x1024",
                    "quality": "hd"
                }
                
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                
                data = response.json()
                for img_data in data.get("data", []):
                    images.append({
                        "prompt": prompt,
                        "url": img_data.get("url"),
                        "api": "nano_banana"
                    })
                    
            except Exception as e:
                print(f"Error generating image with Nano Banana: {e}")
                # Fallback to a placeholder
                images.append({
                    "prompt": prompt,
                    "url": None,
                    "error": str(e),
                    "api": "nano_banana"
                })
        
        return images
    
    def _generate_segmind(self, prompts: List[str], num_images: int) -> List[Dict]:
        """Generate images using Segmind API"""
        images = []
        
        for prompt in prompts:
            try:
                url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
                headers = {
                    "x-api-key": self.api_key,
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "prompt": prompt,
                    "num_inference_steps": 20,
                    "guidance_scale": 7.5,
                    "width": 1024,
                    "height": 1024,
                    "num_images": num_images
                }
                
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                
                # Segmind returns base64 encoded images
                data = response.json()
                for i, img_b64 in enumerate(data.get("images", [])):
                    images.append({
                        "prompt": prompt,
                        "base64": img_b64,
                        "api": "segmind"
                    })
                    
            except Exception as e:
                print(f"Error generating image with Segmind: {e}")
                images.append({
                    "prompt": prompt,
                    "url": None,
                    "error": str(e),
                    "api": "segmind"
                })
        
        return images
    
    def _generate_stability(self, prompts: List[str], num_images: int) -> List[Dict]:
        """Generate images using Stability AI API"""
        images = []
        
        for prompt in prompts:
            try:
                url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "text_prompts": [{"text": prompt}],
                    "cfg_scale": 7,
                    "height": 1024,
                    "width": 1024,
                    "samples": num_images,
                    "steps": 30
                }
                
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                
                data = response.json()
                for img_data in data.get("artifacts", []):
                    images.append({
                        "prompt": prompt,
                        "base64": img_data.get("base64"),
                        "api": "stability"
                    })
                    
            except Exception as e:
                print(f"Error generating image with Stability AI: {e}")
                images.append({
                    "prompt": prompt,
                    "url": None,
                    "error": str(e),
                    "api": "stability"
                })
        
        return images
    
    def save_images(self, images: List[Dict], output_dir: str = "generated_images") -> List[str]:
        """
        Save generated images to local files
        
        Args:
            images: List of image data dictionaries
            output_dir: Directory to save images
            
        Returns:
            List of saved file paths
        """
        import os
        from PIL import Image
        import io
        
        os.makedirs(output_dir, exist_ok=True)
        saved_paths = []
        
        for i, img_data in enumerate(images):
            try:
                if img_data.get("base64"):
                    # Decode base64 image
                    img_bytes = base64.b64decode(img_data["base64"])
                    img = Image.open(io.BytesIO(img_bytes))
                    
                    filename = f"image_{i+1}_{img_data['api']}.png"
                    filepath = os.path.join(output_dir, filename)
                    img.save(filepath)
                    saved_paths.append(filepath)
                    
                elif img_data.get("url"):
                    # Download image from URL
                    response = requests.get(img_data["url"])
                    response.raise_for_status()
                    
                    img = Image.open(io.BytesIO(response.content))
                    filename = f"image_{i+1}_{img_data['api']}.png"
                    filepath = os.path.join(output_dir, filename)
                    img.save(filepath)
                    saved_paths.append(filepath)
                    
            except Exception as e:
                print(f"Error saving image {i+1}: {e}")
                continue
        
        return saved_paths
