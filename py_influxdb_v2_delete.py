from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS
import time
import os

client = InfluxDBClient(url="http://192.168.1.160:8086", token="mysupertopsecrettoken", org="myorg")
delete_api = client.delete_api()
delete_api.delete('2021-08-27T23:20:32.845Z', '2021-08-28T00:20:32.845Z', '_measurement="modbus"', bucket="mybucket", org="myorg")
