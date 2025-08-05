"""
SQL generation functionality using OpenAI LLM.
"""
import streamlit as st
from openai import OpenAI

def init_openai_client(api_key):
    """Initialize and return an OpenAI client"""
    try:
        client = OpenAI(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {e}")
        return None

def generate_sql(question, schema, client, model_id="gpt-4o-mini-2024-07-18:sjsu::BV5M5MaD"):
    """Generate SQL from natural language using LLM"""
    system_prompt = (
        "You are a SQL query generator. Given a natural language question and a database schema, "
        "generate the correct SQL query for SQLite. The schema is provided below:\n\n"
        f"{schema}\n\n"
        "Return only the SQL query without any explanation."
    )
    
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=200,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating SQL: {e}")
        return ""

def fix_sql(sql_query, error_message, schema, client, model_id="gpt-4o-mini-2024-07-18:sjsu::BV5M5MaD"):
    """Fix a failed SQL query using LLM"""
    system_prompt = (
        "You are a SQL expert who fixes broken SQL queries. Given a SQL query, an error message, "
        "and a database schema, provide a corrected SQL query that resolves the error. "
        "The schema is provided below:\n\n"
        f"{schema}\n\n"
        "Return only the fixed SQL query without any explanation."
    )
    
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"The following SQL query failed with error: {error_message}\n\nQuery: {sql_query}"}
            ],
            max_tokens=200,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error fixing SQL: {e}")
        return sql_query  # Return original if fixing fails