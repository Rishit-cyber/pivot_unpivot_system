# controller_agent.py

import os
from agent3_executor import run_agent3_and_save_output
import google.generativeai as genai
import sys


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY environment variable not set.")
    exit(1)

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Input and output paths
input_path = "extended_activity_log.xlsx"
output_path = "output.xlsx"

# --- Agent 1: Format Detection ---
with open("agent1_detection_prompt.txt") as f:
    agent1_prompt = f.read()

response1 = model.generate_content(agent1_prompt + f"\n\nExcel path: {input_path}\n")
format_classification = response1.text.strip()
print("Detected format:", format_classification)

# --- Agent 2: Code Generation ---
with open("agent2_codegen_prompt.txt") as f:
    agent2_prompt = f.read()

# Append dynamic input
generation_prompt = agent2_prompt + f"\n\npath = \"{input_path}\"\nformat_classification = \"{format_classification}\""

response2 = model.generate_content(generation_prompt)
raw_code = response2.text.strip()
import re

# Strip markdown fences
raw_code = re.sub(r"^```(?:python)?\s*", "", raw_code)
raw_code = re.sub(r"\s*```$", "", raw_code)

# Replace path if it already exists (backup)
raw_code = re.sub(r'path\s*=\s*["\'].*?["\']', f'path = "{input_path}"  # forced override', raw_code)

# Inject path and classification at the top (guaranteed)
raw_code = f'path = "{input_path}"\nformat_classification = "{format_classification}"\n\n' + raw_code
print("\n--- Raw Generated Code from Agent 2 ---\n")
print(raw_code)

# Optional: Debugging
print("\n--- Executing Agent 3 ---\n")

# --- Agent 3: Execute Code and Save Output ---
result = run_agent3_and_save_output(raw_code, output_path)

print("Final result:", result)
