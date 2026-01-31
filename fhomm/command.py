from collections import namedtuple

import pygame

QUIT = -1
IGNORE = 0
TOGGLE_FULLSCREEN = 1
SHOW = 2                        # open a new window or a screen
CLOSE = 3                       # close the active window or a screen
TOGGLE_DEBUG_UI_RENDER = 4
TOGGLE_DEBUG_UI_EVENTS = 5
TOGGLE_FPS = 6
UPDATE = 7

Command = namedtuple('Command', ['code', 'kwargs'], defaults=[{}])

CMD_QUIT = Command(QUIT)
CMD_IGNORE = Command(IGNORE)
CMD_TOGGLE_FULLSCREEN = Command(TOGGLE_FULLSCREEN)
CMD_TOGGLE_DEBUG_UI_RENDER = Command(TOGGLE_DEBUG_UI_RENDER)
CMD_TOGGLE_DEBUG_UI_EVENTS = Command(TOGGLE_DEBUG_UI_EVENTS)
CMD_TOGGLE_FPS = Command(TOGGLE_FPS)


# TODO: the opposite of "close" is not "show"...  "open" maybe?
def cmd_show(window, screen_pos, state_key):
    return Command(
        SHOW,
        {
            'window': window,
            'screen_pos': screen_pos,
            'state_key': state_key,
        }
    )


# TODO: name it cmd_return and make the key external (in the window slot)
def cmd_close(return_key=None):
    return Command(CLOSE, {'return_key': return_key})


CMD_CLOSE = cmd_close()


def cmd_update(update_fn):
    return Command(UPDATE, {'update_fn': update_fn})


def cmd_update_other(key, update_fn):
    return Command(UPDATE, {'key': key, 'update_fn': update_fn})


def aslist(cmd):
    if cmd is None:
        return []

    elif isinstance(cmd, Command):
        return [cmd]

    else:
        # we could check for list or tuple here, but Command is a tuple as well...
        return [c for c in cmd if c] # filter out Nones, but why?
