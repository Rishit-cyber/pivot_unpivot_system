# ui_streamlit_app.py

import streamlit as st
import os
import tempfile
import re
import pandas as pd
import google.generativeai as genai
from agent3_executor import run_agent3_and_save_output
import sys
import io
# --- Load API Key ---
# Load Gemini API key from plain text file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY environment variable not set.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

st.set_page_config(page_title="Pivot ↔ Unpivot Transformer", layout="centered")
st.title("🔁 Pivot ↔ Unpivot Transformer")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name
    st.success("✅ File uploaded and saved.")

    try:
        df = pd.read_excel(temp_path)
    except Exception as e:
        st.error(f"❌ Failed to read Excel file: {e}")
        st.stop()

    # Convert a sample of the data to text for Gemini input
    preview = df.head(10).to_csv(index=False)

    # --- Agent 1: Format Detection ---
    with open("agent1_detection_prompt.txt") as f:
        agent1_prompt = f.read()

    detection_prompt = agent1_prompt + f"\n\nHere is a sample of the data:\n\n{preview}"
    response1 = model.generate_content(detection_prompt)
    format_classification = response1.text.strip().upper()

    if format_classification not in {"PIVOTED", "UNPIVOTED"}:
        st.error(f"❌ Invalid format classification: `{format_classification}`")
        st.stop()

    st.info(f"🔍 Detected Format: `{format_classification}`")

    # --- Agent 2: Code Generation ---
    with open("agent2_codegen_prompt.txt") as f:
        agent2_prompt = f.read()

    generation_prompt = agent2_prompt + f'\n\npath = "{temp_path}"\nformat_classification = "{format_classification}"'
    response2 = model.generate_content(generation_prompt)
    raw_code = response2.text.strip()

    # --- Strip Markdown fences ---
    raw_code = re.sub(r"^```(?:python)?", "", raw_code).strip()
    raw_code = re.sub(r"```$", "", raw_code).strip()

    # Force override path
    raw_code = re.sub(r'path\s*=\s*["\'].*?["\']', f'path = "{temp_path}"', raw_code)

    # st.subheader("🧠 Generated Code by Agent 2")
    # st.code(raw_code, language="python")

    # --- Agent 3: Execute ---
    st.subheader("🚀 Output Preview")

    output_path = "output.xlsx"
    try:
        result = run_agent3_and_save_output(raw_code, output_path, temp_path, format_classification)
        if "ERROR" in result:
            st.error(result)
        else:
            st.success("✅ Transformation successful!")

            # Load output file into memory buffer
            with open(output_path, "rb") as f:
                excel_bytes = f.read()
            buffer = io.BytesIO(excel_bytes)

            # Serve with correct MIME
            st.download_button(
                label="📥 Download Output Excel",
                data=buffer,
                file_name="pivot_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Execution Failed: {e}")
