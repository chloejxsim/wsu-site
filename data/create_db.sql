/* database creation */

drop table if exists news;
drop table if exists member;

/* create tables */

create table member(
    member_id integer primary key autoincrement not null,
    name text not null,
    email text not null unique,
    password text not null,
    authorisation integer not null
);

create table news(
    news_id integer primary key autoincrement not null,
    title text not null unique,
    subtitle text not null unique,
    content text not null unique,
    newsdate date not null,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);

insert into member( name, email, password, authorisation)
values ('Florence', 'm@g.com', 'temp', 0 );
insert into member( name, email, password, authorisation)
values ('Ri', 'ri@yahoo.com', 'temp', 0 );
insert into member( name, email, password, authorisation)
values ('Brooke', 'brookethecook@hotmail.com', 'temp', 0 );
insert into member( name, email, password, authorisation)
values ('Arushi', 'arushi@marsden.com', 'temp', 1 );

insert into news(title, subtitle, content, newsdate, member_id)
values('Prem A!',
       'Prem A Round Two',
       'Kia ora everyone! ' || char(10) ||
       'Unfortunately, we have been unable to secure a school to host the upcoming Prem A Round 2 debates. ' ||
       'This means that Round 2 will be postponed till Tuesday the 4th of April. If any central schools are able to host this round, ' ||
       'please let me know either through email or in this comment section. ' || char(10) ||
       'Thank you!',
       '2023-03-19 17:41:00',
       (select member_id from member where name="Ri" )
       );

insert into news(title, subtitle, content, newsdate, member_id)
values('Regionals',
       'Wellington Regional Debating Tournament',
       'Kia ora everyone! ' || char(10) ||
       'The New Zealand Schools Debating Council will be running the annual Wellington Regionals School Debating two-day tournament ' ||
       'this weekend! It will be held at Wellington College on the 1st and 2nd of April. This year we are particularly focused ' ||
       'on development so the tournament will be valuable for both your experienced and new debaters. Additionally, we particularly ' ||
       'encourage new schools to consider entering a team this year. It’s a great opportunity for students to develop their debating ' ||
       'skills and compete against other like minded students in the region! ',
       '2023-03-30 16:30:00',
       (select member_id from member where name="Florence" )
       );