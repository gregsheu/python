import elasticsearch
import os
import socket
import random
from gps3 import gps3
from time import sleep

es = elasticsearch.Elasticsearch()
es = elasticsearch.Elasticsearch(["elasticsearch:9200"])
#es = elasticsearch.Elasticsearch(["192.168.201.39:9200"], sniff_on_start=True)
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
sleep(5)
for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        v = data_stream.TPV['speed']
        w = data_stream.TPV['alt']
        x = data_stream.TPV['time']
        y = data_stream.TPV['lat']
        z = data_stream.TPV['lon']
    if x != "n/a":
        print('Speed = %s' % v)
        print('Altitude = %s' % w)
        print('Time = %s' % x)
        print('Latitude = %s' % y)
        print('Longitude = %s' % z)
        f = open("/var/www/html/map.html", "a")
        f.write("At time %s <a href=\"http://maps.google.com/maps?q=%s,%s\">Trailer 1</a><br> \n" % (x, y, z))
        #f.write("At time %s, Latitude %s, Longitude %s, Altitude %s, Speed %s\n" % (x, y, z, w, v))
        f = open("map.html", "a")
        f.write("At time %s <a href=\"http://maps.google.com/maps?q=%s,%s\">Trailer 1</a><br> \n" % (x, y, z))
        #f.write("At time %s, Latitude %s, Longitude %s, Altitude %s, Speed %s\n" % (x, y, z, w, v))
        y = float(y)
        z = float(z)
        es.index(
            index = "gps_index",
            id = random.randint(5, 1000),
            doc_type = "_doc",
            body = {
                "text": "At time %s" % x,
                "location": {
                    "lat": "%f" % y,
                    "lon": "%f" % z
                }
            }
        )
        sleep(1)
        break
