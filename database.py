import sqlite3

def create_sample_database():
    """Create a sample student database"""
    conn = sqlite3.connect('sample_data.db')
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        grade TEXT,
        marks INTEGER
    )
    ''')
    
    # Insert sample data
    sample_students = [
        (1, 'John Doe', 20, 'A', 85),
        (2, 'Jane Smith', 21, 'B', 78),
        (3, 'Mike Johnson', 19, 'A', 92),
        (4, 'Sarah Williams', 22, 'C', 65),
        (5, 'Tom Brown', 20, 'B', 81),
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO students VALUES (?,?,?,?,?)', 
                       sample_students)
    
    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

if __name__ == "__main__":
    create_sample_database()