import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
from typing import List, Dict

class GenericSceneParser:
    def __init__(self):
        # Generic patterns that work for any educational content
        self.patterns = {
            'scene_marker': r'(.*?)\s*\((\d+)\s*seconds\):',
            'text': r'Text:\s*[\'"]([^\'"]+)[\'"]',
            'animation': r'Animation:\s*([^\.]+)',
            'duration': r'Duration:\s*([^\.]+)',
            'transition': r'Transition:\s*([^\.]+)'
        }

    def parse_script(self, script: str) -> List[Dict]:
        """Parse any educational script into structured scene data"""
        # Split into scenes based on time markers
        scene_splits = re.split(self.patterns['scene_marker'], script)
        scenes = []
        
        # Process each scene
        for i in range(1, len(scene_splits), 3):
            if i + 1 >= len(scene_splits):
                break
                
            scene_name = scene_splits[i].strip()
            duration = int(scene_splits[i + 1])
            content = scene_splits[i + 2].strip()
            
            # Parse scene content
            scene = {
                'name': scene_name,
                'duration': duration,
                'content': self._parse_content(content),
                'raw_text': content
            }
            scenes.append(scene)
            
        return scenes

    def _parse_content(self, content: str) -> Dict:
        """Parse the content of a scene into structured data"""
        parts = [p.strip() for p in content.split('.') if p.strip()]
        
        scene_content = {
            'texts': [],
            'animations': [],
            'transitions': [],
            'timings': []
        }
        
        for part in parts:
            # Extract text elements
            text_match = re.search(self.patterns['text'], part)
            if text_match:
                scene_content['texts'].append(text_match.group(1))
            
            # Extract animations
            anim_match = re.search(self.patterns['animation'], part)
            if anim_match:
                scene_content['animations'].append(anim_match.group(1))
            
            # Extract timing
            duration_match = re.search(self.patterns['duration'], part)
            if duration_match:
                scene_content['timings'].append(duration_match.group(1))
            
            # Extract transitions
            transition_match = re.search(self.patterns['transition'], part)
            if transition_match:
                scene_content['transitions'].append(transition_match.group(1))
        
        return scene_content

class EducationalVideoGenerator:
    def __init__(self, api_key: str, base_url: str):
        self.client_llm = OpenAI(api_key=api_key, base_url=base_url)
        self.parser = GenericSceneParser()

    def generate_scene_prompt(self, scene: Dict) -> str:
        """Generate a prompt for any educational scene"""
        return f"""
Generate a complete Manim scene class that implements the following educational scene.
Scene Name: {scene['name']}
Duration: {scene['duration']} seconds

Required Elements:
1. All text elements must be properly positioned and spaced
2. Animations must follow the specified sequence
3. Timing must match the requirements
4. Elements must not overlap
5. Transitions must be smooth

Scene Details:
{scene['raw_text']}

Scene Requirements:
- Create a self-contained Scene class that handles all specified animations
- Use appropriate Manim animations for the described effects
- Ensure proper positioning of all elements using coordinate system or relative positioning
- Handle all specified transitions
- Follow exact timing requirements
- Maintain proper spacing between elements
- Clear any elements that should not persist between animations

Generate only the complete Manim code for this scene, with no explanations or comments.
"""

    def generate_code(self, script: str) -> str:
        # Parse script into structured scenes
        scenes = self.parser.parse_script(script)
        
        # Generate code for each scene
        all_scenes_code = []
        for i, scene in enumerate(scenes):
            prompt = self.generate_scene_prompt(scene)
            
            response = self.client_llm.chat.completions.create(
                model="deepseek-coder",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a Manim expert. Generate a complete, runnable Scene class for the specified educational animation. Focus on proper positioning and timing. Output only the code, no explanations."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048,
                temperature=0.7,
                stream=False
            )
            
            scene_code = response.choices[0].message.content.strip()
            # Clean up the code if it contains markdown markers
            scene_code = re.sub(r'^```python\s*', '', scene_code)
            scene_code = re.sub(r'\s*```$', '', scene_code)
            
            # Ensure unique scene names
            scene_code = re.sub(
                r'class\s+Scene\s*\(Scene\)',
                f'class Scene{i}(Scene)',
                scene_code
            )
            
            all_scenes_code.append(scene_code)
        
        # Combine all scenes
        final_code = """from manim import *

{scenes}

if __name__ == "__main__":
    scenes_to_render = [{scene_list}]
    for scene in scenes_to_render:
        scene().render()
""".format(
            scenes="\n\n".join(all_scenes_code),
            scene_list=", ".join([f"Scene{i}" for i in range(len(scenes))])
        )
        
        return final_code

# Usage
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('API_KEY')
    
    generator = EducationalVideoGenerator(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    
    script = "Introduction Scene (5 seconds): Text: 'Welcome to Binary Search' (large font, center screen). Animation: Text appears with a Write effect. Subtitle: 'A powerful algorithm for searching sorted arrays' (smaller font, below main text). Animation: Subtitle fades in below the title. Duration: 2 seconds for the animations, 3 seconds of pause. Transition: Both texts fade out simultaneously. What is Binary Search? (10 seconds): Title: 'What is Binary Search?' (large font, center screen). Animation: Title appears with a Write effect, stays on screen for 2 seconds, then fades out. Example Array: '[3, 7, 10, 15, 19, 23, 27]' (displayed horizontally on the screen). Animation: Array values are written out one by one in sequence. Duration: 2 seconds. First Pass: Highlight the entire array. Show 'low' pointer at index 0 with a downward arrow, 'high' pointer at index 6 with a downward arrow, and calculate 'mid' at index 3. Animation: Highlight the value at index 3 (15) in a different color. Display the text: 'Value at mid = 15'. Animation: Fade out the left half ([3, 7, 10]) to indicate it is eliminated. Move the 'low' pointer to index 4. Duration: 3 seconds. Second Pass: Highlight the new array ([19, 23, 27]). Show 'low' pointer at index 4 and 'high' pointer at index 6. Calculate 'mid' at index 5. Animation: Highlight the value at index 5 (23) in a different color. Display the text: 'Value at mid = 23'. Animation: Fade out the right half ([23, 27]) to indicate it is eliminated. Move the 'high' pointer to index 4. Duration: 3 seconds. Third Pass: Highlight the final value ([19]). Show both 'low' and 'high' pointers at index 4. Calculate 'mid' at index 4. Animation: Highlight the value at index 4 (19) in a different color. Display the text: 'Value at mid = 19. Target found!'. Duration: 2 seconds. Code Walkthrough (15 seconds): Title: 'Python Code Implementation' (large font, center screen). Animation: Title appears with a Write effect, stays on screen for 2 seconds, then fades out. Code: Display Python code for binary search line by line, as if being typed out. Animation: Highlight key sections (e.g., while loop, if conditions, and return statements) as they are explained. Duration: 10 seconds for the code walkthrough, including pauses for highlights. Fade out code at the end. Time and Space Complexity (15 seconds): Title: 'Complexity Analysis' (large font, center screen). Animation: Title appears with a Write effect, stays on screen for 2 seconds, then fades out. Display: 'Time Complexity: O(log n)' and 'Space Complexity: O(1)' (stacked vertically, center screen). Animation: Each line appears with a FadeIn effect. Duration: 3 seconds for the animation, 12 seconds of pause for explanation. Fade out both lines at the end. Conclusion Scene (10 seconds): Text: 'Binary Search is simple yet elegant.' (large font, center screen). Animation: Text appears with a Write effect. Subtitle: 'Use it to save time and resources!' (smaller font, below main text). Animation: Subtitle fades in below the title. Duration: 3 seconds for the animations, 7 seconds of pause. Transition: Both texts fade out simultaneously."

    manim_code = generator.generate_code(script)
    print(manim_code)