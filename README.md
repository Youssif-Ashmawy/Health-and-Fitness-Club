COMP 3005
Health and Fitness Club Project

Group Members:
* Youssif Ashmawy
* Ahmad Qwaider

Overview:
The Fitness Management System is a comprehensive application designed to manage the operations of a fitness center. 
It provides functionalities for members, trainers, and administrative staff to manage various aspects of fitness training, scheduling, equipment maintenance, and more.
The system is built using Python and PostgreSQL. The application uses the psycopg2 library to connect to the PostgreSQL database. 
It employs functions to handle various database operations such as registration, login, scheduling, and data retrieval.


Key Features:

Member Management:
- Register new members with details like username, password, full name, email, fitness goal, height, and weight.
- Update member profiles with new information.
- Display member-specific dashboards showing exercise routines, fitness achievements, and health statistics.
- Schedule, reschedule, and delete private training sessions with trainers.
- Join public fitness classes.
- View and pay balance.
- Add new exercise routine, fitness achievement, and health statistic.

Trainer Management:
- Register new trainers with details like username, password, full name, email, specialization, and availability.
- Set availability timings.
- View profiles of members in the Club.

Administrative Staff Management:
- Book fitness rooms for specific durations.
- Monitor and edit equipment maintenance schedules.
- Update class schedules.
  
General Features for Terminal's User Interaction:
- Login systems for members, trainers, and administrative staff.
- Display lists of trainers, classes, rooms, and equipment.
- Check trainer availability before scheduling sessions.
- Display member's schedule.

Installation:
- Install Python3 if not already installed.
- Install PostgreSQL if not already installed.
- Install the psycopg2 library using pip3: pip3 install psycopg2.
  
Database Setup:
- Create a PostgreSQL database named "postgres" with necessary tables (Members, Trainers, Balance, ExerciseRoutines, FitnessAchievements, HealthStatistics, Schedules, Classes, ClassesJoined, RoomBookings, Equipment).
- Update the database connection details (dbname, user, password, host) in the connect() function.

Run the Application:
- Execute the main script program.py.
- Follow the on-screen prompts to navigate through the functionalities.
- Choose options like registering new members/trainers, logging in
- Then choose any of the listed functions as per your role.

