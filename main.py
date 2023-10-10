import numpy as np


class Bingo:
    """
    A class to store bingo cards and tracking whether they win
    """

    def __init__(self, bingo):
        """
        Create a bingo card out of a 2D-list of shape (5, 5)
        :param bingo: a `list` of five `list`s of length 5
        """
        self.lines = np.array(bingo, dtype='object')    # specifying the element type in `np.ndarray`
                                                        # allows storing `str` of variable length
        self.columns = self.lines.T
        # The two attributes store the same object at a right angle, allowing for easy check of both
        # streaking lines or columns

    def check(self, x):
        """
        Check whether the current number is in the bingo card and whether that concludes the game for the card
        :param x: `str` number
        :return: `bool`, `True` if the card wins, `False` otherwise
        """
        if x in flatten(self.lines):    # if the number is in the card
            for i, line in enumerate(self.lines):
                if x in line:
                    self.lines[i][np.where(line == x)[0][0]] += '*'
                    # find the number and mark it by appending an asterix to the `str` value

            if self.check_win():
                return True
            # if it wins, it wins

        return False
        # otherwise it doesn't

    def check_win(self):
        """
        Check whether a column wins by separately collapsing lines and columns into sets of final characters in that
        line/column. If that set is `{'*'}`, this can only mean that every number in that line/column has been marked
        and the card as a whole has won
        :return: `bool`, `True` if the card wins, `False` otherwise
        """
        line_lasts = [{x[-1] for x in line} for line in self.lines]
        column_lasts = [{x[-1] for x in column} for column in self.columns]
        if {'*'} in line_lasts or {'*'} in column_lasts:
            return True
        return False

    def count_unmarked(self):
        """
        To determine a score of the winning card, the sum of unmarked numbers has to be calculated.
        :return: `int`
        """
        unmarked = []
        for x in flatten(self.lines):
            if x[-1] != '*':
                unmarked.append(int(x))

        return sum(unmarked)


def flatten(x):
    """
    Flatten an iterable (`list` or `np.ndarray`, to be precise)
    :param x: `list` or `np.ndarray`
    :return: one-dimensional `list`
    """
    if isinstance(x, list) or isinstance(x, np.ndarray):
        return [flatten(item) for sublist in x for item in sublist]
    return x

# read the input and strip the cosing blank line
#with open('test_input.txt') as f:
with open('real_input.txt') as f:    
    puzzle = f.read().rstrip()

# break input into lines by `'\n'` escape character and filter out empty lines
lines = [x for x in puzzle.split('\n') if x]
# the first line contains the draws separated by commas. Build a list of their string values
draws = lines[0].split(',')
# The rest of the lines are bingo cards
bingos_raw = lines[1:]

# Just to test a personal hypothesis of mine that every card will for sure
# First, every line is split using blank spaces. The resulting 2-dimensional list is flattened and
# collapsed into a set, that is then checked against the draw set. If the draw set contains the bingo set,
# every bingo card will win
bingo_set = set(flatten([x.split() for x in bingos_raw]))
draw_set = set(draws)
print(f'Every board will win: {draw_set >= bingo_set}.')

# Split the raw bingo lines into sets of 5: build a new element in the list once every five `j`s and
# add 5 lines from that `j` into a single 2D element of shape (5, 5) by additionally splitting each line
# using whitespaces
sets = [[bingos_raw[i + j].split() for i in range(5)] for j in range(len(bingos_raw)) if j % 5 == 0]
# use every element in `sets` to make a bingo card
bingos = [Bingo(x) for x in sets]

# initialize variables to store the first and the last winner
first_winner = None
last_winner = None

# check numbers draw by draw
for draw in draws:
    
    # Check the same number against every card. If the card has one this draw, it is deleted from the list
    # since there's no need to mark any mor numbers there, hence the usage of a `while` loop instead of a
    # `for` loop. If the card is not a winner, move to the next one. If this is the last card left, this is
    # the last winner (since my earlier hypothesis turned out to be true, this also breaks the outer loop).
    # If even the first winner has not been determined, remember him. Otherwise just discard the winner and check
    # the next draw
    i = 0
    while i < len(bingos):
        winner = bingos[i].check(draw)
        if not winner:
            i += 1
            continue
        if len(bingos) == 1:
            last_winner, last_draw = bingos[0], draw
            break
        if not first_winner:
            first_winner, first_draw = bingos[i], draw
        del bingos[i]

    if last_winner:
        break

# Now that the first winner and the last winner have been determined, calculate their score.
# The final check is simply my personal curiosity.
print(f"First winner's score is: {first_winner.count_unmarked() * int(first_draw)}.")
print(f"Last winner's score is: {last_winner.count_unmarked() * int(last_draw)}, "
      f"last winning draw was the last overall: {last_draw == draws[-1]}.")
