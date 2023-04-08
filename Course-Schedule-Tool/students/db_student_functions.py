import mysql.connector
def execute_and_fetch_query(query):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="3GUv878pnS@n",
        database="sql_schedule_database"
    )

    mycursor = db.cursor()
    try:
        mycursor.execute(query)
        db.commit()
        result = mycursor.fetchall()
        return result, None
    except mysql.connector.Error as e:
        return None, e

#Returns nothign
def execute_query(query, params=None):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="3GUv878pnS@n",
        database="sql_schedule_database"
    )

    mycursor = db.cursor()
    try:
        if params:
            mycursor.execute(query, params)
        else:
            mycursor.execute(query)
        db.commit()
        print("Query executed successfully.")
    except mysql.connector.Error as e:
        print("Error executing query:", e)

    
def add_student(f_name, l_name):
    query = "INSERT INTO Student (f_name, l_name) VALUES (%s, %s)"
    params = (f_name, l_name)
    execute_query(query, params)

def clear_database():
    # Drop the Student table if it exists
    execute_query("DROP TABLE IF EXISTS Student;")

    # Create the Student table with student_id as the primary key
    execute_query("CREATE TABLE Student (student_id int UNSIGNED AUTO_INCREMENT PRIMARY KEY, f_name varchar (50), l_name varchar(50));")
    
def add_default_database_values():
    add_student("John","Doe")


