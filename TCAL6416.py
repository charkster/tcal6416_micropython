import machine

class TCAL6416():

    def __init__(self, i2c, slave_address=0x20):

        self.i2c                   = i2c
        self.slave_address         = slave_address
        self.INPUT_BASE_ADDR       = 0x00
        self.OUTPUT_BASE_ADDR      = 0x02
        self.CFG_BASE_ADDR         = 0x06
        self.INPUT_LATCH_BASE_ADDR = 0x44
        self.PULL_ENABLE_BASE_ADDR = 0x46
        self.PULL_SELECT_BASE_ADDR = 0x48
    
    def set_pins(self, val=0x0000): # set output value of all pins, if configured as output
        self.i2c.writeto_mem( self.slave_address, self.OUTPUT_BASE_ADDR, bytearray([(val & 0xFF), ((val>>8) & 0xFF)]) )
    
    def set_pin(self, bank=1, pin=7, val=0): # bank values are 0 and 1, pin values are 0 thru 7
        orig_value = int.from_bytes(self.i2c.readfrom_mem(self.slave_address, (self.OUTPUT_BASE_ADDR + bank), 1))
        new_value  = (orig_value & (~(1 << pin))) + (value << pin)
        self.i2c.writeto_mem(self.slave_address, self.OUTPUT_BASE_ADDR + bank, new_value.to_bytes())
    
    def config_pins(self, cfg=0xFFFF): # high is input, low is output
        self.i2c.writeto_mem(self.slave_address, self.CFG_BASE_ADDR, bytearray([(cfg & 0xFF), ((cfg>>8) & 0xFF)]))
    
    def read_pin(self, bank=1, pin=7):
        return (int.from_bytes(self.i2c.readfrom_mem(self.slave_address, self.INPUT_BASE_ADDR + bank, 1)) & (1 << pin)) >> pin
    
    def set_pull_ups(self, cfg=0xFFFF): # high value means pull-up enabled, if configured as input
        orig_value = int.from_bytes(self.i2c.readfrom_mem(self.slave_address,  self.PULL_ENABLE_BASE_ADDR, 1))
        new_value  = (orig_value & (~cfg & 0xFF)) + (cfg & 0xFF)
        self.i2c.writeto_mem(self.slave_address, self.PULL_ENABLE_BASE_ADDR,     new_value.to_bytes())
        orig_value = int.from_bytes(self.i2c.readfrom_mem(self.slave_address, (self.PULL_ENABLE_BASE_ADDR + 1), 1))
        new_value  = (orig_value & (~(cfg>>8) & 0xFF)) + ((cfg>>8) & 0xFF)
        self.i2c.writeto_mem(self.slave_address, self.PULL_ENABLE_BASE_ADDR + 1, new_value.to_bytes())
        self.i2c.writeto_mem( self.slave_address, self.PULL_SELECT_BASE_ADDR, bytearray([(cfg & 0xFF), ((cfg>>8) & 0xFF)]) )
    
    def set_pull_downs(self, cfg=0xFFFF): # high value means pull-down enabled, if configured as input
        orig_value = int.from_bytes(self.i2c.readfrom_mem(self.slave_address,  self.PULL_ENABLE_BASE_ADDR, 1))
        new_value  = (orig_value & (~cfg & 0xFF)) + (cfg & 0xFF)
        self.i2c.writeto_mem(self.slave_address, self.PULL_ENABLE_BASE_ADDR,     new_value.ti_bytes())
        orig_value = int.from_bytes(self.i2c.readfrom_mem(self.slave_address, (self.PULL_ENABLE_BASE_ADDR + 1), 1))
        new_value  = (orig_value & (~(cfg>>8) & 0xFF)) + ((cfg>>8) & 0xFF)
        self.i2c.writeto_mem(self.slave_address, self.PULL_ENABLE_BASE_ADDR + 1, new_value.to_bytes())
        orig_value = int.from_bytes(self.i2c.readfrom_mem(self.slave_address,  self.PULL_SELECT_BASE_ADDR, 1))
        new_value  = orig_value & (~cfg & 0xFF)
        self.i2c.writeto_mem(self.slave_address, self.PULL_SELECT_BASE_ADDR,     new_value.to_bytes())
        orig_value = int.from_bytes(self.i2c.readfrom_mem(self.slave_address,  self.PULL_SELECT_BASE_ADDR + 1, 1))
        new_value  = orig_value & (~(cfg>>8) & 0xFF)
        self.i2c.writeto_mem(self.slave_address, self.PULL_SELECT_BASE_ADDR + 1, new_value.to_bytes())

    def set_input_latch(self, cfg=0xFFFF): # high value is input latch enabled, if configured as input
        self.i2c.writeto_mem( self.slave_address, self.INPUT_LATCH_BASE_ADDR, bytearray([(cfg & 0xFF), ((cfg>>8) & 0xFF)]) )
        