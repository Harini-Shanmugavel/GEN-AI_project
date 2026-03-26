import streamlit as st
import sqlite3
import pandas as pd
from groq import Groq

# Groq API
client = Groq(api_key="")

# Database connection
conn = sqlite3.connect("data_dump/Chinook_Sqlite.sqlite", check_same_thread=False)

st.title("Text to SQL Chatbot")

question = st.text_input("Ask a question about the database")

if st.button("Run Query") and question:

    prompt = f"""
Convert the following English question into a SQLite SQL query.
Return ONLY the SQL query.

Tables:
Customer, Employee, Album, Artist, Track, Invoice

Question: {question}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        sql_query = response.choices[0].message.content.strip()
        sql_query = sql_query.replace("```sql","").replace("```","")

        st.subheader("Generated SQL")
        st.code(sql_query)

        cursor = conn.cursor()
        cursor.execute(sql_query)

        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        st.subheader("Result")

        df = pd.DataFrame(rows, columns=columns)
        st.dataframe(df)

    except Exception as e:
        st.error(e)