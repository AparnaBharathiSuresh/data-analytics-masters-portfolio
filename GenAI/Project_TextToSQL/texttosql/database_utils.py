"""
Database utilities for the Text-to-SQL application.
"""
import os
import sqlite3
import time
import pandas as pd
import streamlit as st
import json

def list_sqlite_files(directory='.'):
    """List all SQLite database files in a directory"""
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # Find all .db files
    sqlite_files = [f for f in os.listdir(directory) if f.endswith('.db')]
    
    # If no databases found, create a sample one
    if not sqlite_files:
        create_sample_database(os.path.join(directory, 'sample.db'))
        sqlite_files = ['sample.db']
    
    return sqlite_files

def connect_to_database(db_path):
    """Connect to SQLite database"""
    try:
        # Create the database file if it doesn't exist
        conn = sqlite3.connect(db_path, check_same_thread=False)
        return conn
    except Exception as e:
        st.error(f"Error connecting to SQLite database: {e}")
        return None

def get_db_schema(conn):
    """Extract schema from SQLite database for prompting"""
    schema_info = []
    try:
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [table[0] for table in cursor.fetchall()]
        
        # Get columns for each table
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            # Format: (id, name, type, notnull, default_value, pk)
            col_info = [f"{col[1]} ({col[2]})" for col in columns]
            schema_info.append(f"Table: {table}")
            schema_info.append(f"Columns: {', '.join(col_info)}")
            
            # Get foreign keys
            cursor.execute(f"PRAGMA foreign_key_list({table});")
            foreign_keys = cursor.fetchall()
            if foreign_keys:
                fk_info = []
                for fk in foreign_keys:
                    # Format: (id, seq, table, from, to, on_update, on_delete, match)
                    fk_info.append(f"{fk[3]} -> {fk[2]}.{fk[4]}")
                schema_info.append(f"Foreign Keys: {', '.join(fk_info)}")
        
        return "\n".join(schema_info)
    except Exception as e:
        st.error(f"Error getting schema: {e}")
        return "Error retrieving schema"

def execute_query(conn, query):
    """Execute SQL query on database"""
    try:
        if conn is None:
            return None, 0, "Database not connected"
            
        cursor = conn.cursor()
        start_time = time.time()
        cursor.execute(query)
        
        # Check if query returns data
        if cursor.description:
            # Fetch column names
            column_names = [col[0] for col in cursor.description]
            # Fetch all rows
            rows = cursor.fetchall()
            execution_time = time.time() - start_time
            
            # Convert rows to a list to ensure thread safety
            row_list = [list(row) for row in rows]
            return pd.DataFrame(row_list, columns=column_names), execution_time, None
        else:
            # For non-SELECT queries
            conn.commit()
            affected_rows = cursor.rowcount
            execution_time = time.time() - start_time
            
            return pd.DataFrame([{"Affected Rows": affected_rows}]), execution_time, None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None, 0, str(e)

def create_sample_database(db_path):
    """Create a sample database with demo tables and data"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create sample tables
        cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            city TEXT,
            state TEXT,
            join_date DATE
        );
        ''')
        
        cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            in_stock INTEGER
        );
        ''')
        
        cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            total_amount REAL,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        );
        ''')
        
        cursor.execute('''
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        );
        ''')
        
        # Insert sample data
        cursor.executemany(
            "INSERT INTO customers (name, email, city, state, join_date) VALUES (?, ?, ?, ?, ?)",
            [
                ("John Smith", "john@example.com", "New York", "NY", "2022-01-15"),
                ("Emily Johnson", "emily@example.com", "Los Angeles", "CA", "2022-02-20"),
                ("Michael Brown", "michael@example.com", "Chicago", "IL", "2022-03-10"),
                ("Emma Wilson", "emma@example.com", "Houston", "TX", "2022-04-05"),
                ("James Taylor", "james@example.com", "Phoenix", "AZ", "2022-05-12"),
                ("Olivia Martinez", "olivia@example.com", "Philadelphia", "PA", "2022-06-25"),
                ("William Davis", "william@example.com", "San Antonio", "TX", "2022-07-08"),
                ("Sophia Anderson", "sophia@example.com", "San Diego", "CA", "2022-08-15"),
                ("Benjamin Thomas", "benjamin@example.com", "Dallas", "TX", "2022-09-20"),
                ("Isabella Jackson", "isabella@example.com", "San Jose", "CA", "2022-10-30")
            ]
        )
        
        cursor.executemany(
            "INSERT INTO products (name, category, price, in_stock) VALUES (?, ?, ?, ?)",
            [
                ("Laptop Pro", "Electronics", 1200.00, 25),
                ("Smartphone X", "Electronics", 800.00, 30),
                ("Coffee Maker", "Home Appliances", 80.00, 15),
                ("Running Shoes", "Footwear", 120.00, 40),
                ("Bluetooth Headphones", "Electronics", 150.00, 35),
                ("Backpack", "Accessories", 45.00, 50),
                ("Water Bottle", "Accessories", 20.00, 100),
                ("Desk Lamp", "Home Decor", 35.00, 20),
                ("Yoga Mat", "Fitness", 25.00, 30),
                ("Blender", "Home Appliances", 70.00, 10)
            ]
        )
        
        cursor.executemany(
            "INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)",
            [
                (1, "2023-01-05", 1250.00, "Delivered"),
                (2, "2023-01-10", 800.00, "Delivered"),
                (3, "2023-02-15", 235.00, "Delivered"),
                (4, "2023-03-20", 120.00, "Delivered"),
                (5, "2023-04-10", 150.00, "Delivered"),
                (1, "2023-05-05", 90.00, "Delivered"),
                (2, "2023-06-15", 45.00, "Delivered"),
                (6, "2023-07-20", 155.00, "Processing"),
                (7, "2023-08-25", 200.00, "Shipped"),
                (8, "2023-09-30", 70.00, "Processing")
            ]
        )
        
        cursor.executemany(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            [
                (1, 1, 1, 1200.00),
                (1, 7, 2, 25.00),
                (2, 2, 1, 800.00),
                (3, 3, 1, 80.00),
                (3, 5, 1, 150.00),
                (3, 9, 1, 25.00),
                (4, 4, 1, 120.00),
                (5, 5, 1, 150.00),
                (6, 6, 2, 45.00),
                (7, 7, 3, 15.00),
                (8, 8, 1, 35.00),
                (8, 9, 2, 25.00),
                (8, 7, 3, 15.00),
                (9, 10, 1, 70.00),
                (9, 6, 1, 45.00),
                (9, 7, 5, 17.00),
                (10, 10, 1, 70.00)
            ]
        )
        
        conn.commit()
        conn.close()
        
        st.success(f"Created sample database at {db_path}")
        return True
    except Exception as e:
        st.error(f"Error creating sample database: {e}")
        return False

def create_spider_databases(tables_json_path, output_dir='spider_databases'):
    """Create SQLite databases for only selected SPIDER db_ids."""
    try:
        with open(tables_json_path, 'r') as f:
            table_defs = json.load(f)

        os.makedirs(output_dir, exist_ok=True)

        # Only include these 5 databases
        target_dbs = {"Addresses", "bbc", "cinema","course_teach", "flight", "pets"}

        for db_schema in table_defs:
            db_id = db_schema['db_id']
            if db_id not in target_dbs:
                continue  # Skip everything except the 5 listed

            db_path = os.path.join(output_dir, f"{db_id}.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            tables = db_schema['table_names_original']
            col_info = db_schema['column_names_original']
            col_types = db_schema['column_types']
            pk_indices = set(db_schema['primary_keys'])
            fk_pairs = db_schema.get('foreign_keys', [])

            # Organize columns by table index
            table_columns = {t: [] for t in range(len(tables))}
            for idx, (table_idx, col_name) in enumerate(col_info):
                if table_idx == -1:
                    continue  # skip "*"
                col_type = col_types[idx]
                is_pk = idx in pk_indices
                table_columns[table_idx].append((col_name, col_type, is_pk, idx))

            # Create tables
            for t_idx, t_name in enumerate(tables):
                cols_sql = []
                for name, col_type, is_pk, idx in table_columns[t_idx]:
                    col_def = f'"{name}" {col_type.upper()}'
                    if is_pk:
                        col_def += " PRIMARY KEY"
                    cols_sql.append(col_def)
                table_sql = f'CREATE TABLE "{t_name}" ({", ".join(cols_sql)});'
                cursor.execute(table_sql)

            # Add foreign keys
            for src_idx, tgt_idx in fk_pairs:
                src_table_idx, src_col_name = col_info[src_idx]
                tgt_table_idx, tgt_col_name = col_info[tgt_idx]
                src_table = tables[src_table_idx]
                tgt_table = tables[tgt_table_idx]
                fk_sql = f'''
                ALTER TABLE "{src_table}"
                ADD FOREIGN KEY ("{src_col_name}") REFERENCES "{tgt_table}"("{tgt_col_name}");
                '''
                try:
                    cursor.execute(fk_sql)
                except Exception as e:
                    print(f"Skipping FK for {src_table}.{src_col_name} → {tgt_table}.{tgt_col_name}: {e}")

            conn.commit()
            conn.close()
            print(f"Created {db_id}.db")

        st.success(f"Created selected SPIDER databases in {output_dir}")
        return True
    except Exception as e:
        st.error(f"Error creating SPIDER databases: {e}")
        return False