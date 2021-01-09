from machine import Pin,ADC
from neopixel import NeoPixel
import aztxt
import time
import math


class LedShow:
    def __init__(self):
        self.led_number = 120
        self.led_pin = 12
        self.np = NeoPixel(Pin(12,Pin.OUT),self.led_number)
        self.KEY1=Pin(27,Pin.IN,Pin.PULL_UP)
        #麦克风
        self.micc = ADC(Pin(34))
        self.micc.atten(self.micc.ATTN_11DB)
        # 144led 变态RGB 实际为GRB
        self.color = [
            (0,0,0),#黑
            (255,0,0),#绿
            (255,255,0),#黄
            (255,255,0),#橙色
            (0,255,0),#红
            (255,0,255),#青色
            (0,0,255),#蓝色
            (0,255,255),#粉红
            (255,255,255),#白
            (247,238,214),#米黄
            (0,0,128),#蓝色
            ] #七彩

    def clear(self):
        for i in range(self.led_number):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def Start(self):
        for x in range(6):
            for y in range(10):
                self.np[x*10+y] = self.color[6]
                self.np[119-x*10-y] = self.color[6]
            time.sleep(0.1)
            self.np.write()
        for x in range(6):
            for y in range(10):
                self.np[(x+6)*10+y] = self.color[0]
                self.np[59-x*10-y] = self.color[0]
            time.sleep(0.1)
            self.np.write()
        
    
    def PrintDot(self,eTxt,cr=6):
        ctext  =aztxt.Zifu[eTxt]
        for x in range(0,8):
            for y in range(0,8):
                if ctext[x][y] is 1:
                    self.np[9-x+y*10]=self.color[cr]
        self.np.write()

    def SetColor(self,cc=6):
        for x in range(self.led_number):            
            self.np[x] = self.color[cc]
            self.np.write()

    def VuColor(self,val,cc=6):
        htt = val
        for x in range(12):
            
            for y in range(10):
                if y < htt[x]:                    
                    self.np[x*10+y] = self.color[cc]
                elif y==htt[x]:
                    self.np[x*10+y] = self.color[10]                    
                else:
                    self.np[x*10+y] = self.color[0]           
        self.np.write()  

    def sample(self):
        values = []
        start = time.ticks_ms()
        for i in range(16):
            val = self.micc.read()
            values.append(val)
        return (time.ticks_ms() - start, max(values) - min(values))

    def getloudness(self):
        maxloudness = 0
        for i in range(8):
            timetaken, loudness = self.sample()  
            if loudness > maxloudness:
                maxloudness = loudness
        val = maxloudness*10/3000
        return math.floor(val)

    def micphone(self):
        while True:
            tones = []
            for i in range(12):
                t = self.getloudness()
                tones.append(t) 
            print(tones)       
            self.VuColor(tones)
            if self.KEY1.value() == 0:     #按键被按下
                time.sleep_ms(2)    #消除抖动
                if self.KEY1.value() == 0:   #确认按键被按下
                    print("Key1 close")
                    break


    
        
        


