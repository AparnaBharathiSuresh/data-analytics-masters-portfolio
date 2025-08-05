"""
Data visualization functions for the Text-to-SQL application.
"""
import streamlit as st
import plotly.express as px
import pandas as pd

def display_results(results, execution_time):
    """Display query results with visualization options"""
    st.success(f"Query executed in {execution_time:.4f} seconds")
    
    # Check for and fix duplicate column names before displaying
    if isinstance(results, pd.DataFrame):
        # Get duplicate column names
        cols = results.columns.tolist()
        duplicate_cols = set([x for x in cols if cols.count(x) > 1])
        
        if duplicate_cols:
            # Create a copy of the dataframe to avoid modifying the original
            fixed_results = results.copy()
            
            # Rename duplicate columns by adding a suffix
            for col in duplicate_cols:
                # Find all occurrences of this column name
                indices = [i for i, x in enumerate(fixed_results.columns) if x == col]
                
                # Rename all but the first occurrence
                for i, idx in enumerate(indices[1:], 1):
                    # Create new column name with suffix
                    new_name = f"{col}_{i}"
                    
                    # Rename the column at this position
                    fixed_results.columns.values[idx] = new_name
                    
            # Display the warning about renamed columns
            st.warning(f"Duplicate column names found and renamed: {', '.join(duplicate_cols)}")
            
            # Use the fixed dataframe
            results = fixed_results
    
    # Display results in a table
    st.subheader("Query Results")
    st.dataframe(results)
    
    # Download option
    csv = results.to_csv(index=False)
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name="query_results.csv",
        mime="text/csv"
    )
    
    # Try to create visualizations if appropriate
    if len(results) > 0 and len(results.columns) >= 2:
        st.subheader("Visualization")
        
        try:
            # Check if there are numeric columns for visualization
            numeric_cols = results.select_dtypes(include=['number']).columns.tolist()
            text_cols = results.select_dtypes(include=['object']).columns.tolist()
            
            if len(numeric_cols) > 0 and len(results) > 1:
                # Offer different visualization types
                viz_type = st.selectbox(
                    "Select visualization type",
                    ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"],
                    key="viz_type"
                )
                
                # Clear previous chart selections when changing chart type
                if 'last_viz_type' not in st.session_state or st.session_state.last_viz_type != viz_type:
                    # Reset axis selections when changing chart type
                    if 'x_col' in st.session_state: del st.session_state.x_col
                    if 'y_col' in st.session_state: del st.session_state.y_col
                    if 'x_col_line' in st.session_state: del st.session_state.x_col_line
                    if 'y_col_line' in st.session_state: del st.session_state.y_col_line
                    if 'x_col_scatter' in st.session_state: del st.session_state.x_col_scatter
                    if 'y_col_scatter' in st.session_state: del st.session_state.y_col_scatter
                    if 'name_col_pie' in st.session_state: del st.session_state.name_col_pie
                    if 'value_col_pie' in st.session_state: del st.session_state.value_col_pie
                    
                    st.session_state.last_viz_type = viz_type
                
                # Visualization settings based on chart type
                if viz_type == "Bar Chart" and len(text_cols) > 0:
                    if len(text_cols) == 0:
                        st.info("Bar chart requires a categorical column for the x-axis")
                        return
                        
                    x_col = st.selectbox("X-axis (categories)", text_cols, key="x_col")
                    y_col = st.selectbox("Y-axis (values)", numeric_cols, key="y_col")
                    
                    # Create bar chart
                    fig = px.bar(results, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                    st.plotly_chart(fig, use_container_width=True)
                
                elif viz_type == "Line Chart":
                    if len(text_cols) == 0:
                        st.info("Line chart requires a categorical column for the x-axis")
                        return
                        
                    x_col = st.selectbox("X-axis", text_cols, key="x_col_line")
                    y_col = st.selectbox("Y-axis", numeric_cols, key="y_col_line")
                    
                    # Create line chart
                    fig = px.line(results, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
                    st.plotly_chart(fig, use_container_width=True)
                
                elif viz_type == "Scatter Plot":
                    if len(numeric_cols) < 2:
                        st.info("Scatter plot requires at least two numeric columns")
                        return
                        
                    x_col = st.selectbox("X-axis", numeric_cols, key="x_col_scatter")
                    # Filter out the selected x-axis column from y-axis options
                    y_options = [c for c in numeric_cols if c != x_col]
                    if not y_options:
                        st.info("Need another numeric column for Y-axis")
                        return
                    y_col = st.selectbox("Y-axis", y_options, key="y_col_scatter")
                    
                    # Create scatter plot
                    fig = px.scatter(results, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                    st.plotly_chart(fig, use_container_width=True)
                
                elif viz_type == "Pie Chart":
                    if len(text_cols) == 0:
                        st.info("Pie chart requires a categorical column for names")
                        return
                    if len(numeric_cols) == 0:
                        st.info("Pie chart requires a numeric column for values")
                        return
                        
                    name_col = st.selectbox("Names", text_cols, key="name_col_pie")
                    value_col = st.selectbox("Values", numeric_cols, key="value_col_pie")
                    
                    # Create pie chart - limit to top 10 categories if more than 10
                    if len(results) > 10:
                        results_sorted = results.sort_values(by=value_col, ascending=False).head(10)
                        title = f"Top 10 {name_col} by {value_col}"
                    else:
                        results_sorted = results
                        title = f"{name_col} by {value_col}"
                    
                    fig = px.pie(results_sorted, names=name_col, values=value_col, title=title)
                    st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.info("Please select a visualization type")
            else:
                st.info("The query results don't contain numeric data suitable for visualization")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            import traceback
            st.text(f"Detailed error: {traceback.format_exc()}")