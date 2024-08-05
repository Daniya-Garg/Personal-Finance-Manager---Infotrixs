USE personal_finance_manager;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);


CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    description VARCHAR(255),
    amount DECIMAL(10, 2),
    category VARCHAR(255),
    tags VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);


INSERT INTO users
VALUES (1,"Daniya","Daniya");

