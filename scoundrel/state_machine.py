# Loading
# Menu
# Playing
# Inventory

LOADING = 0
MENU = 1
PLAYING = 2
INVENTORY = 3

state = None

def playing():
    global state
    state = PLAYING

def loading():
    global state
    state = LOADING

def menu():
    global state
    state = menu

def inventory():
    global state
    state = INVENTORY

