"""
Unit tests for the Scrabble game application.

This module contains tests for the ScrabbleGame class and associated functions.
Tests include score calculation, case insensitivity, input validation,
word length check, dictionary validation, and timer-based scoring.
"""

import unittest
from unittest.mock import patch
from tkinter import Tk, Label, Entry

from scrabble_game import calculate_score, ScrabbleGame


class TestScrabbleGame(unittest.TestCase):
    """
    Unit test case for the ScrabbleGame class.

    This class contains tests for various functionalities of the Scrabble game,
    including score calculation, input validation, and game state management.
    """

    def setUp(self):
        """
        Set up the testing environment before each test.

        Initializes the Tkinter root window, ScrabbleGame instance,
        and GUI components used in the tests.
        """
        self.root = Tk()
        self.game = ScrabbleGame(self.root)
        self.game.entry = Entry(self.root)
        self.game.warning_label = Label(self.root)
        self.game.timer_label = Label(self.root)
        self.game.entry.pack()
        self.game.warning_label.pack()
        self.game.timer_label.pack()

    def tearDown(self):
        """
        Clean up the testing environment after each test.
        Destroys the Tkinter root window to free resources.
        """
        self.root.destroy()

    def test_calculate_score(self):
        """
        Test the calculate_score function with various inputs.
        Verifies that the function correctly calculates
        the score for different words, regardless of letter case.
        """
        self.assertEqual(calculate_score('apple'), 9)
        self.assertEqual(calculate_score('orange'), 7)

    def test_upper_lower_case(self):
        """
        Test case insensitivity of the calculate_score function.
        Ensures that uppercase and lowercase letters are treated equally.
        """
        self.assertEqual(calculate_score('A'), calculate_score('a'))
        self.assertEqual(calculate_score('HELLO'), calculate_score('hello'))
        self.assertEqual(calculate_score('orange'), calculate_score('oRANGe'))

    def test_non_alphabet_input_1(self):
        """
        Test handling of non-alphabetic input in the entry field.
        Verifies that the program displays a warning message
        when non-alphabetic characters are entered.
        """
        self.game.entry.insert(0, '123')
        self.game.check_word()
        self.assertEqual(
            self.game.warning_label.cget('text'),
            "Please enter only alphabetic characters.")

    def test_non_alphabet_input_2(self):
        """
        Test handling of non-alphabetic input in the entry field.
        Verifies that the program displays a warning message
        when non-alphabetic characters are entered.
        """
        self.game.entry.insert(0, '1a2b3')
        self.game.check_word()
        self.assertEqual(
            self.game.warning_label.cget('text'),
            "Please enter only alphabetic characters.")

    def test_input_length_check_below(self):
        """
        Test validation of word length in the entry field.
        Checks that a warning message is displayed if the input word does not
        match the required length.
        """
        self.game.required_length = 5
        self.game.entry.insert(0, 'hi')
        self.game.check_word()
        self.assertEqual(
            self.game.warning_label.cget('text'),
            "Word must be exactly 5 letters long.")

    def test_input_length_check_above(self):
        """
        Test validation of word length in the entry field.
        Checks that a warning message is displayed if the input word does not
        match the required length.
        """
        self.game.required_length = 5
        self.game.entry.insert(0, 'orange')
        self.game.check_word()
        self.assertEqual(
            self.game.warning_label.cget('text'),
            "Word must be exactly 5 letters long.")

    def test_valid_word_from_dictionary(self):
        """
        Test validation of the input word against a dictionary.
        Ensures that a warning message is displayed if the word is not found
        in the dictionary.
        """
        self.game.required_length = 6
        self.game.entry.insert(0, 'quoxyz')
        self.game.check_word()
        self.assertEqual(
            self.game.warning_label.cget('text'),
            "The word is not in the dictionary.")

    @patch('scrabble_game.time.sleep', return_value=None)
    def test_timer_and_score_bonus_5(self, _):
        """
        Test the timer and score bonus functionality.
        Mocks the sleep function to avoid delays and checks that the correct
        score and bonus are displayed based on the time remaining.
        """
        self.game.required_length = 7
        self.game.entry.insert(0, 'cabbage')
        self.game.timer_label.config(text="Time remaining: 4 seconds")
        self.game.check_word()
        self.assertIn(
            "Score: 14 (Bonus: 5)",
            self.game.warning_label.cget('text'))

    @patch('scrabble_game.time.sleep', return_value=None)
    def test_timer_and_score_bonus_10(self, _):
        """
        Test the timer and score bonus functionality.
        Mocks the sleep function to avoid delays and checks that the correct
        score and bonus are displayed based on the time remaining.
        """
        self.game.required_length = 7
        self.game.entry.insert(0, 'cabbage')
        self.game.timer_label.config(text="Time remaining: 7 seconds")
        self.game.check_word()
        self.assertIn(
            "Score: 14 (Bonus: 10)",
            self.game.warning_label.cget('text'))

    @patch('scrabble_game.time.sleep', return_value=None)
    def test_timer_and_score_bonus_20(self, _):
        """
        Test the timer and score bonus functionality.
        Mocks the sleep function to avoid delays and checks that the correct
        score and bonus are displayed based on the time remaining.
        """
        self.game.required_length = 7
        self.game.entry.insert(0, 'cabbage')
        self.game.timer_label.config(text="Time remaining: 12 seconds")
        self.game.check_word()
        self.assertIn(
            "Score: 14 (Bonus: 20)",
            self.game.warning_label.cget('text'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
