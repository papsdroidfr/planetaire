# bipolar stepper motor controled by L298N & Raspberry PICO
# https://www.papsdroid.fr
# October 2021

from machine import Pin
import utime

class BipolarStepper():
    ''' bipolar stepper motor controled by L298N & Raspberry PICO
            In1 - pin14 - A
            In2 - pin15 - A/
            In3 - pin16 - B
            In4 - pin17 - B/
        init parameters
            speed: 'high' (default), 'medium', 'low', or 'test'
            direction: 'forward' (default) , 'backward'
        methods:
            set_direction(direction) # set direction either 'forward' or 'backward'
            set_speed(speed)         # set motor speed (delay between 2 steps)
            next_step(nbsteps)       # move motor *nsteps
        
        example:
            bp = BipolarStepper(speed='medium')
            bp.next_step(100) # move 100 steps forward speed medium
            bp.set_direction('backward')
            bp.set_speed('high')
            bp.next_step(50) # move 50 steps backward highest speed
        
    '''
    # constructor
    def __init__(self, speed='high', direction='forward', steps360=200):
        ''' constructor
            speed = 'high' (default), 'medium', 'low', 'test'
            direction = 'forward' (default), 'backward'
            steps360 (200 default): nb of steps to rotate 360°
        '''
        #speed motor: delays between 2 steps
        self.speed = {'high': 0.005,   # 5ms delay between 2 steps
                      'medium': 0.008, # 8ms delay between 2 steps
                      'low': 0.016,    # 20ms delay between 2 steps
                      'test':0.5,      # 0.5s delay between 2 steps for testing activity
                      }
        self.set_speed(speed)
        #direction forward or backward
        self.dic_direction = { 'forward':1, 'backward':-1 }
        self.set_direction(direction)
        self.steps360 = steps360
        #Raspberry PICO pins output
        self.pins = [
            Pin(14, Pin.OUT), #IN1 - A  - BLACK
            Pin(15, Pin.OUT), #IN2 - A\ - GREEN
            Pin(16, Pin.OUT), #IN3 - B  - RED
            Pin(17, Pin.OUT)] #IN4 - B\ - BLUE
        # sequences to run in circle
        self.full_step_seq = [ 
            [1,0,1,0], # AB 
            [0,1,1,0], # A/B 
            [0,1,0,1], # A/B/
            [1,0,0,1]] # AB/
        self.seq = 0   # current sequence: 0,1,2,3
        #init motor with first position seq 0
        print('init motor')
        self.move_motor()
        utime.sleep(0.5)

    # Private methods
    # -------------------------------------------------
    
    def move_motor(self):
        ''' move motor to curent step and wait
        '''
        #run current sequence
        for i in range(4):
            self.pins[i].value(self.full_step_seq[self.seq][i])
        utime.sleep(self.delay)


    # Public methods
    # ---------------------------------------------------------------
    
    def set_speed(self, speed):
        ''' motor speed: 'high' (default), 'medium', 'low' or 'test'
        '''
        try:
            self.delay = self.speed[speed]
        except:
            self.delay = self.speed['high']
    
    def set_direction(self, direction):
        ''' set direction either forward (default) or backward
        '''
        try:
            self.direction = self.dic_direction[direction]
        except:
            self.direction = self.dic_direction['forward']          
    
    def next_steps(self, nsteps=1):
        ''' move motor to the next sequence * nsteps
        '''
        for i in range(nsteps):
            self.seq = (self.seq + self.direction)%4
            self.move_motor()          

    def next_angle(self, angle=90):
        ''' move motor nsteps = steps360*angle//360 '''
        self.next_steps(self.steps360*angle//360)
    
    def split_steps(self, nsplits=1):
        ''' split steps360 into a list of nsplits equivalent steps
        '''
        l = nsplits*[self.steps360//nsplits] # list of nsplits equal steps
        r = self.steps360%nsplits   # add this value, so that sum of steps = steps360
        for i in range(r):
            l[-1-i]+= 1 #r value added from the end of the list
        return l
        
