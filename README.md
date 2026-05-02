# LeadChat - Chat with Customer Data

## Overview

LeadChat is a web application that allows users to query customer data using natural language. Instead of manually searching through Excel files, users can ask questions in plain English and get accurate results instantly.

For example:
“How many customers have a budget above 90 lakhs?”

The system processes the query and returns results based on real data.

---

## How It Works

The system follows a simple and reliable flow:

1. The user enters a query in natural language
2. The system converts the query into pandas code
3. Pandas executes the code on the dataset
4. The result is returned to the user

The AI component is only used to interpret the query. All computations are performed using pandas, ensuring accuracy and eliminating incorrect or hallucinated results.

---

## Tech Stack

Backend:

* Python #Python version required: 3.11
* FastAPI
* Pandas
* OpenPyXL

Frontend:

* HTML
* CSS
* JavaScript

AI Layer:

* OpenRouter (free large language model)

---

## Features

* Natural language query support
* Accurate data processing using pandas
* Supports filtering, counting, and aggregation
* Lightweight and fast frontend
* Clean API-based backend
* Displays generated logic for transparency

---

## Example Queries

* How many customers have budget above 80 lakhs
* List 2BHK customers in Hinjewadi
* What is the average budget
* Show customers between 50 and 90 lakhs
* Which location has the most customers

---

## Project Structure

leadchat/
backend/
main.py
requirements.txt

frontend/
index.html

data/
pune_real_estate_leads_updated.xlsx

README.md
.gitignore

---

## How to Run the Project

### Backend

step 1)cd backend
step 2)python -3.11 -m venv venv
step 3)venv\Scripts\activate
step 4)pip install -r requirements.txt

Set API key:
step1) gp to OPENROUTER.com
Step2)Create key there
Step3)after activating env set key using syntax:
  set OPENROUTER_API_KEY=your_key_here

Run server:

uvicorn main:app --reload --port 8000

---
split terminal here and run frontend.
### Frontend

step 1)cd frontend
step 2)python -m http.server 3000
step 3)
Open in browser:

http://localhost:3000

---

## API Endpoints

POST /query
Processes user queries

GET /stats
Returns dataset summary

GET /health
Checks server status

---

## Key Design Decision

The system separates interpretation and computation.
The AI converts queries into pandas logic, while pandas executes all operations on real data. This ensures reliability and prevents incorrect outputs.

---

## Conclusion

LeadChat simplifies data exploration by combining natural language interaction with accurate data processing. It demonstrates how AI can assist users while maintaining correctness through deterministic computation.
