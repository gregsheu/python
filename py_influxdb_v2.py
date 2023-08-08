from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS
import time
import os
import csv

# If you want to test against a specific server
servers = []
threads = []
# If you want to use a single threaded test
results_dict = {}
influxdb_host = os.getenv('INFLUXDB')

bucket = 'mybucket'
influx = InfluxDBClient('http://192.168.1.160:8086', token='mysupertopsecrettoken', org='myorg')
#Synchronous
write_api = influx.write_api(write_options=SYNCHRONOUS)
#Asynchronous
write_api = influx.write_api(write_options=ASYNCHRONOUS)

query_api = influx.query_api()

#while True:
#    s = speedtest.Speedtest()
#    s.get_servers(servers)
#    s.get_best_server()
#    s.download(threads=threads)
#    s.upload(threads=threads)
#    s.results.share()
#    results_dict = s.results.dict()
#    #print('Download: %(download)i bits/s Upload: %(upload)i bits/s Ping: %(ping)i ms' % (results_dict))
#    results_dict.update({'measurement': 'speedtest'})
#    results_dict.update({'fields': {'download': '%(download)i' % (results_dict), 'upload': '%(upload)i' % (results_dict), 'ping': '%(ping)i' % (results_dict)}})
#    print('%(download)i %(upload)i %(ping)i' % results_dict)
#    download = int(results_dict['download'])
#    upload = int(results_dict['upload'])
#    ping = int(results_dict['ping'])
#    print('%i %i %i' % (download, upload, ping))
#
#    p1 = Point("speedtest").tag('speed', 'results').field('download', '%i' % int(download)).field('upload', '%i' % int(upload)).field('ping', '%i' % int(ping))
#    #p2 = Point("speedtest").field('upload', '%(upload)i' % results_dict)
#    #p3 = Point("speedtest").field('ping', '%(ping)i' % results_dict)
#    #write_api.write(bucket=bucket, record=[p1, p2, p3])
#    write_api.write(bucket=bucket, record=p1)
#    time.sleep(0.5)
    #tables = query_api.query('from(bucket:"mybucket") |> range(start: -1h)')

    #for table in tables:
    #    print(table)
    #    for record in table.records:
    #        print(record.values)
    #print()
    ## using Table structure
    #tables = query_api.query('from(bucket:"mybucket") |> range(start: -10m)')
    #for table in tables:
    #    print(table)
    #    for row in table.records:
    #        print (row.values)
    #
    ## using csv library
#csv_result = query_api.query_csv('from(bucket:"mybucket") |> range(start: -30d) |> filter(fn: (r) => r["_measurement"] == "modbus") |> filter(fn: (r) => r["_field"] == "Battery Volts")', dialect=Dialect(header=True, delimiter=",", comment_prefix="#", annotations=['datatype', 'group', 'default'], date_time_format="RFC3339"))
#result = ''
#for row in csv_result:
#    #print(','.join(row))
#    result += ','.join(row) + '\n'
#print(result.strip())
    #    for cell in row:
    #        val_count += 1
tables = query_api.query('from(bucket: "mybucket") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "geoip") |> filter(fn: (r) => r["_field"] == "lat" or r["_field"] == "lon") |> group(columns: ["ip", "_measurement"], mode:"by") |> unique() |> yield(name: "unique")')
context = {}
for table in tables:
    lat = None
    lon = None
    #print(table)
    for r in table.records:
        if r['_field'] == 'lat':
            lat = r['_value']
        if r['_field'] == 'lon':
            lon = r['_value']
        context.update({r['ip']: {'lat': lat, 'lon': lon, 'country': r['country'], 'host': r['host']}})
        #print(record.values)
#for k,v in context.items():
#    print(k, v)
#    row_tojson = {
#        'id': v['host'],
#        'ip': k,
#        'lat': v['lat'],
#        'lon': v['lon'],
#        'country': v['country']
#        }
#    data_list.append(row_tojson)
#print(context)
#print(len(context))
#print(data_list)
#print(len(data_list))
data_list = list({'id': v['host'], 'ip': k, 'lat': v['lat'], 'lon': v['lon'], 'country': v['country']} for k, v in context.items())
print(data_list)
print(len(data_list))
