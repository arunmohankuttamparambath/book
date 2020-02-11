CREATE TABLE t_users(id integer primary key autoincrement,
   f_name char(50),
   l_name char(50),
   s_name char(20),
   email varchar(50) NOT NULL,
   u_name varchar(50) NOT NULL,
   p_word varchar(200) NOT NULL);