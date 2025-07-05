import os
import re
import sys
from dotenv import load_dotenv
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel
import requests
from bs4 import BeautifulSoup, Tag
from queryfetch import get_user_query

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = 'models/gemini-1.5-flash-latest'

def web_search_snippets(query, num_results=3):
    search_url = f"https://duckduckgo.com/html/?q=manim+python+{query.replace(' ', '+')}"
    resp = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for a in soup.find_all('a', class_='result__a', limit=num_results):
        if not isinstance(a, Tag):
            continue
        url = a.get('href')
        if not isinstance(url, str):
            continue
        try:
            page = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            page_soup = BeautifulSoup(page.text, "html.parser")
            code_blocks = page_soup.find_all('code')
            if code_blocks:
                for code in code_blocks:
                    snippet = code.get_text().strip()
                    if "manim" in snippet or "Scene" in snippet:
                        results.append(snippet)
                        if len(results) >= num_results:
                            break
            else:
                p = page_soup.find('p')
                if p:
                    results.append(p.get_text().strip())
        except Exception:
            continue
        if len(results) >= num_results:
            break
    return results

def build_gemini_prompt(user_topic):
    return f"""
MANIM ANIMATION GENERATOR - OFFICIAL DOCUMENTATION COMPLIANT

CRITICAL REQUIREMENTS (MUST FOLLOW EXACTLY):
1. ONLY Python code output - no markdown, no comments, no explanations
2. Use mathematical symbols for irrational numbers (π, e, φ) instead of decimal approximations
3. Format all decimal numbers to exactly 2 decimal places (3.14, 2.72, 1.62)
4. Animation must be at least 20 seconds long with proper run_time parameters
5. NO textual labels, axis numbers, or annotations unless mathematically critical

MANIM BEST PRACTICES (FROM OFFICIAL DOCUMENTATION):
- Use np.pi, np.e for mathematical constants
- Initialize ValueTracker with float values: ValueTracker(0.0), ValueTracker(-3.0*np.pi)
- Use .add_updater() method on Manim objects, NEVER always_redraw() on coordinate arrays
- Create proper updater functions that modify Manim objects, not coordinate arrays
- For dynamic elements: create object first, then add updater to modify it

CORRECT UPDATER PATTERNS (FROM MANIM DOCS):
# For dots:
dot = Dot(color=RED)
def update_dot(mob):
    x = tracker.get_value()
    y = function(x)
    mob.move_to(axes.c2p(x, y))
dot.add_updater(update_dot)

# For lines (vertical):
v_line = Line(color=BLUE)
def update_v_line(mob):
    x = tracker.get_value()
    y = function(x)
    mob.put_start_and_end_on(axes.c2p(x, 0), axes.c2p(x, y))
v_line.add_updater(update_v_line)

# For lines (horizontal):
h_line = Line(color=BLUE)
def update_h_line(mob):
    x = tracker.get_value()
    y = function(x)
    mob.put_start_and_end_on(axes.c2p(0, y), axes.c2p(x, y))
h_line.add_updater(update_h_line)

# For text:
text = MathTex()
def update_text(mob):
    x = tracker.get_value()
    y = function(x)
    mob.become(MathTex(f"x = {{x:.2f}}").next_to(axes.c2p(x, 0), DOWN))
text.add_updater(update_text)

CRITICAL ERROR PREVENTION:
- NEVER create lines from a point to itself (causes zero-dimensional vector error)
- For vertical lines: connect from (x, 0) to (x, y) - NOT from (x, y) to (x, y)
- For horizontal lines: connect from (0, y) to (x, y) - NOT from (x, y) to (x, y)
- Always ensure line endpoints are different points
- Initialize ValueTracker with proper float values
- Use f-string formatting with .2f precision for decimal display
- Validate all coordinate calculations produce valid 3D points

TECHNICAL SETUP (REQUIRED):
from manim import *
import numpy as np

config.frame_rate = 30
config.pixel_height = 1080
config.pixel_width = 1920
config.background_color = "#000000"

AXIS RANGE GUIDELINES:
- ALWAYS use y_range=[-3.5, 3.5] for all coordinate systems
- Use generous x_range that provides visual breathing room
- For trigonometric functions: x_range should be [-3*np.pi, 3*np.pi] or wider
- For polynomial functions: calculate x_range based on function behavior with buffer
- Always add significant buffer space around the function's actual range
- Avoid cramped ranges that make the function appear to "hit the edges"

SCENE TEMPLATE:
class MathematicalAnimation(Scene):
    def construct(self):
        # Setup axes and function
        axes = Axes(
            x_range=[-3*np.pi, 3*np.pi, np.pi/2],
            y_range=[-3.5, 3.5, 0.5],
            axis_config={{"include_tip": True, "color": BLUE}}
        )
        func_graph = axes.plot(lambda x: np.cos(x), color=YELLOW)
        
        # Create tracker and dynamic elements
        tracker = ValueTracker(-3.0*np.pi)
        
        # Add dynamic elements with proper updaters
        # ... (implement according to patterns above)
        
        # Animation sequence
        self.play(Create(axes), Create(func_graph))
        self.play(tracker.animate.set_value(3.0*np.pi), run_time=10)
        self.wait(2)

ANIMATION REQUIREMENTS:
- Use smooth transitions with FadeIn/FadeOut, Create, Transform
- Include multiple self.play calls and self.wait for proper timing
- Use ValueTracker animations for dynamic motion
- Ensure total duration is at least 20 seconds
- Use always_redraw only for complex VGroup updates, not simple objects

COLOR SCHEME:
- YELLOW: Primary function
- RED: Moving or tracked points  
- BLUE: Axes and projections
- GREEN: Helper curves or geometry
- WHITE: Background elements if needed

RESTRICTIONS:
- NO MathTex unless for critical dynamic math
- NO axis labels or coordinate labels
- NO text titles or static descriptions
- NO tutorial-style narration
- Avoid clutter: animations should be minimalist and geometric

TOPIC: {user_topic}
OUTPUT: Only clean Python code, executable in Manim, following all above constraints.
"""

def build_rag_prompt(user_topic):
    # Step 1: Retrieve web snippets
    snippets = web_search_snippets(user_topic)
    # Step 2: Build the prompt
    prompt = ""
    if snippets:
        prompt += "# Reference Snippets from the Web\n"
        for i, snip in enumerate(snippets, 1):
            prompt += f"Snippet {i}:\n{snip}\n\n"
    # Step 3: Add your strict Gemini prompt
    prompt += build_gemini_prompt(user_topic)
    return prompt

def extract_code_from_gemini_response(response_text):
    # Remove markdown code blocks if present
    code = re.sub(r"```(?:python)?\\s*", "", response_text)
    code = re.sub(r"```", "", code)
    # Remove comments
    code = re.sub(r"^\s*#.*$", "", code, flags=re.MULTILINE)
    return code.strip()

def post_to_gemini(user_topic):
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set in .env file.")
        sys.exit(1)
    prompt = build_rag_prompt(user_topic)
    configure(api_key=GEMINI_API_KEY)
    model = GenerativeModel(MODEL_NAME)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error: Failed to contact Gemini API: {e}")
        sys.exit(1)

def save_code_to_file(code, filename="generated_manim_code.py"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Code saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_topic = sys.argv[1]
    else:
        user_topic = get_user_query()
    response = post_to_gemini(user_topic)
    code = extract_code_from_gemini_response(response)
    save_code_to_file(code)  
