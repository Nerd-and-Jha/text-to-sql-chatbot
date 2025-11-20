import streamlit as st
from sql_agent import TextToSQLAgent
import os
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL Chatbot",
    page_icon="💬",
    layout="wide"
)

# Main title
st.title("💬 Text-to-SQL RAG Chatbot")
st.markdown("Ask questions about your database in natural language!")

# Initialize the AI agent (cached so it doesn't reload every time)
@st.cache_resource
def load_agent():
    return TextToSQLAgent()

try:
    agent = load_agent()
    
    # Sidebar with database information
    with st.sidebar:
        st.header("📊 Database Schema")
        st.code(agent.get_schema(), language="sql")
        
        st.header("💡 Example Questions")
        st.markdown("""
        Try asking:
        - How many students are there?
        - Show me all students with grade A
        - What is the average marks?
        - Who has the highest marks?
        - List students older than 20
        - What is the total marks of all students?
        - Show me students with marks above 80
        """)
        
        st.header("ℹ️ How It Works")
        st.markdown("""
        1. You ask a question in plain English
        2. AI converts it to SQL query
        3. Query runs on your database
        4. AI converts result back to English
        """)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show SQL query in expandable section
            if "sql" in message:
                with st.expander("🔍 View SQL Query"):
                    st.code(message["sql"], language="sql")
            
            # Show raw database result
            if "result" in message:
                with st.expander("📊 View Raw Database Result"):
                    st.code(message["result"])

    # Chat input box
    if question := st.chat_input("Ask a question about your database..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(question)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking and querying database..."):
                try:
                    # Call the AI agent
                    response = agent.chat(question)
                    
                    # Display the natural language answer
                    st.markdown(response["answer"])
                    
                    # Show SQL query used
                    with st.expander("🔍 View SQL Query"):
                        st.code(response["sql_query"], language="sql")
                    
                    # Show raw result from database
                    with st.expander("📊 View Raw Database Result"):
                        st.code(response["result"])
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sql": response["sql_query"],
                        "result": response["result"]
                    })
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Make sure you have:")
                    st.code("""
1. Created the database (run: python database.py)
2. Added your Google API key in .env file
3. Installed all packages (run: pip install -r requirements.txt)
                    """)

except Exception as e:
    st.error(f"❌ Failed to initialize chatbot: {str(e)}")
    st.info("""
    **Troubleshooting Steps:**
    
    1. Make sure you've created the database:
            python database.py
```
    
    2. Check your .env file has the API key:
```
       GOOGLE_API_KEY=your_actual_key_here
```
    
    3. Verify all packages are installed:
```
       pip install -r requirements.txt
```
    """)