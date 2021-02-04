import atexit
import curses

from bitbitbot import listen
from bitbitbot.models import TwitchTags


def cleanup(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

atexit.register(cleanup, stdscr)
stdscr.clear()
stdscr.refresh()
CHAT_MESSAGES = []


def draw_chat():
    stdscr.clear()
    for idx, msg in enumerate(CHAT_MESSAGES):
        stdscr.addstr(idx, 0, msg)
    stdscr.refresh()


@listen('chat_message')
def chat_logger(event_data) -> None:
    global CHAT_MESSAGES
    tags: TwitchTags = event_data.get('tags')
    msg: str = event_data.get('msg')
    if not msg and tags:
        return

    new_line = f'{tags.display_name}: {msg}'
    CHAT_MESSAGES.append(new_line)
    max_y, __ = stdscr.getmaxyx()
    CHAT_MESSAGES = CHAT_MESSAGES[-max_y:]
    draw_chat()
