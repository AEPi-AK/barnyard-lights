# Lights for Build-a-Beast
# Author: Aaron Meyers

import time
from pprint import pprint
from neopixel import *
import sys
import requests
import colorsys


# LED strip configuration:
LED_COUNT      = 105      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


def player1Join(strip):
	while True:
		r = requests.get('http://barnyard-nuc.local/gamestate')
		gameState = r.json()
		LED_BRIGHTNESS = int(gameState["settings"]["brightness"])
		strip.setBrightness(LED_BRIGHTNESS)
		if gameState["currentPhase"] != "GameJoining" or gameState["player2"]["joined"] == True:
			return
		for q in range(3):
			for i in range(0, strip.numPixels() / 2, 3):
				strip.setPixelColor(i+q, Color(160,160,160))
			strip.show()
			time.sleep(50/1000.0)
			for i in range(0, strip.numPixels() / 2, 3):
				strip.setPixelColor(i+q, 0)


def player2Join(strip):
	while True:
		r = requests.get('http://barnyard-nuc.local/gamestate')
		gameState = r.json()
		LED_BRIGHTNESS = int(gameState["settings"]["brightness"])
		strip.setBrightness(LED_BRIGHTNESS)
		if gameState["currentPhase"] != "GameJoining" or gameState["player1"]["joined"] == True:
			return
		for q in range(3):
			for i in range(strip.numPixels(), strip.numPixels() / 2, -3):
				strip.setPixelColor(i-q, Color(160,160,160))
			strip.show()
			time.sleep(50/1000.0)
			for i in range(strip.numPixels(), strip.numPixels() / 2, -3):
				strip.setPixelColor(i-q, 0)


def player1And2Join(strip):
	while True:
		r = requests.get('http://barnyard-nuc.local/gamestate')
		gameState = r.json()
		LED_BRIGHTNESS = int(gameState["settings"]["brightness"])
		strip.setBrightness(LED_BRIGHTNESS)
		if gameState["currentPhase"] != "GameJoining":
			return
		for q in range(3):
			for i in range(0, strip.numPixels() / 2, 3):
				strip.setPixelColor(i+q, Color(160,160,160))
			for i in range(strip.numPixels(), strip.numPixels() / 2, -3):
				strip.setPixelColor(i-q, Color(160,160,160))
			strip.show()
			time.sleep(50/1000.0)
			for i in range(0, strip.numPixels() / 2, 3):
				strip.setPixelColor(i+q, 0)
			for i in range(strip.numPixels(), strip.numPixels() / 2, -3):
				strip.setPixelColor(i-q, 0)


def player1Win(strip):
	while True:
		r = requests.get('http://barnyard-nuc.local/gamestate')
		gameState = r.json()
		LED_BRIGHTNESS = int(gameState["settings"]["brightness"])
		strip.setBrightness(LED_BRIGHTNESS)
		if gameState["currentPhase"] != "GameWinner":
			return
		for q in range(3):
			for i in range(0, strip.numPixels() / 2, 3):
				strip.setPixelColor(i+q, Color(200,60,0))
			strip.show()
			time.sleep(50/1000.0)
			for i in range(0, strip.numPixels() / 2, 3):
				strip.setPixelColor(i+q, 0)


def player2Win(strip):
	while True:
		r = requests.get('http://barnyard-nuc.local/gamestate')
		gameState = r.json()
		LED_BRIGHTNESS = int(gameState["settings"]["brightness"])
		strip.setBrightness(LED_BRIGHTNESS)
		if gameState["currentPhase"] != "GameWinner":
			return
		for q in range(3):
			for i in range(strip.numPixels(), strip.numPixels() / 2 + 1, -3):
				strip.setPixelColor(i+q, Color(200,60,0))
			strip.show()
			time.sleep(50/1000.0)
			for i in range(strip.numPixels(), strip.numPixels() / 2 + 1, -3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbowCycle(strip, wait_ms=1, iterations=5):
	j = 0
	while True:
		if j % 50 == 0:
			r = requests.get('http://barnyard-nuc.local/gamestate')
			gameState = r.json()
			LED_BRIGHTNESS = int(gameState["settings"]["brightness"])
			strip.setBrightness(LED_BRIGHTNESS)
			if gameState["currentPhase"] != "GameBiomePicking":
				return
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		j += 1
		time.sleep(wait_ms/1000.0)

def timer(strip, start, current):
	ratio = strip.numPixels() / (2.0 * start)
	for i in range(strip.numPixels()):
		if i > strip.numPixels() - (current * ratio):
			strip.setPixelColor(i,Color(0,0,0))
		elif i < current * ratio:
			strip.setPixelColor(i,Color(0,0,0))
		else:
			otherRatio = current / start
			hue = (1-otherRatio)*.33
			(r, g, b) = colorsys.hsv_to_rgb(hue, 1, 1)
			strip.setPixelColor(i,Color(int(r*255),int(g*255),int(b*255)))
	strip.show()

def timeUp(strip):
	while True:
		r = requests.get('http://barnyard-nuc.local/gamestate')
		gameState = r.json()
		LED_BRIGHTNESS = int(gameState["settings"]["brightness"])
		strip.setBrightness(LED_BRIGHTNESS)
		strip.show()
		if gameState["currentPhase"] != "GameTimeUp":
			return
		for i in range(strip.numPixels()):
			strip.setPixelColor(i,Color(255,0,0))
		strip.show()
		time.sleep(250/1000.0)
		for i in range(strip.numPixels()):
			strip.setPixelColor(i,0)
		strip.show()
		time.sleep(250/1000.0)

def sadReactsOnly(strip):
	j = 0
	while True:
		r = requests.get('http://barnyard-nuc.local/gamestate')
		gameState = r.json()
		LED_BRIGHTNESS = int(gameState["settings"]["brightness"])
		strip.setBrightness(LED_BRIGHTNESS)
		strip.show()
		if gameState["currentPhase"] != "GameWinner":
			return
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0,0,max(255-(j*5),0)))
		strip.show()
		j += 1
		time.sleep(100/1000.0)

def clear(strip):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,0,0))
	strip.show()

if __name__ == '__main__':
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	strip.begin()
	clear(strip)
	while True:
		r = requests.get('http://barnyard-nuc.local/gamestate')
		gameState = r.json()
		P1 = gameState["player1"]
		P2 = gameState["player2"]
		LED_BRIGHTNESS = int(gameState["settings"]["brightness"])
		strip.setBrightness(LED_BRIGHTNESS)
		strip.show()
		if gameState["currentPhase"] == "GameJoining":
			clear(strip)
			if P1["joined"] == True and P2["joined"] == True:
				player1And2Join(strip)
			elif P1["joined"] == True:
				player1Join(strip)
			elif P2["joined"] == True:
				player2Join(strip)
		elif gameState["currentPhase"] == "GameBiomePicking":
			clear(strip)
			rainbowCycle(strip,1)
		elif gameState["currentPhase"] == "GameBiomeSelection":
			if gameState["location"] == "Desert":
				color = Color(255,0,0)
			elif gameState["location"] == "Arctic":
				color = Color(0,0,255)
			elif gameState["location"] == "Grassland":
				color = Color(255,255,0)
			else:
				# rainforest
				color = Color(0,255,0)
			for i in range(strip.numPixels()):
				strip.setPixelColor(i,color)
			strip.show()
		elif gameState["currentPhase"] == "GameInProgress":
			timer(strip,float(gameState["phaseTime"]),float(gameState["timeSincePhaseStart"]))
		elif gameState["currentPhase"] == "GameTimeUp":
			clear(strip)
			timeUp(strip)
		elif gameState["currentPhase"] == "GameWinner":
			clear(strip)
			if gameState["winner"] == "Player1":
				player1Win(strip)
			elif gameState["winner"] == "Player2":
				player2Win(strip)
			else:
				sadReactsOnly(strip)
		else:
			clear(strip)
		time.sleep(50.0/1000)
