"""
Components for implementing an agentic approach in the Text-to-SQL application.
"""
import streamlit as st
from openai import OpenAI
import json
import re

class TextToSQLAgent:
    """
    An agent that handles the entire process of converting text to SQL,
    with multi-step reasoning, validation, and correction.
    """
    
    def __init__(self, openai_client, db_connection, schema):
        self.client = openai_client
        self.db_connection = db_connection
        self.schema = schema
        self.conversation_history = []
        self.current_plan = []
        self.needs_clarification = False
        self.clarification_options = []
        
    def process_query(self, query):
        """Process a natural language query through multiple reasoning steps."""
        # First, understand the query and identify potential ambiguities
        understanding = self._understand_query(query)
        
        # Only ask for clarification if highly ambiguous (raised threshold)
        ambiguity_score = understanding.get("ambiguity_score", 0)
        clarification_options = understanding.get("clarification_options", [])
        
        # Only clarify for very ambiguous queries (threshold raised to 0.5)
        if ambiguity_score > 0.5 and len(clarification_options) > 0:
            self.needs_clarification = True
            self.clarification_options = clarification_options[:2]  # Limit to 2 options max
            
            # Return information about the ambiguity
            return {
                "status": "needs_clarification",
                "options": self.clarification_options,
                "reasoning": understanding.get("reasoning", "Query is ambiguous and needs clarification.")
            }
            
        # Generate SQL based on most likely interpretation
        sql = self._generate_sql(query, understanding)
        
        # Return a more concise result
        return {
            "status": "complete",
            "sql": sql,
            "reasoning": understanding.get("reasoning", "Analyzed query and generated SQL based on schema understanding.")
        }
    
    def provide_clarification(self, clarification):
        """Handle user clarification to resolve ambiguity."""
        # Generate SQL with the clarified information
        sql = self._generate_sql(clarification)
        
        return {
            "status": "complete",
            "sql": sql,
            "reasoning": f"Generated SQL based on the clarified query."
        }
    
    def _understand_query(self, query):
        """Analyze the query to understand intent and identify ambiguities."""
        system_prompt = """
        You are an expert data analyst. Analyze the user's query to identify:
        
        1. The main entities and actions in the query
        2. Any potential ambiguities that make interpretation unclear
        3. The most likely interpretation based on the database schema
        
        Only flag a query as ambiguous if there are multiple equally valid interpretations
        that would result in substantially different SQL queries.
        
        Keep your reasoning brief but informative. Number your main points.
        """
        
        user_prompt = f"""
        Query: {query}
        
        Database schema:
        {self.schema}
        
        Analyze this query and determine if clarification is needed.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model="ft:gpt-4o-mini-2024-07-18:sjsu::BV5M5MaD",  # Use your model ID here
                messages=messages,
                temperature=0.0
            )
            
            # Get the text content
            understanding_text = response.choices[0].message.content
            
            # Extract key information using a simpler approach - REMOVED THE CHARACTER LIMIT
            # Replace this section in your agent_components.py

            # Extract key information using a simpler approach - REMOVED THE CHARACTER LIMIT
            understanding = {
                "reasoning": understanding_text,  # Store full reasoning without truncation
                "ambiguity_score": 0.0,  # Default low score
                "clarification_options": []
            }

            # Improved ambiguity detection with more patterns
            ambiguity_phrases = [
                "ambiguous", "unclear", "vague", "not specific", 
                "multiple interpretations", "lacks context", 
                "clarification is needed", "clarification needed",
                "cannot determine", "not enough information",
                "could mean", "could refer to", "could be interpreted",
                "not clear what", "not clear which"
            ]

            # Set ambiguity score based on content
            for phrase in ambiguity_phrases:
                if phrase in understanding_text.lower():
                    # Start with moderate ambiguity
                    understanding["ambiguity_score"] = 0.6
                    break

            # Check for stronger indicators of high ambiguity
            high_ambiguity_phrases = [
                "highly ambiguous", "completely ambiguous", "extremely ambiguous",
                "very ambiguous", "totally ambiguous", "entirely ambiguous",
                "definitely needed", "definitely need clarification",
                "impossible to determine", "cannot interpret",
                "no likely interpretation", "no way to determine"
            ]

            for phrase in high_ambiguity_phrases:
                if phrase in understanding_text.lower():
                    # Set high ambiguity
                    understanding["ambiguity_score"] = 0.9
                    break

            # Generate default clarification options if ambiguous but no questions found
            if understanding["ambiguity_score"] > 0.5:
                # Try to extract question marks
                options = re.findall(r'[?][^?]*[?]', understanding_text)
                
                if options:
                    understanding["clarification_options"] = options[:2]
                else:
                    # Default clarification options for highly ambiguous queries
                    understanding["clarification_options"] = [
                        "Could you specify what information you're looking for?",
                        "Which table or entity are you interested in?"
                    ]
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": query,
                "understanding": understanding
            })
            
            return understanding
            
        except Exception as e:
            st.error(f"Error in query understanding: {str(e)}")
            return {
                "reasoning": "Analyzing query to generate SQL",
                "ambiguity_score": 0,
                "clarification_options": []
            }
    
    def _generate_sql(self, query_text, understanding=None):
        """Generate SQL based on understanding and parameters."""
        system_prompt = (
            "You are a SQL query generator. Given a natural language question and a database schema, "
            "generate the correct SQL query for SQLite. The schema is provided below:\n\n"
            f"{self.schema}\n\n"
            "Return only the SQL query without any explanation."
        )
        
        try:
            response = self.client.chat.completions.create(
                model="ft:gpt-4o-mini-2024-07-18:sjsu::BV5M5MaD",  # Use your model ID here
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query_text}
                ],
                temperature=0.0
            )
            
            sql = response.choices[0].message.content.strip()
            return sql
            
        except Exception as e:
            st.error(f"Error generating SQL: {str(e)}")
            return "SELECT * FROM customers LIMIT 10; -- Error occurred, showing sample data"