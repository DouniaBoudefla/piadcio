import spidev
import RPi.GPIO as GPIO
import toml

class MCP3208:

    # Inputs and Outputs pins 
    CLK    = 23 # Clock
    DIN    = 19 # Digital in MOSI
    DOUT   = 21 # Digital out MISO

    def __init__(self, spi_bus=0, spi_cs=0, spi_max_speed_hz=5000, cs_pin=24):
        #Initialize SPI
        self.spibus = spidev.SpiDev()
        self.spibus.open(spi_bus,spi_cs)
        self.spibus.max_speed_hz = spi_max_speed_hz

        self.CS = cs_pin

        self._gpio_setup()

    def _gpio_setup(self):
        # Turn OFF Warnings
        GPIO.setwarnings(False)

        # We use board numbering system
        GPIO.setmode(GPIO.BOARD)

        # Set pins CLK/DIN/CS as Outputs
        GPIO.setup(self.CLK, GPIO.OUT)
        GPIO.setup(self.DIN, GPIO.OUT)
        GPIO.setup(self.CS, GPIO.OUT)

        # Set pin for DOUT as Input
        GPIO.setup(self.DOUT, GPIO.IN)

        # Flick the Chip-Select to awake the MCP
        GPIO.output(self.CS, GPIO.HIGH)
        GPIO.output(self.CS, GPIO.LOW)
        GPIO.output(self.CLK, GPIO.LOW)

    def read_adc_channel(self, spi, channel):
        (msg_up, msg_dn) = (
            (0x06, 0x00) if channel == 0
            else (0x06, 0x40) if channel == 1
            else (0x06, 0x80) if channel == 2
            else (0x06, 0xC0) if channel == 3
            else (0x07, 0x00) if channel == 4
            else (0x07, 0x40) if channel == 5
            else (0x07, 0x80) if channel == 6
            else (0x07, 0xC0) 
        )

        resp = spi.xfer([msg_up, msg_dn,0x00])
        value = (resp[1] << 8) + resp[2]
        value = int(value)

        if value <= 0:
            value = 0
        elif value > 4095:
            value = 4095

        return value
    
    def read_all_adc_channels(self, spi, config): 
        num_average = config['num_average']

        values = [0]*8

        # We do multiple measurements and average
        for i in range(num_average):
            for channel in range(8):
                values[channel] += self.read_adc_channel(channel)
        return [int(value / num_average) for value in values]
    
    def close(self):
        self.spibus.close()
        GPIO.cleanup()

    def read_config(config_file):
        # load config file
        with open(config_file, "r") as f:
            config = toml.load(f)
        return config

#-----------------
from time import sleep

def main():
    adc = MCP3208()
    try:
        while True: 
            value = adc.read_adc_channel(adc.spibus, 0)
            print("Value for channel 0: ")
            print(value)

            config = adc.read_config()
            values = adc.read_all_adc_channels(adc.spibus, config)
            print("Values for all channels: ")
            print(values)

            sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        adc.close()

if __name__ == "__main__":
    main()



