import tkinter as tk
from tkinter import  messagebox
import random


class Minesweeper:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.generate_mines()

        self.buttons = [[tk.Button(master, width=2, height=1, command=lambda r = row, c = col: self.click(r,c))
                         for col in range(cols)] for row in range(rows)]

        for row in range(rows):
            for col in range(cols):
                self.buttons[row][col].grid(row=row, column = col)


    def generate_mines(self):
        mine_count = 0
        while mine_count < self.mines:
            row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mine_count += 1


    def check_victory(self):
        safe_cells = sum(1 for row in self.buttons for button in row if button['state'] == 'disabled' and button['text'] != '*')
        if safe_cells == (self.rows * self.cols - self.mines):
            self.victory()


    def victory(self):
        for row in self.buttons:
            for button in row:
                button.config('disabled')
        tk.messagebox.showinfo("Victory!", "Congratulations! You won!")


    def click(self, row, col):
        if self.board[row][col] == -1:
            self.buttons[row][col].config(text = '*', state="disabled", disabledforeground='red')
            self.game_over()
        else:
            mines_nearby = sum (1 for r in range(row - 1, row + 2) for c in range(col - 1, col + 2)
                                if 0<= r < self.rows and 0 <= c < self.cols and self.board[r][c] == -1)
            self.buttons[row][col].config(text = mines_nearby, state = "disabled", disabledforeground="black")
            if mines_nearby == 0:
                self.clear_zeros(row, col)
            self.check_victory()


    def clear_zeros(self, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.rows and 0 <= c < self.cols and self.buttons[r][c]['state'] == 'normal':
                    self.click(r, c)


    def game_over(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
        self.create_new_game()


    def create_new_game(self):
        self.master.destroy()
        root = tk.Tk()
        root.title("Minesweeper")
        minesweeper = Minesweeper(root, rows = 20, cols = 15, mines = 50)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    minesweeper = Minesweeper(root, rows = 20, cols = 15, mines = 1)
    root.mainloop()
