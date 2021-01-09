import config
import network
import utime
import ntptime
from machine import Pin,RTC
import DS1302
from ledshow import LedShow

ds = DS1302.DS1302(Pin(5),Pin(18),Pin(19))

led = LedShow()
led.clear()


rtc = RTC()

def sync_ntp():
     ntptime.NTP_DELTA = 3155644800   # 可选 UTC+8偏移时间（秒），不设置就是UTC0
     #ntptime.host = 'ntp1.aliyun.com'  # 可选，ntp服务器，默认是"pool.ntp.org"
     ntptime.settime()   # 修改设备时间,到这就已经设置好了
     ds.DateTime(rtc.datetime()) #将时间写入DS1302中


def do_connect():
    global sta_if
    sta_if = network.WLAN(network.STA_IF)    
    wifi_pass = config.wifi_config
    num = 0
    hit = 0
    while not sta_if.isconnected():
        timed_out = False
        start = utime.time()
        if num==3 :
            num = 0
        sta_if.active(True)
        sta_if.connect(wifi_pass[num]["ssid"], wifi_pass[num]["password"])
        while not sta_if.isconnected() and not timed_out:        
            if utime.time() - start >= 20:
                timed_out = True
            else:
                pass
        num +=1
        
        if hit >20 :
            break
        hit += 1
    
    netinfo = sta_if.ifconfig()    
    print('network config:', netinfo) 
    led.Start()

    


do_connect()

if sta_if.isconnected():
    sync_ntp() #如果联网，更新网络时间，同步到DS1302
else:        
    rtc.datetime(ds.DateTime())
    rtc.datetime() #如果不联网，将DS1302时间同步到ESP32


