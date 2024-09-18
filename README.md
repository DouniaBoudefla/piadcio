PIADC-IO

PIADC-IO is a versatile and I/O expansion project designed to enhance the GPIO capabilities of the Raspberry Pi. The project integrates the MCP23S08 I/O expander and the MCP3208 ADC (Analog-to-Digital Converter) with the Raspberry Pi, enabling efficient control of multiple devices and precise analog signal measurements via the SPI protocol. This repository contains all the necessary resources, including schematics, PCB designs, code, and documentation, to set up and use the PIADC-IO system for various applications, such as slow control in experimental setups and monitoring analog inputs.

Features

I/O Expansion: Utilize the MCP23S08 to expand the Raspberry Pi's GPIO capabilities by 8 configurable pins per expander, supporting multiple input/output configurations.
Analog-to-Digital Conversion: Integrate the MCP3208 to enable reading from up to 8 analog input channels with 12-bit resolution.
Power Indication LED: Monitor power status with a controllable LED, which can be managed via the Raspberry Pi.
Modular and Configurable: Easily adapt the system to different hardware setups with a TOML configuration file used to define hardware-specific settings like SPI bus numbers and chip select lines.

Repository Structure

pcb/ - Includes PCB design files and contains the electronic schematics used for the project, designed in KiCad.
src/ - Source code for interacting with the MCP23S08 and MCP3208, including Python classes for each.

Preliminary Configuration

Before starting, you need to enable the SPI function on your Raspberry Pi using 'raspi-config'.
The Raspberry Pi have 2 different SPI bus: one will be known as /dev/spi0.* and the other as /dev/spi1.*.

Enabling SPI1

if '/dev/spi1.0' and '/dev/spi1.1' are not available, you need to enable SPI1 manually:

1. Edit the boot configuration file:

        sudo nano /boot/config.txt

2. Add the following lines at the end of the file to enable SPI1:

        dtparam=spi=on
        dtoverlay=spi1-3cs

3. Save the file and exit the editor (Ctrl + O, Enter, Ctrl + X)
4. Reboot your Raspberry Pi to apply the changes:

        sudo reboot

After rebooting, you should see '/dev/spi1.0' and '/dev/spi1.1' available for use.


Communication with MCP23S08

To communicate with MCP23S08, you need to send and receive data via the SPI interface. Here is how you can read from and write to the the MCP23S08 registers using Python with the 'spidev' library.

Understanding MCP23S08 Communication

Commmand Structure

Communication with the MCP23S08 involves sending a sequence of bytes over the SPI interface. 
Each command generally consists of the following parts:

- Opcode: Determines whether the operation is a read or write
- Register Address: Specifies which register to access
- Data: The value to write to the register (for write operations)

Opcode

Write Opcode: Ox40 (A0=0, A1=0)
Read Opcode: 0x41 (A0=0, A1=0)

The opcode is followed by the register address and then the data byte

Register Address

The MCP23S08 has several registers for configuring and controlling the I/Os. Here are some key registers:

- IODIR (0X00): I/O Direction Register (1 = input, 0 = output)
- GPIO (0x09): GPIO Register (read/write I/O values)
- OLAT (0x0A): Output Latch Register (maintain output values)

Data 

The data byte is the value you write to the register. For read operations, the data byte received from the MCP23S08 will contain the registers's current value. 





