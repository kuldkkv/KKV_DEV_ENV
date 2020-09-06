/*  database - postgresql */

create table securitydbo.master
(
master_id integer not null,
provider_desc varchar(50) not null,
sub_provider_desc varchar(50) not null,
security_name varchar(500) not null,
security_type varchar(10) not null,
rating varchar(10) not null,
isin varchar(50),
cusip varchar(50),
cins varchar(50),
live_cusip varchar(50),
sedol varchar(50),
bbc_ticker varchar(50),
wkn varchar(50),
insert_ts timestamp not null,
update_ts timestamp
);

create table securitydbo.xref
(
master_id integer not null,
x_type varchar(50) not null,
x_id varchar(100) not null,
curr_ind boolean not null,
insert_ts timestamp not null,
update_ts timestamp
);


create sequence securitydbo.master_id_seq as int increment by 1 start with 1;

