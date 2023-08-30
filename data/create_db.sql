/* database creation */

drop table if exists news;
drop table if exists member;
drop table if exists schedule;
drop table if exists draw;
drop table if exists comment;

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
    foreign key(member_id) references member(member_id)
);

create table draw(
    draw_id integer primary key autoincrement not null,
    grade text not null,
    round integer not null,
    affirming text not null,
    negating text not null,
    winner text
);

create table comment(
    comment_id integer primary key autoincrement not null,
    news_id integer not null,
    member_id integer not null,
    comment text not null,
    commentdate date not null,
    foreign key(news_id) references news(news_id),
    foreign key(member_id) references member(member_id)
);

insert into member( firstname, lastname, email, password, authorisation)
values ('Florence', 'Oakley', 'm@g.com', 'temp', 0 );
insert into member( firstname, lastname, email, password, authorisation)
values ('Ri', 'Comer', 'ri@yahoo.com', 'temp', 0 );
insert into member( firstname, lastname, email, password, authorisation)
values ('Brooke', 'Kinajil-Moran', 'brookethecook@hotmail.com', 'temp', 0 );
insert into member( firstname, lastname,email, password, authorisation)
values ('Arushi', 'Bhatnager-Stewart', 'arushi@marsden.com', 'temp', 1 );

/* news items */
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

/* schedule items */

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

/* comment items */

insert into comment(news_id, member_id, comment, commentdate)
values( (select news_id from news where title='Regionals'),
       (select member_id from member where firstname='Arushi'),
       'How many teams are able to enter per school, and is there a cost?',
       '2023-04-02 12:13:00'
       );

insert into comment(news_id, member_id, comment, commentdate)
values( (select news_id from news where title='Regionals'),
       (select member_id from member where firstname='Florence'),
       'Hi Arushi,'||
       ' There is no limit to the number of teams able to enter per school, however'||
       ' there is an entry cost of $60 per team',
       '2023-04-03 18:01:00'
       );

insert into comment(news_id, member_id, comment, commentdate)
values( (select news_id from news where title='Prem A!'),
       (select member_id from member where firstname='Arushi'),
       'Hi Ri, I think that Marsden might be able to host.',
       '2023-03-20 15:25:00'
       );