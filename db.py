import sqlite3
import streamlit as st
import pandas as pd

def save_to_sqlite(entries_out_range):
    # connect to db file
    conn = sqlite3.connect("data/test_data.db")
    # tool to send to db file
    cursor = conn.cursor()
    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS foia_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        foia TEXT,
        name TEXT,
        open TEXT,
        close TEXT,
        report TEXT
    )
    """)
    # Insert data
    try:
        for f in entries_out_range:
            cursor.execute("""
                SELECT 1 FROM foia_requests WHERE foia = ? AND name = ?
            """, (f["foia"], f["name"]))
            
            exists = cursor.fetchone()
        
            if not exists:
                cursor.execute("""
                    INSERT INTO foia_requests (foia, name, open, close, report)
                    VALUES (?, ?, ?, ?, ?)
                """, (f["foia"], f["name"], f["open"], f["close"], f["report"]))

        # Commit and close
        conn.commit()
        conn.close()
        return len(entries_out_range)

    except Exception as e:
        conn.rollback()  # undo changes if anything went wrong
        return 'failure'

def fetch_all_data():
    conn = sqlite3.connect("data/test_data.db")
    # tool to send to db file

    df = pd.read_sql_query("SELECT * FROM foia_requests", conn)
    conn.close()
    return df

   

