import pypot.dynamixel
import datetime
import time


dxl = pypot.dynamixel.DxlIO('/dev/ttyUSB0', 1000000)
dxl.scan(range(10))  # so that we have info about the motor

cycle = 4       # how long in seconds is a cycle (up/down=180deg)
minutes = 1     # now many minutes to run the test
# sets moving speed in degrees per second
dxl.set_moving_speed({1:180/cycle})
# bring home
dxl.set_goal_position({1:0})
# wait to go into position
time.sleep(5)

for i in range (minutes * 60 / cycle):   
        for position in [90,0]:
                # set to position degree
                dxl.set_goal_position({1:position})
                # it will take cycle/2 seconds to get there
                # during this time we will read the servo information and dump it
                # 10 times a second (10Hz)
                for j in range (5 * cycle):
                        data = dxl.get_present_position_speed_load([1])
                        # we only need the first motor
                        d = data[0]
                        # read the temp
                        temp =  dxl.get_present_temperature([1])
                        d += temp
                        timestamp = datetime.datetime.now()
                        print '%s, %.2f, %.2f, %.2f, %.2f' % (timestamp, d[0], d[1], d[2], d[3])
                        time.sleep(0.1)