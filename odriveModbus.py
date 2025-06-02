import odrive
import pymodbus
import odrive.enums
from time import sleep
from pyModbusTCP.server import ModbusServer, DataBank


speed = 0
def MotorCalibration(axisNumber):
    odrv0.clear_errors()
    if not odrv0.axis1.motor.is_calibrated or not odrv0.axis1.encoder.is_ready:
        if axisNumber ==1:
            if not odrv0.axis1.motor.is_calibrated and not odrv0.axis1.encoder.is_ready:
                odrv0.axis1.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                print('ODRV calibrating...')
                sleep(40)
        if axisNumber ==0:
            if not odrv0.axis0.motor.is_calibrated and not odrv0.axis0.encoder.is_ready:
                odrv0.axis0.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
                print('ODRV calibrating...')
                sleep(40)
    print('ODRV calibrated')

try:
    odrv0 = odrive.find_any()
    odrv0.clear_errors()
    print('ODRV connected')
    MotorCalibration(1)
    odrv0.axis1.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis1.controller.config.control_mode = odrive.enums.CONTROL_MODE_VELOCITY_CONTROL
    odrv0.axis1.controller.config.input_mode = odrive.enums.INPUT_MODE_PASSTHROUGH
    odrv0.axis1.controller.config.vel_limit = 15
except:
    print('ODRV could not connect')
    odrv0.axis1.controller.input_vel = 0

try:
    server = ModbusServer(host='192.168.0.1',port=502,no_block=True)
    db = server.data_bank
    server.start()
    print("MODBUS online")

    db.set_holding_registers(0, [0] * 16)
    state = [0] * 16
except:
    db.set_holding_registers(0, [2]) #status 2 or 0 - does not work
    server.stop()
    print("MODBUS offline")

while True:
        db.set_holding_registers(0, [1]) #status 1 - works
        db.set_holding_registers(1, [odrv0.axis1.encoder.vel_estimate*1000]) 
        new_state = db.get_holding_registers(0,16)  

        

        if state[8] != new_state[8]:
            state = new_state
            print("Value of Register has changed to " +str(state))
            print('prędkość silnika ustawiona na ', state[8])
            odrv0.axis1.controller.input_vel = state[8]
            db.set_holding_registers(1, [1])
        else:
            print(new_state)
        sleep(0.5)

