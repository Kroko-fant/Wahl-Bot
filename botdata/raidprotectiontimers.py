import asyncio as a
import time as t

time = 301

timer1 = 0
timer2 = 0
timer3 = 0
timer4 = 0
timer5 = 0
timer6 = 0
timer7 = 0
timer8 = 0
timer9 = 0
timer10 = 0

active = False


async def cleartimer1():
    cleartime1 = t.time()
    while t.time() - cleartime1 < 300:
        await a.sleep(time)
    global timer1
    timer1 = 0
    await trydeactivateraid()
    print("Timer 1 gelöscht")


async def cleartimer2():
    cleartime2 = t.time()
    while t.time() - cleartime2 < 300:
        await a.sleep(time)
    global timer2
    timer2 = 0
    await trydeactivateraid()
    print("Timer 2 gelöscht")


async def cleartimer3():
    cleartime3 = t.time()
    while t.time() - cleartime3 < 300:
        await a.sleep(time)
    global timer3
    timer3 = 0
    await trydeactivateraid()
    print("Timer 3 gelöscht")


def cleartimer4():
    cleartime4 = t.time()
    while t.time() - cleartime4 < 300:
        await a.sleep(time)
    global timer4
    timer4 = 0
    await trydeactivateraid()
    print("Timer 4 gelöscht")


async def cleartimer5():
    cleartime5 = t.time()
    while t.time() - cleartime5 < 300:
        await a.sleep(time)
    global timer5
    timer5 = 0
    await trydeactivateraid()
    print("Timer 5 gelöscht")


async def cleartimer6():
    cleartime6 = t.time()
    while t.time() - cleartime6 < 300:
        await a.sleep(time)
    global timer6
    timer6 = 0
    await trydeactivateraid()
    print("Timer 6 gelöscht")


async def cleartimer7():
    cleartime7 = t.time()
    while t.time() - cleartime7 < 300:
        await a.sleep(time)
    global timer7
    timer7 = 0
    await trydeactivateraid()
    print("Timer 7 gelöscht")


async def cleartimer8():
    cleartime8 = t.time()
    while t.time() - cleartime8 < 300:
        t.sleep(301)
    global timer8
    timer8 = 0
    await trydeactivateraid()
    print("Timer 8 gelöscht")


async def cleartimer9():
    cleartime9 = t.time()
    while t.time() - cleartime9 < 300:
        await a.sleep(time)
    global timer9
    timer9 = 0
    await trydeactivateraid()
    print("Timer 9 gelöscht")


async def cleartimer10():
    cleartime10 = t.time()
    while t.time() - cleartime10 < 300:
        await a.sleep(time)
    global timer10
    timer10 = 0
    await trydeactivateraid()

    print("Timer 10 gelöscht")


# Checken ob ein Raid vorhanden ist
def checkraid():
    if active:
        return True
    else:
        if max([timer1, timer2, timer3, timer4, timer5, timer6, timer7, timer8, timer9, timer10]) < 5:
            return False
        else:
            activateraid()
            return True


def activateraid():
    print("Raid-Protection active!")
    global active
    active = True
    await trydeactivateraid()


async def trydeactivateraid():
    if active:
        if max([timer1, timer2, timer3, timer4, timer5, timer6, timer7, timer8, timer9, timer10]) < 5:
            print("Raid-Protection wird deaktiviert! Check 1/2")
            await a.sleep(301)
            if max([timer1, timer2, timer3, timer4, timer5, timer6, timer7, timer8, timer9, timer10]) < 5:
                deactivateraid()
                print("Raid-Protection wird deaktiviert! Check 2/2")
            else:
                await trydeactivateraid()


def deactivateraid():
    global active
    active = False
    print("Raid-Protection deaktiviert!")


def printtimers():
    print(timer1, timer2, timer3, timer4, timer5, timer6, timer7, timer8, timer9, timer10)
