import os
import re
import sys
from dotenv import load_dotenv
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = 'models/gemini-1.5-flash-latest'

def build_supervisor_prompt(user_topic, code):
    return f"""
MANIM CODE SUPERVISOR - OFFICIAL DOCUMENTATION COMPLIANT

ROLE:
You are a mathematical code supervisor and expert in Manim. You will receive a user query and a Manim Python code. Your job is to:
- Validate if the code is mathematically accurate and directly addresses the query: **{user_topic}**
- Ensure all formulas, notation, and visual representations are correct
- Check that the code structure, transitions, and phases follow best practices for Manim
- If the code is incomplete, inaccurate, or not fully about the query, IMPROVE and CORRECT it
- Output ONLY the improved, complete, executable Python code (no explanations, no markdown, no comments outside code)

CRITICAL REQUIREMENTS (MUST FOLLOW EXACTLY):
1. Use mathematical symbols for irrational numbers (π, e, φ) instead of decimal approximations
2. Format all decimal numbers to exactly 2 decimal places (3.14, 2.72, 1.62)
3. Use np.pi, np.e for mathematical constants
4. Initialize ValueTracker with float values: ValueTracker(0.0), ValueTracker(-3.0*np.pi)
5. Use .add_updater() method on Manim objects, NEVER always_redraw() on coordinate arrays
6. Create proper updater functions that modify Manim objects, not coordinate arrays

MANIM BEST PRACTICES (FROM OFFICIAL DOCUMENTATION):
- For dynamic elements: create object first, then add updater to modify it
- Use f-string formatting with .2f precision for decimal display
- Validate all coordinate calculations produce valid 3D points
- Use smooth transitions with FadeIn/FadeOut, Create, Transform
- Include multiple self.play calls and self.wait for proper timing
- Use ValueTracker animations for dynamic motion
- Ensure total duration is at least 20 seconds

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
- Check for incorrect always_redraw() usage on coordinate arrays
- Ensure all updaters use .add_updater() on Manim objects, not numpy arrays
- Verify that axes.c2p() results are not used directly with always_redraw()
- Make sure dynamic elements follow proper Manim updater patterns

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

USER QUERY: {user_topic}

CODE TO VERIFY AND IMPROVE:
{code}

FINAL OUTPUT: Only the improved, complete Python code, starting with imports and ending with the final fade out.
"""

def extract_code_from_gemini_response(response_text):
    code_pattern = r'```(?:python)?\s*(.*?)```'
    match = re.search(code_pattern, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response_text.strip()

def post_to_gemini_supervisor(user_topic, code):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in .env file.")
    prompt = build_supervisor_prompt(user_topic, code)
    configure(api_key=GEMINI_API_KEY)
    model = GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text

def save_code_to_file(code, filename="verified_manim_code.py"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Verified code saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python geminiverify.py <user_query>")
        sys.exit(1)
    user_topic = sys.argv[1]
    with open("generated_manim_code.py", "r", encoding="utf-8") as f:
        code = f.read()
    response_text = post_to_gemini_supervisor(user_topic, code)
    improved_code = extract_code_from_gemini_response(response_text)
    save_code_to_file(improved_code)
