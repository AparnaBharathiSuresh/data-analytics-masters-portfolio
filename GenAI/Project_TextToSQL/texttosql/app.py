import streamlit as st
import os
from database_utils import list_sqlite_files, connect_to_database, get_db_schema, execute_query
from sql_generator import init_openai_client
from visualization import display_results
from database_utils import create_spider_databases
import re
# Import the agent
from agent_components import TextToSQLAgent

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL Converter",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'db_connection' not in st.session_state:
    st.session_state.db_connection = None
if 'openai_client' not in st.session_state:
    st.session_state.openai_client = None
if 'schema' not in st.session_state:
    st.session_state.schema = None
if 'connected_db' not in st.session_state:
    st.session_state.connected_db = None
if 'history' not in st.session_state:
    st.session_state.history = []
# Add agent to session state
if 'agent' not in st.session_state:
    st.session_state.agent = None

# App title and description
st.title("🔍 Text-to-SQL Converter")
st.markdown("""
    Transform natural language questions into SQL queries using an intelligent AI agent.
    Our agent will understand your question, plan the approach, and create the best SQL query!
""")

# Data directory
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Auto-create SPIDER databases if not already created
SPIDER_DB_DIR = os.path.join(DATA_DIR, "spider_databases")
TABLES_JSON_PATH = os.path.join(os.path.dirname(__file__), "tables.json")

if not os.path.exists(SPIDER_DB_DIR) or not os.listdir(SPIDER_DB_DIR):
    create_spider_databases(TABLES_JSON_PATH, SPIDER_DB_DIR)

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # OpenAI API setup
    st.subheader("LLM Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    model_id = st.text_input("Model ID", value="ft:gpt-4o-mini-2024-07-18:sjsu::BV5M5MaD")
    
    # Database selection
    st.subheader("Database Selection")

    allowed_dbs = {"address.db","bbc.db", "cinema.db", "course_teach.db", "flight.db","sample.db", "pets.db"}

    db_files = [
    os.path.join(DATA_DIR, f) for f in list_sqlite_files(DATA_DIR) if f in allowed_dbs
    ] + [
    os.path.join(SPIDER_DB_DIR, f) for f in list_sqlite_files(SPIDER_DB_DIR) if f in allowed_dbs
    ]
    
    # Find all available SQLite databases
    #db_files = list_sqlite_files(DATA_DIR)
    
    # Option to upload own database
    uploaded_db = st.file_uploader("Upload a SQLite database", type="db")
    
    if uploaded_db:
        # Save the uploaded file temporarily
        with open(os.path.join(DATA_DIR, uploaded_db.name), "wb") as f:
            f.write(uploaded_db.getbuffer())
        selected_db = uploaded_db.name
    else:
        # Select from existing databases
        selected_db = st.selectbox("Select a database", db_files)
    
    # Connect buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Initialize LLM"):
            if api_key:
                try:
                    st.session_state.openai_client = init_openai_client(api_key)
                    st.success("LLM initialized successfully!")
                except Exception as e:
                    st.error(f"Error initializing LLM: {e}")
            else:
                st.warning("Please enter your API key")
    
    with col2:
        if st.button("Connect Database"):
            if selected_db:
                db_path = selected_db
                #db_path = os.path.join(DATA_DIR, selected_db)
                try:
                    conn = connect_to_database(db_path)
                    st.session_state.db_connection = conn
                    st.session_state.connected_db = selected_db
                    st.session_state.schema = get_db_schema(conn)
                    
                    # Initialize the agent with the database connection and schema
                    if st.session_state.openai_client:
                        st.session_state.agent = TextToSQLAgent(
                            st.session_state.openai_client,
                            st.session_state.db_connection,
                            st.session_state.schema
                        )
                    
                    st.success(f"Connected to {selected_db}!")
                except Exception as e:
                    st.error(f"Error connecting to database: {e}")
            else:
                st.warning("Please select a database")
    
    # History section
    st.subheader("Query History")
    if st.button("Clear History"):
        st.session_state.history = []
    
    for i, (q, s) in enumerate(st.session_state.history):
        if st.button(f"{i+1}. {q[:30]}...", key=f"hist_{i}"):
            st.session_state.reload_query = q
            st.session_state.reload_sql = s
            st.rerun()

# Main content area
if not st.session_state.openai_client:
    st.warning("Please initialize the LLM first")
elif not st.session_state.db_connection:
    st.warning("Please connect to a database first")
elif not st.session_state.agent:
    st.warning("Agent not initialized. Please reconnect to the database.")
else:
    # Display connected database name
    st.subheader(f"Connected to: {st.session_state.connected_db}")
    
    # Database schema section
    with st.expander("Database Schema", expanded=False):
        st.text(st.session_state.schema)
    
    # Input for natural language query
    st.subheader("Ask a question")
    if 'reload_query' in st.session_state:
        query_input = st.text_area("Enter your question:", 
                                  value=st.session_state.reload_query,
                                  height=80)
        del st.session_state.reload_query
    else:
        query_input = st.text_area("Enter your question:", height=80)
    
    # Generate SQL using the agent
    generate_button = st.button("Process Query", type="primary")

    if generate_button and query_input:
        # Clear previous results when processing a new query
        if 'current_result' in st.session_state:
            del st.session_state.current_result
        if 'current_sql' in st.session_state:
            del st.session_state.current_sql
            
        # Also clear any executed results display  
        if 'executed_results' in st.session_state:
            del st.session_state.executed_results
        if 'last_viz_type' in st.session_state:
            del st.session_state.last_viz_type
        
        # Add to history
        if (query_input, "") not in st.session_state.history:
            st.session_state.history.insert(0, (query_input, ""))
            if len(st.session_state.history) > 10:
                st.session_state.history.pop()
        
        # Use the agent to process the query
        with st.spinner("Processing your query..."):
            # Call the agent to process the query
            result = st.session_state.agent.process_query(query_input)
            
            # Check if clarification is needed
            if result.get("status") == "needs_clarification":
                # Store only the clarification request, not the SQL results
                st.session_state.needs_clarification = True
                st.session_state.clarification_options = result.get("options", [])
                st.session_state.clarification_reasoning = result.get("reasoning", "")
                # Do NOT set current_result or current_sql
                
                # Force a rerun to show clarification UI without results
                st.rerun()
            else:
                # Only store results if clarification isn't needed
                st.session_state.needs_clarification = False
                st.session_state.current_result = result
                st.session_state.current_sql = result.get("sql", "")
                
                # Update history with SQL
                for i, (q, _) in enumerate(st.session_state.history):
                    if q == query_input:
                        st.session_state.history[i] = (q, st.session_state.current_sql)
                        break
                
                # Force a rerun to show the results
                st.rerun()
    elif generate_button:
        st.warning("Please enter a question first")

    # After the generate button section, add this to handle clarification state
    if 'needs_clarification' in st.session_state and st.session_state.needs_clarification:
        st.subheader("I need some clarification:")
        
        for i, option in enumerate(st.session_state.clarification_options):
            if st.button(option, key=f"clarify_{i}"):
                with st.spinner("Processing with clarification..."):
                    clarified_result = st.session_state.agent.provide_clarification(option)
                    
                    # Clear clarification state
                    st.session_state.needs_clarification = False
                    
                    # Store the clarified result
                    st.session_state.current_result = clarified_result
                    st.session_state.current_sql = clarified_result.get("sql", "")
                    
                    # Update history
                    if len(st.session_state.history) > 0:
                        q = st.session_state.history[0][0]
                        st.session_state.history[0] = (q, st.session_state.current_sql)
                    
                    # Force a rerun to show the results
                    st.rerun()
        
        # Show reasoning for why clarification is needed
        if 'clarification_reasoning' in st.session_state:
            with st.expander("Reasoning Process", expanded=False):
                reasoning_text = st.session_state.clarification_reasoning
                
                # Split by lines and clean up
                lines = [line.strip() for line in reasoning_text.split('\n') if line.strip()]
                
                # Simply display each line
                for line in lines:
                    st.write(line)

    # Only show results if clarification isn't needed
    if 'needs_clarification' not in st.session_state or not st.session_state.needs_clarification:
        # Display results if available
        if 'current_result' in st.session_state:
            result = st.session_state.current_result
            
            # Show the reasoning process
            if "reasoning" in result:
                with st.expander("Reasoning Process", expanded=False):
                    reasoning_text = result["reasoning"]
                    
                    # Split by lines and clean up
                    lines = [line.strip() for line in reasoning_text.split('\n') if line.strip()]
                    
                    # Simply display each line
                    for line in lines:
                        st.write(line)
            
            # Display generated SQL
            if "sql" in result:
                st.subheader("Generated SQL")
                st.code(result["sql"], language="sql")
                
                # Execute SQL button
                execute_button = st.button("Execute SQL", type="primary", key="execute_sql_button")
                if execute_button:
                    # Clear any previous visualization state
                    if 'last_viz_type' in st.session_state:
                        del st.session_state.last_viz_type
                    
                    with st.spinner("Executing query..."):
                        results, execution_time, error = execute_query(
                            st.session_state.db_connection,
                            result["sql"]
                        )
                    
                    # Store executed results in session state
                    st.session_state.executed_results = {
                        "results": results,
                        "execution_time": execution_time,
                        "error": error
                    }
                    
                    # Force a rerun to show results
                    st.rerun()
        
        # Display executed results if available
        if 'executed_results' in st.session_state:
            executed = st.session_state.executed_results
            
            if executed["error"]:
                st.error(f"Error executing query: {executed['error']}")
            else:
                display_results(executed["results"], executed["execution_time"])

# Footer
st.markdown("---")
st.markdown("Text-to-SQL Application with Agentic Approach")