import sqlite3

def create_enterprise_database():
    """Create a realistic company database for practice"""
    conn = sqlite3.connect('company_data.db')
    cursor = conn.cursor()
    
    print("Creating tables...")
    
    # 1. Employees Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT,
        position TEXT,
        salary INTEGER,
        hire_date TEXT,
        manager_id INTEGER
    )
    ''')
    
    # 2. Departments Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT NOT NULL,
        location TEXT,
        budget INTEGER
    )
    ''')
    
    # 3. Sales Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        product_name TEXT,
        amount INTEGER,
        sale_date TEXT,
        region TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
    )
    ''')
    
    # 4. Products Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT,
        price INTEGER,
        stock INTEGER
    )
    ''')
    
    print("Inserting sample data...")
    
    # Insert Sample Data - Employees
    employees_data = [
        (1, 'Rajesh Kumar', 'Sales', 'Manager', 75000, '2020-01-15', None),
        (2, 'Priya Sharma', 'Sales', 'Executive', 45000, '2021-03-10', 1),
        (3, 'Amit Singh', 'IT', 'Developer', 60000, '2019-06-20', None),
        (4, 'Sneha Verma', 'IT', 'Developer', 58000, '2021-08-15', 3),
        (5, 'Vikram Patel', 'HR', 'Manager', 70000, '2018-11-05', None),
        (6, 'Anjali Gupta', 'Sales', 'Executive', 42000, '2022-01-20', 1),
        (7, 'Rahul Mehta', 'IT', 'Senior Developer', 80000, '2017-04-10', 3),
        (8, 'Neha Kapoor', 'HR', 'Executive', 38000, '2022-05-15', 5),
        (9, 'Arjun Reddy', 'Sales', 'Executive', 44000, '2023-02-10', 1),
        (10, 'Divya Nair', 'Marketing', 'Manager', 72000, '2019-09-25', None),
    ]
    
    # Insert Departments
    departments_data = [
        (1, 'Sales', 'Mumbai', 5000000),
        (2, 'IT', 'Bangalore', 8000000),
        (3, 'HR', 'Delhi', 2000000),
        (4, 'Marketing', 'Pune', 3000000),
    ]
    
    # Insert Sales (more data for better analysis)
    sales_data = [
        (1, 2, 'Laptop', 50000, '2024-01-15', 'North'),
        (2, 2, 'Mobile', 25000, '2024-01-20', 'North'),
        (3, 6, 'Tablet', 30000, '2024-02-10', 'South'),
        (4, 2, 'Laptop', 52000, '2024-02-15', 'North'),
        (5, 6, 'Mobile', 28000, '2024-03-05', 'South'),
        (6, 2, 'Desktop', 65000, '2024-03-20', 'North'),
        (7, 6, 'Laptop', 48000, '2024-04-10', 'South'),
        (8, 2, 'Mobile', 26000, '2024-04-25', 'North'),
        (9, 9, 'Laptop', 51000, '2024-05-12', 'West'),
        (10, 6, 'Desktop', 67000, '2024-05-20', 'South'),
        (11, 2, 'Tablet', 31000, '2024-06-08', 'North'),
        (12, 9, 'Mobile', 27000, '2024-06-15', 'West'),
    ]
    
    # Insert Products
    products_data = [
        (1, 'Laptop', 'Electronics', 50000, 25),
        (2, 'Mobile', 'Electronics', 25000, 50),
        (3, 'Tablet', 'Electronics', 30000, 30),
        (4, 'Desktop', 'Electronics', 65000, 15),
        (5, 'Headphones', 'Accessories', 2000, 100),
        (6, 'Mouse', 'Accessories', 500, 200),
        (7, 'Keyboard', 'Accessories', 1500, 150),
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO employees VALUES (?,?,?,?,?,?,?)', employees_data)
    cursor.executemany('INSERT OR REPLACE INTO departments VALUES (?,?,?,?)', departments_data)
    cursor.executemany('INSERT OR REPLACE INTO sales VALUES (?,?,?,?,?,?)', sales_data)
    cursor.executemany('INSERT OR REPLACE INTO products VALUES (?,?,?,?,?)', products_data)
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*50)
    print("✅ Enterprise database created successfully!")
    print("="*50)
    print("\n📊 Tables created:")
    print("   1. employees (10 records)")
    print("   2. departments (4 records)")
    print("   3. sales (12 records)")
    print("   4. products (7 records)")
    print("\n💾 Database file: company_data.db")
    print("\n🎯 Ready to use with your chatbot!")

if __name__ == "__main__":
    create_enterprise_database()