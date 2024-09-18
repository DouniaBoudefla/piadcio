import spidev
import RPi.GPIO as GPIO

# MCP23S08 Registers
REG_IODIR   = 0x00 # I/O DIRECTION REGISTER
REG_IPOL    = 0x01 # INPUT POLARITY REGISTER
REG_GPINTEN = 0x02 # INTERRUPT-ON-CHANGE CONTROL REGISTER
REG_DEFVAL  = 0x03 # DEFAULT COMPARE REGISTER
REG_INTCON  = 0x04 # INTERRUPT CONTROL REGISTER
REG_IOCON   = 0x05 # CONFIGURATION REGISTER
REG_GPPU    = 0x06 # PULL-UP RESISTOR CONFIGURATION REGISTER
REG_INTF    = 0x07 # INTERRUPT FLAG REGISTER
REG_INTCAP  = 0x08 # INTERRUPT CAPTURE REGISTER
REG_GPIO    = 0x09 # PORT REGISTER
REG_OLAT    = 0x0A # OUTPUT LATCH REGISTER

class MCP23S08:
    def __init__(self, spi_bus=0, spi_cs=0, spi_max_speed_hz=5000, cs_pin=24):
        # Initialize SPI
        self.spibus = spidev.SpiDev()
        self.spibus.open(spi_bus, spi_cs)
        self.spibus.max_speed_hz = spi_max_speed_hz

        self.cs_pin = cs_pin

        self._gpio_setup()
    
    def _gpio_setup(self):
        # Turn OFF the warnings
        GPIO.setwarnings(False)

        # We use the board numbering system
        GPIO.setmode(GPIO.BOARD)

        # Setup GPIO for Chip Select
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.output(self.cs_pin, GPIO.HIGH)
    
    def _spi_write(self, register, value):
        # Write a value in a register
        GPIO.output(self.cs_pin, GPIO.LOW)
        self.spibus.xfer([0x40, register, value])
        GPIO.output(self.cs_pin, GPIO.HIGH)

    def _spi_read(self, register):
        # Read the value from a register
        GPIO.output(self.cs_pin, GPIO.LOW)
        value = self.spibus.xfer([0x41, register, 0x00])
        GPIO.output(self.cs_pin, GPIO.HIGH)
        return value[2]
    
    def set_direction(self, direction):
        # Set the direction of the GPIO pins
        self._spi_write(REG_IODIR, direction)

    def write_in_gpio_pins(self, value):
        # Write a value in GPIO pins
        self._spi_write(REG_GPIO, value)

    def read_all_gpio_pins(self):
        # Read the state of all pins
        return self._spi_read(REG_GPIO)
    
    def print_state_pins(self):
        # Print the state of all pins
        state = self.read_all_gpio_pins()
        temp = 0x01
        for i in range(0,8):
            pin = state & temp
            if pin == temp:
                print("Pin ", i, ' is HIGH \n')
            else:
                print("Pin ", i, "is LOW \n")
            temp = temp << 1

    
    def close(self):
        # Finish the SPI communication and cleanup GPIO
        self.spibus.close()
        GPIO.cleanup()

#-----------------

def main():
    mcp = MCP23S08()
    try:
        print("We set all pins HIGH:\n")
        mcp.set_direction(0x00) # Set all pins as output
        mcp.write_in_gpio_pins(0xff) # Set all pins HIGH
        mcp.print_state_pins() # Print state of all pins

        print("\nWe set all pins LOW:\n")
        mcp.write_in_gpio_pins(0x00) # Set all pins LOW
        mcp.print_state_pins() # Print state of all pins
    except KeyboardInterrupt:
        pass
    finally:
        mcp.close()

if __name__ == "__main__":
    main()





    
