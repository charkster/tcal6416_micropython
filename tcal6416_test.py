import machine
import TCAL6416

i2c = machine.I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000) #Xiao RP2350
tcal = TCAL6416.TCAL6416(i2c=i2c)

tcal.config_pins(0xFFFE)
tcal.set_pins(0x0001)
tcal.set_pins(0x0000)
