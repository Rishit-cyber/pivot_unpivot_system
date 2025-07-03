
# 🔁 Pivot ↔ Unpivot Transformer

A modular, agent-based data transformation system that automatically detects an Excel file's format (`PIVOTED` or `UNPIVOTED`), generates transformation code using Gemini, executes it, and provides a downloadable output file via a Streamlit UI.

---

## 🧠 Components

- **Agent 1**: Detects if input Excel data is in `PIVOTED` or `UNPIVOTED` format.
- **Agent 2**: Generates transformation code dynamically using Gemini.
- **Agent 3**: Executes the generated code and returns the transformed DataFrame.

---

## 🚀 Deploy on Render

1. Push this repo to GitHub.
2. Create a **new Web Service** on [Render.com](https://render.com/).
3. Configure the **environment variable**:
   - `GEMINI_API_KEY`: *(your Google Generative AI API key)*
4. Set the **Start Command** to:
   ```bash
   streamlit run ui_streamlit_app.py


5. After deployment, upload your Excel file and download the transformed result.

---

## 🧪 Local Development

To test locally:

```bash
pip install -r requirements.txt
streamlit run ui_streamlit_app.py
```

> Ensure `GEMINI_API_KEY` is available in your environment:
>
> ```bash
> export GEMINI_API_KEY=your_api_key_here
> ```

---

## 📁 Final Folder Structure

```bash
pivot_unpivot_system/
├── agent1_detection_prompt.txt       # Agent 1 prompt for detecting format
├── agent2_codegen_prompt.txt         # Agent 2 prompt for code generation
├── agent3_executor.py                # Executes generated code
├── controller_agent.py               # (Optional) CLI version for testing
├── ui_streamlit_app.py               # Streamlit UI for upload + output
├── requirements.txt                  # Python dependencies
├── render.yaml                       # Render deployment config
├── README.md                         # This file
```

---

## 📌 Notes

* The system uses the **Gemini 2.0 Flash model** via Google Generative AI.
* Automatically handles numeric and non-numeric pivot structures.
* Easily extensible to support more formats or transformation rules in future.

