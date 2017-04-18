# Water animation for AEPi booth
# Author: Aaron Meyers
import time

from neopixel import *


# LED strip configuration. ONLY CHANGE STUFF WITH COMMENTS!!!
LED_COUNT      = 111     # <--Set this to the number of lights you have.
LED_PIN        = 18      # <--Set this to the GPIO pin you're using. Make sure it supports PWM!
LED_FREQ_HZ    = 800000  
LED_DMA        = 5       
LED_BRIGHTNESS = 255     # <--Brightness. Scale goes from 0 to 255.
LED_INVERT     = False   

if __name__ == '__main__':
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
  strip.begin()
  j = 0
  speed = 100 # <--Speed of the animation, in milliseconds.
  size = 4 # <--Size of animation, in number of lights. Should be less than the number of lights.
  while True:
    strip.setPixelColor((j - 1) % strip.numPixels(),0)
    for i in range(j % strip.numPixels(), (j + size) % strip.numPixels()):
      strip.setPixelColor(i, Color(0,0,255))
    strip.show()
    j += 1
    time.sleep(speed/1000.0) 
