import sys, json, time, getopt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse

mc = ModbusClient(method='rtu', port='/dev/ttyUSB0', stopbits=1, bytesize=8, parity='N', baudrate=9600, timeout=5, unit=1)

con = mc.connect()

r = mc.read_holding_registers(20, 4, unit=1)
soft_major = r.registers[0] & 0x00ff
soft_minor = r.registers[1] >> 8
soft_patch = r.registers[1] & 0x00ff
hard_major = r.registers[2] & 0x00ff
hard_minor = r.registers[3] >> 8
hard_patch = r.registers[3] & 0x00ff
software_version = 'V{}.{}.{}'.format(soft_major, soft_minor, soft_patch)
hardware_version = 'V{}.{}.{}'.format(hard_major, hard_minor, hard_patch)
print(r.registers[0])
print(r.registers[1])
print(r.registers[2])
print(r.registers[3])
print(software_version)
print(hardware_version)
