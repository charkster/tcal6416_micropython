import machine
import TCAL6416

i2c = machine.I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
tcal = TCAL6416.TCAL6416(i2c=i2c)

tcal.set_pins(0x0002)
tcal.config_pins(0xFFFD)

# tuple is (bank, pin)
board_dict = { 'signal_in1'   : (0,0),
               'signal_out2'  : (0,1),
               'signal_out16' : (1,7) }

tcal.set_pin(board_dict['signal_out1' ], 0)
tcal.set_pin(board_dict['signal_out16'], 1)

tcal.config_pin(board_dict['signal_in1'  ], 'input')
tcal.config_pin(board_dict['signal_out1' ], 'output')
tcal.config_pin(board_dict['signal_out16'], 'output')

tcal.set_pull_down(board_dict['signal_in1'])

print("signal_in1 has value {:d}".format(tcal.read_pin(board_dict['signal_in1'])))
