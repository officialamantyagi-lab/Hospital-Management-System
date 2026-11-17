create database HospitalDB;
use HospitalDB;

CREATE TABLE Department(
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL,
    location VARCHAR(100)
);

CREATE TABLE Doctor(
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(100) NOT NULL,
    gender ENUM('Male','Female','Other'),
    phone VARCHAR(15) UNIQUE,
    specialization VARCHAR(100),
    experience INT,
    department_id INT,
    FOREIGN KEY (department_id)
    REFERENCES Department(department_id)
);

CREATE TABLE Patient(
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    gender ENUM('Male','Female','Other'),
    age INT,
    phone VARCHAR(15),
    address VARCHAR(255),
    blood_group VARCHAR(5)
);

CREATE TABLE Appointment(
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    appointment_time TIME,
    status VARCHAR(20),
    FOREIGN KEY(patient_id)
    REFERENCES Patient(patient_id),
    FOREIGN KEY(doctor_id)
    REFERENCES Doctor(doctor_id)
);

CREATE TABLE Room(
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) UNIQUE,
    room_type VARCHAR(20),
    charges DECIMAL(10,2),
    availability BOOLEAN DEFAULT TRUE
);

CREATE TABLE Admission(
    admission_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    room_id INT,
    admit_date DATE,
    discharge_date DATE,
    FOREIGN KEY(patient_id)
    REFERENCES Patient(patient_id),
    FOREIGN KEY(room_id)
    REFERENCES Room(room_id)
);

CREATE TABLE Medicine(
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_name VARCHAR(100),
    price DECIMAL(10,2),
    stock INT
);

CREATE TABLE Prescription(
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    medicine_id INT,
    dosage VARCHAR(100),
    days INT,
    FOREIGN KEY(patient_id)
    REFERENCES Patient(patient_id),
    FOREIGN KEY(doctor_id)
    REFERENCES Doctor(doctor_id),
    FOREIGN KEY(medicine_id)
    REFERENCES Medicine(medicine_id)
);

CREATE TABLE Billing(
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    amount DECIMAL(10,2),
    payment_status VARCHAR(20),
    bill_date DATE,
    FOREIGN KEY(patient_id)
    REFERENCES Patient(patient_id)
);















