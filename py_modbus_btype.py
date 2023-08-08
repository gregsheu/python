import sys, json, time, getopt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse

mc = ModbusClient(method='rtu', port='/dev/ttyUSB0', stopbits=1, bytesize=8, parity='N', baudrate=9600, timeout=5, unit=1)

con = mc.connect()

rtype = mc.read_holding_registers(57348, 1, unit=1)
btype = rtype.registers[0]
print(btype)
mc.write_register(57348, 3, unit=1)
rtype = mc.read_holding_registers(57348, 1, unit=1)
btype = rtype.registers[0]
print(btype)
