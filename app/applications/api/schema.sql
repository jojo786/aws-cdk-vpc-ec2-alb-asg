DROP TABLE IF EXISTS applications;

CREATE TABLE applications ( 
id SERIAL PRIMARY KEY, 
student_name TEXT NOT NULL, 
student_email TEXT NOT NULL
);