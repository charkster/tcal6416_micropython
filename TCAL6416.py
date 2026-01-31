import machine

class TCAL6416():

    def __init__(self, i2c, slave_id=0x20):

        self.i2c                   = i2c
        self.slave_id              = slave_id
        self.INPUT_BASE_ADDR       = 0x00
        self.OUTPUT_BASE_ADDR      = 0x02
        self.CFG_BASE_ADDR         = 0x06
        self.INPUT_LATCH_BASE_ADDR = 0x44
        self.PULL_ENABLE_BASE_ADDR = 0x46
        self.PULL_SELECT_BASE_ADDR = 0x48
    
    def write_data(self, address=0x00, data=0x00, num_bytes=0):
        self.i2c.writeto_mem(self.slave_id, address, bytearray(data, "ascii"), addrsize=8) # MicroPython

    def read_data(self, address=0x00, num_bytes=1):
        return int.from_bytes(self.i2c.readfrom_mem(self.slave_id, address, num_bytes, addrsize=8)) # MicroPython
    
    def set_pins(self, val=0x0000): # set output value of all pins, if configured as output
        self.write_data(self.OUTPUT_BASE_ADDR, [(val & 0xFF), ((val>>8) & 0xFF)] )
    
    def set_pin(self, bank_pin=(1,7), val=0): # bank values are 0 and 1, pin values are 0 thru 7
        bank = bank_pin[0]
        pin  = bank_pin[1]
        orig_value = self.read_data(self.OUTPUT_BASE_ADDR + bank, 1)
        new_value  = (orig_value & (~(1<<pin))) + (value<<pin)
        self.write_data( self.OUTPUT_BASE_ADDR + bank, [new_value] )
    
    def config_pins(self, cfg=0xFFFF): # high is input, low is output
        self.write_data( self.CFG_BASE_ADDR, [(cfg & 0xFF), ((cfg>>8) & 0xFF)] )
    
    def config_pin(self, bank_pin=(1,7), dir='output'):
        if (dir.lower() == 'output'):
            dir_val = 0
        else: # input is the default
            dir_val = 1
        bank = bank_pin[0]
        pin  = bank_pin[1]
        orig_value = self.read_data(self.CFG_BASE_ADDR + bank, 1)
        new_value  = (orig_value & (~(1<<pin))) + (dir_val<<pin)
        self.write_data( self.OUTPUT_BASE_ADDR + bank, [new_value] )
    
    def read_pins(self):
        return self.read_data(self.INPUT_BASE_ADDR, 2)
    
    def read_pin(self, bank_pin=(1,7)):
        bank = bank_pin[0]
        pin  = bank_pin[1]
        return ( self.read_data(self.INPUT_BASE_ADDR + bank, 1) & (1<<pin) ) >> pin
    
    def set_pull_ups(self, cfg=0xFFFF): # high value means pull-up enabled, if configured as input
        # read-modify-write PULL_ENABLE, high is enabled
        orig_value = self.read_data(self.PULL_ENABLE_BASE_ADDR, 1)
        new_value  = (orig_value & (~(cfg & 0xFF))) + (cfg & 0xFF)
        self.write_data(self.PULL_ENABLE_BASE_ADDR, [new_value])
        orig_value = self.read_data(self.PULL_ENABLE_BASE_ADDR + 1, 1)
        new_value  = (orig_value & (~((cfg>>8) & 0xFF))) + ((cfg>>8) & 0xFF)
        self.write_data(self.PULL_ENABLE_BASE_ADDR + 1, [new_value])
        # read-modify-write PULL_SELECT, high is pull-up, low is pull-down
        orig_value = self.read_data(self.PULL_SELECT_BASE_ADDR, 1)
        new_value  = (orig_value & (~(cfg & 0xFF))) + (cfg & 0xFF)
        self.write_data(self.PULL_SELECT_BASE_ADDR, [new_value])
        orig_value = self.read_data(self.PULL_SELECT_BASE_ADDR + 1, 1)
        new_value  = (orig_value & (~((cfg>>8) & 0xFF))) + ((cfg>>8) & 0xFF)
        self.write_data(self.PULL_SELECT_BASE_ADDR + 1, [new_value])
    
    def set_pull_up(self, bank_pin=(1,7)):
        bank = bank_pin[0]
        pin  = bank_pin[1]
        # read-modify-write PULL_ENABLE, high is enabled
        orig_value = self.read_data(self.PULL_ENABLE_BASE_ADDR + bank, 1)
        new_value  = (orig_value & (~(1<<pin) & 0xFF)) + (1<<pin)
        self.write_data(self.PULL_ENABLE_BASE_ADDR, [new_value])
        # read-modify-write PULL_SELECT, high is pull-up, low is pull-down
        orig_value = self.read_data(self.PULL_SELECT_BASE_ADDR + bank, 1)
        new_value  = (orig_value & (~(1<<pin) & 0xFF)) + (1<<pin)
        self.write_data(self.PULL_SELECT_BASE_ADDR, [new_value])
    
    def set_pull_downs(self, cfg=0xFFFF): # high value means pull-down enabled, if configured as input
        # read-modify-write PULL_ENABLE, high is enabled
        orig_value = self.read_data(self.PULL_ENABLE_BASE_ADDR, 1)
        new_value  = (orig_value & (~(cfg & 0xFF))) + (cfg & 0xFF)
        self.write_data(self.PULL_ENABLE_BASE_ADDR, [new_value])
        orig_value = self.read_data(self.PULL_ENABLE_BASE_ADDR + 1, 1)
        new_value  = (orig_value & (~((cfg>>8) & 0xFF))) + ((cfg>>8) & 0xFF)
        self.write_data(self.PULL_ENABLE_BASE_ADDR + 1, [new_value])
        # read-modify-write PULL_SELECT, high is pull-up, low is pull-down
        orig_value = self.read_data(self.PULL_SELECT_BASE_ADDR, 1)
        new_value  = orig_value & (~cfg & 0xFF)
        self.write_data(self.PULL_SELECT_BASE_ADDR, [new_value])
        orig_value = self.read_data(self.PULL_SELECT_BASE_ADDR + 1, 1)
        new_value  = orig_value & (~(cfg>>8) & 0xFF)
        self.write_data(self.PULL_SELECT_BASE_ADDR + 1, [new_value])
    
    def set_pull_down(self, bank_pin=(1,7)):
        bank = bank_pin[0]
        pin  = bank_pin[1]
        # read-modify-write PULL_ENABLE, high is enabled
        orig_value = self.read_data(self.PULL_ENABLE_BASE_ADDR + bank, 1)
        new_value  = (orig_value & (~(1<<pin) & 0xFF)) + (1<<pin)
        self.write_data(self.PULL_ENABLE_BASE_ADDR, [new_value])
        # read-modify-write PULL_SELECT, high is pull-up, low is pull-down
        orig_value = self.read_data(self.PULL_SELECT_BASE_ADDR + bank, 1)
        new_value  = orig_value & (~(1<<pin) & 0xFF)
        self.write_data(self.PULL_SELECT_BASE_ADDR, [new_value])
    
    def clear_pulls(self, cfg=0xFFFF): # a high bit clears a pull enable
        orig_value = self.read_data(self.PULL_ENABLE_BASE_ADDR, 1)
        new_value = orig_value & (~(cfg & 0xFF))
        self.write_data(self.PULL_ENABLE_BASE_ADDR, [new_value])
        orig_value = self.read_data(self.PULL_ENABLE_BASE_ADDR + 1, 1)
        new_value = orig_value & (~((cfg>>8) & 0xFF))
        self.write_data(self.PULL_ENABLE_BASE_ADDR + 1, [new_value])

    def clear_pull(self, bank_pin=(1,7)):
        bank = bank_pin[0]
        pin  = bank_pin[1]
        orig_value = self.read_data(self.PULL_ENABLE_BASE_ADDR + bank, 1)
        new_value = orig_value & (~(1<<pin))
        self.write_data(self.PULL_ENABLE_BASE_ADDR, [new_value])

    def set_input_latch(self, cfg=0xFFFF): # high value is input latch enabled, if configured as input
        self.write_data(self.INPUT_LATCH_BASE_ADDR, [(cfg & 0xFF), ((cfg>>8) & 0xFF)])
