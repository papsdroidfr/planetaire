# runs on PICO

from machine import Pin
import utime
from bipolarStepper import BipolarStepper

bp = BipolarStepper(speed='medium')
bp.next_steps(100) 
utime.sleep(0.5)
bp.set_speed('high')
bp.set_direction('backward')
bp.next_steps(50)





       
            
        

