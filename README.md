# Text_to_SQL_GenAI
This GenAI model uses Google Gemini to create queries on an SQL database based on the question entered on the prompt

# GenAI SQL Query Generator

This repository contains a Streamlit application that utilizes Google Generative AI (GenAI) to convert English questions into SQL queries. The SQL queries are then executed against a SQLite database to retrieve the desired data. The application is designed to help users easily generate and run SQL queries without needing to know SQL.

## Features

- Converts natural language questions to SQL queries using Google GenAI.
- Executes the generated SQL queries on a SQLite database.
- Displays the results of the queries in a user-friendly interface.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10 or higher
- Streamlit
- SQLite
- Google Generative AI API key

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/genai-sql-query-generator.git
    cd genai-sql-query-generator
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the SQLite database:**

    Create a script `initialize_db.py` to set up your database:
    ```python
    import sqlite3

    conn = sqlite3.connect('student.ds')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS STUDENT (
        NAME TEXT,
        CLASS TEXT,
        SECTION TEXT
    )
    ''')

    cur.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION) VALUES ('John Doe', 'Data Science', 'A')")
    cur.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION) VALUES ('Jane Smith', 'Data Science', 'B')")
    cur.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION) VALUES ('Alice Johnson', 'Machine Learning', 'A')")

    conn.commit()
    conn.close()
    ```

    Run the script:
    ```sh
    python initialize_db.py
    ```

5. **Set up your environment variables:**

    Create a `.env` file in the root directory of your project and add your Google API key:
    ```env
    GOOGLE_API_KEY=your_google_api_key
    ```

### Usage

1. **Run the Streamlit application:**
    ```sh
    streamlit run sql.py
    ```

2. **Interact with the application:**

    - Enter your question in natural language.
    - Click the "Ask the question" button.
    - View the generated SQL query and the query results.

### Example

1. **User enters a question:**
    ![User Input](path/to/user_input_image.png)

2. **Generated SQL query is displayed:**
    ![Generated SQL](path/to/generated_sql_image.png)

3. **Query results are shown:**
    ![Query Results](path/to/query_results_image.png)

### Code Explanation

The main components of the application are:

- **`sql.py`**: The main Streamlit application script.
- **`initialize_db.py`**: A script to initialize the SQLite database with sample data.
- **`.env`**: A file to store environment variables securely.
- **`requirements.txt`**: A file listing all the required Python packages.

#### `sql.py`

```python
from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure genai key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load google Gemini model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve queries from database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define your prompt
prompt = [
    """
    You are an expert in converting ENGLISH questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.
    For example:
    Example 1 - How many entries of records are present?
    The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;
    Example 2 - Show me all the students studying in Data Science class?
    The SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS="Data Science";
    Also, the SQL code should not have ''' in the beginning or end and SQL word in output.
    """
]

# Streamlit app
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App to Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If Submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("Generated SQL Query")
    st.code(response)
    response = read_sql_query(response, "student.ds")
    st.subheader("The response is")
    for row in response:
        st.write(row)

