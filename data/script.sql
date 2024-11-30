DROP TABLE IF EXISTS kb_input, kb_output CASCADE;

CREATE TABLE kb_input(
    id_kb_input serial NOT NULL PRIMARY KEY,
    kb_usage varchar(45) NOT NULL, 
    budget int NOT NULL (budget > 0),
    switch varchar(50) NOT NULL, 
    kb_size varchar(30) NOT NULL,
    kb_connection varchar(20) NOT NULL,
    mk_before BOOLEAN NOT NULL, 
    mk_input varchar(300) NOT NULL
);

CREATE TABLE kb_output (
  id_kb_output serial NOT NULL PRIMARY KEY, 
  id_kb_input int NOT NULL,
  kb_shown int NOT NULL, 
  price int not null (price >= 0), 
  switch varchar (50) not null,
  kb_size varchar (50) not null,
  mk_output varchar(300) NOT NULL,
  FOREIGN KEY (id_kb_input) REFERENCES kb_input(id_kb_input)
);

