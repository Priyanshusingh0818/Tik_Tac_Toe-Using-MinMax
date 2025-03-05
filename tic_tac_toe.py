import tkinter as tk
from tkinter import messagebox, ttk
import copy

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Neon Tic Tac Toe")
        self.window.configure(bg='black')
        self.window.minsize(500, 600)

        self.board_size = 3  
        self.init_game_state()
        
        self.container = tk.Frame(self.window, bg='black')
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_menu_frame()
        self.create_game_frame()
        
        self.create_board()
        self.style_config()
        
        self.window.mainloop()

    def init_game_state(self):
        """Initialize or reset game state variables"""
        self.board = [[" " for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.player = "X"
        self.ai = "O"
        self.board_history = []
        self.current_player = "X"
        self.game_mode = "AI"

    def create_menu_frame(self):
        self.menu_frame = tk.Frame(self.container, bg='black')
        self.menu_frame.pack(fill=tk.X, pady=(0, 20))
        
        size_label = tk.Label(
            self.menu_frame,
            text="Board Size:",
            bg='black',
            fg='#00ff00',  # Neon green
            font=('Arial', 12)
        )
        size_label.pack(side=tk.LEFT, padx=5)
        
        self.size_var = tk.StringVar(value="3x3")
        size_menu = ttk.OptionMenu(
            self.menu_frame,
            self.size_var,
            "3x3",
            "3x3",
            "4x4",
            "5x5",
            command=self.change_board_size
        )
        size_menu.pack(side=tk.LEFT, padx=5)
        
        mode_label = tk.Label(
            self.menu_frame,
            text="Mode:",
            bg='black',
            fg='#00ff00', 
            font=('Arial', 12)
        )
        mode_label.pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="AI")
        mode_menu = ttk.OptionMenu(
            self.menu_frame,
            self.mode_var,
            "AI",
            "AI",
            "2 Players",
            command=self.change_game_mode
        )
        mode_menu.pack(side=tk.LEFT, padx=5)

    def create_game_frame(self):
        self.game_frame = tk.Frame(self.container, bg='black')
        self.game_frame.pack(expand=True, fill=tk.BOTH)
        
        self.status_label = tk.Label(
            self.game_frame,
            text="Player X's turn",
            font=('Arial', 14),
            bg='black',
            fg='#00ff00'  
        )
        self.status_label.pack(pady=(0, 10))
        
        self.board_frame = tk.Frame(self.game_frame, bg='black')
        self.board_frame.pack(expand=True)
        
        self.control_frame = tk.Frame(self.game_frame, bg='black')
        self.control_frame.pack(pady=(20, 0))
        
        button_style = {
            'bg': 'black',
            'fg': '#00ff00',  
            'font': ('Arial', 12),
            'relief': 'raised',
            'borderwidth': 2
        }
        
        self.undo_button = tk.Button(
            self.control_frame,
            text="Undo Move",
            command=self.undo_move,
            **button_style
        )
        self.undo_button.pack(side=tk.LEFT, padx=5)
        
        self.hint_button = tk.Button(
            self.control_frame,
            text="Get Hint",
            command=self.show_hint,
            **button_style
        )
        self.hint_button.pack(side=tk.LEFT, padx=5)
        
        self.new_game_button = tk.Button(
            self.control_frame,
            text="New Game",
            command=self.reset_game,
            **button_style
        )
        self.new_game_button.pack(side=tk.LEFT, padx=5)

    def create_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col] = tk.Button(
                    self.board_frame,
                    text=" ",
                    font=('Arial', 24, 'bold'),
                    width=3,
                    height=1,
                    bg='black',
                    fg='#00ff00',  # Neon green text
                    activebackground='#003300',  
                    relief='raised',
                    borderwidth=2,
                    command=lambda r=row, c=col: self.player_move(r, c)
                )
                self.buttons[row][col].grid(
                    row=row,
                    column=col,
                    padx=2,
                    pady=2,
                    ipadx=10,
                    ipady=10
                )

    def style_config(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))
        style.configure('TMenubutton', font=('Arial', 12))

    def change_board_size(self, size_str):
        self.board_size = int(size_str[0])
        self.init_game_state()
        self.create_board()
        self.reset_game()

    def undo_move(self):
        if len(self.board_history) > 0:
            self.board = copy.deepcopy(self.board_history.pop())
            self.update_board_display()
            self.current_player = "X" if self.current_player == "O" else "O"
            self.status_label.config(text=f"Player {self.current_player}'s turn")

    def update_board_display(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col].config(text=self.board[row][col])
                if self.board[row][col] == "X":
                    self.buttons[row][col].config(fg='#ff0000')  # Neon red for X
                elif self.board[row][col] == "O":
                    self.buttons[row][col].config(fg='#00ff00')  # Neon green for O

    def player_move(self, row, col):
        if self.board[row][col] == " ":
            self.board_history.append(copy.deepcopy(self.board))
            
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(
                text=self.current_player,
                fg='#ff0000' if self.current_player == 'X' else '#00ff00'
            )
            
            if self.check_winner(self.current_player):
                self.game_over(f"{self.current_player} wins!")
            elif self.is_draw():
                self.game_over("It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(text=f"Player {self.current_player}'s turn")
                
                if self.game_mode == "AI" and self.current_player == "O":
                    self.window.after(500, self.ai_move)

    def ai_move(self):
        if self.board_size > 3:
            self.make_simple_ai_move()
        else:
            self.make_minimax_move()

    def make_simple_ai_move(self):
        """Simple AI for larger boards"""
        import random
        empty_cells = [
            (r, c) for r in range(self.board_size) 
            for c in range(self.board_size) 
            if self.board[r][c] == " "
        ]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.player_move(row, col)

    def make_minimax_move(self):
        """Minimax AI for 3x3 board"""
        best_score = -float("inf")
        best_move = None
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == " ":
                    self.board[row][col] = self.ai
                    score = self.minimax(self.board, False)
                    self.board[row][col] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        if best_move:
            row, col = best_move
            self.player_move(row, col)

    def show_hint(self):
        if self.board_size > 3:
            messagebox.showinfo("Hint", "Hints are only available for 3x3 board")
            return
            
        if " " in [cell for row in self.board for cell in row]:
            best_move = self.get_best_move()
            if best_move:
                row, col = best_move
                current_bg = self.buttons[row][col]['bg']
                self.buttons[row][col].config(bg='#003300')  # Highlight hint
                self.window.after(1000, lambda: self.buttons[row][col].config(bg=current_bg))

    def check_winner(self, player):
        for i in range(self.board_size):
            if all(self.board[i][j] == player for j in range(self.board_size)) or \
               all(self.board[j][i] == player for j in range(self.board_size)):
                return True
        
        if all(self.board[i][i] == player for i in range(self.board_size)) or \
           all(self.board[i][self.board_size-1-i] == player for i in range(self.board_size)):
            return True
        
        return False

    def is_draw(self):
        return all(cell != " " for row in self.board for cell in row)

    def game_over(self, message):
        messagebox.showinfo("Game Over", message)
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col]['state'] = 'disabled'

    def reset_game(self):
        self.init_game_state()
        self.create_board()
        self.status_label.config(text="Player X's turn")

    def change_game_mode(self, mode):
        self.game_mode = "AI" if mode == "AI" else "2Player"
        self.reset_game()

    # Minimax methods remain the same as before...
    def minimax(self, board, is_maximizing):
        if self.check_winner(self.ai):
            return 10
        if self.check_winner(self.player):
            return -10
        if self.is_draw():
            return 0
        
        if is_maximizing:
            best_score = -float("inf")
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if board[row][col] == " ":
                        board[row][col] = self.ai
                        score = self.minimax(board, False)
                        board[row][col] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if board[row][col] == " ":
                        board[row][col] = self.player
                        score = self.minimax(board, True)
                        board[row][col] = " "
                        best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        best_score = -float("inf")
        best_move = None
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == " ":
                    self.board[row][col] = self.current_player
                    score = self.minimax(self.board, False)
                    self.board[row][col] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        return best_move

if __name__ == "__main__":
    TicTacToe()