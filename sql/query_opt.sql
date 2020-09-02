select r.reportId, r.ipv4, e.eventId, e.eventName, b.nodetId, b.bucketIndex, b.lowerEdge, b.upperEdge, b.nodeCount 
from report_tbl as r 
inner join event_tbl as e 
on r.reportId = e.reportId 
inner join bucket_node_tbl as b 
on e.eventId = b.eventId;