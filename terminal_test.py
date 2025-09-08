from dashing import HSplit, VSplit, Text, Log
import time
from blessed import Terminal
from contextlib import contextmanager
from typing import Generator

@contextmanager
def open_terminal() -> Generator:
    """
    Helper function that creates a Blessed terminal session to restore the screen after
    the UI closes.
    """
    t = Terminal()

    with t.fullscreen(), t.hidden_cursor():
        yield t


if __name__ == "__main__":

    ui = HSplit(
        VSplit(
            Text("Left Top", color = 2),
            Log(title='logs', border_color=5, color=7)
        ),
        title = "My Terminal UI",
    )
    log = ui.items[0].items[1]

    terminal = Terminal()

    with terminal.fullscreen(), terminal.hidden_cursor(), terminal.cbreak():
        for i in range(100):
            t = int(time.time())
            log.append("%s" % t)

            ui.display()

            val = ''
            print('123')
            val = terminal.inkey(timeout = 0.1)
            if val.lower() == 'q':
                break
            else:
                log.append("Pressed: %s" % val.lower())


