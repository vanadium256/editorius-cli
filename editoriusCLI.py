import curses
import os

class TextEditor:
    def __init__(self, stdscr, filename=None):
        self.stdscr = stdscr
        self.filename = filename
        self.text = []
        self.cursor_x = 0
        self.cursor_y = 0

        if filename and os.path.exists(filename):
            self.open_file(filename)
        else:
            self.new_file()

        self.run_editor()

    def new_file(self):
        self.text = ['']
        self.cursor_x = 0
        self.cursor_y = 0

    def open_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            self.text = file.readlines()
        self.cursor_y = len(self.text) - 1 if self.text else 0
        self.cursor_x = len(self.text[self.cursor_y]) if self.text else 0

    def save_file(self):
        if self.filename is None:
            self.filename = self.get_filename()
        if self.filename:
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.writelines(self.text)

    def get_filename(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "File name: ")
        curses.echo()
        filename = self.stdscr.getstr(1, 0).decode('utf-8')
        curses.noecho()
        return filename

    def run_editor(self):
        while True:
            self.stdscr.clear()
            self.display_text()
            self.stdscr.addstr(curses.LINES - 1, 0, "Ctrl+S: Save | Ctrl+Q: Exit")

            # Проверка границ курсора
            self.cursor_y = min(self.cursor_y, len(self.text) - 1)
            self.cursor_x = min(self.cursor_x, len(self.text[self.cursor_y]) if self.cursor_y >= 0 else 0)

            self.stdscr.move(self.cursor_y, self.cursor_x)

            key = self.stdscr.getch()

            if key == curses.KEY_BACKSPACE or key == 127:
                if self.cursor_x > 0:
                    self.text[self.cursor_y] = (self.text[self.cursor_y][:self.cursor_x - 1] +
                                                 self.text[self.cursor_y][self.cursor_x:])
                    self.cursor_x -= 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.text.insert(self.cursor_y + 1, '')
                self.cursor_y += 1
                self.cursor_x = 0
            elif key == curses.KEY_UP:
                if self.cursor_y > 0:
                    self.cursor_y -= 1
                    self.cursor_x = min(self.cursor_x, len(self.text[self.cursor_y]))
            elif key == curses.KEY_DOWN:
                if self.cursor_y < len(self.text) - 1:
                    self.cursor_y += 1
                    self.cursor_x = min(self.cursor_x, len(self.text[self.cursor_y]))
            elif key == curses.KEY_LEFT:
                if self.cursor_x > 0:
                    self.cursor_x -= 1
                elif self.cursor_y > 0:
                    self.cursor_y -= 1
                    self.cursor_x = len(self.text[self.cursor_y])
            elif key == curses.KEY_RIGHT:
                if self.cursor_x < len(self.text[self.cursor_y]):
                    self.cursor_x += 1
                elif self.cursor_y < len(self.text) - 1:
                    self.cursor_y += 1
                    self.cursor_x = 0
            elif key == 19:  # Ctrl+S
                self.save_file()
            elif key == 17:  # Ctrl+Q
                break
            else:
                if 0 <= key < 256:  # Printable characters
                    if self.cursor_y >= len(self.text):
                        self.text.append('')
                    self.text[self.cursor_y] = (self.text[self.cursor_y][:self.cursor_x] +
                                                 chr(key) +
                                                 self.text[self.cursor_y][self.cursor_x:])
                    self.cursor_x += 1

    def display_text(self):
        for i, line in enumerate(self.text):
            self.stdscr.addstr(i, 0, line.rstrip('\n'))
        self.stdscr.clrtoeol()  # Очистить остаток строки

if __name__ == "__main__":
    filename = None
    if len(os.sys.argv) > 1:
        filename = os.sys.argv[1]
    curses.wrapper(TextEditor, filename)

