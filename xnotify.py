import tkinter as tk
from tkinter import font as tkfont
import time
import ctypes
import requests
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os
import pygame
import time
import sys
import winreg
import json

version = "0.3b"
alerts = False
consoleHide = True
nullCounter = 0
soundName = "nil"


# onstart function
def onStart():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_large_font("XNOTIFY")
    create_default_json()
    data = read_json_data()
    print("")
    print("Obsah JSON souboru:")
    print(data)
    global alerts
    global soundName
    alerts = not data["alerts"]
    soundName = data["soundName"]





# afterstartup setup
script_path = os.path.abspath(sys.argv[0])
key = winreg.HKEY_CURRENT_USER
sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
try:
    with winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE) as key_handle:
        winreg.SetValueEx(key_handle, "XNOTIFY", 0, winreg.REG_SZ, script_path)
except Exception as e:
    print(f"Nepodařilo se přidat aplikaci k automatickému spuštění. Chyba: {e}")
# afterstartup setup










# data manager

# data manager







    






# icon
def create_icon():

    icon = pystray.Icon("name")
    # icon_path = resource_path("pepeico.png")
    icon_path = "C:/Users/Xdmis/Desktop/XNOTIFY/pepeico.png"
    icon.icon = Image.open(icon_path)

    def alertsS():
        alertSwitch()
        menu()
        
    def console():
        consoleSwitch()
        menu()
    
    def menu():
        icon.menu = (
            item('Version ' + version, lambda icon, item: create_notification("Version: " + version, "XNOTIFY", 5)),
            item('Alerts ' + str(alerts), lambda icon, item: alertsS()),
            item('Console ' + str(consoleHide), lambda icon, item: console()),
            item('Exit', lambda icon, item: exit()),
            )
        icon.update_menu
        
    menu();
    icon.title = "XNOTIFY"
    icon.run()

icon_thread = threading.Thread(target=create_icon)
icon_thread.start()

def exit():
    os._exit(0)

def alertSwitch():
    global alerts
    alerts = not alerts
    update_json_data("alerts", alerts)
    
def consoleSwitch():
    global consoleHide
    consoleHide = not consoleHide
    if consoleSwitch:
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        SW_HIDE = 1

        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            user32.ShowWindow(hWnd, SW_HIDE)
    if not consoleHide:
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        SW_HIDE = 0

        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            user32.ShowWindow(hWnd, SW_HIDE)
# icon












# notify
user32 = ctypes.windll.user32
_SCREEN_WIDTH = user32.GetSystemMetrics(0)
_SCREEN_HEIGHT = user32.GetSystemMetrics(1)

def fade_in_animation(root, delay, alpha):
    if alpha < 1:
        root.attributes("-alpha", alpha)
        alpha += 0.01
        root.after(delay, fade_in_animation, root, delay, alpha)

def fade_out_animation(root, delay, width, x_coordinate):
    if width > 0:
        root.geometry("{}x{}+{}+{}".format(width, root.winfo_height(), x_coordinate, root.winfo_y()))
        width -= 20
        x_coordinate += 10
        root.after(delay, fade_out_animation, root, delay, width, x_coordinate)
    else:
        root.destroy()


def create_notification(message, title="Notification", timeout=None):
    root = tk.Tk()
    root.title("Notification")
    root.attributes("-alpha", 0)
    root.wm_attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    taskbar_height = _SCREEN_HEIGHT - screen_height
    font = tkfont.Font(family='Helvetica', size=11)
    title_font = tkfont.Font(family='Helvetica', size=12, weight='bold')
    text_lines = len(message.split('\n'))
    max_width = 300  
    text_width = min(font.measure(line) for line in message.split('\n'))
    text_width = min(text_width, max_width)
    notification_height = 60 + text_lines * 25
    padding = 10
    initial_x = screen_width - text_width - padding*2 - 5  
    initial_y = screen_height - notification_height - taskbar_height - 50
    root.geometry("{}x{}+{}+{}".format(text_width + padding*2, notification_height, initial_x, initial_y))  
    root.configure(bg='#323542')
    root.overrideredirect(True)  

    # soundPath = resource_path(soundName)
    soundPath = "C:/Users/Xdmis/Desktop/XNOTIFY/" + soundName
    play_sound(soundPath)

    title_label = tk.Label(root, text=title, fg='#E0E6FF', bg='#323542', font=title_font)  # Přidá titulek do notifikace
    title_label.pack(anchor='nw', padx=10, pady=10)

    label = tk.Label(root, text=message, fg='#E0E6FF', bg='#323542', justify='left', anchor='w', width=text_width, wraplength=text_width, padx=10, pady=10, font=font)  # Upravit padding
    label.pack()

    def on_click(event):
        fade_out_animation(root, 20, root.winfo_width(), root.winfo_x())

    label.bind("<Button-1>", on_click)

    if timeout:
        root.after(timeout * 1000, lambda: fade_out_animation(root, 20, root.winfo_width(), root.winfo_x()))  # Zavře okno po uplynutí timeoutu
        
    fade_in_animation(root, 10, 0.1)
    root.mainloop()
# notify end














# api
def get_public_ip():
    response = requests.get('https://httpbin.org/ip')
    if response.status_code == 200:
        data = response.json()
        return data['origin']
    else:
        return None

def check_notification():
    while True:
        time.sleep(1)
        ip_address = get_public_ip()

        if ip_address:
            url = 'https://xdmister.eu/xcore/api/notify.php'

    
            data = {
                'ip': ip_address,
            }
            response = requests.post(url, json=data)

         
    
            if 'status' in response.json():
                global nullCounter
                nullCounter += 1
                os.system('cls' if os.name == 'nt' else 'clear')
                print_large_font("XNOTIFY")
                global version
                print("-----------------------------------------------------------")
                print("")
                print("Author: Xdmister")
                print("Version: " + version)
                print("")
                print("Null Count:" + str(nullCounter))
                print("")
                print(response.text)
                # status = response.json()['status']        
            else:
                print("Notification creating")
                if isinstance(response.json(), list):
                    for item in response.json():
                        message = item.get('message')
                        title = item.get('title')
                        timestamp = int(item.get('time'))
                        if message and title and timestamp:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print_large_font("XNOTIFY")
                            print("-----------------------------------------------------------")
                            print("")
                            print("Author: Xdmister")
                            print("Version: " + version)
                            print("")
                            print("Null Count:" + str(nullCounter))
                            print("")
                            print(response.text)
                            create_notification(message, title, timestamp)
                        else:
                            print("Některé klíče chybí v odpovědi API.")
# api




# label
def print_large_font(text):
    characters = {'A': ['  A  ', ' A A ', 'AAAAA', 'A   A', 'A   A'],
                  'B': ['BBBB ', 'B   B', 'BBBB ', 'B   B', 'BBBB '],
                  'C': [' CCCC', 'C    ', 'C    ', 'C    ', ' CCCC'],
                  'D': ['DDD  ', 'D  D ', 'D   D', 'D  D ', 'DDD  '],
                  'E': ['EEEEE', 'E    ', 'EEEEE', 'E    ', 'EEEEE'],
                  'F': ['FFFFF', 'F    ', 'FFFFF', 'F    ', 'F    '],
                  'G': [' GGGG', 'G    ', 'G  GG', 'G   G', ' GGGG'],
                  'H': ['H   H', 'H   H', 'HHHHH', 'H   H', 'H   H'],
                  'I': ['IIIII', '  I  ', '  I  ', '  I  ', 'IIIII'],
                  'J': ['JJJJJ', '   J ', '   J ', 'J  J ', ' JJ  '],
                  'K': ['K   K', 'K  K ', 'KK   ', 'K  K ', 'K   K'],
                  'L': ['L    ', 'L    ', 'L    ', 'L    ', 'LLLLL'],
                  'M': ['M   M', 'MM MM', 'M M M', 'M   M', 'M   M'],
                  'N': ['N   N', 'NN  N', 'N N N', 'N  NN', 'N   N'],
                  'O': [' OOO ', 'O   O', 'O   O', 'O   O', ' OOO '],
                  'P': ['PPPP ', 'P   P', 'PPPP ', 'P    ', 'P    '],
                  'Q': [' QQQ ', 'Q   Q', 'Q   Q', 'Q  Q ', ' QQ Q'],
                  'R': ['RRRR ', 'R   R', 'RRRR ', 'R  R ', 'R   R'],
                  'S': [' SSSS', 'S    ', ' SSS ', '    S', 'SSSS '],
                  'T': ['TTTTT', '  T  ', '  T  ', '  T  ', '  T  '],
                  'U': ['U   U', 'U   U', 'U   U', 'U   U', ' UUU '],
                  'V': ['V   V', 'V   V', 'V   V', ' V V ', '  V  '],
                  'W': ['W   W', 'W   W', 'W W W', 'WW WW', 'W   W'],
                  'X': ['X   X', ' X X ', '  X  ', ' X X ', 'X   X'],
                  'Y': ['Y   Y', ' Y Y ', '  Y  ', '  Y  ', '  Y  '],
                  'Z': ['ZZZZZ', '    Z', '   Z ', '  Z  ', 'ZZZZZ'],
                  ' ': ['     ', '     ', '     ', '     ', '     '],
                  '/': ['    /', '   / ', '  /  ', ' /   ', '/    '],
                  '|': ['  |  ', '  |  ', '  |  ', '  |  ', '  |  '],
                  ':': ['     ', '  :  ', '     ', '  :  ', '     ']}
    for row in range(5):
        for char in text:
            if char.upper() in characters:
                print(characters[char.upper()][row], end='  ')
            else:
                print("     ", end='  ')
        print()
# label

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)





def play_sound(sound_file):
    if alerts:
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        
        
def create_default_json():
    documents_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
    xnotify_folder_path = os.path.join(documents_path, 'XNOTIFY')
    if not os.path.exists(xnotify_folder_path):
        os.makedirs(xnotify_folder_path)
        print(f"Složka {xnotify_folder_path} byla vytvořena.")
    json_file_path = os.path.join(xnotify_folder_path, 'data.json')
    if not os.path.exists(json_file_path):
        default_data = {
            'alerts': True,
            'soundName': "sound.mp3"
        }
        with open(json_file_path, 'w') as file:
            json.dump(default_data, file, indent=4)
            print(f"Soubor {json_file_path} byl vytvořen s výchozími hodnotami.")
    else:
        print(f"Soubor {json_file_path} již existuje.")

def read_json_data():
    documents_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
    json_file_path = os.path.join(documents_path, 'XNOTIFY', 'data.json')
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                return data
        except json.JSONDecodeError as e:
            print(f"Chyba při načítání JSON souboru: {e}")
            return None
    else:
        print(f"Soubor {json_file_path} neexistuje.")

def update_json_data(key, value):
    documents_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
    json_file_path = os.path.join(documents_path, 'XNOTIFY', 'data.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            data[key] = value
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)
            print("Hodnota proměnné byla úspěšně aktualizována.")
    else:
        print(f"Soubor {json_file_path} neexistuje.")
        
        
        
        
        
        
        
        
        
# endFunctions
onStart()
time.sleep(20)
check_notification()