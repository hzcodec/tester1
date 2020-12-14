from common_files.common import *
from common_files.common_mcp23s17 import *

MCP1 = {
           "Device": str(MCP23S17_DEVICE_0),
           "SPI-addr": str(SPI_ADDRESS_0),
           "Reg": hex(SPI_IODIRA), 
           "Port": str(SPI_GPA0),
           "Mode": str(OUT)}

MCP2 = {
           "Device": str(MCP23S17_DEVICE_0),
           "SPI-addr": str(SPI_ADDRESS_0),
           "Reg": hex(SPI_GPIOA),
           "Port": str(SPI_GPA0),
           "Mode": str(HIGH)}

AD1 = {
           "Device": str(AD4112_DEVICE_0),
           "SPI-addr": str(SPI_ADDRESS_0)}
