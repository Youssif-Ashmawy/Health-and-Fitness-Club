CREATE TABLE Members (
    member_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    full_name VARCHAR(100),
    email VARCHAR(100),
    fitness_goal VARCHAR(100),
    height FLOAT,
    weight FLOAT
);

CREATE TABLE Trainers (
    trainer_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    full_name VARCHAR(100),
    email VARCHAR(100),
    specialization VARCHAR(100),
    availability VARCHAR(42)  -- Two timestamps, each in 'YYYY-MM-DD HH:MI:SS' format
);

CREATE TABLE Administrative_Staff (
    staff_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    full_name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE Rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(100),
    capacity INT
);

CREATE TABLE RoomBookings (
    booking_id SERIAL PRIMARY KEY,
    room_id INT,
    booking_date_time TIMESTAMP,
    duration_minutes INT
);

CREATE TABLE Classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100),
    trainer_id INT,
    room_id INT,
    schedule TIMESTAMP,
    --test
    price INT,
    FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id),
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
);

CREATE TABLE ClassesJoined (
    joined_id SERIAL PRIMARY KEY,
    member_id INT,
    class_id INT,
    trainer_id INT,
    room_id INT,
    schedule TIMESTAMP,
    FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id),
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);


CREATE TABLE Equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(100),
    maintenance_date DATE
);

CREATE TABLE Balance (
    balance_id SERIAL PRIMARY KEY,
    member_id INT UNIQUE,
    balance INT DEFAULT 0,
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

CREATE TABLE ExerciseRoutines (
    routine_id SERIAL PRIMARY KEY,
    member_id INT,
    routine_date DATE,
    exercise_type VARCHAR(100),
    duration_minutes INT,
    calories_burned FLOAT,
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

CREATE TABLE FitnessAchievements (
    achievement_id SERIAL PRIMARY KEY,
    member_id INT,
    achievement_date DATE,
    achievement_description VARCHAR(255),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

CREATE TABLE HealthStatistics (
    statistic_id SERIAL PRIMARY KEY,
    member_id INT,
    statistic_date DATE,
    weight FLOAT,
    height FLOAT,
    body_fat_percentage FLOAT,
    heart_rate INT,
    blood_pressure VARCHAR(20),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);


CREATE TABLE Schedules (
    schedule_id SERIAL PRIMARY KEY,
    member_id INT,
    trainer_id INT,
    date_time VARCHAR(50),
    duration INT,
    --test
    price INT DEFAULT 30,
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id)
);