import google.generativeai as genai
from langchain_community.utilities import SQLDatabase
import os
from dotenv import load_dotenv
import re

load_dotenv()

class TextToSQLAgent:
    def __init__(self, db_path="sample_data.db"):
        """Initialize the Text to SQL Agent"""
        # Configure Google Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        
        # Try different model names
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-flash-latest')
            except:
                self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Connect to database
        self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
    def get_schema(self):
        """Get database schema"""
        return self.db.get_table_info()
    
    def generate_sql(self, question):
        """Generate SQL query from natural language"""
        try:
            schema = self.get_schema()
            
            prompt = f"""You are a SQL expert. Convert the natural language question to a SQL query.

Database Schema:
{schema}

Question: {question}

Rules:
1. Return ONLY the SQL query
2. No explanations or markdown
3. No ``` or formatting
4. Just the executable SQL query

SQL Query:"""
            
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            
            # Clean the response
            sql_query = re.sub(r'```sql\n?', '', sql_query)
            sql_query = re.sub(r'```\n?', '', sql_query)
            sql_query = sql_query.strip()
            
            return sql_query
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def execute_sql(self, sql_query):
        """Execute SQL query on database"""
        try:
            # Use the database connection to run query
            result = self.db.run(sql_query)
            return result
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def get_natural_response(self, question, sql_query, result):
        """Convert result to natural language"""
        try:
            prompt = f"""Answer the user's question based on the SQL query result.

Question: {question}
SQL Query Used: {sql_query}
Result: {result}

Provide a clear, concise answer in natural language.

Answer:"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Result: {result}"
    
    def chat(self, question):
        """Main chat function"""
        # Step 1: Generate SQL
        sql_query = self.generate_sql(question)
        
        if sql_query.startswith("Error"):
            return {
                "sql_query": "N/A",
                "result": "N/A",
                "answer": sql_query
            }
        
        # Step 2: Execute SQL
        result = self.execute_sql(sql_query)
        
        if isinstance(result, str) and result.startswith("Error"):
            return {
                "sql_query": sql_query,
                "result": "N/A",
                "answer": result
            }
        
        # Step 3: Convert to natural language
        natural_response = self.get_natural_response(question, sql_query, result)
        
        return {
            "sql_query": sql_query,
            "result": result,
            "answer": natural_response
        }