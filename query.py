import sqlite3
import ollama
import re

# ollama model being used
mymodel = "qwen2.5-coder:3b"

# Initialize SQLite connection
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

SCHEMA = """
USERS (id, name, email, department)
"""

TASK = "Retrieve all users from the USERS table where the department is 'Finance'"

USER_QUERY_TEMPLATE = """
Generate a valid SQL query. Only return the SQL query as plain text.
Do not include any explanations, comments, markdown, numbering, or formatting.


Table schema:
{schema}

Task: {task}.
"""

user_query = USER_QUERY_TEMPLATE.format(schema=SCHEMA, task=TASK)

# Step 1: Ask the model for an SQL query
response = ollama.chat(model=mymodel, messages=[{"role": "user", "content": user_query}])
sql_query = response['message']['content'].strip()

# Step 2: Extract SQL query from markdown formatting if present
sql_query = re.sub(r"```sql\s*([\s\S]*?)\s*```", r"\1", sql_query).strip()

# Step 3: Execute the query in SQLite
try:
    cursor.execute(sql_query)
    results = cursor.fetchall()
except sqlite3.Error as e:
    print("SQLite Error:", e)
    results = []

# Step 4: Send the results back to the model for response generation
results_str = "\n".join([str(row) for row in results])
response = ollama.chat(model=mymodel, messages=[
    {"role": "user", "content": f"The result of the query '{sql_query}' is: {results_str}. Generate a summary for non technical people keeping in mind the following task: '{TASK}'."}
])
print("Generated Response:", response['message']['content'])

# Close connection
cursor.close()
conn.close()
