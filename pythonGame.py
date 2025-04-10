import tkinter as tk
import random
import time

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Emoji Memory Puzzle By Pratiksha")
        self.root.config(bg="#f0f4f8")
        self.root.geometry("620x720")
        self.root.resizable(False, False)

        self.score_history = []  # 🔁 store scores from multiple games

        self.reset_game()

    def reset_game(self):
        self.grid_size = None
        self.total_pairs = None
        self.emojis = []
        self.buttons = []
        self.emoji_colors = [
            "#FF5733", "#33C1FF", "#33FF57", "#F333FF",
            "#FFB533", "#8E44AD", "#2ECC71", "#E74C3C",
            "#3498DB", "#F1C40F", "#D35400", "#1ABC9C"
        ]
        self.first_click = None
        self.second_click = None
        self.locked = True
        self.score = 0
        self.start_time = None
        self.countdown_seconds = 3
        self.hint_limit = 2

        self.countdown_label = None
        self.top_frame = None
        self.game_frame = None
        self.score_label = None
        self.timer_label = None
        self.restart_btn = None
        self.end_btn = None
        self.hint_btn = None
        self.start_btns = []

        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_start_now_ui()

    def create_start_now_ui(self):
        title = tk.Label(self.root, text="🎲 Emoji Memory Puzzle 🎲",
                         font=("Comic Sans MS", 22, "bold"), bg="#f0f4f8", fg="#333")
        title.pack(pady=80)

        start_btn = tk.Button(self.root, text="Start Now", font=("Arial", 16, "bold"),
                              bg="#007bff", fg="white", padx=20, pady=10,
                              command=self.create_difficulty_ui)
        start_btn.pack(pady=20)

    def create_difficulty_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="🎮 Choose Difficulty Level",
                         font=("Comic Sans MS", 18, "bold"), bg="#f0f4f8", fg="#333")
        title.pack(pady=40)

        difficulties = [("Easy (4x4)", 4), ("Medium (6x6)", 6), ("Hard (8x8)", 8)]
        for label, size in difficulties:
            btn = tk.Button(self.root, text=label, font=("Arial", 14, "bold"),
                            bg="#28a745", fg="white", padx=20, pady=10,
                            command=lambda size=size: self.set_difficulty(size))
            btn.pack(pady=5)
            self.start_btns.append(btn)

    def set_difficulty(self, size):
        self.grid_size = size
        self.total_pairs = (size * size) // 2

        emoji_pool = [
            '🐶','🐱','🐭','🐹','🐰','🦊','🐻','🐼','🐨','🐯',
            '🦁','🐮','🐷','🐸','🐵','🐔','🐧','🐢','🐍','🐙',
            '🦋','🐞','🐝','🦄','🐬','🐳','🦕','🦖','🐲','🐊',
            '🐘','🐓','🦜','🦩','🦔','🐿️'
        ]
        self.emojis = random.sample(emoji_pool, self.total_pairs) * 2
        random.shuffle(self.emojis)

        for btn in self.start_btns:
            btn.destroy()

        self.start_countdown()

    def start_countdown(self):
        self.countdown_label = tk.Label(self.root, text="", font=("Comic Sans MS", 26, "bold"),
                                        bg="#f0f4f8", fg="#444")
        self.countdown_label.pack(pady=200)
        self.run_countdown()

    def run_countdown(self):
        if self.countdown_seconds >= 0:
            self.countdown_label.config(text=f"Starting in {self.countdown_seconds}...")
            self.countdown_seconds -= 1
            self.root.after(1000, self.run_countdown)
        else:
            self.countdown_label.destroy()
            self.start_game()

    def start_game(self):
        self.start_time = time.time()
        self.locked = False
        self.create_ui()
        self.update_timer()

    def create_ui(self):
        self.top_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.top_frame.pack(pady=10)

        self.score_label = tk.Label(self.top_frame, text="Score: 0", font=("Arial", 12, "bold"),
                                    bg="#f0f4f8", fg="#333")
        self.score_label.pack(side="left", padx=20)

        self.timer_label = tk.Label(self.top_frame, text="Time: 0s", font=("Arial", 12, "bold"),
                                    bg="#f0f4f8", fg="#333")
        self.timer_label.pack(side="left", padx=20)

        self.hint_btn = tk.Button(self.top_frame, text=f"💡 Hint ({self.hint_limit})", font=("Arial", 12),
                                  bg="#ffc107", fg="black", command=self.show_hint)
        self.hint_btn.pack(side="left", padx=10)

        self.end_btn = tk.Button(self.top_frame, text="❌ End Game", font=("Arial", 12),
                                 bg="#dc3545", fg="white", command=self.end_game)
        self.end_btn.pack(side="left", padx=10)

        self.game_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.game_frame.pack()

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                color = random.choice(self.emoji_colors)
                btn = tk.Button(
                    self.game_frame,
                    text=" ",
                    width=3,
                    height=1,
                    font=("Arial", 24),
                    bg="white",
                    fg=color,
                    activebackground="white",
                    command=lambda i=i, j=j: self.reveal(i, j)
                )
                btn.grid(row=i, column=j, padx=3, pady=3)
                row.append(btn)
            self.buttons.append(row)

    def show_hint(self):
        if self.locked or self.hint_limit == 0:
            return
        self.hint_limit -= 1
        self.hint_btn.config(text=f"💡 Hint ({self.hint_limit})")
        self.locked = True
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                index = i * self.grid_size + j
                self.buttons[i][j]["text"] = self.emojis[index]
        self.root.after(1000, self.hide_all_unmatched)

    def hide_all_unmatched(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.buttons[i][j]["state"] != "disabled":
                    self.buttons[i][j]["text"] = " "
        self.locked = False

    def reveal(self, i, j):
        if self.locked or self.buttons[i][j]["state"] == "disabled":
            return

        index = i * self.grid_size + j
        btn = self.buttons[i][j]
        btn["text"] = self.emojis[index]
        btn.update_idletasks()

        if not self.first_click:
            self.first_click = (i, j)
        elif not self.second_click and (i, j) != self.first_click:
            self.second_click = (i, j)
            self.check_match()

    def check_match(self):
        self.locked = True
        i1, j1 = self.first_click
        i2, j2 = self.second_click

        index1 = i1 * self.grid_size + j1
        index2 = i2 * self.grid_size + j2

        if self.emojis[index1] == self.emojis[index2]:
            self.root.after(500, self.disable_buttons, i1, j1, i2, j2)
        else:
            self.root.after(800, self.hide_buttons, i1, j1, i2, j2)

    def disable_buttons(self, i1, j1, i2, j2):
        self.buttons[i1][j1]["state"] = "disabled"
        self.buttons[i2][j2]["state"] = "disabled"
        self.score += 1
        self.score_label.config(text=f"Score: {self.score * 2}")
        self.reset_turn()

        if self.score == self.total_pairs:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"🎉 Completed in {elapsed}s!")
            self.show_celebration(elapsed)

    def hide_buttons(self, i1, j1, i2, j2):
        self.buttons[i1][j1]["text"] = " "
        self.buttons[i2][j2]["text"] = " "
        self.reset_turn()

    def reset_turn(self):
        self.first_click = None
        self.second_click = None
        self.locked = False

    def update_timer(self):
        if self.total_pairs and self.score < self.total_pairs:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def end_game(self):
        elapsed = int(time.time() - self.start_time)
        self.show_celebration(elapsed)

    def show_celebration(self, time_taken):
        for widget in self.root.winfo_children():
            widget.destroy()

        score = self.score * 2
        self.score_history.append((score, time_taken))

        msg = f"🎉 You scored {score} points in {time_taken}s!"
        summary = "\n".join([f"Game {i+1}: {s} pts in {t}s" for i, (s, t) in enumerate(self.score_history)])

        tk.Label(self.root, text=msg, font=("Comic Sans MS", 18, "bold"), bg="#f0f4f8", fg="#28a745").pack(pady=30)
        tk.Label(self.root, text="🏆 Score History", font=("Arial", 14, "bold"), bg="#f0f4f8", fg="#555").pack(pady=5)
        tk.Label(self.root, text=summary, font=("Arial", 12), bg="#f0f4f8", fg="#555").pack(pady=10)

        restart = tk.Button(self.root, text="🔁 Play Again", font=("Arial", 14),
                            bg="#007bff", fg="white", command=self.reset_game)
        restart.pack(pady=20)

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()  