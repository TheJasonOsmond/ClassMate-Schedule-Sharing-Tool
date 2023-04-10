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
                    f_name varchar (50),\
                    l_name varchar(50))"\
                  )
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
    execute_query("CREATE TABLE University (\
                    `name` VARCHAR(100) PRIMARY KEY,\
                    location VARCHAR(50) NOT NULL)"
                  )
    execute_query("CREATE TABLE Department (\
                    `name` VARCHAR(50) PRIMARY KEY,\
                    `university` VARCHAR(100) NOT NULL,\
                    FOREIGN KEY (`university`) REFERENCES University(`name`))"
                  )
    execute_query("CREATE TABLE Professor (\
                    professor_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
                    f_name VARCHAR(50) NOT NULL,\
                    l_name VARCHAR(50) NOT NULL,\
                    `department` VARCHAR(50) NOT NULL,\
                    `university` VARCHAR(100) NOT NULL,\
                    FOREIGN KEY (`department`) REFERENCES Department(`name`),\
                    FOREIGN KEY (`university`) REFERENCES University(`name`))"
                  )
    execute_query("CREATE TABLE Room (\
                    building_id INT UNSIGNED,\
                    room_id INT UNSIGNED,\
                    `university` VARCHAR(100) NOT NULL,\
                    PRIMARY KEY (building_id, room_id),\
                    FOREIGN KEY (`university`) REFERENCES University(`name`))"
                  )
    
def add_default_values():
    # Insert a row into the Student table
    execute_query("INSERT INTO Student(f_name, l_name) VALUES (%s, %s)", ('Student', 'Student'))
    execute_query("INSERT INTO Student(f_name, l_name) VALUES (%s, %s)", ('John', 'Doe'))
    student_id = execute_query("SELECT student_id FROM Student WHERE f_name=%s AND l_name=%s", ('Student', 'Student'), fetch=True)
    print("Student ID:", student_id)

    # Insert a row into the Admin table
    execute_query("INSERT INTO Admin(f_name, l_name) VALUES (%s, %s)", ('Admin', 'Admin'))
    admin_id = execute_query("SELECT admin_id FROM Admin WHERE f_name=%s AND l_name=%s", ('Admin', 'Admin'), fetch=True)
    print("Admin ID:", admin_id)

    # Insert a row into the Login table with the student_id value
    execute_query("INSERT INTO Login(username, password, student_id) VALUES (%s, %s, %s)", ('student0', '1234', student_id))

    # Insert a row into the Login table with the admin_id value
    execute_query("INSERT INTO Login(username, password, admin_id) VALUES (%s, %s, %s)", ('admin0', '1234', admin_id))

    # Insert rows into the Course table with the Course names
    courses = [('CPSC 200',),('CPSC 250',),('CPSC 255',),('CPSC 270',),('CPSC 290',),
            ('CPSC 300',),('CPSC 350',),('CPSC 355',),('CPSC 360',),('CPSC 400',)]

    for course in courses:
        execute_query(f"INSERT INTO Course (name) VALUES ('{course[0]}')")

    # Insert values into University table
    universities = [('University of XYZ', 'New York'), ('ABC University', 'California'), ('XYZ State University', 'Texas')]
    for university in universities:
        execute_query(f"INSERT INTO University (`name`, location) VALUES ('{university[0]}', '{university[1]}')")

    # Insert values into Department table, referencing universities by name
    departments = [('Computer Science', 'University of XYZ'), ('Business Administration', 'ABC University'), ('Mechanical Engineering', 'XYZ State University')]
    for department in departments:
        execute_query(f"INSERT INTO Department (`name`, `university`) SELECT '{department[0]}', u.`name` FROM University u WHERE u.`name` = '{department[1]}'")

    # Insert values into Professor table, referencing departments and universities by name
    professors = [('John', 'Doe', 'Computer Science', 'University of XYZ'), ('Jane', 'Smith', 'Business Administration', 'ABC University'), ('Bob', 'Johnson', 'Mechanical Engineering', 'XYZ State University')]
    for professor in professors:
        execute_query(f"INSERT INTO Professor (f_name, l_name, `department`, `university`) SELECT '{professor[0]}', '{professor[1]}', d.`name`, u.`name` FROM Department d, University u WHERE d.`name` = '{professor[2]}' AND d.`university` = u.`name` AND u.`name` = '{professor[3]}'")

    # Insert values into Room table, referencing universities by name
    rooms = [(1, 101, 'University of XYZ'), (2, 201, 'ABC University'), (3, 301, 'XYZ State University')]
    for room in rooms:
        execute_query(f"INSERT INTO Room (building_id, room_id, `university`) SELECT {room[0]}, {room[1]}, u.`name` FROM University u WHERE u.`name` = '{room[2]}'")



def create_database():
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="3GUv878pnS@n"
    )
    
    mycursor = db.cursor()

    mycursor.execute("DROP DATABASE IF EXISTS sql_schedule_database")
    mycursor.execute("CREATE DATABASE sql_schedule_database")









def main():
    create_database() #Replaces Database
    create_tables()
    add_default_values()

    
main()