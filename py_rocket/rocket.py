import time
import math
import cv2
from PIL import Image
from mss import mss
import numpy as np
import mss.tools
import os
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def screenshot():
    monitor = {"top": 0, "left": 0, "width": 960, "height": 1080}
    im =  sct.grab(monitor)
    im = Image.frombytes("RGB", im.size, im.rgb)
    im = np.array(im) 
    im = im[:, :, ::-1].copy()
    return im

class World(object):
    def __init__(self):
        self.time=time.time()
        self.dt = None
        self.old_times = []
        self.rocket = None
        self.platform = None

    def __str__(self):
        out = "time=" + str(self.time)
        out = out + "\n"
        out = out + "dt=" + str(self.dt)
        out = out + "\n"
        out = out + ", rocket=" + str(self.rocket)
        out = out + "\n"
        out = out + ", platform=" + str(self.platform)
        return out

    def calcDelta(self, old):
        self.dt = self.time - old.time
        self.old_times = ([self.time] + old.old_times)[:20]
        if self.rocket and old.rocket:
            self.rocket.old_angles = ([self.rocket.angle] + old.rocket.old_angles)[:20]
            self.rocket.dx = (self.rocket.x - old.rocket.x) / self.dt
            self.rocket.dy = (self.rocket.y - old.rocket.y) / self.dt
            self.rocket.dangle = (self.rocket.angle - old.rocket.angle) / self.dt
            #if len(self.rocket.old_angles) > 6:
            #    self.rocket.dangle  = (self.rocket.angle - self.rocket.old_angles[5]) / \
            #                          (self.time - self.old_times[5])
            #else:
            #   self.rocket.dangle = 0

class Rocket(object):
    """A rocket.

    Attributes:
        x dx
        y dy
        angle dangle old_angles
    """
    def __init__(self, cnt_external, cnt_window):
        self.dx = None
        self.dy = None
        self.dangle = None
        self.old_angles = []
        [dir1_x, dir1_y, self.x, self.y] = cv2.fitLine(
            cnt_external, cv2.DIST_L2,0,0.01,0.01)
        self.angle2=180-math.degrees(math.atan2(dir1_x,dir1_y))
        if self.angle2 > 90:
            self.angle2 = self.angle2 - 180
        (window_x,window_y),radius = cv2.minEnclosingCircle(cnt_window)
        dir2_x = window_x-self.x
        dir2_y = window_y-self.y
        self.angle=180-math.degrees(math.atan2(dir2_x,dir2_y))
        if self.angle>180:
            self.angle = self.angle-360
        self.y = 1080 - self.y
        self.angle, self.angle2 = self.angle2, self.angle
        
    def __str__(self):
        out = "pos=(" + str(int(self.x)) + ',' + str(int(self.y)) + "),"
        out = out + "angle=" + str(int(self.angle)) + ","
        out = out + "v=(" + str(self.dx) + ',' + str(self.dy) + "),"
        out = out + "vangle=" + str(self.dangle)
        return out

class Platform(object):
    def __init__(self, cnt):
        x,y,w,h = cv2.boundingRect(cnt)
        self.x = x + w/2
        self.y = y
        self.y = 1080 - self.y

    def __str__(self):
        return "(" + str(self.x) + ',' + str(self.y) + ")"

def findContours(im, b, g, r, isDebug = False):
    rng = 3
    low = np.array([b-rng,g-rng,r-rng])
    high= np.array([b+rng,g+rng,r+rng])

    mask=cv2.inRange(im,low,high)
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    if isDebug:
        cv2.imshow('mask', mask)
    return contours
    
def findRocket(im):
    contours = findContours(im, 224, 169, 53)
    if len(contours) != 2:
        return None
    return Rocket(contours[1], contours[0])

def findPlatform(im):
    contours = findContours(im, 142, 11, 232)
    if len(contours) == 0:
        return None
    bestArea=0
    bestContour = None
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if h*w>bestArea:
            bestArea = h*w
            bestContour = contour
    if bestArea < 3000:
        return None
    return Platform(bestContour)

def findWorld(im):
    w = World()
    w.rocket=findRocket(im)
    w.platform=findPlatform(im)
    return w


eprint("w.time, w.dt, r.x, r.dx, r.y, r.dy, r.angle, r.angle2, r.dangle, throttlePower, turnPower")

def driveRocket(w):
    r=w.rocket
    targetX = 300
    targetY = 300
    targetAngle = ((targetX-r.x)-r.dx)/20
    #targetAngle = -15 #max(min(25,targetAngle),-25)
    #turnPower = targetAngle-r.angle-r.dangle/2
    turnPower = int((targetAngle-r.angle)*20.0 - r.dangle * 40.0)
    if abs(turnPower) < 0.1:
        turnPower = 0
    throttlePower = targetY-r.y-r.dy
    print(int(throttlePower), int(turnPower))
    
    eprint(str((w.time, w.dt, float(r.x), float(r.dx), float(r.y), float(r.dy), float(r.angle), float(r.angle2), float(r.dangle), int(throttlePower), turnPower))[1:-1])

    sys.stdout.flush()


w=None

with mss.mss() as sct:
    while True:
        im = screenshot()
        old = w
        w = findWorld(im)
        if old:
            w.calcDelta(old)
        if w.rocket and w.rocket.dx is not None:
            driveRocket(w)
        #cv2.imshow('image', im)

        #k = cv2.waitKey(5) & 0xFF
        #if k == 27:
        #    break

cv2.destroyAllWindows()
