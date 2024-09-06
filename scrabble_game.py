"""
scrabble_game.py

This module implements a Scrabble game where users input words,
and the score is calculated based on letter values.
The game includes features like time limits, input validation,
word verification, and scoring bonuses based on speed.
"""
import tkinter as tk
import time
import random
from threading import Thread, Event
from spellchecker import SpellChecker

# Initialize the SpellChecker
spell = SpellChecker()


# Calculate Scrabble score
def calculate_score(word):
    """
    Calculate the Scrabble score of a given word based on letter values.
    """
    letter_values = {
        'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1,
        'L': 1, 'N': 1, 'R': 1, 'S': 1, 'T': 1,
        'D': 2, 'G': 2,
        'B': 3, 'C': 3, 'M': 3, 'P': 3,
        'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4,
        'K': 5,
        'J': 8, 'X': 8,
        'Q': 10, 'Z': 10
    }
    return sum(letter_values.get(letter.upper(), 0) for letter in word)


# Check if the word is valid
def is_valid_word(word):
    """
    Check if the input word is valid by verifying it in the dictionary.
    """
    return word.lower() in spell


# Calculate the bonus based on time
def calculate_time_bonus(elapsed_time):
    """
    Calculate the bonus score based on the time taken to input the word.
        0 to 5 seconds:         20 bonus points.
        6 to 10 seconds:        10 bonus points.
        11 to 15 seconds:       5 bonus points.
    """
    if elapsed_time <= 5:
        return 20
    if elapsed_time <= 10:
        return 10
    if elapsed_time <= 15:
        return 5
    return 0


class ScrabbleGame:
    """
    ScrabbleGame class handles the main logic and GUI for the Scrabble game.
    """
    def __init__(self, game_root):
        self.root = game_root
        self.root.title("Scrabble Game")
        # Set fixed window size
        self.root.geometry("400x400")
        self.root.resizable(False, False)  # Disable resizing
        # Initialize game state
        self.required_length = None
        self.total_score = 0
        self.current_round = 0
        self.max_rounds = 10
        self.timer_running = False
        self.stop_event = Event()
        self.timer_thread = None
        # Setup GUI elements
        self.setup_gui()

    def setup_gui(self):
        """
        Set up the GUI elements for the Scrabble game.
        """
        # Round and score display
        self.round_label = tk.Label(
            self.root,
            text=f"Round: {self.current_round + 1}/{self.max_rounds}",
            font=("Arial", 14))
        self.round_label.pack(pady=10)
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.total_score}",
            font=("Arial", 17))
        self.score_label.pack(pady=10)
        self.timer_label = tk.Label(
            self.root,
            text="Time remaining: 15 seconds",
            font=("Arial", 14), fg="red")
        self.timer_label.pack(pady=10)
        self.required_length_label = tk.Label(
            self.root,
            text="Enter a word with exactly X letters",
            font=("Arial", 14))
        self.required_length_label.pack(pady=10)
        # Warning label
        self.warning_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 17), fg="red")
        self.warning_label.pack(pady=10)
        # Entry and buttons
        self.entry = tk.Entry(self.root, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.submit_button = tk.Button(
            self.root,
            text="Submit", command=self.check_word,
            font=("Arial", 14))
        self.submit_button.pack(pady=10)
        self.quit_button = tk.Button(
            self.root,
            text="Quit",
            command=self.quit_game,
            font=("Arial", 14))
        self.quit_button.pack(pady=10)
        # Start the game
        self.start_round()

    def start_round(self):
        """
        Start a new round of the Scrabble game.
        """
        if self.current_round < self.max_rounds:
            self.current_round += 1
            self.round_label.config(
                text=f"Round: {self.current_round}/{self.max_rounds}")
            self.required_length = random.randint(3, 7)
            self.entry.delete(0, tk.END)
            self.required_length_label.config(
                text=(
                    f"Enter a word with exactly {self.required_length} "
                    "letters"
                )
            )
            # Clear any previous warnings
            self.warning_label.config(text="")
            # Start the timer
            self.start_timer()
        else:
            # Show final screen after the last round
            self.show_end_game_screen()

    def start_timer(self):
        """
        Start the countdown timer for each round.
        """
        if self.timer_running and self.timer_thread:
            self.stop_event.set()
            self.timer_thread.join()
        self.stop_event.clear()
        self.timer_running = True
        self.timer_thread = Thread(target=self.countdown_timer)
        self.timer_thread.start()

    def countdown_timer(self):
        """
        Countdown function that updates the timer each second.
        """
        for remaining in range(15, 0, -1):
            if self.stop_event.is_set():
                break
            self.update_timer_display(remaining)
            time.sleep(1)
        if not self.stop_event.is_set():
            self.update_timer_display(0)
            # Show "Time's up!"
            self.warning_label.config(text="Time's up!")
            # Wait a moment before starting a new round
            self.root.after(1000, self.start_round)

    def update_timer_display(self, remaining):
        """
        Update the timer label text in the main thread.
        """
        self.root.after(
            0,
            lambda: self.timer_label.config(
                text=f"Time remaining: {remaining} seconds")
        )

    def check_word(self):
        """
        Check the user's input word for validity
        and update the score accordingly.
        """
        if not self.timer_running:
            return
        user_input = self.entry.get().strip()
        if not user_input.isalpha():
            self.show_warning("Please enter only alphabetic characters.")
            return
        if len(user_input) != self.required_length:
            self.show_warning(
                f"Word must be exactly {self.required_length} letters long.")
            return
        if not is_valid_word(user_input):
            self.show_warning("The word is not in the dictionary.")
            return
        elapsed_time = 15 - int(self.timer_label.cget("text").split()[2])
        base_score = calculate_score(user_input)
        time_bonus = calculate_time_bonus(elapsed_time)
        round_score = base_score + time_bonus
        self.total_score += round_score
        self.score_label.config(text=f"Score: {self.total_score}")
        self.warning_label.config(text="")  # Clear any previous warnings
        # Show score and bonus before moving to the next round
        self.show_score(base_score, time_bonus)

    def show_score(self, base_score, time_bonus):
        """
        Display the score and bonus for the current round.
        """
        self.warning_label.config(
            text=f"Score: {base_score} (Bonus: {time_bonus})",
            fg="green")
        # Wait 2 seconds before starting a new round
        self.root.after(2000, self.start_round)

    def show_end_game_screen(self):
        """
        Display the final score.
        """
        # Hide existing widgets
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Show final score
        final_score_label = tk.Label(
            self.root,
            text=f"Total Score: {self.total_score}",
            font=("Arial", 40))
        final_score_label.pack(pady=20, expand=True)  # Center horizontally

    def show_warning(self, message):
        """
        Display a warning message in red.
        """
        self.warning_label.config(text=message, fg="red")

    def reset_game(self):
        """
        Reset the game state and start a new game.
        """
        # Reset the game state
        self.total_score = 0
        self.current_round = 0
        # Clear the GUI
        for widget in self.root.winfo_children():
            widget.pack_forget()
        # Setup GUI and start a new round
        self.setup_gui()
        self.start_round()

    def quit_game(self):
        """
        Show the final score and quit the game after 2 seconds.
        """
        # Hide existing widgets
        for widget in self.root.winfo_children():
            widget.pack_forget()
        # Show final score
        final_score_label = tk.Label(
            self.root,
            text=f"Total Score: {self.total_score}",
            font=("Arial", 40))
        final_score_label.pack(pady=20, expand=True)  # Center horizontally
        # Wait 2 seconds and then quit the game
        self.root.after(2000, self.root.quit)


# Main loop to run the Scrabble game
if __name__ == "__main__":
    root = tk.Tk()
    game = ScrabbleGame(root)
    root.mainloop()
