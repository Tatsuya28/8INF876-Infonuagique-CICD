CREATE DATABASE IF NOT EXISTS django_cicd_db;
CREATE USER IF NOT EXISTS 'myuser'@'%' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON django_cicd_db.* TO 'myuser'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS test_django_cicd_db;
CREATE USER IF NOT EXISTS 'myuser'@'%' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON test_django_cicd_db.* TO 'myuser'@'%';
FLUSH PRIVILEGES;
