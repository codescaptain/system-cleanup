import curses
from config.settings import COLOR_SCHEME
class ProgressBar:
    def __init__(self, stdscr, total, y, x, width):
        self.stdscr = stdscr
        self.total = total
        self.current_progress = 0
        self.y = y
        self.x = x
        self.width = width
        self.operation_name = ""
        self.elapsed_time = 0

    def update(self, progress, operation_name, elapsed_time):
        self.current_progress = progress
        self.operation_name = operation_name
        self.elapsed_time = elapsed_time
        self.render()

    def render(self):
        bar_width = self.width - 2
        filled = int(self.current_progress / self.total * bar_width)

        self.stdscr.attron(curses.color_pair(COLOR_SCHEME['default']))

        # Progress bar
        self.stdscr.addstr(self.y, self.x, "[" + "=" * filled + " " * (bar_width - filled) + "]")

        # Operation name and progress percentage
        progress_text = f"{self.operation_name} - {self.current_progress}% Complete"
        self.stdscr.addstr(self.y, self.x + 1, progress_text[:bar_width])

        # Elapsed time
        time_text = f"Time: {self.elapsed_time:.1f}s"
        self.stdscr.addstr(self.y, self.width - len(time_text) - 1, time_text)

        self.stdscr.attroff(curses.color_pair(COLOR_SCHEME['default']))


class DialogBox:
    def __init__(self, stdscr, message):
        self.stdscr = stdscr
        self.message = message

    def render(self):
        # Get screen dimensions
        max_y, max_x = self.stdscr.getmaxyx()

        # Calculate the position
        box_width = max_x // 2
        box_height = max_y // 4
        start_y = (max_y // 2) - (box_height // 2)
        start_x = (max_x // 2) - (box_width // 2)

        # Draw the box
        self.stdscr.attron(curses.color_pair(COLOR_SCHEME['highlight']))
        self.stdscr.addstr(start_y, start_x, "+" + "-" * (box_width - 2) + "+")
        for y in range(1, box_height - 1):
            self.stdscr.addstr(start_y + y, start_x, "|" +
                               " " * (box_width - 2) + "|")
        self.stdscr.addstr(start_y + box_height - 1, start_x,
                           "+" + "-" * (box_width - 2) + "+")
        self.stdscr.attroff(curses.color_pair(COLOR_SCHEME['highlight']))

        # Add the message in the center
        message_x = start_x + (box_width // 2) - (len(self.message) // 2)
        self.stdscr.addstr(start_y + (box_height // 2),
                           message_x, self.message)
