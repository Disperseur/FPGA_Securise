
# FPGA Interface

This module provides a class `FPGA` to communicate with an FPGA device via a serial port. The class includes methods to open and close the connection, set memory addresses, write and read memory values, and display memory values on LEDs.

## Usage

1. **Initialization**: Create an instance of the `FPGA` class by providing the serial port and baud rate.
2. **Open Connection**: Use the `open_instrument` method to open the connection to the FPGA.
3. **Set Memory Address**: Use the `set_memory_addr` method to set the memory address.
4. **Write Memory Value**: Use the `write_val_mem` method to write a value to the memory.
5. **Read Memory Value**: Use the `read_mem_val` method to read a value from the memory.
6. **Display Memory Values on LEDs**: Use the `display_mem_vals_leds` method to display memory values on the FPGA's LEDs.
7. **Close Connection**: Use the `close_instrument` method to close the connection to the FPGA.

## Methods

### `__init__(self, port, baudrate)`
Initializes the FPGA class with the specified serial port and baud rate.

### `open_instrument(self)`
Opens the connection to the FPGA.

### `set_memory_addr(self, addr=0x00)`
Sets the memory address on the FPGA.

### `write_val_mem(self, val=0x00)`
Writes a value to the memory at the current address.

### `read_mem_val(self)`
Reads the value from the memory at the current address.

### `display_mem_vals_leds(self)`
Displays the memory values on the FPGA's LEDs.

### `close_instrument(self)`
Closes the connection to the FPGA.

