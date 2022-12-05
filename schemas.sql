use academiclease;
DROP TABLE IF EXISTS room_post;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS university_list;
CREATE TABLE user (id INTEGER AUTO_INCREMENT PRIMARY KEY,name VARCHAR(50) NOT NULL,email VARCHAR(50) UNIQUE NOT NULL,password VARCHAR(50) NOT NULL,created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE university_list (id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,name VARCHAR(100) UNIQUE NOT NULL,url VARCHAR(100) NOT NULL,created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE room_post (id INTEGER PRIMARY KEY AUTO_INCREMENT,user_id INTEGER NOT NULL,university_id INTEGER NOT NULL,created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,title TEXT NOT NULL,body TEXT NOT NULL,status VARCHAR(50) NOT NULL,FOREIGN KEY (user_id) REFERENCES user (id),FOREIGN KEY (university_id) REFERENCES university_list (id));