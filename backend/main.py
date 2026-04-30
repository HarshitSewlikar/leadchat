import os
import json
import re
import requests
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ===================== API KEY =====================

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set")

# ===================== FASTAPI =====================
app = FastAPI(title="Chat with Customer Data API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== LOAD DATA =====================
DATA_PATH = r"C:\Users\LENOVO\Desktop\leadchat\data\pune_real_estate_leads_updated.xlsx"

def load_data():
    df = pd.read_excel(DATA_PATH)
    df.columns = [c.strip() for c in df.columns]

    # Ensure correct columns
    if "Budget (INR)" in df.columns:
        df["Budget (INR)"] = pd.to_numeric(df["Budget (INR)"], errors="coerce")
        df["Budget (Lakhs)"] = (df["Budget (INR)"] / 100000).round(2)

    return df

df_global = load_data()

print("Loaded columns:", df_global.columns.tolist())

# ===================== PROMPT =====================
SYSTEM_PROMPT = """
You are a Python pandas expert.

The dataframe name is df.

Columns:
- Name
- Budget (Lakhs)
- Property Type
- Location
- Last Call Status

Rules:
- ALWAYS use exact column names
- Use df['Budget (Lakhs)']
- Use df['Location']
- Store output in variable 'result'
- Only return Python code
- No explanation
"""

# ===================== OPENROUTER =====================
def call_openrouter(prompt: str) -> str:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-oss-120b:free",
            "messages": [
                {"role": "system", "content": "Return ONLY pandas Python code."},
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()

    if "choices" not in data:
        raise Exception(f"OpenRouter error: {data}")

    return data["choices"][0]["message"]["content"]

# ===================== SAFE EXECUTION =====================
def execute_code(code: str):
    local_vars = {"df": df_global.copy(), "pd": pd}

    try:
        exec(code, {}, local_vars)

        if "result" not in local_vars:
            return {"error": "No result variable", "code": code}

        result = local_vars["result"]

        if result is None:
            return {"error": "Result is None", "code": code}

        return result

    except Exception as e:
        return {"error": str(e), "code": code}

# ===================== MODEL =====================
class QueryRequest(BaseModel):
    query: str

# ===================== MAIN API =====================
@app.post("/query")
def handle_query(req: QueryRequest):
    query = req.query.strip()

    try:
        prompt = SYSTEM_PROMPT + "\nQuery: " + query

        code = call_openrouter(prompt)

        # Clean markdown
        code = re.sub(r"```python\n?|```", "", code).strip()

        print("\nGenerated Code:\n", code)

        result = execute_code(code)

        # Handle errors
        if isinstance(result, dict) and "error" in result:
            return {
                "answer": "Execution Error",
                "details": result,
                "generated_code": code
            }

        return {
            "answer": str(result),
            "generated_code": code
        }

    except Exception as e:
        return {"error": str(e)}

# ===================== STATS =====================
@app.get("/stats")
def stats():
    return {
        "total": len(df_global),
        "avg_budget": round(df_global["Budget (Lakhs)"].mean(), 2),
    }

# ===================== HEALTH =====================
@app.get("/health")
def health():
    return {"status": "ok"}