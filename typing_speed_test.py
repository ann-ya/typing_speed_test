import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    #to empty a screen
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    #waits for a user to type smth, without getkey text would be shown for a sec and then dissapear, program would be closed immediately
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def load_text():
    #with - ensures that the file will be closed after you open it - Context Manager
    with open("test_text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()
        #strip() would remove \n or any whitespace character


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    #program won't wait for a user to hit a key
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        #If user doesn't enter a key (line 33, nodelay), this line <key = stdscr.getkey()> throws an exception.
        #To handle it, except and continue need to be implemented. Continue will bring you back to the top of the while loop.
        #If this line throws an exception, key variable doesn't have value, there is no need to check a type of a key.
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

        
def main(stdscr):
    #foreground - green color, background - black color, represented by id 1
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)