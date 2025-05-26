import odrive
import pymodbus
import odrive.enums
from time import sleep
from pyModbusTCP.server import ModbusServer, DataBank

print('starting server')
server = ModbusServer(host='192.168.1.10',port=702,no_block=True)
db = server.data_bank

#odrv0 = odrive.find_any()
#odrv0.clear_errors()
#odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
#odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
#odrv0.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
#odrv0.axis1.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
#odrv0.axis1.controller.input_vel = 1

try:
    print("Start server...")
    server.start()
    print("Server is online")
    db.set_holding_registers(0, [0] * 10)
    state = [0] * 10

    while True:
        new_state = db.get_holding_registers(0,10)
        print(new_state)
        DataBank.set_words(0, 5) 
        
        db.set_holding_registers(0, 1) #status 1 - works

        if state[1] != new_state[1]:
            state = new_state
            #odrv0.axis0.controller.input_vel = new_state[1]
            print("Value of Register has changed to " +str(state))
        sleep(0.5)

except Exception as e:
    db.set_holding_registers(0, 2) #status 2 or 0 - does not work
    print("Shutdown server ...")
    print(f"Error: {e}")
    server.stop()
    print("Server is offline")
"""
odrv0 = odrive.find_any()
odrv0.clear_errors()
odrv0.axis0.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.config.control_mode = odrive.enums.CONTROL_MODE_POSITION_CONTROL


odrv0.axis0.controller.input_pos += 1
"""
print('kupadupa')