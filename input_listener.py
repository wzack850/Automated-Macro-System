import threading
import win32api
import win32con
import time
import keyboard
import os
import pyautogui as pag

class InputListener:
    def __init__(self):
        self.events = []
        self.loaded_events = []
        self.thread = threading.Thread(target=self.listen)
        self.thread_on = True
        self.hotkey = "ctrl+shift+j"
        self.projects = []
        self.is_playing = False
    
    def get_projects(self):
        with open(r"C:\projects\projects.log", "r") as f:
            self.projects = f.readlines()
        
        for i, v in enumerate(self.projects):
            self.projects[i] = v.replace("\n", "")
        
        return self.projects

    def play(self, filename):
        threading.Thread(target=self.play_project, args=(filename,)).start()

    def wait_for_hotkey(self):
        keyboard.wait(self.hotkey)
    
    def set_hotkey(self, hotkey):
        self.hotkey = hotkey

    def start(self):
        self.thread_on = True
        self.thread.start()
    
    def stop(self):
        self.thread_on = False

    def play_project(self, filename):
        events = self.load_events(filename)
        for x in events:
            self.is_playing = True
            if x[0] == "mouseclick":
                time.sleep(x[-1])
                win32api.SetCursorPos((x[1][0], x[1][1]))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                time.sleep(x[-2])
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            if x[0] == "mousemove":
                time.sleep(x[-1])
                win32api.SetCursorPos((x[1][0], x[1][1]))
            if x[0] == "key":
                time.sleep(x[-1])
                keyboard.press(x[1])
                time.sleep(0.05)
                keyboard.release(x[1])
            if keyboard.is_pressed(self.hotkey):
                break
        self.is_playing = False
    
    def save_events(self, filename):
        try:
            os.mkdir(r"C:\projects")
        except:
            pass

        with open(r"C:\projects\projects.log", "a") as f:
            f.write(filename + "\n")
        
        open(fr"C:\projects\{filename}.log", "w").close()
        file = open(fr"C:\projects\{filename}.log", "a")
        
        for i, v in enumerate(self.events):
            pos = self.events[i][1]
            if type(pos) == list:
                for j, l in enumerate(pos):
                    pos[j] = str(l)

                pos = ",".join(pos)
                self.events[i][1] = pos

            for x, k in enumerate(self.events[i]):
                    self.events[i][x] = str(k)
            
            file.write(" ".join(v) + "\n")
        file.close()
    
    def load_events(self, filename):
        file = open(fr"C:\projects\{filename}.log", "r")
        events = file.readlines()
        new_events = []

        for x in events:
            split = x.split(" ")
            if split[0] == "mouseclick":
                split[1] = split[1].split(",")
                split[3] = float(split[3])
                split[4] = float(split[4].replace("\n", ""))
                
                for i, v in enumerate(split[1]):
                    split[1][i] = int(v)
            if split[0] == "mousemove":
                split[1] = split[1].split(",")
                split[2] = float(split[2].replace("\n", ""))
                
                for i, v in enumerate(split[1]):
                    split[1][i] = int(v)
            if split[0] == "key":
                split[2] = float(split[2].replace("\n", ""))

            new_events.append(split)

        return new_events

    def listen(self):
        state_left = win32api.GetKeyState(0x01)
        time_left = 0
        left_elapsed = 0

        state_right = win32api.GetKeyState(0x02)
        time_right = 0
        right_elapsed = 0

        between_elapsed = 0
        time_between = 0

        keys = list(
                "1234567890!@#$%^&*()-=_+[]{};':\",./<>?qwertyuiopasdfghjklzxcvbnm\|`~"
            ) + [
                    "caps_lock", "space", "tab", "right_shift", "shift", "alt", "right_alt",
                    "ctrl", "right_ctrl", "esc", "up", "down", "left", "right", "enter", "backspace",
                    "num_lock", "delete", "end", "print_screen", "page_down", "page_up", "insert",
                    "home", "left_windows", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10",
                    "f11", "f12"
                ]

        temp_pos = list(pag.position())

        while True:
            if not self.thread_on:
                break
            
            # Movement
            curr_pos = list(pag.position())
            if curr_pos != temp_pos:
                temp_pos = curr_pos
                between_elapsed = (time.time() - time_between)
                if len(self.events) > 0:
                    self.events.append(["mousemove", list(temp_pos), between_elapsed])
                else:
                    self.events.append(["mousemove", list(temp_pos), 0])
                
                time_between = time.time()

            # Clicks
            change_left = win32api.GetKeyState(0x01)
            change_right = win32api.GetKeyState(0x02)
            
            if change_left != state_left:
                state_left = change_left
                if change_left < 0:
                    time_left = time.time()
                    between_elapsed = (time.time() - time_between)
                else:
                    left_elapsed = (time.time() - time_left)
                    if len(self.events) > 0:
                        self.events.append(["mouseclick", list(pag.position()), "left", left_elapsed, between_elapsed])
                    else:
                        self.events.append(["mouseclick", list(pag.position()), "left", left_elapsed, 0])                    

                time_between = time.time()
                    
            if change_right != state_right:
                state_right = change_right
                if change_right < 0:
                    time_right = time.time()
                    between_elapsed = (time.time() - time_between)
                else:
                    right_elapsed = (time.time() - time_right)
                    if len(self.events) > 0:
                        self.events.append(["mouseclick", pag.position(), "right", right_elapsed, between_elapsed])
                    else:
                        self.events.append(["mouseclick", pag.position(), "right", right_elapsed, 0])

                time_between = time.time()

            # Key Presses
            for x in keys:
                if keyboard.is_pressed(x):
                    if len(self.events) > 0:
                        self.events.append(["key", x, between_elapsed])
                    else:
                        self.events.append(["key", x, 0])
                        
                    between_elapsed = (time.time() - time_between)
                    time_between = time.time()
                    time.sleep(0.05)