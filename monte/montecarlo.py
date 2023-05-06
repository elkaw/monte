import numpy as np
import pandas as pd


class Die:
    """
        A die has N sides, or “faces”, and W weights, and can be rolled to select a face.
            -W defaults to 1.0 for each face but can be changed after the object is created.
            -Note that the weights are just numbers, not a normalized probability distribution.
            -The die has one behavior, which is to be rolled one or more times.
            -Note that what we are calling a “die” here can be any discrete
             random variable associated with a stochastic process, such as
            using a deck of cards or flipping a coin or speaking a language.
            - Our probability model for such variable is, however, very simple
            – since our weights apply to only to single events, we are assuming that the events are independent.
            This makes sense for coin tosses but not for language use.
    """
    _faces = np.array([1.0], dtype=np.float)
    _w = np.array([1.0], dtype=np.float)
    _dice = pd.DataFrame({"face": [_faces], "weight": [_w]})

    def __init__(self, faces):
        """
        This function will initialize a "dice"
        which defines a space of outcomes and the probability of each one happening

        INPUT:
            faces: numpy array of strings or numbers which represents a possible outcome of a dice

        OUTPUT:
            Updates the dataframe attribute that represents the dice
        """
        self._faces = faces
        if self._faces.dtype in (np.short, np.ushort, np.intc, np.uintc, np.int_, np.uint, np.longlong, np.ulonglong,
                                 np.float16, np.float, np.cfloat, np.single, np.double, np.longdouble, np.float64,
                                 np.int64, np.string_, np.str)\
                or self._faces.dtype.type in (np.string_, np.str_) or self._faces.dtype.kind in ('f', 'i', 'u', 'S', 'U'):

            self._w = np.array([1 for i in faces.tolist()], dtype=np.float32)
            self._dice = pd.DataFrame({"face": self._faces.tolist(), "weight": self._w.tolist()}, index=list(range(len(self._faces.tolist
                                                                                                                       ()))))
            if self._faces.dtype.type in (np.string_, np.str_) or self._faces.dtype.kind in ('S', 'U'):
                self._dice['face'] = self._dice['face'].astype('string')
        else:
            print("Please pass a numerical or string dtype numpy array")

    def change_weight(self, face, weight):
        """
        This function will change the weight of a the passed dice face to be the argument passed into the function

        INPUT:
            face: identifies the face that should have its weight changed
            weight: desired weight

        OUTPUT:
            The dice attribute will be updated to reflect the desired face-weight combination

        """
        if self._dice[self._dice['face'] == face].shape[0] > 0:
            if type(weight) == int or type(weight) == float:
                self._dice.loc[self._dice['face'] == face, "weight"] = float(weight)
            elif type(weight) == str:
                if weight.isnumeric() or weight.replace('.', '', 1).isdigit():
                    self._dice.loc[self._dice['face'] == face, "weight"] = float(weight)
                else:
                    print("Weight not numerical, please enter a numerical weight")
            else:
                print("Weight not numerical, please enter a numerical weight")
        else:
            print("Face value not in dictionary")

    def roll(self, roll_count=1):
        """
        Chooses faces based on the probability weights. Returns the number of faces defined in roll_count in a list.

        INPUT:
            rollCount: number of faces to return (number of rolls)

        OUTPUT:
            outcomes: list of results with the result count = rowCount parameter
        """
        outcomes = []
        print(self._dice.sample(n=1, weights=self._dice['weight'].to_numpy())['face'].values[0])
        for i in range(roll_count):
            outcomes.append(self._dice.sample(n=1, weights=self._dice['weight'].to_numpy())['face'].values[0])
        return outcomes

    def show(self):
        """
        Returns the faces, weights dice dataframe
        OUTPUT:
            dice: faces, weight dataframe
        """

        return self._dice


class Game:
    """
        A game consists of rolling of one or more dice of the same kind one or more times.
        Each game is initialized with one or more of similarly defined dice (Die objects).
        By “same kind” and “similarly defined” we mean that each die in a given game has...
        the same number of sides and associated faces,
        but each die object may have its own weights.
        The class has a behavior to play a game, i.e. to rolls all of the dice a given number of times.
        The class keeps the results of its most recent play.
    """

    _dice_list = []
    _dice_rolls = None

    def __init__(self, dice_list):
        """
        Takes a single parameter, a list of already instantiated similar Die objects.

        INPUT:
            dice_list: list of dice objects that will be rolled
        """
        self._dice_list = dice_list

    def play(self, roll_count):
        """
            Takes a parameter to specify how many times the dice should be rolled.
            Saves the result of the play to a private dataframe of shape N rolls by M dice.
            The private dataframe should have the roll number is (as) a named index.
            This results in a table of data with columns for roll number, the die number (its list index),
            and the face rolled in that instance.

            INPUT:
                rollCount: Number of rolls for all di(c)e
        """
        self._dice_rolls = pd.DataFrame(columns=[str(i+1) for i in range(len(self._dice_list))])
        self._dice_rolls['roll_number'] = [i+1 for i in range(roll_count)]
        self._dice_rolls.set_index('roll_number',inplace=True)
        self._dice_rolls.index.name = 'roll_number'
        dice_number = 1
        print(["IN METHOD DICE LIST"] + self._dice_list)
        for dice in self._dice_list:
            self._dice_rolls[str(dice_number)] = dice.roll(roll_count)
            dice_number = dice_number + 1

    def show(self, wide=True):
        """
        A method to show the user the results of the most recent play.
        This method just passes the private dataframe to the user.
        Takes a parameter to return the dataframe in narrow or wide form.
        This parameter defaults to wide form.
        This parameter should raise an exception of the user passes an invalid option.
        The narrow form of the dataframe will have a two column index with the roll number and the die number,
        and a column for the face rolled.
        The wide form of the dataframe will a single column index with the roll number, and each die number as a column.
        INPUT
            wide: True returns a dataframe which each row as a series of face values of all di(c)e rolled, False
            returns a dataframe where each row is a value for an individual di(c)e

        OUTPUT
            dice_rolls:
        """
        try:
            if wide:
                return self._dice_rolls
            else:
                self._dice_rolls.reset_index(inplace=True)
                melted_frame = pd.melt(self._dice_rolls, id_vars='roll_number', var_name='dice_number_or_id', value_name='face_value', ignore_index=True)
                #melted_frame. reset_index(inplace=True))
                melted_frame['roll_number'] = melted_frame['roll_number'].astype(int)
                melted_frame.set_index(['roll_number', 'dice_number_or_id'], inplace=True)
                melted_frame.sort_values(['roll_number', 'dice_number_or_id', 'face_value'], ascending=True, inplace=True)
                self._dice_rolls.set_index('roll_number', inplace=True)
                return melted_frame
        except TypeError:
            print("Please pass a boolean (True or False) or a 1 or 0 for the wide argument")


class Analyzer:
    """
    An analyzer takes the results of a single game and computes various
    descriptive statistical properties about it. These properties results are
    available as attributes of an Analyzer object. Attributes (and associated methods) include:
        -A face counts per roll, i.e. the number of times a given face
        appeared in each roll. For example, if a roll of five dice has all
        sixes, then the counts for this roll would be 6 for the face value '6' and 0 for the other faces.
        - A jackpot count, i.e. how many times a roll resulted in all faces being the same,
        e.g. all one for a six-sided die.
        - A combo count, i.e. how many combination types of faces were rolled and their counts.

    """
    _game = None
    jackpot_df = None
    combo_df = None
    face_counts_per_roll_df = None
    _faces = None
    die_face_type = None

    def __init__(self, game):
        """
        Takes a game object as its input parameter.
        At initialization time, it also infers the data type of the di(c)e faces used.

        INPUT:
        game: a completed game with one or more dice rolls with one or multiple di(c)e
        """
        self._faces = game._dice_list[0]._faces
        die_face_type = type(self._faces)
        self._game = game

    def jackpot(self):
        """"
        A jackpot method to compute how many times the game resulted in all faces being identical.
            -Returns an integer for the number times to the user.
            -Stores the results as a dataframe of jackpot results in a public attribute.
            -The dataframe should have the roll number as a named index.
        """

        game_results_df = self._game.show(wide=False)
        game_results_df.reset_index(inplace=True)
        game_results_df_reduced = game_results_df[['roll_number', 'face_value']]
        game_results_df_count_summary = game_results_df_reduced.groupby(game_results_df_reduced["roll_number"]).agg(face_value=('face_value','nunique')).reset_index()
        game_results_df_wide = self._game.show(wide=True).reset_index()
        self.jackpot_df = game_results_df_wide[game_results_df_wide['roll_number'].isin(game_results_df_count_summary[game_results_df_count_summary['face_value']==1]['roll_number']) ]
        self.jackpot_df.set_index("roll_number", inplace=True)
        self.jackpot_df.index.name = "roll_number"
        return self.jackpot_df.shape[0]# game_results_df[['roll_number', 'face_value']].groupby("roll_number").agg({'face_value':'count'}).reset_index().shape[0]

    def combo(self):
        """
        A combo method to compute the distinct combinations of faces rolled, along with their counts.
            - Combinations should be sorted and saved as a multi-columned index.
            - Stores the results as a dataframe in a public attribute.
        """
        game_results_df = self._game.show(wide=True)
        game_results_df.reset_index(inplace=True)
        columns = [ col for col in game_results_df.columns.values.tolist() ] #if col not in ['face_value', 'roll_number']
        game_results_df = game_results_df[columns]
        dice_name_columns = [col for col in columns if col != "roll_number"]
        game_results_combo_count = game_results_df.groupby(dice_name_columns).agg(count=('roll_number','count'))
        game_results_combo_count.reset_index(inplace=True)
        #game_results_combo_count.sort_values('count', ascending=False, inplace=True)
        game_results_combo_count_sorted = game_results_combo_count.set_index(dice_name_columns)
        self.combo_df = game_results_combo_count_sorted.sort_index(level=sorted(dice_name_columns))

    def face_counts_per_roll(self):
        """
        A face counts per roll method to compute how many times a given face is rolled in each event.
            - Stores the results as a dataframe in a public attribute.
            - The dataframe has an index of the roll number and face values as columns (i.e. it is in wide format).
        """
        game_results_df_long = self._game.show(wide=False)
        game_results_df_long.reset_index(inplace=True)
        roll_face_value_count_summary = game_results_df_long.\
            groupby(['roll_number', 'face_value']).agg(count=("dice_number_or_id", 'count'))
        roll_face_value_count_summary.reset_index(inplace=True)
        roll_number_list = self._game.show(wide=True).index.values.tolist()
        self.face_counts_per_roll_df = pd.DataFrame(data={**{face:["" for i in roll_number_list] for face in self._faces},**{"roll_number": roll_number_list}})
        self.face_counts_per_roll_df.reset_index( inplace=True)
        self.face_counts_per_roll_df.set_index('roll_number', inplace=True)
        for face_value in self._faces:
            for j in self.face_counts_per_roll_df.index.values.tolist():
                if int(roll_face_value_count_summary[(roll_face_value_count_summary['roll_number']==j) & (roll_face_value_count_summary['face_value'] == str(face_value))]["count"].shape[0]) == 0:
                    self.face_counts_per_roll_df.at[j, str(face_value)] = 0
                else:
                    self.face_counts_per_roll_df.at[j, str(face_value)] = roll_face_value_count_summary[(roll_face_value_count_summary.index.isin([j])) & (roll_face_value_count_summary["face_value"] == str(face_value))]["count"]
                    #self.face_counts_per_roll_df.drop("index", inplace=True)
        self.face_counts_per_roll_df.reset_index(inplace=True)
        self.face_counts_per_roll_df.drop("index", inplace=True, axis=1)
        self.face_counts_per_roll_df.set_index("roll_number", inplace=True, )
