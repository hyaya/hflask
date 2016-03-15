DROP TABLE if EXISTS entries;
CREATE TABLE entries(
  id INTEGER PRIMARY KEY autoincrement,--id为主键，自增
  title text NOT NULL,
  text text NOT NULL
);