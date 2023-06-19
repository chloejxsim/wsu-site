/* database creation */

drop table if exists news;
drop table if exists member;
drop table if exists schedule;
drop table if exists grade;
drop table if exists round;
drop table if exists draw;

/* create tables */

create table member(
    member_id integer primary key autoincrement not null,
    firstname text not null,
    lastname text not null,
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

create table schedule(
    post_id integer primary key autoincrement not null,
    event text not null,
    description text not null,
    scheduledate date not null,
    location text not null,
    member_id integer not null,
    foreign key(member_id) references member (member_id)
);

create table grade(
    grade_id integer primary key autoincrement not null,
    name text not null
);

create table round(
    round_id integer primary key autoincrement not null,
    moot text not null,
    grade_id integer not null,
    foreign key(grade_id) references grade (grade_id)
);

create table draw(
    draw_id integer primary key autoincrement not null,
    affirming text not null,
    negating text not null,
    winner text not null,
    round_id integer not null,
    foreign key(round_id) references round (round_id)
);

insert into member( firstname, lastname, email, password, authorisation)
values ('Florence', 'Oakley', 'm@g.com', 'temp', 0 );
insert into member( firstname, lastname, email, password, authorisation)
values ('Ri', 'Comer', 'ri@yahoo.com', 'temp', 0 );
insert into member( firstname, lastname, email, password, authorisation)
values ('Brooke', 'Kinajil-Moran', 'brookethecook@hotmail.com', 'temp', 0 );
insert into member( firstname, lastname,email, password, authorisation)
values ('Arushi', 'Bhatnager-Stewart', 'arushi@marsden.com', 'temp', 1 );

insert into news(title, subtitle, content, newsdate, member_id)
values('Prem A!',
       'Prem A Round Two',
       'Kia ora everyone! ' || char(10) ||
       'Unfortunately, we have been unable to secure a school to host the upcoming Prem A Round 2 debates. ' ||
       'This means that Round 2 will be postponed till Tuesday the 4th of April. If any central schools are able to host this round, ' ||
       'please let me know either through email or in this comment section. ' || char(10) ||
       'Thank you!',
       '2023-03-19 17:41:00',
       (select member_id from member where firstname='Ri' )
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
       (select member_id from member where firstname='Florence' )
       );

insert into schedule(event, description, scheduledate, location, member_id)
values('Stockley Cup',
       'WSUs largest public speaking competition for senior students',
       '2023-06-22 18:00:00',
       'Rutherford House',
       (select member_id from member where firstname='Brooke' )
       );

insert into schedule(event, description, scheduledate, location, member_id)
values('Dunsheath Shield',
       'WSUs largest public speaking competition for junior students',
       '2023-06-20 18:00:00',
       'Rutherford House',
       (select member_id from member where firstname='Brooke' )
       );

insert into grade(name)
values('Premier Advanced');

insert into grade(name)
values('Premier B');

insert into round(moot, grade_id)
values('THW ban zoos',
       (select grade_id from grade where name='Premier Advanced')
       );

insert into round(moot, grade_id)
values('THW ban fireworks',
       (select grade_id from grade where name='Premier B')
       );

insert into draw(round_id, affirming, negating, winner)
values((select round_id from round where moot='THW ban zoos'),
       'Marsden',
       'Onslow',
       'Marsden');

insert into draw(round_id, affirming, negating, winner)
values((select round_id from round where moot='THW ban fireworks'),
       'QMC',
       'Marsden',
       'QMC');