#Include the library files
import machine, onewire, ds18x20
from machine import ADC, Pin, Timer, I2C
from time import sleep
import utime
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

led = Pin(3, Pin.OUT) #Include the LED pin
potentiometer = ADC(28) #Include the potentiometer pin
ds_pin = machine.Pin(27)
 
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
conversion_factor = 3.3 / (65535)
switch = Pin(16, Pin.OUT) #Include the relay switch pin
button = Pin(17, Pin.IN, Pin.PULL_DOWN) 
logic_state = 0  


lcd.move_to(6,0)                       #
lcd.putstr("CZESC")             #  LCD      #
lcd.move_to(5,1)                       # DISPLAY
lcd.putstr("MIECIU!")
sleep(4)                            # #
lcd.clear()
  
    
    
def working():
    switch.value(0)
    led.value(1)
    lcd.move_to(0,0)                       #
    lcd.putstr("Zadaj temp: ")             #  LCD
    lcd.putstr(str(round(set_temp)))       #
    lcd.move_to(1,1)                       # DISPLAY
    lcd.putstr("Temp: ")                   #
    lcd.putstr(str(round(reading)))

def wygaszanie():
    led.value(0)
    switch.value(1)           
    lcd.move_to(0,0)
    lcd.putstr("Wyl. grzania...")
    lcd.move_to(1,1)
    lcd.putstr("Temp: ")
    lcd.putstr(str(round(reading)))
    
                
if __name__ == '__main__':
    
   while True:
        #Waiting for button click
        
        if button.value() == 0:
            if logic_state==0:
                print(button.value())
                led.value(0)
                sleep(0.1)
                lcd.putstr("WLACZ ")
                lcd.move_to(1,1)
                lcd.putstr("GRZALKE")
                switch.value(1)
                sleep_ms=100
                while button.value() == 0:
                    logic_state=1
            
            while True:              #Performing main loop
                
                
                ds_sensor.convert_temp()
                for rom in roms:
                    print(ds_sensor.read_temp(rom))
                #reading = sensor_temp.read_u16() * conversion_factor   #reading Temp
                reading = ds_sensor.read_temp(rom)         #converting voltages to celsius
                utime.sleep(0.1)
                #print("temp: ",reading)    #Print value on the shell
                
                value = potentiometer.read_u16() * conversion_factor  #Setting temp
                set_temp = (value - 0.5) * 35                         #converting voltages to celsius
                utime.sleep(0.1)
                #print("set temp: ",set_temp)    #Print value on the shell
                
                
                if (round(set_temp - reading)) >= 2:
                    utime.sleep(0.1)#reading + 2 < set_temp:
                    working()

                    print(round(set_temp - reading))
                                
                elif reading > set_temp:
                    utime.sleep(0.1)
                    wygaszanie()
                
                
                else:                                   #keep heating
                    print("Test")
                    
                if button.value() == 1:                 #finish loop
                    lcd.clear()
                    logic_state=0
                    break
