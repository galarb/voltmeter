import machine

def voltage(pin_num):
    """Read the voltage from an analog pin and return the voltage value in volts.

    Args:
        pin_num (int): The pin number to read from.

    Returns:
        float: The voltage value in volts.
    """
    adc = machine.ADC(machine.Pin(pin_num))  # Create ADC object
    adc.atten(machine.ADC.ATTN_11DB)  # Set attenuation for 0-3.6V range
    adc.width(machine.ADC.WIDTH_12BIT)  # Set width to 12 bits

    reading = adc.read()  # Read the raw ADC value (0-4095)
    voltage_value = (reading / 4095.0) * 3.6  # Convert to voltage (0-3.6V)

    return voltage_value
