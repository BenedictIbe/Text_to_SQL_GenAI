from dotenv import load_dotenv
load_dotenv() ## Load all the environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai
##Configure genai key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##function to load google Gemini model and prrovide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


##Function to retrieve querries from database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows

##Define your prompt

prompt=[
    """
    
    You are an expert in connverting ENGLISH questions to SQL query!
    The SQL database has the name STUDENT and has the following columnns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records ae present?,
    the sql command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - show me all the students studying in Data Science class?,
    the sql command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science";
    also the sql code should not have ''' in the beginning or end and sql word in output
    
    """
    
]


##Streamlit app

st.set_page_config(page_title="1 can Retrieve Any SQL query")
st.header("Gemini App to Retrieve SQL Data")

question=st.text_input("Input: ", key="input")

submit=st.button("Ask the question")

##If Submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    st.subheader("Generated SQL Query")
    print(response)
    response=read_sql_query(response, "student.db")
    st.subheader("The response is")
    for row in response:
        st.write(row)

