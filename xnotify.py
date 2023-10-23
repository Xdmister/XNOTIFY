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
import tkinter as tk
import time
import ctypes
import sys
import winreg

alerts = False
consoleHide = True


def onStart():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_large_font("XNOTIFY")





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








    






# icon
def create_icon():
    # Vytvoření ikony
    icon = pystray.Icon("name")
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # icon_path = resource_path("pepeico.png")
    icon_path = "C:/Users/Xdmis/Desktop/XNOTIFY/pepeico.png"
    
    icon.icon = Image.open(icon_path)


    
    def menu():
        alertSwitch()
        consoleSwitch()
        icon.menu = (
            item('Version 0.2b', lambda icon, item: create_notification("Verze 0.2b", "XNOTIFY", 5)),
            item('Alerts ' + str(alerts), lambda icon, item: menu()),
            item('Console ' + str(consoleHide), lambda icon, item: menu()),
            item('Exit', lambda icon, item: exit()),
            )
        icon.update_menu
        
    menu();
    icon.title = "XNOTIFY"
    icon.run()

icon_thread = threading.Thread(target=create_icon)
icon_thread.start()

def exit():
    print("exiting")
    os._exit(0)

def alertSwitch():
    global alerts
    alerts = not alerts
    
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
    root.attributes("-alpha", 0)  # Nastaví průhlednost na 0 pro začátek animace
    root.wm_attributes("-topmost", True)  # Zajišťuje, že okno zůstane nad ostatními okny
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    taskbar_height = _SCREEN_HEIGHT - screen_height
    font = tkfont.Font(family='Helvetica', size=11)  # Změna velikosti písma na 11
    title_font = tkfont.Font(family='Helvetica', size=12, weight='bold')  # Změna velikosti a stylu písma pro titulek
    text_lines = len(message.split('\n'))
    max_width = 300  # Maximální šířka notifikačního okna
    text_width = min(font.measure(line) for line in message.split('\n'))  # Získání šířky textu
    text_width = min(text_width, max_width)  # Omezení na maximální šířku
    notification_height = 60 + text_lines * 25  # Nastaví výšku podle délky textu
    padding = 10  # Upravit podle potřeby
    initial_x = screen_width - text_width - padding*2 - 5  # Updatuje počáteční x souřadnici
    initial_y = screen_height - notification_height - taskbar_height - 50  # Updatuje počáteční y souřadnici
    root.geometry("{}x{}+{}+{}".format(text_width + padding*2, notification_height, initial_x, initial_y))  
    root.configure(bg='#323542')  # Nastaví matné skleněné pozadí
    root.overrideredirect(True)  # odstraní border


    current_directory = os.path.dirname(os.path.abspath(__file__))
    # soundPath = resource_path("sound.mp3")
    soundPath = "C:/Users/Xdmis/Desktop/XNOTIFY/sound.mp3"
    
    sound_file = soundPath  # Nahraďte cestu k vašemu zvukovému souboru
    play_sound(sound_file)


    title_label = tk.Label(root, text=title, fg='#E0E6FF', bg='#323542', font=title_font)  # Přidá titulek do notifikace
    title_label.pack(anchor='nw', padx=10, pady=10)

    label = tk.Label(root, text=message, fg='#E0E6FF', bg='#323542', justify='left', anchor='w', width=text_width, wraplength=text_width, padx=10, pady=10, font=font)  # Upravit padding
    label.pack()

    def on_click(event):
        fade_out_animation(root, 20, root.winfo_width(), root.winfo_x())

    label.bind("<Button-1>", on_click)  # Při kliknutí na notifikaci spustí fade out animaci

    if timeout:
        root.after(timeout * 1000, lambda: fade_out_animation(root, 20, root.winfo_width(), root.winfo_x()))  # Zavře okno po uplynutí timeoutu

    fade_in_animation(root, 10, 0.1)  # Spustí animaci postupného zvýšení průhlednosti

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
    
# Funkce pro kontrolu API
def check_notification():
    while True:
        time.sleep(1)  # Pauza pro 1 sekundu
        response = requests.get('https://ipinfo.io')
        data = response.json()
        ip_address = get_public_ip()

        if ip_address:
            # Definování URL API
            url = 'https://xdmister.eu/xcore/api/notify.php'

            # Odeslání požadavku na API s veřejnou IP adresou
            data = {
                'ip': ip_address,
                'message': 'Zpráva na testování',
                'title': 'Notifikace pro test'
            }
            response = requests.post(url, json=data)

            # Zkontrolujte, zda klíč 'status' existuje v JSON odpovědi
            print(response.text)
            if 'status' in response.json():
                status = response.json()['status']            
            else:
                print("Notification creating")
                if isinstance(response.json(), list):
                    for item in response.json():
                        message = item.get('message')
                        title = item.get('title')
                        timestamp = int(item.get('time'))
                        if message and title and timestamp:
                            create_notification(message, title, timestamp)
                        else:
                            print("Některé klíče chybí v odpovědi API.")
check_notification()
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
        # PyInstaller creates a temp folder and stores path in _MEIPASS
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
        
onStart()
