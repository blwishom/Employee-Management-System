from department import Department
from db import create_db, view_departments, view_department, insert_department, update_department, delete_department, view_employees, delete_employee, update_employee, view_employee
import datetime
import sqlite3

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


def print_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. View All Departments")
    print("2. View Department")
    print("3. Add Department")
    print("4. Update Department")
    print("5. Delete Department")
    print("6. Hire Employee")
    print("7. View All Employees")
    print("8. Delete Employee")
    print("9. Update Employee")
    print("10. View an Employee")
    print("11. Filter Employees/Departments")
    print("12. Quit")
    print(67 * "-")

create_db()

loop = True
while loop:
    print_menu()
    choice = input("Enter your choice [0-12]: ")

    if choice == '1':
        view_departments()
    elif choice == '2':
        name = input("Enter the name of the department: ")
        view_department(name)
    elif choice == '3':
        name = input("Enter the name of the department: ")
        # employee_count = input("Enter the number of employees in the department: ")
        employee_count = 0
        department_domain = f"@{name}.io"
        # labor_cost = input("Enter the labor cost: ")
        labor_cost = 0
        department = Department(name, employee_count, department_domain, labor_cost)
        insert_department(department.to_dict())
        print("Department added successfully.")
    elif choice == '4':
        id = input("Enter the ID of the department to update: ")
        print('Department\'s Attributes:',cursor.execute("SELECT * FROM departments WHERE id = ?", (id)).fetchone())
        name = input("Enter the new name of the department: ")
        employee_count = input("Enter the new number of employees in the department: ")
        department_domain = input("Enter the new department domain: ")
        labor_cost = input("Enter the new labor cost: ")
        payload = {'id': id, 'name': name, 'employee_count': employee_count, 'department_domain': department_domain, 'labor_cost': labor_cost}
        update_department(payload)
        print("Department updated successfully.")
    elif choice == '5':
        id = input("Enter the ID of the department to delete: ")
        payload = {'id': id}
        delete_department(payload)
        print("Department deleted successfully.")
    elif choice == '6':
        department_name = input("Enter the name of the department to hire an employee: ")
        department = view_department(department_name)
        if department:
            department = Department(department[1], department[2], department[3], department[4])
            department.hire_employee()
        else:
            print(f"No department found with name {department_name}")
    elif choice == '7':
        view_employees()
    elif choice == '8':
        # id = input("Enter the ID of the employee to delete: ")
        temp_name = input("Enter the Last Name of the employee to delete: ")
        temp_empl = view_employee(temp_name)
        # print(type(temp_empl))
        temp_sal = temp_empl[4]
        # print(temp_sal)

        temp_empl_dict = (("id",str(temp_empl[0])),('fname',temp_empl[1]),('lname',temp_empl[2]),('doe',temp_empl[3]),('salary',temp_empl[4]),('department',temp_empl[5]))
        temp_empl_dict = dict(temp_empl_dict)
        # print(temp_empl_dict)
        temp_dept = view_department(temp_empl[5])
        temp_dept_dict = (('id',temp_dept[0]),('name',temp_dept[1]),('employee_count',temp_dept[2]-1),('department_domain',temp_dept[3]),('labor_cost',temp_dept[4]))
        temp_dept_dict = dict(temp_dept_dict)
        temp_dept_dict["labor_cost"] = temp_dept_dict['labor_cost'] - temp_sal
        update_department(temp_dept_dict)

        # payload = {'id': id}
        delete_employee(temp_empl_dict)
        print("Employee deleted successfully.")
    elif choice == '9':
        id = input("Enter the ID of the employee to update: ")
        print('Employee\'s Attributes:',cursor.execute("SELECT * FROM employees WHERE id = ?", (id)).fetchone())
        fname = input("Enter the new first name of the employee: ")
        lname = input("Enter the new last name of the employee: ")
        doe = datetime.date.today()
        salary = input("Enter the new salary of the employee: ")
        department = input("Enter the new department of the employee: ")
        payload = {'id': id, 'fname': fname, 'lname': lname, 'doe': doe, 'salary': salary, 'department' : department}
        update_employee(payload)
        print("Employee updated successfully.")
    elif choice == '10':
        lname = input("Enter the last name of the Employee: ")
        view_employee(lname.capitalize())
    elif choice == '11':
        print(' ')
        print('Would you like to filter Employees or Departments? \n 1. Employees \n 2. Department')
        print(' ')
        filterChoice = input('Enter number you\'d like to filter: ')
        if filterChoice == '1':
            print(' ')
            lastname = input('Enter the first letter of the last name you\'d like to filter: ')

            # TRIED USING "LIKE [A-Z]%" BUT NAMES WOULDN'T DISPLAY INSTEAD RETURNED AN EMPTY LIST******************
            letter = [lastname + '%']
            filteredNames = cursor.execute("SELECT * FROM employees WHERE lname LIKE ?", (letter)).fetchall()
            for name in filteredNames:
                print(name)
        elif filterChoice == '2':
            deptNames = input('Enter the first letter of the departments you\d like to filter: ')

            # TRIED USING "LIKE [A-Z]%" BUT NAMES WOULDN'T DISPLAY INSTEAD RETURNED AN EMPTY LIST******************
            letter = [deptNames + '%']
            filteredDepts = cursor.execute("SELECT * FROM departments WHERE name LIKE ?", (letter)).fetchall()
            for name in filteredDepts:
                print(name)
    elif choice == '12':
        loop = False
    else:

        print("Invalid choice. Please enter a number from 1 to 8.")

db.close()

# print_menu()
