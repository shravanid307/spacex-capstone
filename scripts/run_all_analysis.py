import os
import sys
import subprocess

def run_step(step_name, script_path):
    print(f"\n{'='*70}\n[STEP] {step_name}\n{'='*70}")
    cmd = [sys.executable, script_path]
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"FAILED: {step_name} with exit code {result.returncode}")
        return False
    print(f"SUCCESS: {step_name}")
    return True

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scripts_dir = os.path.join(base_dir, "scripts")

    steps = [
        ("Generate Jupyter Notebooks", os.path.join(scripts_dir, "create_notebooks.py")),
        ("Generate High-Resolution Visual Assets", os.path.join(scripts_dir, "generate_visuals.py")),
        ("Generate Folium Interactive Geospatial Map", os.path.join(scripts_dir, "generate_folium_map.py")),
        ("Build PowerPoint Deck & Final PDF Report", os.path.join(scripts_dir, "build_presentation.py")),
    ]

    for name, path in steps:
        if not run_step(name, path):
            print(f"\nExecution stopped due to failure in: {name}")
            sys.exit(1)

    print("\n" + "="*70)
    print("ALL PIPELINE STEPS COMPLETED SUCCESSFULLY!")
    print(f"Final PDF Report: {os.path.join(base_dir, 'Data Science Capstone Project Report.pdf')}")
    print(f"PowerPoint Deck:  {os.path.join(base_dir, 'Data Science Capstone Project Report.pptx')}")
    print("="*70)

if __name__ == '__main__':
    main()
