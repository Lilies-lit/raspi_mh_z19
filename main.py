# -*- coding: utf-8 -*-
import time
import json
import subprocess
import mh_z19
import datetime
import botcontrol
import asyncio

SETTINGS = {}

def getValue(instr):
    # {'co2' : xxx} --> xxx(int)
    valuestr = instr.split(':')[1][:-1]
    value = int(valuestr)
    return value

def getco2():
    out = mh_z19.read()
    V = getValue(str(out))
    return V

def measureco2():
    Vlist = []
    for i in range(5):
        v = getco2()
        Vlist.append(v)
        print("getCO2 #" + str(i + 1) + ' co2 = ' + str(v))
        time.sleep(SETTINGS['logInterval'])

    Vlist.sort()
    outV = (Vlist[1] + Vlist[2] + Vlist[3]) // 3

    return outV

def writetolog(V, dt_now):
    FileName = dt_now.strftime('%Y-%m-%d')
    FileName = SETTINGS['logDirectory'] + FileName + '.csv'
    print(FileName + ' co2 = ' + str(V))

    try:
        fs = open(FileName, 'a')
    except OSError:
        print("file can't open(output)")
        return 1

    
    writestr = dt_now.strftime('%H:%M') + ',' + str(V) + '\n'
    fs.write(writestr)
    fs.close()
    

def jsonload():
    global SETTINGS
    try:
        json_open = open('settings.json', 'r')
    except OSError:
        print("file can't open(json)")
        return 1

    try:
        SETTINGS = json.load(json_open)
    except:
        print("json load error!")
        return 1

    return 0


def main():
    print("initializing...")
    if jsonload() != 0:
        print("config error!")
        return 1
    else:
        print("config load OK")

    lastworkmin = -1

    while True:
        dt_now = datetime.datetime.now()
        Interval = SETTINGS['logInterval']
        if dt_now.minute % Interval == 0 and lastworkmin != dt_now.minute: #  1act /10min
            print("start measuring...")
            V = measureco2()
            if SETTINGS['writeLog'] == True:
                writetolog(V, dt_now)

            lastworkmin = dt_now.minute

        time.sleep(5)


main()