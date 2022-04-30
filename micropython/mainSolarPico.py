#RUNS ON PICO
from bipolarStepper import BipolarStepper
from machine import Pin, I2C, Timer
from machine_i2c_lcd import I2cLcd
import sys, time, _thread


class MyLCD:
    ''' LCD1602 screen '''
    def __init__(self):
        
        #i2c detection
        i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
        l=i2c.scan() #liste les adresses I2C trouvées
        try:   
            i2c_adr = hex(l[0])
            print('Init LCD, adresse I2C: ', i2c_adr)
        except:
            print('aucun LCD I2C trouvé, vérifiez vos branchements...')
            sys.exit()
        
        self.lcd = I2cLcd(i2c, int(i2c_adr), 2, 16)
        
        # generator custom character: http://omerk.github.io/lcdchargen/
        charmap = [
            #chr(0): logo papsdroid
            [0b01110,0b11111,0b10101,0b11111,0b11111,0b10001,0b11111,0b01110],
            #chr(1): fusée
            [0b00100,0b01110,0b01010,0b11111,0b11111,0b11111,0b10101,0b10001],
            #chr(2): pi
            [0b00000,0b00000,0b11111,0b01010,0b01010,0b01010,0b10011,0b00000],
            #chr(3): batterie full
            [0b01110,0b11011,0b10001,0b10101,0b10101,0b10101,0b10001,0b11111],
        ]
        for i in range(len(charmap)):
            self.lcd.custom_char(i,charmap[i])
        
        self.id_day=0    # updated with motor rotation
        self.id_mode=0   # updated with mode change
        self.mode=''     # updated with mode change
    
        self.msg_init()
    
    def msg_init(self):
        '''displsay init message'''
        self.lcd.clear()
        self.lcd.move_to(0,0)
        self.lcd.putchar(chr(0)) #logo paspdroid
        self.lcd.putstr(' PapsDroid.fr ')
        self.lcd.putchar(chr(0))
        self.lcd.putchar(chr(2))
        self.lcd.putstr('\n'+' PICOPLANETES ')
        self.lcd.putchar(chr(2))
        time.sleep(1)
       
    def displ_mode(self):
        ''' display mode'''
        self.lcd.move_to(0,0)
        self.lcd.putstr('Mode: ')
        for _i in range(self.id_mode+1):
            self.lcd.putchar(chr(3))
        for _i in range(4-self.id_mode):
            self.lcd.putchar(' ')
        self.lcd.move_to(12,0)
        self.lcd.putstr(self.mode)
        
        
    def displ_jour(self, _tm):
        '''display day number, called in Timer every 200ms'''
        str_day = str(self.id_day)
        self.lcd.move_to(0,1)
        self.lcd.putstr('Jour: ' + str_day)
    
class Application:
    
    def __init__(self):
        ''' initialize lcd, push Button and stepper motor'''
        self.mylcd = MyLCD();
        self.ledStatus = Pin(25, Pin.OUT)     # led témoin du pico
        self.buttonMode = Pin(18, Pin.IN, Pin.PULL_DOWN) #bouton poussoir avec resistance de rappel activée
        self.buttonNext = Pin(19, Pin.IN, Pin.PULL_DOWN) #bouton poussoir avec resistance de rappel activée
        self.id_mode=0
        self.l_modes = ['+01J', '+07J', '+30J', '+inf']
        self.bouncetime = 0.05 #stabilization period with push buttons
        #callback function called with push buttons
        self.buttonMode.irq(self.callbackMode, Pin.IRQ_FALLING)
        self.buttonNext.irq(self.callbackNext, Pin.IRQ_FALLING)
        self.buttonModePressed = False #button not pressed
        self.buttonNextPressed = False #button not pressed
        self.bp = BipolarStepper()     #stepper motor
        self.l_step_day = self.bp.split_steps(7) # split steps into 7 phases
        self.id_day = 0
        self.motorON = False       # False: motor is Off, True: motor is On
        self.ledStatus.value(0)    # led pico off
        #init motor
        self.bp.set_speed('low')
        self.bp.next_steps(nsteps=100)
        self.bp.set_speed('high')
        self.mylcd.lcd.clear()
        self.mylcd.mode = self.l_modes[self.id_mode]
        self.mylcd.id_day = self.id_day
        self.mylcd.displ_mode()
        #self.mylcd.displ_jour()
        self.timLCD = Timer(period=200, callback=self.mylcd.displ_jour) #timer update LCD toutes les 200 ms
        self.loop()  #inifinite loop of events     
    
    def callbackMode(self, pin):
        ''' callback function called when buttonMode is pushed '''
        time.sleep(self.bouncetime)      # wait stabilization to avoid rebounds.
        if not(self.buttonMode.value()): # push button still pressed after the stabilization period ?
            if (self.buttonModePressed == False) : # run only 1 time the callbac
                self.buttonModePressed = True
                self.id_mode = (self.id_mode + 1) % len(self.l_modes) # next mode
                #print('mode: ', self.l_modes[self.id_mode])
                self.mylcd.id_mode = self.id_mode
                self.mylcd.mode = self.l_modes[self.id_mode]
                self.mylcd.displ_mode()
 
    def callbackNext(self, pin):
        ''' callback function called when buttonNext is pushed '''
        time.sleep(self.bouncetime)      # wait stabilization to avoid rebounds.
        if not(self.buttonNext.value()): # push button still pressed after the stabilization period ?
            if (self.buttonNextPressed == False) : # run only 1 time the callback
                self.buttonNextPressed = True
       
    def move_1_day(self):
        ''' rotate stepper motor for 1 day '''
        self.id_day += 1
        #print('day: ', self.id_day)
        self.mylcd.id_day = self.id_day
        self.bp.next_steps(nsteps=self.l_step_day[self.id_day % 7]) #move motor: next day

    def move_1_week(self):
        ''' rotate stepper motor for 1 week '''
        for _i in range(7):
            self.move_1_day()

    def move_4_weeks(self):
        ''' rotate stepper motor for 4 weeks '''
        for _i in range(30):
            self.move_1_day()

    def loop(self):
        ''' infinite loop of events '''
        while(True):

            self.buttonModePressed = False           
 
            #gestion du moteur, bouton 'next' pressé
            if self.buttonNextPressed :
                if self.id_mode <3 :
                    self.motorON = True
                    self.ledStatus.value(1)   #led pico on
                    if (self.id_mode == 0):
                        self.move_1_day()
                    elif (self.id_mode == 1):
                        self.move_1_week()
                    else:
                        self.move_4_weeks()
                    self.ledStatus.value(0)   #led pico off
                    self.motorON = False
            
                #mode infini 
                else:
                    self.motorON = not(self.motorON)
                    #gestion alumage pico led
                    self.ledStatus.value(self.motorON) 

                self.buttonNextPressed = False
            
            #mode infini et motor ON
            if (self.id_mode==3 and self.motorON):
                self.move_1_day()           
            else:
                time.sleep(0.2)

appl=Application()

