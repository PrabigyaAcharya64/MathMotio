import subprocess
import sys
import os
import re

def extract_class_name(code):
    match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
    if match:
        return match.group(1)
    return ""

def render_manim(filename, class_name=None):
    if not class_name:
        
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        class_name = extract_class_name(code)
        if not class_name:
            print("Could not find a Scene class in the code.")
            return
    cmd = f"manim {filename} {class_name} -pql"
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("Manim rendering failed. Please check the code and try again.")
    else:
        print("Rendering complete. Check the media/videos/ directory for the output video.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render.py <python_file> [SceneClassName]")
        sys.exit(1)
    filename = sys.argv[1]
    class_name = sys.argv[2] if len(sys.argv) > 2 else None
    render_manim(filename, class_name)
