import subprocess
import sys
from queryfetch import get_user_query
from Automated_Post_Processing import check_manim_code_quality

if __name__ == "__main__":
    print("Welcome to MathMotio! Let's create your Manim animation video.")
   
    user_query = get_user_query()

    
    print("\nGenerating Manim code with Gemini...")
    result = subprocess.run([sys.executable, "geminipostfetch.py", user_query], check=True)
    if result.returncode != 0:
        print("Error: Code generation failed.")
        sys.exit(1)

    # Automated post-processing check for generated code
    try:
        with open("generated_manim_code.py", "r", encoding="utf-8") as f:
            code = f.read()
        issues = check_manim_code_quality(code)
        if issues:
            print("\n[Code Quality Warning] Issues found in generated_manim_code.py:")
            for issue in issues:
                print("-", issue)
            resp = input("Continue anyway? (y/n): ").strip().lower()
            if resp != 'y':
                print("Aborting due to code quality issues.")
                sys.exit(1)
    except Exception as e:
        print(f"[Warning] Could not check generated_manim_code.py: {e}")

    
    print("\nValidating and improving code with Gemini supervisor...")
    result = subprocess.run([sys.executable, "geminiverify.py", user_query], check=True)
    if result.returncode != 0:
        print("Error: Code validation failed.")
        sys.exit(1)

    # Automated post-processing check for verified code
    try:
        with open("verified_manim_code.py", "r", encoding="utf-8") as f:
            code = f.read()
        issues = check_manim_code_quality(code)
        if issues:
            print("\n[Code Quality Warning] Issues found in verified_manim_code.py:")
            for issue in issues:
                print("-", issue)
            resp = input("Continue anyway? (y/n): ").strip().lower()
            if resp != 'y':
                print("Aborting due to code quality issues.")
                sys.exit(1)
    except Exception as e:
        print(f"[Warning] Could not check verified_manim_code.py: {e}")

    
    print("\nRendering animation with Manim...")
    result = subprocess.run([sys.executable, "render.py", "verified_manim_code.py"], check=True)
    if result.returncode != 0:
        print("Error: Rendering failed.")
        sys.exit(1)

    print("\n Done! Check the media/videos/ directory for your animation video.")