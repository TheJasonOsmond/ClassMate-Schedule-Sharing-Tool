import mysql.connector

def execute_query(query, params=None, fetch=False):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="3GUv878pnS@n",
        database="sql_schedule_database"
    )

    mycursor = db.cursor(buffered=True)
    result = None
    try:
        if params:
            mycursor.execute(query, params)
        else:
            mycursor.execute(query)
        db.commit()
        print("Query executed successfully.")
        if fetch:
            fetched_row = mycursor.fetchone()
            result = fetched_row[0] if fetched_row else None
    except mysql.connector.Error as e:
        print("Error executing query:", e)
    finally:
        mycursor.close()
        db.close()
    return result

# Create the tables
def create_tables():
    execute_query("CREATE TABLE Student (\
                    student_id int UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
                    f_name varchar (50) NOT NULL,\
                    l_name varchar(50) NOT NULL,\
                    email varchar(100) UNIQUE NOT NULL,\
                    date_of_birth char(10)\
                  )")
    execute_query("CREATE TABLE Admin   (\
                    admin_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
                    f_name VARCHAR(50),\
                    l_name VARCHAR(50))"
                  )
    execute_query("CREATE TABLE Course  (\
                    course_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
                    name VARCHAR(50))"
                  )
    execute_query("CREATE TABLE Login (\
                    username VARCHAR(50) PRIMARY KEY,\
                    password VARCHAR(50),\
                    student_id INT UNSIGNED NULL,\
                    admin_id INT UNSIGNED NULL,\
                    FOREIGN KEY (student_id) REFERENCES Student(student_id),\
                    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id))"
                )
    
def add_default_values():
    # Insert a row into the Student table
    execute_query("INSERT INTO Student(f_name, l_name, email) VALUES (%s, %s,%s)", ('Student', 'Student', 'Student.Student@Unversity.ca'))
    student_id = execute_query("SELECT student_id FROM Student WHERE l_name=%s AND email=%s" , ('Student', 'Student.Student@Unversity.ca'), fetch=True) #not the best solution 
    print("Student ID:", student_id)

    # Insert a row into the Admin table
    execute_query("INSERT INTO Admin(f_name, l_name) VALUES (%s, %s)", ('Admin', 'Admin'))
    admin_id = execute_query("SELECT admin_id FROM Admin WHERE f_name=%s AND l_name=%s", ('Admin', 'Admin'), fetch=True) #not the best solution 
    print("Admin ID:", admin_id)

    # Insert a row into the Login table with the student_id value
    execute_query("INSERT INTO Login(username, password, student_id) VALUES (%s, %s, %s)", ('student0', '1234', student_id))

    # Insert a row into the Login table with the admin_id value
    execute_query("INSERT INTO Login(username, password, admin_id) VALUES (%s, %s, %s)", ('admin0', '1234', admin_id))


# Creates a fresh database
def create_database():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="3GUv878pnS@n",
    )

    mycursor = db.cursor(buffered=True)
    mycursor.execute("DROP DATABASE IF EXISTS sql_schedule_database")
    mycursor.execute("CREATE DATABASE sql_schedule_database")





def main():
    create_database()
    create_tables()
    add_default_values()

    
main()