# montecarlo_final_project_DS5100_ekaw
DS5100 Final project E.L. Kaw submission


#Metadata
Eashan Kaw
Montecarlo Simulator DS5100 Final Project

Synopsis

#Install

```
!pip install monte
```

#Synopsis

```
from montecarlo import Die
```


##Creating dice

```
dice = Die(np.array([1,2,3,4,5,6], dtype=np.int64))
```

##Playing games

```
fair_game = Game([fair_die for i in range(5)])
fair_game.play(10000)
```

##Analyzing games

```
analyzer_bot = Analyzer(game)
analyzer_bot.jackpot()
analyzer_bot.jackpot_df
analyzer_bot.combo()
analyzer_bot.combo_df
```

#API description

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

    _faces """Float np array"""
    _w """Float np array"""
    _dice """pandas data frame"""


    def __init__(self, faces):
        """
        This function will initialize a "dice"
        which defines a space of outcomes and the probability of each one happening

        INPUT:
            faces: numpy array of strings or numbers which represents a possible outcome of a dice

        OUTPUT:
            Updates the dataframe attribute that represents the dice
        """

    def change_weight(self, face, weight):
        """
        This function will change the weight of a the passed dice face to be the argument passed into the function

        INPUT:
            face: identifies the face that should have its weight changed
            weight: desired weight

        OUTPUT:
            The dice attribute will be updated to reflect the desired face-weight combination

        """

    def roll(self, roll_count=1):
        """
        Chooses faces based on the probability weights. Returns the number of faces defined in roll_count in a list.

        INPUT:
            rollCount: int number of faces to return (number of rolls)

        OUTPUT:
            outcomes: list of results with the result count = rowCount parameter
        """

    def show(self):
        """
        Returns the faces, weights dice dataframe
        OUTPUT:
            dice: faces, weight pandas dataframe
        """

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

    _dice_list """List of die objects"""
    _dice_rolls """Pandas dataframe of results"""

    def __init__(self, dice_list):
        """
        Takes a single parameter, a list of already instantiated similar Die objects.

        INPUT:
            dice_list: list of dice objects that will be rolled
        """

    def play(self, roll_count):
        """
            Takes a parameter to specify how many times the dice should be rolled.
            Saves the result of the play to a private dataframe of shape N rolls by M dice.
            The private dataframe should have the roll number is (as) a named index.
            This results in a table of data with columns for roll number, the die number (its list index),
            and the face rolled in that instance.

            INPUT:
                rollCount: Int number of rolls for all di(c)e
        """

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
            wide: True returns a pandas dataframe which each row as a series of face values of all di(c)e rolled, False
            returns a dataframe where each row is a value for an individual di(c)e

        OUTPUT
            dice_rolls:
        """

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

    _game """Game object"""
    jackpot_df """Pandas DF"""
    combo_df """Pandas DF"""
    face_counts_per_roll_df """Pandas DF"""
    _faces """List of stings or numbers"""
    die_face_type  """type object"""

    def __init__(self, game):
        """
        Takes a game object as its input parameter.
        At initialization time, it also infers the data type of the di(c)e faces used.

        INPUT:
        game: a completed game object with one or more dice rolls with one or multiple di(c)e
        """
    def jackpot(self):
        """"
        A jackpot method to compute how many times the game resulted in all faces being identical.
            -RETURNS an integer for the number times to the user.
            -STORES the results as a pandas dataframe of jackpot results in a public attribute.
            -The dataframe should have the roll number as a named index.
        """

    def combo(self):
        """
        A combo method to compute the distinct combinations of faces rolled, along with their counts.
            - Combinations should be sorted and saved as a multi-columned index.
            - STORES the results as a pandas dataframe in a public attribute.
        """

    def face_counts_per_roll(self):
        """
        A face counts per roll method to compute how many times a given face is rolled in each event.
            - STORES the results as a pandas dataframe in a public attribute.
            - The dataframe has an index of the roll number and face values as columns (i.e. it is in wide format).
        """

#Manifest

FinalProjectSubmissionTemplate.ipynb
README.md
setup.py
monte/
  __init__.py
  montecarlo.py
  montecarlo_results.txt
  montecarlo_test.py
monte.egg-info/
  PKG-INFO
  SOURCES.txt
  dependency_links.txt
  top_level.txt
