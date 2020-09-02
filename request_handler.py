import getpass
import json
import pymysql
import logging
import socket

class MysqlController:
  def __init__(self):
    self.db = None
    self.db_host = "172.20.127.29"
    self.db_user_name = "walle"
    self.db_name = "statistic"
  
  def connect(self):
    password = getpass.getpass(prompt="Enter password:")
    self.db = pymysql.connect(self.db_host, self.db_user_name, password, self.db_name)
    logging.info("Connnect success!")

  def insertStatistic(self, report, events):
    try:
      cursor = self.db.cursor()
      report_id = self.insertReport(cursor, report, events)
      for event in events:
        event_id = self.insertEvent(cursor, report_id, event)
        for node in event.nodes:
          node_id = self.insertNode(cursor, event_id, node)
      self.db.commit()
    except:
      self.db.rollback()
      logging.error("Insert statistic failed, rollback!")
      raise
  
  def insertReport(self, cursor, report, events):
    sql = """
    insert into report_tbl(ipv4, eventCount) values(inet_aton('%s'), %u)
    """ % (report.ipv4, len(events))
    cursor.execute(sql)
    insert_id = self.db.insert_id()
    return insert_id

  def insertEvent(self, cursor, report_id, event):
    sql = """
    insert into event_tbl(reportId, eventName, eventSum, eventMinimum, eventMaximum, bucketCount)
    values(%u, '%s', %u, %d, %d, %u)
    """ % (report_id, event.name, event.sum, event.minimum, event.maximum, event.bucket_count)
    cursor.execute(sql)
    insert_id = self.db.insert_id()
    return insert_id

  def insertNode(self, cursor, event_id, node):
    sql = """
    insert into bucket_node_tbl(eventId, bucketIndex, lowerEdge, upperEdge, nodeCount)
    values(%u, %u, %d, %d, %u)
    """ % (event_id, node.bucket_index, node.lower, node.upper, node.count)
    cursor.execute(sql)
    insert_id = self.db.insert_id()
    return insert_id

class Report:
  def __init__(self, ipv4):
    self.ipv4 =ipv4 

class Event:
  def __init__(self, name, sum, min, max, count):
    self.name =name 
    self.sum = sum 
    self.minimum = min
    self.maximum = max
    self.bucket_count = count
    self.nodes = []

class Node:
  def __init__(self, index, lower, upper, count):
    self.bucket_index = index
    self.lower = lower 
    self.upper = upper
    self.count = count

class StatisticRequestHandler:
  def __init__(self):
    self.model = MysqlController()
    self.model.connect()

  def submitNewStatistic(self, reporter, content):
    report = Report(reporter.ipv4)
    event_list = []
    try:
      events_json = content["histograms"]
      event_count = len(events_json)
      for event_json in events_json:
        params_json = event_json["params"]
        new_event = Event(event_json["name"], int(event_json["sum"]), int(params_json["minimum"]), int(params_json["maximum"]), int(params_json["bucket_count"]))
        buckets_json = event_json["buckets"]
        if len(buckets_json) == 0:
          continue
        for (index, node_data) in buckets_json.items():
          new_node = Node(int(index), int(float(node_data["lower"])), int(float(node_data["upper"])), int(node_data["count"]))
          new_event.nodes.append(new_node)
        event_list.append(new_event)
    except Exception as err:
      logging.error("Failed parse response content. %s" % err)
      return
    logging.debug(report)
    logging.debug(event_list)
    self.model.insertStatistic(report, event_list)
