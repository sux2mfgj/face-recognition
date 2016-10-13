drop table if exists images;
create table if not exists images(
    id integer primary key autoincrement,
    path varchar(255) not null
);

create table if not exists count (
    id integer primary key autoincrement,
    count integer not null,
    time integer not null
);
