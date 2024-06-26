create database vishal_db1;
use vishal_db1;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    password VARCHAR(255) NOT NULL
);

select * from users;

drop table if exists admin;
create table admin(
	email varchar(255) primary key not null,
    password varchar(255) not null
);
insert into admin (email, password) values ('vishalpaints@gmail.com', 'VISHAL123');
select * from admin;