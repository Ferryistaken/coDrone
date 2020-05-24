import CoDrone
from CoDrone import Direction

import sys, tty, termios


drone = CoDrone.CoDrone()

power = 20
duration = 1


def main():
    print("Drone object created")
    print("Pairing Drone")
    pairStatus = drone.pair(drone.Nearest)
    if pairStatus == False:
        raise RuntimeError("Couldn't pair drone")
    elif pairStatus == True:
        print("Drone Paired")
        drone.calibrate()
        print("Drone calibrated")
        cmdcontrol()
        drone.close()

def cmdnull():
    print("Command not implemented yet\r")

def cmdhelp():
    print("Command list:\r")

def cmdtakeoff():
    print("Drone taking off\r")
    drone.takeoff()

def cmdland():
    print("Drone landing\r")
    drone.land()

def cmdemergency():
    print("EMERGENCY LANDING")
    drone.emergency_stop()

def cmdbattery():
    print("Battery Level: " + drone.get_battery_percentage())
    print("Battery Voltage: " + drone.get_battery_voltage())


def cmdleft():
    print("Drone going left\r");
    drone.set_roll(-power)
    drone.move(duration)


def cmdright():
    print("Drone going right\r");
    drone.set_roll(power)
    drone.move(duration)


def cmdup():
    print("Drone going up\r");
    drone.set_throttle(power)
    drone.move(duration)
    drone.set_throttle(0)


def cmddown():
    print("Drone going down\r");
    drone.set_throttle(-power)
    drone.move(duration)

def cmdforward():
    print("Drone going forward\r");
    drone.set_pitch(power)

def cmdbackward():
    print("Drone going back\r");
    drone.set_pitch(-power)
    drone.move(duration)


def cmdrotateclock():
    print("Drone rotating clockwise\r");
    drone.set_yaw(-power)
    drone.move(duration)



def cmdrotatecounterclock():
    print("Drone rotating counter clockwise\r");
    drone.set_yaw(power)
    drone.move(duration)

def cmdpowerincr():
    global power
    power = power + 5
    if power > 100:
        power = 100
    print("Power level: " + str(power))

def cmdpowerdecr():
    global power
    power = power - 5
    if power < 0:
        power = 0
    print("Power level: " + str(power))


def cmddurationincr():
    global duration
    duration = duration + 0.1
    if duration > 2:
        duration = 2
    print("Duration of movement: " + str(duration))

def cmddurationdecr():
    global duration
    duration = duration - 0.1
    if duration < 0.1:
        duration = 0.1
    print("Duration of movement: " + str(duration))


def cmdreset():
    drone.set_throttle(0)
    drone.set_pitch(0)
    drone.set_yaw(0)
    drone.set_roll(0)



# Function to convert number into string 
# Switcher is dictionary data type here 
switcher = {
    'd': cmdright,
    'a': cmdleft,
    'w': cmdforward,
    's': cmdbackward,
    'k': cmdup,
    'j': cmddown,
    'q': cmdrotatecounterclock,
    'e': cmdrotateclock,
    't': cmdtakeoff,
    'g': cmdland,
    ' ': cmdemergency,
    'b': cmdbattery,
    'c': cmdnull,
    '+': cmdpowerincr,
    '-': cmdpowerdecr,
    ',': cmddurationdecr,
    '.': cmddurationincr,
} 

def cmdcontrol():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())


    ch=sys.stdin.read(1)
    while( ch != 'c'):
        cmd = switcher.get(ch,cmdhelp)
        cmd()
        cmdreset()
        termios.tcflush(sys.stdin,termios.TCIFLUSH);
        print("Ready:\r")
        ch=sys.stdin.read(1)

    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    main()
