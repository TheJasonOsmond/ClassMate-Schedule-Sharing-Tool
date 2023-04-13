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
                    student_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
                    f_name varchar (50),\
                    l_name varchar(50))"\
                    )
    execute_query("CREATE TABLE Admin   (\
                    admin_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
                    f_name VARCHAR(50),\
                    l_name VARCHAR(50))"
                    )
    execute_query("CREATE TABLE Login (\
                    username VARCHAR(50) PRIMARY KEY,\
                    password VARCHAR(50),\
                    student_id INT UNSIGNED NULL,\
                    admin_id INT UNSIGNED NULL,\
                    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,\
                    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id) ON DELETE CASCADE)"
                    )
    execute_query("CREATE TABLE University (\
                    `name` VARCHAR(100) PRIMARY KEY,\
                    location VARCHAR(50) NOT NULL)"
                    )
    execute_query("CREATE TABLE Department (\
                    `name` VARCHAR(50),\
                    `university` VARCHAR(100),\
                    PRIMARY KEY (`name`, `university`),\
                    FOREIGN KEY (`university`) REFERENCES University(`name`) ON DELETE CASCADE)"
                    )
    execute_query("CREATE TABLE Professor (\
                    professor_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
                    f_name VARCHAR(50) NOT NULL,\
                    l_name VARCHAR(50) NOT NULL,\
                    `department` VARCHAR(50) NOT NULL,\
                    `university` VARCHAR(100) NOT NULL,\
                    FOREIGN KEY (`department`, `university`) REFERENCES Department(`name`, `university`) ON DELETE CASCADE)"
                    )
    execute_query("CREATE TABLE Room (\
                    building_id INT UNSIGNED,\
                    room_id INT UNSIGNED,\
                    `university` VARCHAR(100),\
                    PRIMARY KEY (building_id, room_id, `university`),\
                    FOREIGN KEY (`university`) REFERENCES University(`name`) ON DELETE CASCADE)"
                    )
    #Days conversions: MWF = 21, TT = 10, MW = 20, WF = 5
    execute_query("CREATE TABLE Courses (\
                    course_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
                    name VARCHAR(50) NOT NULL,\
                    university VARCHAR(100) NOT NULL,\
                    department VARCHAR(50) NOT NULL,\
                    building_id INT UNSIGNED NULL,\
                    room_id INT UNSIGNED NULL,\
                    time VARCHAR(50) NULL,\
                    info VARCHAR(255) NULL,\
                    days INT UNSIGNED NULL,\
                    professor_id INT UNSIGNED NULL,\
                    FOREIGN KEY (`department`, `university`) REFERENCES Department(`name`, `university`) ON DELETE CASCADE,\
                    FOREIGN KEY (professor_id) REFERENCES Professor(professor_id) ON DELETE SET NULL,\
                    FOREIGN KEY (building_id, room_id) REFERENCES Room(building_id, room_id) ON DELETE SET NULL)"
                    )
    execute_query("CREATE TABLE CourseList (\
                    student_id INT UNSIGNED ,\
                    course_id INT UNSIGNED,\
                    PRIMARY KEY (student_id, course_id),\
                    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,\
                    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE)"
                    )
    execute_query("CREATE TABLE Friends (\
                    student_id INT UNSIGNED ,\
                    friend_id INT UNSIGNED,\
                    PRIMARY KEY (student_id, friend_id),\
                    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,\
                    FOREIGN KEY (friend_id) REFERENCES Student(student_id) ON DELETE CASCADE)"
                    )
            
def add_default_values():
    # Insert a row into the Student table
    execute_query("INSERT INTO Student(f_name, l_name) VALUES (%s, %s)", ('Jane', 'Doe')) # student_id = 1
    execute_query("INSERT INTO Student(f_name, l_name) VALUES (%s, %s)", ('John', 'Smith')) # student_id = 2

    # Insert a row into the Friends table
    execute_query("INSERT INTO Friends(student_id, friend_id) VALUES (%s, %s)", (1, 2))

    # Insert a row into the Login table with the student_id value
    execute_query("INSERT INTO Login(username, password, student_id) VALUES (%s, %s, %s)", ('student1', '1234', 1))
    execute_query("INSERT INTO Login(username, password, student_id) VALUES (%s, %s, %s)", ('student2', '1234', 2))

    # Insert a row into the Admin table
    execute_query("INSERT INTO Admin(f_name, l_name) VALUES (%s, %s)", ('Admin', 'Admin')) # admin_id = 1

    # Insert a row into the Login table with the admin_id value
    execute_query("INSERT INTO Login(username, password, admin_id) VALUES (%s, %s, %s)", ('admin0', '1234', 1))

    # Insert values into University table
    universities = [('University of Calgary', 'Canada'), 
                    ('University of British Columbia', 'Canada'), 
                    ('University of Toronto', 'Canada')]
    for university in universities:
        execute_query(f"INSERT INTO University (`name`, location) VALUES ('{university[0]}', '{university[1]}')")

    # Insert values into Department table, referencing universities by name
    departments = [ ('Computer Science', 'University of Calgary'),
                    ('Computer Science', 'University of British Columbia'),
                    ('Computer Science', 'University of Toronto'),
                    ('Business Administration', 'University of British Columbia'),
                    ('Mechanical Engineering', 'University of Toronto')]
    for department in departments:
        execute_query(f"INSERT INTO Department (`name`, `university`) SELECT '{department[0]}', u.`name` FROM University u WHERE u.`name` = '{department[1]}'")

    # Insert values into Professor table, referencing departments and universities by name
    professors = [  ('Cal', 'Gary', 'Computer Science', 'University of Calgary'),
                    ('Brit', 'Columbia', 'Business Administration', 'University of British Columbia'), 
                    ('To', 'Ronto', 'Computer Science', 'University of British Columbia')]
    for professor in professors:
        execute_query(f"INSERT INTO Professor (f_name, l_name, `department`, `university`) SELECT '{professor[0]}', '{professor[1]}', d.`name`, u.`name` FROM Department d, University u WHERE d.`name` = '{professor[2]}' AND d.`university` = u.`name` AND u.`name` = '{professor[3]}'")

    # Insert values into Room table, referencing universities by name
    rooms = [(1, 101, 'University of Calgary'), (2, 201, 'University of British Columbia'), (3, 301, 'University of Toronto')]
    for room in rooms:
        execute_query(f"INSERT INTO Room (building_id, room_id, `university`) SELECT {room[0]}, {room[1]}, u.`name` FROM University u WHERE u.`name` = '{room[2]}'")

    # Insert rows into the Courses table with the Course names and other required data 
    courses = [('CPSC 200', 'University of Calgary', 'Computer Science', 1, 101, '10:00-11:30', 'Intro to Computer Science', 21, 1),
            ('CPSC 250', 'University of Calgary', 'Computer Science', 1, 101, '12:00-13:30', 'Data Structures', 21, 1),
            ('CPSC 255', 'University of British Columbia', 'Computer Science', 2, 201, '14:00-15:30', 'Algorithms', 10, 2),
            ('CPSC 270', 'University of British Columbia', 'Computer Science', 2, 201, '16:00-17:30', 'Software Engineering', 10, 2),
            ('CPSC 290', 'University of Toronto', 'Computer Science', 3, 301, '10:00-11:30', 'Operating Systems', 20, 3),
            ('CPSC 300', 'University of Toronto', 'Computer Science', 3, 301, '12:00-13:30', 'Computer Networks', 20, 3),
            ('CPSC 350', 'University of Calgary', 'Computer Science', 1, 101, '14:00-15:30', 'Artificial Intelligence', 21, 1),
            ('CPSC 355', 'University of British Columbia', 'Computer Science', 2, 201, '16:00-17:30', 'Machine Learning', 5, 2),
            ('CPSC 360', 'University of Toronto', 'Computer Science', 3, 301, '10:00-11:30', 'Computer Graphics', 21, 3),
            ('CPSC 400', 'University of Toronto', 'Computer Science', 3, 301, '12:00-13:30', 'Cryptography', 10, 3)]

    for course in courses:
        execute_query(f"INSERT INTO Courses (name, university, department, building_id, room_id, time, info, days, professor_id) SELECT \
                '{course[0]}', d.`university`, d.`name`, {course[3]}, {course[4]}, '{course[5]}', '{course[6]}', '{course[7]}', {course[8]} FROM \
                Department d WHERE d.`university` = '{course[1]}' AND d.`name` = '{course[2]}'")


    # Insert rows into CourseList table
    # For student_id = 1 aka Jane Doe
    execute_query("INSERT INTO CourseList(student_id, course_id) VALUES (%s, %s)", (1, 1)) #CPSC 200
    execute_query("INSERT INTO CourseList(student_id, course_id) VALUES (%s, %s)", (1, 2)) #CPSC 250
    execute_query("INSERT INTO CourseList(student_id, course_id) VALUES (%s, %s)", (1, 7)) #CPSC 350

    # For student_id = 2 aka John Smith
    execute_query("INSERT INTO CourseList(student_id, course_id) VALUES (%s, %s)", (2, 1)) #CPSC 200
    execute_query("INSERT INTO CourseList(student_id, course_id) VALUES (%s, %s)", (2, 2)) #CPSC 250


    


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