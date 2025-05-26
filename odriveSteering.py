import odrive
import odrive.enums
from time import sleep

try:
    odrv0 = odrive.find_any()
    odrv0.clear_errors()
    print('connected to odrive')
except:
    print('could not connect to odrive')

speed = 0

def MotorCalibration(axisNumber):
    if not odrv0.axis1.motor.is_calibrated and not odrv0.axis1.encoder.is_ready:
        if axisNumber ==1:
            odrv0.axis1.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        if axisNumber == 0:
            odrv0.axis0.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while not odrv0.axis1.motor.is_calibrated and not odrv0.axis1.encoder.is_ready:
            print('calibrating...')
            sleep(1)
        print('motor calibrated')
    else:
        print('motor calibrated')


while 1:
    MotorCalibration(1)
    try:
        odrv0.axis1.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL
        odrv0.axis1.controller.config.control_mode = odrive.enums.CONTROL_MODE_VELOCITY_CONTROL
        odrv0.axis1.controller.config.input_mode = odrive.enums.INPUT_MODE_PASSTHROUGH
        odrv0.axis1.controller.config.vel_limit = 15
        print('configured control setting. type in speed:')
        speed = input()
        while 1:
            odrv0.axis1.controller.input_vel = speed
            print('current speed: ', odrv0.axis1.encoder.vel_estimate)
            sleep(1)
    except:
        odrv0.axis1.controller.input_vel = 0
        print('EXCEPTION, type in anything to continue,\n'
        't for errors dump,\n'
        'r for error reset,\n'
        'e for exit')
        inCommand = input()
        if inCommand == 'e':
            break
        if inCommand == 'r':
            odrv0.clear_errors()
        if inCommand == 't':########### nie działa, sprawdzić naprawić
            print(odrv0.dump_errors())   