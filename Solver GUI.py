import tkinter as tk
import itertools
import random


class Sudoku:
    def __init__(self, master):
        # creates class variables of the board
        self.display_numbers = [[0 for _ in range(9)] for _ in range(9)]
        self.real_numbers = [[0 for _ in range(9)] for _ in range(9)]
        self.clock = Timer(self)

        for y, x in itertools.product(range(9), repeat=2):
            self.display_numbers[y][x] = tk.StringVar(master)

        # creates GUI
        master.geometry('467x520')
        master.title("Sudoku Solver")

        self.frame = tk.Frame(master, bg='light gray')
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # creates squares
        self.squares = []

        for y in range(1, 10):
            new_row = []
            for x in range(1, 10):
                if x < 4 or x > 6:
                    colour = 'gray'
                    if 3 < y < 7:
                        colour = 'white'
                else:
                    colour = 'white'
                    if 3 < y < 7:
                        colour = 'gray'
                square = tk.Entry(self.frame, width=2, bg=colour, highlightthickness=0,
                                  textvar= self.display_numbers[y - 1][x - 1], validate='key',
                                  validatecommand=(master.register(self.square_input), '%P'), disabledbackground=colour)
                square.grid(column=x, row=y, sticky='nsew')
                square['font'] = ('Arial', 40, 'bold italic')
                new_row.append(square)
            self.squares.append(new_row)

        for x in range(1,10):
            tk.Grid.columnconfigure(self.frame, x, weight=1)

        for y in range(1,10):
            tk.Grid.rowconfigure(self.frame, y, weight=1)

        # calls function to create buttons
        self.button("Solve Board", 1, 10, self.correct_board)
        self.button("Clear Board", 1, 11, self.clear)
        self.button("New Puzzle", 7, 10, self.new_puzzle)
        self.button("Check Puzzle", 7, 11, self.check_sudoku)

        # places timer
        self.timer = tk.Label(self.frame, text="0:00", bg='light gray', width=5, font='Arial 35')
        self.timer.grid(column=4, row=10, columnspan=3, rowspan=2, sticky='nsew')

    def button(self, text, column, row, command):  # creates buttons
        button = tk.Button(self.frame, text=text, highlightthickness=0, highlightbackground='light gray',
                           width=13, font="Arial 20", command=lambda: command())
        button.grid(column=column, row=row, columnspan=3, sticky='nsew')

    def check_sudoku(self):  # checks if user had correctly filled in a puzzle
        self.clock.stop()
        blank = 0
        wrong = False
        try:
            for y, x in itertools.product(range(9), repeat=2):
                if self.display_numbers[y][x].get() == "" or self.solved_board[y][x] != int(
                        self.display_numbers[y][x].get()):
                    wrong = True
                    break
        except:
            pass

        for y, x in itertools.product(range(9), repeat=2):
            if self.display_numbers[y][x].get() == "":
                blank += 1

        if blank == 81:
            self.winner_screen(None)
        elif wrong:
            self.winner_screen(False)
        else:
            self.winner_screen(True)

    def winner_screen(self, winner):  #creates a pop up screen when won
        # create GUI
        screen = tk.Tk()
        frame = tk.Frame(screen, bg='light blue')
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        label = tk.Label(frame, text="", bg='light blue')
        label.place(relx=0, rely=0.1)
        label['font'] = ("Arial", 15)
        ok_btn = tk.Button(frame, text="OK", command=lambda: screen.destroy(), highlightthickness=0, bg='gray',
                           highlightbackground='light blue')
        ok_btn.place(relx=0.5, rely=0.65, anchor='n')
        ok_btn['font'] = ("Arial", 15)

        if winner is True:
            screen.geometry('175x80')
            screen.title('Correct Solution')
            label.config(text="Congrats! You solved the\nsudoku puzzle in {}!".format(self.timer.cget("text")))
        elif winner is False:
            screen.geometry('200x85')
            screen.title("Incorrect Solution")
            label.config(text="Sorry, this is not correct.\nPlease try a different solution")
            ok_btn.config(command=lambda: [screen.destroy(), self.clock.start(self.clock.seconds)])
        elif winner is None:
            screen.geometry('145x75')
            screen.title('Empty board')
            label.config(text="This soduko board is \nempty. Try a puzzle")
        else:
            screen.geometry('150x75')
            screen.title('Empty board')
            label.config(text="This soduko board is \nunsolvable")

        screen.mainloop()

    def new_puzzle(self):  # creates a new solvable puzzle
        self.generate_board()
        self.solved_board = self.real_numbers

        # Randomly removes squares
        while self.empty_square() < 48:
            y, x = ((random.randint(0, 8) for _ in range(2)))
            original_board = self.real_numbers
            original_value = self.real_numbers[y][x]

            if original_value == 0:
                continue

            self.real_numbers[y][x] = 0

            # if after removing number it is still unique
            if not self.solve(True, [y, x, original_value]):
                self.real_numbers = original_board
                self.real_numbers[y][x] = 0
            # if after removing number there it is not unique
            else:
                self.real_numbers = original_board

        # displays board clues
        for y, x in itertools.product(range(9), repeat=2):
            if self.real_numbers[y][x] == 0:
                self.display_numbers[y][x].set("")
            else:
                self.display_numbers[y][x].set(self.real_numbers[y][x])
                self.squares[y][x].config(font='Arial 40 bold italic', disabledforeground='black', state='disabled')

        self.clock.start(0)

    def generate_board(self):  # creates a random filled in sudoku for users to solve
        self.clear()

        # fills the 3 diagonal boxes
        numbers = [i for i in range(1, 10)]
        for y, x in itertools.product(range(3), repeat=2):
            num = random.choice(numbers)
            self.real_numbers[y][x] = num
            numbers.remove(num)

        numbers = [i for i in range(1, 10)]
        for y, x in itertools.product(range(3, 6), repeat=2):
            num = random.choice(numbers)
            self.real_numbers[y][x] = num
            numbers.remove(num)

        numbers = [i for i in range(1, 10)]
        for y, x in itertools.product(range(6, 9), repeat=2):
            num = random.choice(numbers)
            self.real_numbers[y][x] = num
            numbers.remove(num)

        # solves random board
        self.solve()

    def empty_square(self):  # counts how many squares on the board are empty
        num = 0
        for i in range(9):
            num += self.real_numbers[i].count(0)
        return num

    @staticmethod
    def square_input(inp):  # checks if input of square is valid(only single digit numbers)
        num_list = [str(i) for i in range(1, 10)]
        return True if inp in num_list and len(inp) < 2 or inp == "" else False

    def isvalid(self, y, x, num):  # checks if potential square is valid with given number
        # row
        for i in range(9):
            if num == self.real_numbers[y][i] and i != x:
                return False

        # column
        for i in range(9):
            if num == self.real_numbers[i][x] and i != y:
                return False

        # boxes
        x_box = x // 3
        y_box = y // 3

        for i in range(y_box * 3, y_box * 3 + 3):
            for j in range(x_box * 3, x_box * 3 + 3):
                if self.real_numbers[i][j] == num and i != y and j != x:
                    return False

        return True

    def clear(self):  # clears the entire board
        for y, x in itertools.product(range(9), repeat=2):
            self.squares[y][x].config(font='Arial 40 bold italic', fg='black', state='normal')
            self.display_numbers[y][x].set('')
            self.real_numbers[y][x] = 0

        self.timer.config(text="0:00")
        self.clock.stop()

    def find_cell(self):  # finds an empty cell
        for i in range(9):
            if 0 in self.real_numbers[i]:
                return i, self.real_numbers[i].index(0)
        return False

    def solve(self, multiple_solutions=False, forbidden_value=None):  # finds solution to current board
        # finds an empty cell, if none found puzzle is solved
        find = self.find_cell()

        if not find:
            return True
        else:
            y, x = find

        # solving algorithm(backtracking)
        for n in range(1, 10):
            if multiple_solutions is True and y == forbidden_value[0] and x == forbidden_value[1] and n == \
                    forbidden_value[2]:
                continue
            if self.isvalid(y, x, n):
                self.squares[y][x].config(font='Arial 40 bold', fg='dark blue')
                self.real_numbers[y][x] = n
                if self.solve(multiple_solutions, forbidden_value):
                    return True
                self.real_numbers[y][x] = 0
        return False

    def correct_board(self):  # implements correct board
        # sets the board
        for y, x in itertools.product(range(9), repeat=2):
            self.real_numbers[y][x] = 0
        for y, x in itertools.product(range(9), repeat=2):
            if self.display_numbers[y][x].get() != "":
                self.real_numbers[y][x] = int(self.display_numbers[y][x].get())
            else:
                self.real_numbers[y][x] = 0

        # checks if user input invalid board
        impossible = False
        for y, x in itertools.product(range(9), repeat=2):
            if self.real_numbers[y][x] != 0:
                if not self.isvalid(y, x, self.real_numbers[y][x]):
                    impossible = True
                    break

        # solves and displays correct board
        if not impossible and self.solve():  # True, [int(input("y")), int(input("x")), int(input("n"))]
            for y, x in itertools.product(range(9), repeat=2):
                self.display_numbers[y][x].set(self.real_numbers[y][x])
        else:
            self.winner_screen('invalid')


class Timer:
    def __init__(self, game):
        self.game = game
        self.repeat = 0
        self.seconds = 0

    def start(self, seconds):  # starts timer
        self.stop()
        self.repeat += 1
        self.seconds = seconds
        self.end = False
        self.increment()

    def stop(self):  #stops timer
        self.end = True

    def increment(self):  # waits 1 second to call a function to update the timer
        self.game.timer.after(1000, self.update_timer, self.repeat)

    def update_timer(self, repeat):  # updates the timer
        if not self.end and repeat == self.repeat:
            self.seconds += 1
            minute = self.seconds // 60
            second = str(self.seconds - minute * 60)
            if len(second) < 2:
                second = '0' + second
            self.game.timer.config(text="{}:{}".format(minute, second))
            self.increment()


root = tk.Tk()  #creates the root for the GUI
game = Sudoku(root)  # runs the code
root.mainloop()
