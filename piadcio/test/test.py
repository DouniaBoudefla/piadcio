from mcp23s08 import MCP23S08
from mcp2308 import MCP3208
from time import sleep
import toml

# Define LED pins
LED1 = 0
LED2 = 0

def read_config(config_file):
    # load config file
    with open(config_file, "r") as f:
        config = toml.load(f)
    return config

def setup_io_expander(config):
    # Initialize 2 MCP23S08

    mcp_io_expander_1 = MCP23S08(
        config["mcp23s08_1"]["spi_bus"],
        config["mcp23s08_1"]["spi_cs"],
        config["mcp23s08_1"]["spi_max_speed_hz"],
        config["mcp23s08_1"]["cs_pin"]
    )

    mcp_io_expander_2 = MCP23S08(
        config["mcp23s08_2"]["spi_bus"],
        config["mcp23s08_2"]["spi_cs"],
        config["mcp23s08_2"]["spi_max_speed_hz"],
        config["mcp23s08_2"]["cs_pin"]
    )

    return mcp_io_expander_1, mcp_io_expander_2

def setup_adc(config):
    # Define 2 MCP3208

    adc1 = MCP3208(
        config["mcp3208_1"]["spi_bus"],
        config["mcp3208_1"]["spi_cs"],
        config["mcp3208_1"]["spi_max_speed_hz"],
        config["mcp3208_1"]["cs_pin"]
    )

    adc2 = MCP3208(
        config["mcp3208_2"]["spi_bus"],
        config["mcp3208_2"]["spi_cs"],
        config["mcp3208_2"]["spi_max_speed_hz"],
        config["mcp3208_2"]["cs_pin"]
    )
        
def main():
    config = read_config("config.toml")
    mcp_io_expander_1, mcp_io_expander_2 = setup_io_expander(config)
    adc1, adc2 = setup_adc(config)

    def setup():
        mcp_io_expander_1.set_direction(0xfe) # Set all pins as inputs except the pin 0 for the LED
        mcp_io_expander_2.set_direction(0xfe) # Set all pins as inputs except the pin 0 for the LED

    def turn_on_led(io, led_pin):
        # Turn on an LED
        io.write_in_gpio_pins(1 << led_pin)

    def turn_off_led(io, led_pin):
        # Turn off an LED
        io.write_in_gpio_pins(0 << led_pin)

    def read_adc_value(adc, channel):
        # Read the value from the ADC
        adc.read_adc_channel(channel)
            
    setup()

    try:
        while True:
            # We read the value from the channel 0 from the ADC 1
            # If the value is more than 2048, the LED is turned ON
            value_adc1 = read_adc_value(adc1,0)
            if value_adc1 > 2048:
                turn_on_led(mcp_io_expander_1, LED1)
            else:
                turn_off_led(mcp_io_expander_1, LED1)

            # We read the value from the channel 0 from the ADC 2
            # If the value is less than 2048, the LED is turned ON
            value_adc2 = read_adc_value(adc2,0)
            if value_adc2 <= 2048:
                turn_on_led(mcp_io_expander_2, LED2)
            else:
                turn_off_led(mcp_io_expander_2, LED2)

            sleep(0.5)

    except KeyboardInterrupt:
        pass
    finally:
        mcp_io_expander_1.close()
        mcp_io_expander_2.close()
        adc1.close()
        adc2.close()

if __name__ == "__main__":
    main()