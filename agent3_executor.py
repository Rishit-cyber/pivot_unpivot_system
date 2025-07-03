# agent3_executor.py

import pandas as pd
import traceback

def run_agent3_and_save_output(code_str: str, output_path: str, path: str, format_classification: str = "") -> str:
    try:
        # Prepare the execution environment
        exec_globals = {
            "__builtins__": __builtins__,
            "pd": pd,
            "path": path,
            "format_classification": format_classification
        }
        exec_locals = {}

        # Run the code
        exec(code_str, exec_globals, exec_locals)

        # Retrieve output
        output_df = exec_globals.get("output_df") or exec_locals.get("output_df")

        if output_df is None:
            return "ERROR: output_df not found in executed code."

        if not isinstance(output_df, pd.DataFrame):
            return "ERROR: output_df is not a DataFrame."

        # Save to Excel
        output_df.to_excel(output_path, index=True)
        return "SUCCESS"

    except Exception:
        return "ERROR: Exception during execution:\n" + traceback.format_exc()
