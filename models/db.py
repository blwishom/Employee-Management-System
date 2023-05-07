import sqlite3

# initialize database

def create_db():
    db = sqlite3.connect('ems.db')

    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            [id] INTEGER PRIMARY KEY,
            [name] TEXT,
            [employee_count] INTEGER,
            [department_domain] TEXT,
            [labor_cost] INTEGER
            )
            ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            [id] INTEGER PRIMARY KEY,
            [fname] VARCHAR(255) NOT NULL,
            [lname] VARCHAR(255) NOT NULL,
            [doe] VARCHAR(255) NOT NULL,
            [salary] INTEGER NOT NULL,
            [department] TEXT
            );
            ''')
    db.close()

# create a department

def insert_department(department):
    db = sqlite3.connect('ems.db')
    cursor = db.cursor()
    params = (department['name'], department['employee_count'], department['department_domain'], department['labor_cost'] )
    cursor.execute(f"INSERT INTO departments (name, employee_count, department_domain, labor_cost) VALUES(?, ?, ?, ?)", params)
    db.commit()

# view all departments

def view_departments():
    db = sqlite3.connect('ems.db')

    cursor = db.cursor()
    cursor.execute(
            '''
            SELECT * FROM departments
            '''

    )

    results = cursor.fetchall()
    print(results)
    db.close()
    return results

# create an employee

def insert_employee(employee):
    print(employee)
    db = sqlite3.connect('ems.db')
    cursor = db.cursor()
    params = (employee['fname'], employee['lname'], employee['doe'], employee['salary'], employee['department'] )
    cursor.execute(f"INSERT INTO employees (fname, lname, doe, salary, department) VALUES(?, ?, ?, ?, ?)", params)
    db.commit()
    db.close()

# view all employees

def view_employees():
    db = sqlite3.connect('ems.db')

    cursor = db.cursor()
    cursor.execute(
            '''
            SELECT * FROM employees
            '''
    )

    results = cursor.fetchall()
    print(results)
    db.close()
    return results

# view a single employee

def view_employee(lname):
    db = sqlite3.connect('ems.db')

    cursor = db.cursor()
    cursor.execute("SELECT * FROM employees WHERE lname = ?", [lname])

    results = cursor.fetchone()
    print(results)
    db.close()
    return results

# view a single department

def view_department(name):
    db = sqlite3.connect('ems.db')

    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM departments WHERE name = ?", [name])

    results = cursor.fetchone()
    print(results)
    db.close()
    return results

# update a department

def update_department(payload):
    db = sqlite3.connect('ems.db')
    cursor = db.cursor()

    name = payload['name']
    employee_count = payload['employee_count']
    department_domain = payload['department_domain']
    labor_cost = payload['labor_cost']

    id = payload['id']
    cursor.execute(f"UPDATE departments set name = ?, employee_count = ?, department_domain = ?, labor_cost = ? WHERE id = ?", (name, employee_count, department_domain, labor_cost, id))

    db.commit()
    db.close()

# update an employee

def update_employee(payload):
    db = sqlite3.connect('ems.db')
    cursor = db.cursor()

    fname = payload['fname']
    lname = payload['lname']
    doe = payload['doe']
    salary = payload['salary']
    department = payload['department']
    id = payload['id']

    cursor.execute(f"UPDATE employees set fname = ?, lname = ?, doe = ?, salary = ?, department = ? WHERE id = ?", (fname, lname, doe, salary, department, id))

    db.commit()
    db.close()

# delete an employee

def delete_employee(employee):
    db = sqlite3.connect('ems.db')
    cursor = db.cursor()

    id = employee['id']
    cursor.execute(f"DELETE from employees WHERE id = ?", id)
    print("successfully deleted")
    db.commit()
    db.close()

# delete a department

def delete_department(department):
    db = sqlite3.connect('ems.db')
    cursor = db.cursor()

    id = department['id']
    cursor.execute(f"DELETE from departments WHERE id = ?", id)
    print("successfully deleted")
    db.commit()
    db.close()
