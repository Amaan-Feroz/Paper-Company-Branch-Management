import tkinter as tk
from tkinter import ttk
import mysql.connector

# Create a Tkinter window for login
login_root = tk.Tk()
login_root.title("DUNDER MIFFLIN Login")

# Create variables to store the username and password
username_var = tk.StringVar()
password_var = tk.StringVar()

# Function to create a database connection and switch to the main window
def connect_to_database():
    username = username_var.get()
    password = password_var.get()

    try:
        # Create a MySQL database connection
        conn = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="Dunder_Mifflin"
        )
        cursor = conn.cursor()

        # Close the login window
        login_root.destroy()

        # Function to fetch and display data for a specific table
        def fetch_data(table_name):

            if table_name == "products":
                cursor.execute(f"SELECT * FROM Papers")
                data = cursor.fetchall()
                cursor.execute(f"SELECT * FROM Binders")
                data += cursor.fetchall()
            elif table_name == "sales":
                cursor.execute(f"SELECT * FROM Sales")
                data = cursor.fetchall()
            elif table_name == "branches":
                cursor.execute(f"SELECT * FROM Branch")
                data = cursor.fetchall()
            elif table_name == "employees":
                cursor.execute(f"SELECT * FROM Employees")
                data = cursor.fetchall()
            else:
                return

            column_names = [desc[0] for desc in cursor.description]

            # Create a new window for displaying data
            data_window = tk.Toplevel(main_root)
            data_window.title(f"DUNDER MIFFLIN {table_name.capitalize()} Data")

            if table_name == "branches":
                # Create a treeview widget to display branch data
                tree = ttk.Treeview(data_window, columns=column_names, show="headings")
                tree.pack()

                for col in column_names:
                    tree.heading(col, text=col)
                    tree.column(col, width=100)

                for row in data:
                    tree.insert("", "end", values=row)

                def view_office_details(event):
                    selected_item = tree.selection()[0]  # Get the selected branch
                    selected_branch_id = tree.item(selected_item, "values")[0]  # ID of the selected branch
                    selected_branch_address = tree.item(selected_item, "values")[1]  # Address of the selected branch

                    cursor.execute(f"SELECT * FROM Office WHERE address = %s", (selected_branch_address,))
                    office_data = cursor.fetchall()

                    # Print column names for debugging
                    print([desc[0] for desc in cursor.description])

                    office_window = tk.Toplevel(main_root)
                    office_window.title(f"Office Details for {selected_branch_address}")

                    office_tree = ttk.Treeview(office_window, columns=["address", "size", "office_id", "vacancy"], show="headings")
                    office_tree.pack()

                    office_tree.heading("address", text="Address")
                    office_tree.heading("size", text="Size")
                    office_tree.heading("office_id", text="Office ID")
                    office_tree.heading("vacancy", text="Vacancy")

                    for row in office_data:
                        office_tree.insert("", "end", values=row)


                        office_id = row[2]
                        print(office_id)
                        cursor.execute("SELECT * FROM Lease WHERE office_id = %s", (office_id,))
                        lease_data = cursor.fetchall()

                        lease_tree = ttk.Treeview(office_window, columns=["lease_id", "status", "start_date", "end_date"], show="headings")
                        lease_tree.pack()

                        lease_tree.heading("lease_id", text="Lease ID")
                        lease_tree.heading("status", text="Status")
                        lease_tree.heading("start_date", text="Start Date")
                        lease_tree.heading("end_date", text="End Date")

                        for lease_row in lease_data:
                            lease_tree.insert("", "end", values=lease_row)

                    manager_window = tk.Toplevel(main_root)
                    manager_window.title(f"Manager Details for {selected_branch_address}")

                    cursor.execute(f"SELECT * FROM Managers WHERE branch_id = %s", (selected_branch_id,))
                    manager_data = cursor.fetchall()

                    manager_tree = ttk.Treeview(manager_window, columns=["m_id", "branch_id" ,"year_joined", "name", "age"], show="headings")
                    manager_tree.pack()

                    manager_tree.heading("m_id", text="Manager ID")
                    manager_tree.heading("branch_id",text = "Branch")
                    manager_tree.heading("year_joined", text="Year Joined")
                    manager_tree.heading("name", text="Name")
                    manager_tree.heading("age", text="Age")

                    for manager_row in manager_data:
                        manager_tree.insert("", "end", values=manager_row)

                        manager_id = manager_row[0]
                        cursor.execute(f"SELECT * FROM Employees WHERE m_id = %s", (manager_id,))
                        employee_data = cursor.fetchall()

                        employee_tree = ttk.Treeview(manager_window, columns=["e_id", "m_id","year_joined", "name", "age", "dep_id"], show="headings")
                        employee_tree.pack()

                        employee_tree.heading("e_id", text="Employee ID")
                        employee_tree.heading("m_id",text = "Manager ID")
                        employee_tree.heading("year_joined", text="Year Joined")
                        employee_tree.heading("name", text="Name")
                        employee_tree.heading("age", text="Age")
                        employee_tree.heading("dep_id", text="Department ID")

                        for employee_row in employee_data:
                            employee_tree.insert("", "end", values=employee_row)

                        
                        cursor.execute(f"SELECT * FROM Department")
                        department_data = cursor.fetchall()

                        department_tree = ttk.Treeview(manager_window, columns=["dep_id", "emp_count", "head_of_department"], show="headings")
                        department_tree.pack()

                        department_tree.heading("dep_id", text="Department ID")
                        department_tree.heading("emp_count", text="Employee Count")
                        department_tree.heading("head_of_department", text="Head of Department")

                        for department_row in department_data:
                            department_tree.insert("", "end", values=department_row)

                tree.bind("<Double-1>", view_office_details)  # Double-click to view office details

            else:
                # Create a treeview widget to display data
                tree = ttk.Treeview(data_window, columns=column_names, show="headings")
                tree.pack()

                for col in column_names:
                    tree.heading(col, text=col)
                    tree.column(col, width=100)

                for row in data:
                    tree.insert("", "end", values=row)
            # Function to perform a nested query

# ... (rest of the code remains the same)




                # CRUD operations for the "Employees" table

                def add_employee():
                    # Create a new window for adding an employee
                    add_employee_window = tk.Toplevel(main_root)
                    add_employee_window.title("Add Employee")

                    # Create variables to store employee details
                    emp_id_var=tk.IntVar()
                    emp_mid_var=tk.IntVar()
                    emp_year_var = tk.IntVar()
                    emp_name_var = tk.StringVar()
                    emp_age_var = tk.IntVar()
                    emp_dep_id_var = tk.IntVar()

                    # Create labels and entry fields for employee details
                    emp_name_label = tk.Label(add_employee_window, text="ID:")
                    emp_name_label.pack()
                    emp_name_entry = tk.Entry(add_employee_window, textvariable=emp_id_var)
                    emp_name_entry.pack()

                    emp_name_label = tk.Label(add_employee_window, text="M_ID:")
                    emp_name_label.pack()
                    emp_name_entry = tk.Entry(add_employee_window, textvariable=emp_mid_var)
                    emp_name_entry.pack()

                    emp_name_label = tk.Label(add_employee_window, text="year_joined:")
                    emp_name_label.pack()
                    emp_name_entry = tk.Entry(add_employee_window, textvariable=emp_year_var)
                    emp_name_entry.pack()

                    emp_name_label = tk.Label(add_employee_window, text="Name:")
                    emp_name_label.pack()
                    emp_name_entry = tk.Entry(add_employee_window, textvariable=emp_name_var)
                    emp_name_entry.pack()

                    emp_age_label = tk.Label(add_employee_window, text="Age:")
                    emp_age_label.pack()
                    emp_age_entry = tk.Entry(add_employee_window, textvariable=emp_age_var)
                    emp_age_entry.pack()

                    emp_dep_id_label = tk.Label(add_employee_window, text="Department ID:")
                    emp_dep_id_label.pack()
                    emp_dep_id_entry = tk.Entry(add_employee_window, textvariable=emp_dep_id_var)
                    emp_dep_id_entry.pack()

                    # Function to add the employee to the database
                    def add_employee_to_database():
                        e_id = emp_id_var.get()
                        m_id = emp_mid_var.get()
                        year_joined = emp_year_var.get()
                        name = emp_name_var.get()
                        age = emp_age_var.get()
                        dep_id = emp_dep_id_var.get()

                        # Perform the database insertion
                        cursor.callproc('InsertEmployee', (e_id, m_id, year_joined, name, age, dep_id))
                        conn.commit()

                        # Close the window after adding the employee
                        add_employee_window.destroy()

                    # Create a button to add the employee
                    add_button = tk.Button(add_employee_window, text="Add Employee", command=add_employee_to_database)
                    add_button.pack()

                def update_employee():
                    # Create a new window for updating an employee
                    update_employee_window = tk.Toplevel(main_root)
                    update_employee_window.title("Update Employee")

                    # Create variables to store employee details
                    emp_id_var = tk.IntVar()
                    emp_name_var = tk.StringVar()
                    emp_age_var = tk.IntVar()
                    emp_dep_id_var = tk.IntVar()

                    # Create labels and entry fields for employee details
                    emp_id_label = tk.Label(update_employee_window, text="Employee ID:")
                    emp_id_label.pack()
                    emp_id_entry = tk.Entry(update_employee_window, textvariable=emp_id_var)
                    emp_id_entry.pack()

                    emp_name_label = tk.Label(update_employee_window, text="Name:")
                    emp_name_label.pack()
                    emp_name_entry = tk.Entry(update_employee_window, textvariable=emp_name_var)
                    emp_name_entry.pack()

                    emp_age_label = tk.Label(update_employee_window, text="Age:")
                    emp_age_label.pack()
                    emp_age_entry = tk.Entry(update_employee_window, textvariable=emp_age_var)
                    emp_age_entry.pack()

                    emp_dep_id_label = tk.Label(update_employee_window, text="Department ID:")
                    emp_dep_id_label.pack()
                    emp_dep_id_entry = tk.Entry(update_employee_window, textvariable=emp_dep_id_var)
                    emp_dep_id_entry.pack()

                    # Function to update the employee in the database
                    def update_employee_in_database():
                        emp_id = emp_id_var.get()
                        name = emp_name_var.get()
                        age = emp_age_var.get()
                        dep_id = emp_dep_id_var.get()

                        # Perform the database update
                        cursor.execute("UPDATE Employees SET name=%s, age=%s, dep_id=%s WHERE e_id=%s", (name, age, dep_id, emp_id))
                        conn.commit()

                        # Close the window after updating the employee
                        update_employee_window.destroy()

                    # Create a button to update the employee
                    update_button = tk.Button(update_employee_window, text="Update Employee", command=update_employee_in_database)
                    update_button.pack()

                def delete_employee():
                    # Create a new window for deleting an employee
                    delete_employee_window = tk.Toplevel(main_root)
                    delete_employee_window.title("Delete Employee")

                    # Create a variable to store the employee ID to be deleted
                    emp_id_var = tk.IntVar()

                    # Create labels and entry fields for employee details
                    emp_id_label = tk.Label(delete_employee_window, text="Employee ID:")
                    emp_id_label.pack()
                    emp_id_entry = tk.Entry(delete_employee_window, textvariable=emp_id_var)
                    emp_id_entry.pack()

                    # Function to delete the employee from the database
                    def delete_employee_from_database():
                        emp_id = emp_id_var.get()

                        # Perform the database deletion
                        cursor.execute("DELETE FROM Employees WHERE e_id=%s", (emp_id,))
                        conn.commit()

                        # Close the window after deleting the employee
                        delete_employee_window.destroy()

                    # Create a button to delete the employee
                    delete_button = tk.Button(delete_employee_window, text="Delete Employee", command=delete_employee_from_database)
                    delete_button.pack()




                # Add buttons for CRUD operations
                if username == 'steve':
                    add_employee_button = tk.Button(data_window, text="Add Employee", command=add_employee)
                    add_employee_button.pack()

                    update_employee_button = tk.Button(data_window, text="Update Employee", command=update_employee)
                    update_employee_button.pack()

                    delete_employee_button = tk.Button(data_window, text="Delete Employee", command=delete_employee)
                    delete_employee_button.pack()
        
        def nested_query():
            cursor.execute("""
                SELECT branch_id, (SELECT COUNT(*) FROM Employees WHERE branch_id = Branch.branch_id) as employee_count
                FROM Branch
            """)
            data = cursor.fetchall()
            display_query_results("Nested Query Results", data)

        # Function to perform an aggregate query
        def aggregate_query():
            cursor.execute("""
                SELECT dep_id, AVG(age) as average_age
                FROM Employees
                GROUP BY dep_id
            """)
            data = cursor.fetchall()
            display_query_results("Aggregate Query Results", data)

        # Function to perform a join query
        def join_query():
            cursor.execute("""
                SELECT Employees.name, Department.head_of_department
                FROM Employees
                INNER JOIN Department ON Employees.dep_id = Department.dep_id
            """)
            data = cursor.fetchall()
            display_query_results("Join Query Results", data)

        # Function to display query results in a new window
        def display_query_results(title, data):
            query_window = tk.Toplevel(main_root)
            query_window.title(title)

            tree = ttk.Treeview(query_window, columns=[desc[0] for desc in cursor.description], show="headings")
            tree.pack()

            for col in cursor.description:
                tree.heading(col[0], text=col[0])
                tree.column(col[0], width=100)

            for row in data:
                tree.insert("", "end", values=row)


        # Create a Tkinter window for the main application
        main_root = tk.Tk()
        main_root.title("DUNDER MIFFLIN")

        # Create buttons to view data from different tables
        view_employees_button = tk.Button(main_root, text="View Employees", command=lambda: fetch_data("employees"))
        view_sales_button = tk.Button(main_root, text="View Sales", command=lambda: fetch_data("sales"))
        view_products_button = tk.Button(main_root, text="View Products", command=lambda: fetch_data("products"))
        # view_departments_button = tk.Button(main_root, text="View Departments", command=lambda: fetch_data("departments"))
        view_branches_button = tk.Button(main_root, text="View Branches", command=lambda: fetch_data("branches"))

                # Create buttons for additional queries
        nested_query_button = tk.Button(main_root, text="Nested Query", command=nested_query)
        aggregate_query_button = tk.Button(main_root, text="Aggregate Query", command=aggregate_query)
        join_query_button = tk.Button(main_root, text="Join Query", command=join_query)

        # Place buttons in the main window
        view_employees_button.pack()
        view_sales_button.pack()
        view_products_button.pack()
        # view_departments_button.pack()
        view_branches_button.pack()
        nested_query_button.pack()
        aggregate_query_button.pack()
        join_query_button.pack()

        # Create a label for the main screen heading
        heading_label = tk.Label(main_root, text="DUNDER MIFFLIN", font=("Arial", 20))
        heading_label.pack()

        # Start the main application
        main_root.mainloop()

        # Close the database connection when the main window is closed
        conn.close()

    except mysql.connector.Error as err:
        error_label.config(text=f"Error: {err}")

# Create labels and entry fields for the login screen
username_label = tk.Label(login_root, text="Username:")
username_label.pack()
username_entry = tk.Entry(login_root, textvariable=username_var)
username_entry.pack()

password_label = tk.Label(login_root, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_root, textvariable=password_var, show="*")
password_entry.pack()

# Create a button to log in and connect to the database
login_button = tk.Button(login_root, text="Log In", command=connect_to_database)
login_button.pack()

# Create a label to display login errors
error_label = tk.Label(login_root, text="", fg="red")
error_label.pack()

# Start the login window
login_root.mainloop()
