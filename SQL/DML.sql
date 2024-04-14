-- Starting Members
INSERT INTO Members (username, password, full_name, email, fitness_goal, height, weight) 
VALUES 
('mike_logan', 'password1', 'Mike Logan', 'mike@example.com', 'Lose weight', 175, 80),
('drake_smith', 'password2', 'Drake Smith', 'drake@example.com', 'Gain muscle', 160, 55);

-- Starting Trainers
INSERT INTO Trainers (username, password, full_name, email, specialization, availability)
VALUES
('big_ramy', 'password3', 'Big Ramy', 'big@example.com', 'Weightlifting', '2024-04-20 09:00:00,2024-04-20 17:00:00'),
('dwayne_johnson', 'password4' ,'Dwayne Johnson', 'dwayne@example.com', 'Yoga', '2024-04-21 10:00:00,2024-04-21 18:00:00');

-- Starting Administrative Staff
INSERT INTO Administrative_Staff (username, password, full_name, email)
VALUES
('admin_user', 'password0', 'Admin User', 'admin@example.com');

-- Starting Rooms
INSERT INTO Rooms (room_name, capacity)
VALUES
('Weight Room', 20),
('Yoga Studio', 15);

-- Starting RoomBookings
INSERT INTO RoomBookings (room_id, booking_date_time, duration_minutes)
VALUES
(1, '2024-04-20 10:00:00', 60),
(2, '2024-04-22 14:00:00', 90);

-- Starting Classes
INSERT INTO Classes (class_name, trainer_id, room_id, schedule, price)
VALUES
('Weightlifting Class', 1, 1, '2024-04-20 20:00:00',50),
('Yoga Class', 2, 2, '2024-04-25 17:30:00',60);

-- Starting Equipment
INSERT INTO Equipment (equipment_name, maintenance_date)
VALUES
('Treadmill', '2024-04-01'),
('Dumbbells', '2024-03-15');

-- Starting data for ExerciseRoutines table
INSERT INTO ExerciseRoutines (member_id, routine_date, exercise_type, duration_minutes, calories_burned)
VALUES
(1, '2024-04-10', 'Yoga', 30, 300),
(1, '2024-04-12', 'Weightlifting', 45, 200),
(2, '2024-04-11', 'Yoga', 60, 150);


-- Starting data for FitnessAchievements table
INSERT INTO FitnessAchievements (member_id, achievement_date, achievement_description)
VALUES
(1, '2024-04-15', 'Benched 4 plates'),
(1, '2024-04-16', 'Completed 10 pull-ups'),
(2, '2024-04-17', 'Attended yoga class for 30 consecutive days');

-- Starting data for HealthStatistics table
INSERT INTO HealthStatistics (member_id, statistic_date, weight, height, body_fat_percentage, heart_rate, blood_pressure)
VALUES
(1, '2024-04-10', 70.5, 175, 15.0, 65, '120/80'),
(1, '2024-04-15', 69.8, 175, 14.5, 64, '118/78'),
(2, '2024-04-11', 60.0, 160, 20.0, 70, '122/82'),
(2, '2024-04-16', 59.5, 160, 19.5, 68, '120/80');

-- Starting data for Balance table
INSERT INTO Balance (member_id)
VALUES
(1),  
(2);
