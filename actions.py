# actions.py
import webbrowser
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import time
import os  # Added for launching system apps


def perform_open_hand_action():
    webbrowser.open("https://www.youtube.com")

def volume_up():
    volume = _get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(min(1.0, current + 0.05), None)

def volume_down():
    volume = _get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(max(0.0, current - 0.05), None)

def mouse_click():
    pyautogui.click()

def move_mouse(x, y):
    screen_width, screen_height = pyautogui.size()
    pyautogui.moveTo(int(x * screen_width), int(y * screen_height), duration=0.1)

def _get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def perform_middle_finger_action():
    os.system("start spotify")  # Windows only

def perform_ring_finger_action():
    os.system("notepad")

def perform_little_finger_action():
    os.system("calc")


