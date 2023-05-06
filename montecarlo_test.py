import unittest as u
from unittest.mock import patch
import numpy as np
import pandas as pd
from montecarlo import Die
from io import StringIO
from montecarlo import Game
from montecarlo import Analyzer


class MontecarloSuite(u.TestCase):

    def test_1_change_weight(self):
        """
            Tests whether the weight change works by forcing the outcome
            to be 3 as opposed to a default fair 6-sided die
        """
        dice = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        dice.change_weight(1, 0)
        dice.change_weight(2, 0)
        dice.change_weight(4, 0)
        dice.change_weight(5, 0)
        dice.change_weight(6, 0)
        self.assertEqual(dice.roll()[0], 3)

    def test_2_change_weight_float(self):
        """
            Tests whether a float weight parameter is accepted
        """
        dice = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        dice.change_weight(1, 0.0)
        self.assertEqual(0.0, dice.show()[dice.show()['face'] == 1]['weight'].values[0])

    def test_3_change_weight_int(self):
        """3
            Tests whether a int weight parameter is accepted and returns float
        """
        dice = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        dice.change_weight(1, 0)
        self.assertEqual(0.0, dice.show()[dice.show()['face'] == 1]['weight'].values[0])

    def test_4_change_weight_num_string(self):
        """
            Tests whether a numerical weight parameter is accepted
        """
        dice = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        dice.change_weight(1, '0.0')
        self.assertEqual(0.0, dice.show()[dice.show()['face'] == 1]['weight'].values[0])

    def test_5_change_weight_nonnum_string(self):
        """
            Tests whether a numeriacl weight parameter is rejected
        """
        dice = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        with patch('sys.stdout', new=StringIO()) as fake_out:
            dice.change_weight(1, 'notanumricalstring')
            self.assertEqual(fake_out.getvalue(), "Weight not numerical, please enter a numerical weight\n")

    def test_6_change_weight_rejects_face(self):
        """
            Tests whether a change weight rejects a face outside the Diue
        """
        dice = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        with patch('sys.stdout', new=StringIO()) as fake_out:
            dice.change_weight(13, 0)
            self.assertEqual(fake_out.getvalue(), "Face value not in dictionary\n")

    def test_7_roll_twice(self):
        """
            Tests whether the roll(2) method produces two outputs
        """
        dice = Die(np.array(['H', 'T'], dtype=np.str_))
        dice.change_weight('T', 0)
        self.assertEqual(dice.roll(2), ['H', 'H'])

    def test_8_roll_three_times(self):
        """
            Tests whether the roll(3) method produces two outputs
        """
        dice = Die(np.array(['H', 'T'], dtype=np.str_))
        dice.change_weight('T', 0)
        self.assertEqual(len(dice.roll(3)), 3)

    def test_9_show_die(self):
        """
            Tests show returns the _dice object
        """
        dice = Die(np.array(['H', 'T'], dtype=np.str_))
        self.assertEqual(True, dice._dice.equals(dice.show()))

    def test_10_game_init(self):
        """
            Test whether the game initializer successfully sets the dice list variable
        """
        game = Game([Die(np.array(['H', 'T'], dtype=np.str_)), Die(np.array(['H', 'T'], dtype=np.str_))])
        self.assertEqual(game._dice_list[0]._faces.tolist(), ['H', 'T'])
        self.assertEqual(game._dice_list[0]._w.tolist(), [1.0, 1.0])

    def test_11_play_values(self):
        """
            Test whether the game play function successfully sets the dice list variable
        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('H', 0.0)
        game = Game([d1, d2])
        print("DICE LIST " + str(game._dice_list))
        game.play(2)
        print("DICE ROLLS " + str(game._dice_rolls))
        self.assertEqual([['H', 'T'], ['H', 'T']], game._dice_rolls.values.tolist())

    def test_12_play_index_column(self):
        """
            Test whether the game play function includes the dice numbers as columns
        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('H', 0.0)
        game = Game([d1, d2])
        game.play(2)
        self.assertEqual([1, 2], game._dice_rolls.index.values.tolist())

    def test_13_play_column_name(self):
        """
            Test whether the game play function successfully sets the dice list variable
        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('H', 0.0)
        game = Game([d1, d2])
        game.play(2)
        self.assertEqual(['1', '2'], game._dice_rolls.columns.values.tolist())

    def test_14_play_column_name(self):
        """
            Test whether the game play function column is named correctly
        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('H', 0.0)
        game = Game([d1, d2])
        game.play(2)
        self.assertEqual('roll_number', game._dice_rolls.index.name)

    def test_15_game_show_wide(self):
        """
            Test whether the game show method returns a wide dataframe with roll-game results when wide = 1, True, or default
            The model and result dataframe should look like below
            Index           1      2
            _____
            roll_number
            int           face data type (str here)
            1               'H'    'T'
            2               'H'    'T'

        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('H', 0.0)
        game = Game([d1, d2])
        game.play(2)
        wide_df = pd.DataFrame({'1': ['H', 'H'], '2': ['T', 'T']}, index=[1, 2])
        wide_df.index.name = 'roll_number'
        wide_df['1'] = wide_df['1'].astype('str')
        wide_df['2'] = wide_df['2'].astype('str')
        print(wide_df)
        pd.testing.assert_frame_equal(game.show(wide=1), wide_df, check_names=True, check_index_type=True,
                                      check_column_type=True)
        pd.testing.assert_frame_equal(game.show(wide=True), wide_df, check_names=True, check_index_type=True,
                                      check_column_type=True)
        pd.testing.assert_frame_equal(game.show(1), wide_df, check_names=True, check_index_type=True,
                                      check_column_type=True)

    def test_16_game_show_narrow(self):
        """
            Test whether the game show method returns a narrow dataframe with roll-game results when wide = 0 or False
            The model and result dataframe should look like below

            Index
            _______________________________      face_value
            roll_number  dice_number_or_id        face value of input die (str here)
            int               str
            1                  1                      H
            1                  2                      T
            2                  1                      H
            3                  2                      T

        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('H', 0.0)
        game = Game([d1, d2])
        game.play(2)
        narrow_df = pd.DataFrame({'roll_number': [1, 1, 2, 2], 'dice_number_or_id': ['1', '2', '1', '2'],
                                  'face_value': ['H', 'T', 'H', 'T']})
        narrow_df['roll_number'] = narrow_df['roll_number'].astype(int)
        narrow_df['dice_number_or_id'] = narrow_df['dice_number_or_id'].astype(str)
        narrow_df['face_value'] = narrow_df['face_value'].astype(str)
        narrow_df.set_index(['roll_number', 'dice_number_or_id'], inplace=True)
        pd.testing.assert_frame_equal(game.show(wide=0), narrow_df, check_names=True, check_index_type=True,
                                      check_column_type=True)
        pd.testing.assert_frame_equal(game.show(wide=False), narrow_df, check_names=True, check_index_type=True,
                                      check_column_type=True)

    def test_17_catch_exception_in_game_show(self):
        """
            Test whether non-boolean/binary/default input argument to wide returns a typeerror exception
        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('H', 0.0)
        game = Game([d1, d2])
        self.assertRaises(TypeError, game.show(wide="banana"))

    def test_18_analyzer_init(self):
        """
            Test whether the analyzer object includes the expected di(c)e
        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('H', 0.0)
        game = Game([d1, d2])
        game.play(2)
        analyzer_bot = Analyzer(game)
        self.assertEqual([d1, d2], analyzer_bot._game._dice_list)

    def test_19_jackpot_count(self):
        """
            Test that the jackpot method accurately calculates jackpots
            Create two loaded di(c)e that always produce heads, roll twice, yielding two jackpots
        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('T', 0.0)
        game = Game([d1, d2])
        analyzer_bot = Analyzer(game)
        game.play(2)
        self.assertEqual(2, analyzer_bot.jackpot())

    def test_20_jackpot_df(self):
        """
            Test that the jackpot method saves the jackpot values in a wide dataframe
            Roll a 6 sided dice a ton of times and check that each row has min value = max value
        """
        d1 = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        d2 = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        d3 = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        d4 = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        d5 = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        d6 = Die(np.array([1, 2, 3, 4, 5, 6], dtype=np.int64))
        game = Game([d1, d2, d3, d4, d5, d6])
        game.play(100)
        analyzer_bot = Analyzer(game)
        analyzer_bot.jackpot()
        wide_results = game.show(wide=1).sort_index()
        not_jackpot_df = wide_results[~((wide_results['1'] == wide_results['2'])
                                        & (wide_results['2'] == wide_results['3']) & (
                                                    wide_results['3'] == wide_results['4'])
                                        & (wide_results['4'] == wide_results['5']) & (
                                                    wide_results['5'] == wide_results['6']))]
        reconstituted_wide_results = pd.concat([analyzer_bot.jackpot_df, not_jackpot_df]).sort_index()
        pd.testing.assert_frame_equal(wide_results, reconstituted_wide_results, check_names=True, check_index_type=True,
                                      check_column_type=True)
        self.assertEqual('roll_number', analyzer_bot.jackpot_df.index.name)

    def test_22_combo(self):
        """
        Test that a dataframe with dupliates becomes unique and with count of duplicates when combo function is applied
        Example below is a dataframe with three heads becomes one with 1 head and a count of 3
        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('T', 0.0)
        d3 = Die(np.array(['H', 'T'], dtype=np.str_))
        d3.change_weight('T', 0.0)
        game = Game([d1, d2, d3])
        game.play(3)
        analyzer_bot = Analyzer(game)
        model_df = pd.DataFrame({'1': ['H'], '2': ['H'], '3': ['H'], 'count': [3]})
        model_df.set_index(['1', '2', '3'], inplace=True)
        model_df.index.name = 'roll_number'
        analyzer_bot.combo()
        pd.testing.assert_frame_equal(model_df, analyzer_bot.combo_df, check_names=True, check_index_type=True,
                                      check_column_type=True)

    def test_23_face_counts_per_roll(self):
        """
        Test that the reported face counts are consistent with the results of the game
        Model will be
                       H      T
        roll_number
        int           int    int
        1              3      0
        2              3      0
        3              3      0

        """
        d1 = Die(np.array(['H', 'T'], dtype=np.str_))
        d1.change_weight('T', 0.0)
        d2 = Die(np.array(['H', 'T'], dtype=np.str_))
        d2.change_weight('T', 0.0)
        d3 = Die(np.array(['H', 'T'], dtype=np.str_))
        d3.change_weight('T', 0.0)
        game = Game([d1, d2, d3])
        game.play(3)
        analyzer_bot = Analyzer(game)
        model_df = pd.DataFrame({'H': [3, 3, 3], 'T': [0, 0, 0], 'roll_number': [1, 2, 3]}, dtype=object)
        model_df.set_index('roll_number', inplace=True)
        analyzer_bot.face_counts_per_roll()
        pd.testing.assert_frame_equal(model_df, analyzer_bot.face_counts_per_roll_df, check_names=True,
                                      check_index_type=True, check_column_type=True)


if __name__ == '__main__':
    u.main(verbosity=3)


