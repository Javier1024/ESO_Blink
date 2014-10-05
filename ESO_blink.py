#
# ESO blink v0.1
# Written by: Paul Anthony Wilson
# E-mail: paultheastronomer@gmail.com
#
# 3. Oct. 2014 - Program uploaded to PC
# 

import os
from pyquery import *
from time import sleep
from multiprocessing import Process

def blink_tool(arg):
    os.system('./blink1-tool '+arg)

def getData():
  html = PyQuery(url='http://www.ls.eso.org/lasilla/dimm/meteo_light.html')
  trs = html('tr')

  WindSpeed = 0
  Humidity = 0

  for tr in trs:
    tds = tr.getchildren()
    if tds[0].text == 'Wind Speed:':
      WindSpeed = float(tds[3].text)
    if tds[0].text == 'Humidity:':
      Humidity = float(tds[3].text)  
  return WindSpeed, Humidity

def CheckConditions():
  
  blink_tool('--off')
  
  while True:
    print "Collecting data"
    WindSpeed, Humidity = getData()

    print "\nWind:",WindSpeed,"m/s\t\tHumidity:",Humidity,"%\n"

    # RED - close everything!
    if 20. <= WindSpeed or 90. <= Humidity:
      blink_tool('--rgb 0xFF,0,00 --blink 3')
      blink_tool('--rgb 0xFF,0,00')
      #sleep(60)
    # Pointing restriction or close NTT + 2P2
    elif 12. <= WindSpeed < 20. or 70. <= Humidity < 90.:
      blink_tool('--rgb 0xff,0x8c,0x00 --blink 1')#Orange
      blink_tool('--rgb 0xFF,0,00 --blink 3')#red
      blink_tool('--rgb 0xff,0x8c,0x00 --blink 1')#orange
      blink_tool('--rgb 0xFF,0,00 --blink 3')#red
      blink_tool('--rgb 0xff,0x8c,0x00')#orange
      #sleep(30)
    # YELLOW - be aware!
    elif 10. <= WindSpeed < 12. or 50. <= Humidity < 70.:
      blink_tool('--rgb 0xff,0xff,0x00 -t 1000 --blink 30')
      #sleep(5)
    #sleep(60)
  
if __name__ == "__main__":
    p = Process(target=CheckConditions)
    p.start()
