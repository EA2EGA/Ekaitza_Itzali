import time
import serial
from math import *
import os
import logging, sys
import urllib2
i=0;

while (True):
    time.sleep(0.1)
    i=i+1
    to_send="http://192.168.1.180/emoncms/input/post.json?json={RPM:"+str(i)+"}&apikey=59361aed146010d206b1842a45664089"
    urllib2.urlopen(to_send).read()