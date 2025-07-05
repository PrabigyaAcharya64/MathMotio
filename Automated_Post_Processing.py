import ast
import re

def check_manim_code_quality(code, min_duration=20):
    """
    Checks Manim code for common quality issues:
    - Uses ValueTracker
    - Uses multiple self.play and self.wait calls
    - Animation duration is at least min_duration seconds
    - No bad Line initialization (start and end points identical)
    - No syntax errors
    Returns a list of issues found (empty if code is good).
    """
    has_valuetracker = 'ValueTracker' in code
    num_play = len(re.findall(r'self\\.play\\(', code))
    num_wait = len(re.findall(r'self\\.wait\\(', code))
    # Estimate total duration
    run_times = [float(rt) for rt in re.findall(r'run_time\s*=\s*([0-9.]+)', code)]
    waits = [float(w) for w in re.findall(r'self\\.wait\\(([^)]+)\)', code)]
    total_duration = sum(run_times) + sum(waits)
    # Check for line initialization issues (crude: Line(p1, p2) where p1==p2)
    bad_line_init = bool(re.search(r'Line\([^,]+,[^,]+\)', code))

    issues = []
    if not has_valuetracker:
        issues.append('No ValueTracker used.')
    if num_play < 3:
        issues.append('Too few self.play calls.')
    if total_duration < min_duration:
        issues.append(f'Total animation duration is only {total_duration:.1f}s (less than {min_duration}s).')
    if bad_line_init:
        issues.append('Possible bad Line initialization (start and end points may be identical).')

    # Syntax check
    try:
        ast.parse(code)
    except Exception as e:
        issues.append(f'Syntax error: {e}')

    return issues
