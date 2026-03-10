-- Active: 1769823356550@@127.0.0.1@3306@practice_users
CREATE DATABASE practice_users;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profiles(
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    bio VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


select * FROM users;

INSERT INTO users(email)
VALUES
    ("A@gmail.com"),
    ("b@gmail.com"),
    ("c@gmail.com");

DESCRIBE users;

SELECT * FROM users;

INSERT INTO profiles (user_id, bio)
VALUES
(1, 'Alice likes SQL and data'),
(2, 'Bob is learning backend'),
(3, 'Carol wants to do ML');



SELECT * FROM profiles;


SELECT u.user_id, u.email, p.bio
from users u
JOIN profiles p ON u.user_id = p.user_id;