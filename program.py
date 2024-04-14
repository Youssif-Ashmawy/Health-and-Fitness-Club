import psycopg2
from psycopg2 import sql

from datetime import datetime, timedelta

import math

# Function to establish connection to PostgreSQL database
def connect():
    conn = psycopg2.connect(
        dbname="postgres", # Database name
        user="postgres", # Username
        password="5trika22", # Password
        host="localhost" # Host
    )
    return conn

#Member Functions

# Function to add new member
def memberRegisteration(username, password, full_name, email, fitness_goal, height, weight):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("INSERT INTO Members (username, password, full_name, email, fitness_goal, height, weight) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING member_id",
                       (username, password, full_name, email, fitness_goal, height, weight))    
    # Fetch the member_id
    member_id = cur.fetchone()[0]

    # Insert the member_id into Balance table
    cur.execute("INSERT INTO Balance (member_id) VALUES (%s)", (member_id,))

    print("Member registered successfully!")
    conn.commit() #Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to add new trainer
def trainerRegisteration(username, password, full_name, email, specialization, availability):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("INSERT INTO Trainers (username, password, full_name, email, specialization, availability) VALUES (%s, %s, %s, %s, %s, %s)",
                       (username, password, full_name, email, specialization, availability))
    conn.commit()  # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to modify member's info
def profileManagement(member_id, new_full_name, new_fitness_goal, new_height, new_weight):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("UPDATE Members SET full_name = %s, fitness_goal = %s, height = %s, weight = %s WHERE member_id = %s",
                       (new_full_name, new_fitness_goal, new_height, new_weight, member_id))
    conn.commit()  # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to display member's dashboard
def dashboardDisplay(member_id):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    # Fetch exercise routines for the member
    cur.execute("SELECT * FROM ExerciseRoutines WHERE member_id = %s", (member_id,))
    exercise_routines = cur.fetchall()

    # Fetch fitness achievements for the member
    cur.execute("SELECT * FROM FitnessAchievements WHERE member_id = %s", (member_id,))
    fitness_achievements = cur.fetchall()

    # Fetch health statistics for the member
    cur.execute("SELECT * FROM HealthStatistics WHERE member_id = %s", (member_id,))
    health_statistics = cur.fetchall()

    # Display exercise routines
    print("Exercise Routines:")
    for routine in exercise_routines:
        print(f"Date: {routine[2]}, Exercise Type: {routine[3]}, Duration (minutes): {routine[4]}, Calories Burned: {routine[5]}")

    # Display fitness achievements
    print("\nFitness Achievements:")
    for achievement in fitness_achievements:
        print(f"Date: {achievement[2]}, Achievement Description: {achievement[3]}")

    # Display health statistics
    print("\nHealth Statistics:")
    for statistic in health_statistics:
        print(f"Date: {statistic[2]}, Weight: {statistic[3]}, Height: {statistic[4]}, Body Fat Percentage: {statistic[5]}, Heart Rate: {statistic[6]}, Blood Pressure: {statistic[7]}")

    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to schedule a private training session
def scheduleManagement(member_id, trainer_id, session_date_time, duration):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object

    available = check_trainer_availability(trainer_id, session_date_time, duration)
    if available == False:
        print(f"Trainer {trainer_id} is not available")
        return

    # Schedule the session
    cur.execute("INSERT INTO Schedules (member_id, trainer_id, date_time, duration) VALUES (%s, %s, %s, %s)",
                (member_id, trainer_id, session_date_time, duration))
    
    # Update Balance
    cur.execute("SELECT price FROM Schedules WHERE trainer_id = %s AND duration = %s", (trainer_id, duration))
    price = cur.fetchone()[0]  # Fetch the price from the result
    print(f"Price for any private training session: ${price} per hr")
    final_price = math.ceil(duration / 60) * price
    print(f"You will pay ${final_price}")

    # Update the balance in the Balance table
    cur.execute("UPDATE Balance SET balance = balance + %s WHERE member_id = %s", (final_price, member_id))

    conn.commit()  # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    print("Session scheduled successfully!")

# Function to reschedule a private training session
def rescheduleSession(schedule_id, new_session_date_time):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    
    # Check if the schedule exists
    cur.execute("SELECT * FROM Schedules WHERE schedule_id = %s", (schedule_id,))
    if cur.rowcount == 0:
        print(f"Schedule with ID {schedule_id} not found")
        return
    
    # Check trainer availability for the new session date and time
    existing_schedule = cur.fetchone()
    available = check_trainer_availability(existing_schedule[2], new_session_date_time, existing_schedule[4])  
    
    if not available:
        print(f"Trainer {existing_schedule[2]} is not available at the new time")
        cur.close()
        conn.close()
        return
    
    # Update the session date and time
    cur.execute("UPDATE Schedules SET date_time = %s WHERE schedule_id = %s", (new_session_date_time, schedule_id))
    
    conn.commit()  # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    print(f"Session with ID {schedule_id} rescheduled successfully to {new_session_date_time}")

# Function to delete a scheduled private training session
def deleteSession(schedule_id):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    
    # Check if the schedule exists
    cur.execute("SELECT * FROM Schedules WHERE schedule_id = %s", (schedule_id,))
    if cur.rowcount == 0:
        print(f"Schedule with ID {schedule_id} not found")
        return
    
    # Delete the session
    cur.execute("DELETE FROM Schedules WHERE schedule_id = %s", (schedule_id,))
    
    conn.commit()  # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    print(f"Session with ID {schedule_id} deleted successfully")

# Function to join a group class session
def joinClass(member_id,class_id):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    
    # Fetch trainer_id, room_id, and schedule from Classes table
    cur.execute("SELECT trainer_id, room_id, schedule FROM Classes WHERE class_id = %s", (class_id,))
    result = cur.fetchone()
        
    if result:
        trainer_id, room_id, schedule = result
            
        # Insert the member to the class
        cur.execute("INSERT INTO ClassesJoined (member_id, class_id, trainer_id, room_id, schedule) VALUES (%s, %s, %s, %s, %s)", 
                     (member_id, class_id, trainer_id, room_id, schedule))
        
         # Update Balance
        cur.execute("SELECT price FROM Classes WHERE class_id = %s", (class_id))
        price = cur.fetchone()[0]  # Fetch the price from the result

        # Update the balance in the Balance table
        cur.execute("UPDATE Balance SET balance = balance + %s WHERE member_id = %s", (price, member_id))
        print(f"Member with ID {member_id} joined class with ID {class_id} successfully!")
    else:
        print(f"Class with ID {class_id} not found.")

    conn.commit() # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to view member's balance
def viewBalance(member_id):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    
    cur.execute(f"SELECT balance FROM Balance WHERE member_id = {member_id}")

    # Fetch the balance
    balance = cur.fetchone()

    if balance:
        print(f"you got a balance of {balance[0]}")  # print the balance value
    else:
        print(f"Member ID {member_id} not found")
    
    conn.commit() # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to pay amount and add it to the member's balance
def payBalance(member_id,amount):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    
    cur.execute(f"SELECT balance FROM Balance WHERE member_id = {member_id}")

    # Fetch the balance
    balance = cur.fetchone()

    # Update the balance in the Balance table
    cur.execute("UPDATE Balance SET balance = balance - %s WHERE member_id = %s", (amount, member_id))
    
    
    if balance:
        print(f"payment completed")  
    else:
        print(f"Member ID {member_id} not found")
    
    conn.commit() # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to add a new exercise routine
def newExerciseRoutine(member_id, routine_date, exercise_type, duration_minutes, calories_burned):
    conn = connect()
    cur = conn.cursor()
    conn.commit() # Commit the transaction
    cur.execute("INSERT INTO ExerciseRoutines (member_id, routine_date, exercise_type, duration_minutes, calories_burned) VALUES (%s, %s, %s, %s, %s)",
                 (member_id, routine_date, exercise_type, duration_minutes, calories_burned))

    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted into ExerciseRoutines table successfully!")

# Function to add a new fitness achievment
def newFitnessAchievement(member_id, achievement_date, achievement_description):
    conn = connect()
    cur = conn.cursor()
    conn.commit() # Commit the transaction
    cur.execute("INSERT INTO FitnessAchievements (member_id, achievement_date, achievement_description) VALUES (%s, %s, %s)",
                (member_id, achievement_date, achievement_description))

    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted into FitnessAchievements table successfully!")

# Function to add a new health statistics
def newHealthStatistic(member_id, statistic_date, weight, height, body_fat_percentage, heart_rate, blood_pressure):
    conn = connect()
    cur = conn.cursor()
    conn.commit() # Commit the transaction
    cur.execute("INSERT INTO HealthStatistics (member_id, statistic_date, weight, height, body_fat_percentage, heart_rate, blood_pressure) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (member_id, statistic_date, weight, height, body_fat_percentage, heart_rate, blood_pressure))

    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted into HealthStatistics table successfully!")


#Trainer Functions

# Function to change the trainer's availability
def setAvailability(trainer_id, availability):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("UPDATE Trainers SET availability = %s WHERE trainer_id = %s", (availability, trainer_id))
    conn.commit() # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    print("Availability set successfully!")

# Function to view a member's profile by searching his name
def memberProfileViewing(member_name):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("SELECT * FROM Members WHERE full_name ILIKE %s", ('%' + member_name + '%',))
    members = cur.fetchall()
    if members:
        for member in members:
            print("Member ID:", member[0])
            print("Username:", member[1])
            print("Full Name:", member[3])
            print("Email:", member[4])
            print("Fitness Goal:", member[5])
            print("Height:", member[6])
            print("Weight:", member[7])

    else:
        print("Member not found.")

    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

#Administrative Staff Functions

# Function to book a room
def book_room(room_id, booking_date_time, duration_minutes):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    # Check if the room is available
    cur.execute("SELECT room_id FROM RoomBookings WHERE room_id = %s AND booking_date_time = %s", (room_id, booking_date_time))
    if cur.fetchone():
        print("Room is not available at this time. Please choose another time.")
        return

    cur.execute("INSERT INTO RoomBookings (room_id, booking_date_time, duration_minutes) VALUES (%s, %s, %s)",
                (room_id, booking_date_time, duration_minutes))
    conn.commit() # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    print("Room booked successfully!")
    
# Function to monitor and modify equipment maintenance 
def equipmentMaintenanceMonitoring(equipment_id, maintenance_date):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("UPDATE Equipment SET maintenance_date = %s WHERE equipment_id = %s", (maintenance_date, equipment_id))
    if cur.rowcount == 0:
        print(f"Equipment ID {equipment_id} not found!")
    else:
        print("Maintenance date updated successfully!")
    conn.commit() # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    
# Function to modify a class's schedule
def update_class_schedule(class_id, new_schedule):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("UPDATE Classes SET schedule = %s WHERE class_id = %s", (new_schedule, class_id))
    conn.commit() # Commit the transaction
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    print("Class schedule updated successfully!")

# Some extra functions needed

# Function to login as a member      
def memberLogin(username, password):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("SELECT * FROM Members WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    
    if user:
        print(f"{user[1]} has successfully login")
        return user[0]  # Return the member_id if login is successful
    else:
        print("Incorrect username or password")
        return None  # Return None if login fails
        
# Function to login as a trainer    
def trainerLogin(username, password):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("SELECT * FROM Trainers WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    
    if user:
        print(f"{user[1]} has successfully login")
        return user[0]  # Return the trainer_id if login is successful
    else:
        print("Incorrect username or password")
        return None  # Return None if login fails
# Function to login as an admin
def adminLogin(username, password):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("SELECT * FROM Administrative_Staff WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()  # Close the cursor
    conn.close()  # Close the database connection
    
    if user:
        print(f"{user[1]} has successfully login")
        return user[0]  # Return the staff_id if login is successful
    else:
        print("Incorrect username or password")
        return None  # Return None if login fails

# Function to display all trainers
def trainersDisplay():
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    # Fetch trainers
    cur.execute("SELECT * FROM Trainers")
    trainers = cur.fetchall()

    # Display trainers
    print("Trainers:")
    for trainer in trainers:
        print(f"ID: {trainer[0]}, Full Name: {trainer[3]}, Email: {trainer[4]}, Specialization: {trainer[5]}, Availability: {trainer[6]}")

    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to display all classes
def classesDisplay():
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    
    # Fetch classes 
    cur.execute("SELECT * FROM Classes")
    classes = cur.fetchall()

    # Display classes
    print("Classes:")
    for aClass in classes:
        print(f"ID: {aClass[0]}, Name: {aClass[1]}, Trainer's ID: {aClass[2]}, Room's ID: {aClass[3]}, Schedule: {aClass[4]}, Price: {aClass[5]}")

    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to display all rooms
def roomsDisplay():
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    # Fetch Rooms
    cur.execute("SELECT * FROM Rooms")
    rooms = cur.fetchall()

    # Display Rooms
    print("Rooms:")
    for room in rooms:
        print(f"ID: {room[0]}, Room Name: {room[1]}, Capacity: {room[2]}")


    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to display all equipments
def equipmentDisplay():
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object
    # Fetch Equipments
    cur.execute("SELECT * FROM Equipment")
    equipments = cur.fetchall()

    # Display Equipments
    print("Equipments:")
    for equipment in equipments:
        print(f"ID: {equipment[0]}, Equipment Name: {equipment[1]}, Maintenance Date: {equipment[2]}")


    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Function to check if trainer is available for a session
def check_trainer_availability(trainer_id, start_time, duration):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object

    cur.execute("SELECT availability FROM Trainers WHERE trainer_id = %s", (trainer_id,))
    availability_str = cur.fetchone()[0]

    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

    if availability_str:
        available_from, available_until = availability_str.split(',') 
        fromTimeStamp = datetime.strptime(available_from, "%Y-%m-%d %H:%M:%S")
        untilTimeStamp = datetime.strptime(available_until, "%Y-%m-%d %H:%M:%S")
        startTimeStamp = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        endTimeStamp = startTimeStamp + timedelta(minutes=duration)  
        return startTimeStamp >= fromTimeStamp and endTimeStamp <= untilTimeStamp
    else:
        return False

# Function to display a member's schedule
def displayMemberSchedule(member_id):
    conn = connect()  # Establish a connection to the database
    cur = conn.cursor()  # Create a cursor object

    cur.execute("SELECT * FROM Schedules WHERE member_id = %s", (member_id,))
    memberSchedule = cur.fetchall()

    for memberS in memberSchedule:
        print(f"Schedule ID: {memberS[0]}. Member ID: {memberS[1]}. Trainer ID: {memberS[2]}. Date & Time: {memberS[3]}. Duration: {memberS[4]} minutes")

    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

# Interacting Terminal
if __name__ == "__main__":
    command = None
    while (command != "exit"):
        print("------------------------------")
        print("Please choose an option from the list below")
        print("newM   -> registering new member")
        print("newT   -> registering new trainer")
        print("loginM -> login as member")
        print("loginT -> login as trainer")
        print("loginA -> login as admin")
        print("exit   -> exit the terminal")
        command = input("Please enter your selection here: ")
        print("------------------------------")
        if command == "exit": break
        elif command == "newM":
            username =     input("Please enter your username: ")
            password =     input("Please enter your password: ")
            email =        input("Please enter your email: ")
            full_name =    input("Please enter your full name: ")
            fitness_goal = input("Please enter your fitness goal: ")
            height =       input("Please enter your height: ")
            weight =       input("Please enter your weight: ")
            memberRegisteration(username, password, full_name, email, fitness_goal, height, weight)
            
        elif command == "newT":
            username =       input("Please enter your username: ")
            password =       input("Please enter your password: ")
            full_name =      input("Please enter your full name: ")
            email =          input("Please enter your email: ")
            specialization = input("Please enter your specialization: ")
            availability =   input("Please enter your availabity in this format 'YYYY-MM-DD HH:MI:SS, YYYY-MM-DD HH:MI:SS', seperating the start of your availabilty and the end by a comma(,): ")
            trainerRegisteration(username, password, full_name, email, specialization, availability)

        elif command == "loginM":
            member_id = None
            while member_id == None:
                username =       input("Please enter your username: ")
                password =       input("Please enter your password: ")
                member_id = memberLogin(username, password)
                print("------------------------------")
                if member_id == None: 
                    print("Please input the correct credentials")
                    print("------------------------------")

            function = None
            print("------------------------------")
            print("Welcome to the System!")
            while function != "logout":
                print("------------------------------")
                print("Functions avaliable:")
                print("profM    -> profile management")
                print("dashD    -> dashboard display")
                print("schedM   -> schedule management")
                print("reschedM -> reschedule session")
                print("delM     -> delete scheduled session")
                print("joinC    -> join public class")
                print("exeR     -> new exercise routine")
                print("fitA     -> new fitness achievements")
                print("hlthS    -> new health statistics")
                print("viewB    -> view balance")
                print("payB     -> pay balance")
                print("logout   -> logout from the system")
                function = input("Please enter your selection here: ")
                print("------------------------------")
                if function == "logout": break

                elif function == "profM":
                    new_full_name =    input("Please enter your new full name: ")
                    new_fitness_goal = input("Please enter your new fitness goal: ")
                    new_height =       input("Please enter your new height: ")
                    new_weight =       input("Please enter your new weight: ")
                    profileManagement(member_id, new_full_name, new_fitness_goal, new_height, new_weight)
                    print("Updated Successfully")

                elif function == "dashD":
                    dashboardDisplay(member_id)

                elif function == "schedM":
                    trainersDisplay()
                    trainer_id =         input("Please enter the trainer's id: ")
                    session_date_time =  input("Please enter your session time in this format 'YYYY-MM-DD HH:MI:SS': ")
                    duration =           int(input("Please enter the duration of your session in minutes: "))
                    scheduleManagement(member_id, trainer_id, session_date_time, duration)
                
                elif function == "reschedM":
                    displayMemberSchedule(member_id)
                    schedule_id = input("Please input the ID of the schedule you want to change: ")
                    new_session_date_time = input("Please enter your new session time in this format 'YYYY-MM-DD HH:MI:SS': ")
                    rescheduleSession(schedule_id, new_session_date_time)

                elif function == "delM":
                    displayMemberSchedule(member_id)
                    schedule_id = input("Please input the ID of the schedule you want to delete: ")
                    deleteSession(schedule_id)
                
                elif function == "joinC":
                    classesDisplay()
                    class_id = input("Please input the id of the class you want to join: ")
                    joinClass(member_id,class_id)

                elif function == "exeR":
                    routine_date = input("Enter routine date (YYYY-MM-DD): ")
                    exercise_type = input("Enter exercise type: ")
                    duration_minutes = input("Enter duration in minutes: ")
                    calories_burned = input("Enter calories burned: ")
                    newExerciseRoutine(member_id, routine_date, exercise_type, duration_minutes, calories_burned)
                                
                elif function == "fitA":
                    achievement_date = input("Enter achievement date (YYYY-MM-DD): ")
                    achievement_description = input("Enter achievement description: ")
                    newFitnessAchievement(member_id, achievement_date, achievement_description)

                elif function == "hlthS":
                    statistic_date = input("Enter statistic date (YYYY-MM-DD): ")
                    weight = input("Enter your weight: ")
                    height = input("Enter your height: ")
                    body_fat_percentage = input("Enter your body fat percentage: ")
                    heart_rate = input("Enter your heart rate: ")
                    blood_pressure = input("Enter blood pressure (e.g. 120/80): ")
                    newHealthStatistic(member_id, statistic_date, weight, height, body_fat_percentage, heart_rate, blood_pressure)


                elif function == "viewB":
                    viewBalance(member_id)

                elif function == "payB":
                    viewBalance(member_id)
                    amount = input("Please input the amount you want to pay: $")
                    payBalance(member_id,amount)
                    viewBalance(member_id)

                else: print("Please input a valid function from the list given")


        elif command == "loginT":
            trainer_id = None
            while trainer_id == None:
                username =       input("Please enter your username: ")
                password =       input("Please enter your password: ")
                trainer_id = trainerLogin(username, password)
                print("------------------------------")
                if trainer_id == None: 
                    print("Please input the correct credentials")
                    print("------------------------------")
                    
            function = None
            print("------------------------------")
            print("Welcome to the System!")
            while function != "logout":
                print("------------------------------")
                print("Functions avaliable:")
                print("setA    -> set availability")
                print("memP    -> member profile viewing")
                print("logout  -> logout from the system")
                function = input("Please enter your selection here: ")
                print("------------------------------")
                if function == "logout": break

                elif function == "setA":
                    availability = input("Please input your availability in this format 'YYYY-MM-DD HH:MI:SS,YYYY-MM-DD HH:MI:SS' (seperating the start and the end by a comma): ")
                    setAvailability(trainer_id, availability)

                elif function == "memP":
                    member_name = input("Please input the member's name you are looking for: ")
                    memberProfileViewing(member_name)

                else: print("Please input a valid function from the list given")

        elif command == "loginA":
            admin_id = None
            while admin_id == None:
                username =       input("Please enter your username: ")
                password =       input("Please enter your password: ")
                admin_id = adminLogin(username, password)
                print("------------------------------")
                if admin_id == None: 
                    print("Please input the correct credentials")
                    print("------------------------------")

            function = None
            print("------------------------------")
            print("Welcome to the System!")
            while function != "logout":
                print("------------------------------")
                print("Functions avaliable:")
                print("bookR   -> book room")
                print("equM    -> equipment display")
                print("updCS   -> update class schedule")
                print("logout  -> logout from the system")
                function = input("Please enter your selection here: ")
                print("------------------------------")
                if function == "logout": break

                elif function == "bookR":
                    roomsDisplay()
                    room_id =            input("Please enter the room's id: ")
                    booking_date_time =  input("Please enter the booking's date and time in this format 'YYYY-MM-DD HH:MI:SS': ")
                    bookingTimeStamp = datetime.strptime(booking_date_time, "%Y-%m-%d %H:%M:%S")
                    duration_minutes =   input("Please enter the booking's duration in minutes: ")
                    book_room(room_id, bookingTimeStamp, duration_minutes)

                elif function == "equM":
                    equipmentDisplay()
                    equipment_id =      input("Please enter the equipment's id: ")
                    maintenance_date =  input("Please enter the equipment's maintenance date: ")
                    equipmentMaintenanceMonitoring(equipment_id, maintenance_date)

                elif function == "updCS":
                    classesDisplay()
                    class_id =           input("Please enter the class's id: ")
                    new_schedule =       input("Please enter the new schedule day and time in this format 'YYYY-MM-DD HH:MI:SS': ")
                    newScheduleTimeStamp = datetime.strptime(new_schedule, "%Y-%m-%d %H:%M:%S")
                    update_class_schedule(class_id, newScheduleTimeStamp)

                else: print("Please input a valid function from the list given")

        else: print("Please input a valid option from the list given")
