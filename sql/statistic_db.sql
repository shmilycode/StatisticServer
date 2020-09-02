create database Statistic;

use Statistic;

create table if not exists report_tbl
(
  reportId int unsigned primary key not null auto_increment,
  createTime datetime not null default current_timestamp,
  updateTime datetime not null default current_timestamp,
  ipv4 int unsigned not null,
  eventCount int unsigned not null
) engine=InnoDB;

create table if not exists event_tbl 
(
  eventId bigint unsigned primary key not null auto_increment,
  reportId int unsigned not null,
  createTime datetime not null default current_timestamp,
  updateTime datetime not null default current_timestamp,
  eventName varchar(100) not null,
  eventSum int unsigned not null,
  eventMinimum int not null,
  eventMaximum int not null,
  bucketCount int unsigned not null,
  foreign key (reportId)
  references report_tbl(reportId)
  on delete cascade
  on update cascade
) engine=InnoDB;

create table if not exists bucket_node_tbl
(
  nodeId bigint unsigned primary key not null auto_increment,
  eventId bigint unsigned not null,
  createTime datetime not null default current_timestamp,
  updateTime datetime not null default current_timestamp,
  bucketIndex int unsigned not null,
  lowerEdge int not null,
  upperEdge int not null,
  nodeCount int unsigned not null,
  foreign key (eventId)
  references event_tbl(eventId)
  on delete cascade
  on update cascade
) engine=InnoDB;