# HW 8, Problems 1 and 2

# load NumPy, requires Anaconda to be installed locally and chosen as the interpreter
import numpy as numpy
# load required files from SupportLib, requires newest version of SupportLib to be loaded in content root
import scr.StatisticalClasses as Stat
import scr.FormatFunctions as Format

# Modified HW 6 code
# create Game class
class Game(object):
    def __init__(self, flip_probability):
        self.flip_probability = flip_probability #probability of heads
        self.totalwinnings = 0 # initialize total winnings
        self.winningslist = [] # empty list to place each game's winnings into for CI construction

     # create Simulate function
    def Simulate(self, number_of_flips, number_of_realizations):
        self.number_of_flips = number_of_flips
        self.number_of_realizations = number_of_realizations
        gamecost = -250 # cost of playing the game

        for j in range(0, self.number_of_realizations):
            fliplist = "" # create an empty string

            for i in range(0, self.number_of_flips): # iterate through 20 flips, treating 1's as heads and 0's as tails
                fliplist = fliplist + str((numpy.random.binomial(1, self.flip_probability))) #per https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.binomial.html, add each flip to fliplist

            winnings = gamecost+(100*(fliplist.count("001"))) # find the number of Tails, Tails, Heads, multiply by fifty, add to cost of game to find winnings
            self.winningslist.append(winnings) # append winningslist with each games winnings
            self.totalwinnings = self.totalwinnings + winnings # add all the realizations of winnings together
    # create way to access winingslist in Game object created by the simulation run
    def get_winningslist(self):
        """ :returns the winningslist of this Game's simulation run"""
        return self.winningslist

# Calculate average change in reward for a steady state (casino owner), code modified from SupportSteadyState.py
def print_comparative_outcomes_steadystate(unfair_coin, fair_coin):
    """ prints expected change in winnings when coin is unfair available
    """
    # change in winnings
    increase = Stat.DifferenceStatIndp(
        name='Change in average reward',
        x=unfair_coin.get_winningslist(),
        y_ref=fair_coin.get_winningslist()
    )
    # estimate and CI
    estimate_CI = Format.format_estimate_interval(
        estimate=increase.get_mean(),
        interval=increase.get_t_CI(alpha=0.05),
        deci=1
    )
    print("Average change in reward (dollars) and {:.{prec}%} confidence interval:".format(1 - 0.05, prec=0),
          estimate_CI)

# Calculate average change in reward for a transient state (player), code modified from SupportTransientState.py
def print_comparative_outcomes_transientstate(unfair_coin, fair_coin):
    """ prints expected change in winnings when coin is unfair available
    """
    # change in winnings
    increase = Stat.DifferenceStatIndp(
        name='Change in average reward',
        x=unfair_coin.get_winningslist(),
        y_ref=fair_coin.get_winningslist()
    )
    # estimate and prediction interval
    estimate_PI = Format.format_estimate_interval(
        estimate=increase.get_mean(),
        interval=increase.get_PI(alpha=0.05),
        deci=1
    )
    print("Expected change in mean reward (dollars) and {:.{prec}%} prediction interval:".format(1 - 0.05, prec=0),
          estimate_PI)

# PROBLEM 1

# Initialize an even 50-50 game
faircoin_casino = Game(0.5)
# Run the simulation as a casino owner (1000 games)
faircoin_casino.Simulate(20, 1000)

# Initialize an uneven 45-65 game (45% chance of heads)
unfaircoin_casino = Game(0.45)
# Run the simulation as a casino owner (1000 games)
unfaircoin_casino.Simulate(20, 1000)

# Print the expected change in reward and clarifications
print("Problem 1:")
print_comparative_outcomes_steadystate(unfaircoin_casino, faircoin_casino)
print("As this model is coded from the perspective of the player, any positive change in reward indicates a loss for the casino owner, while any negative change in reward indicates a gain for the casino owner. As the coin is waited against heads, and fewer heads is in the player's favor, the casino owner will usually have their reward decreases in this scenario.", "\n")

# PROBLEM 2

# Initialize an even 50-50 game
faircoin_player = Game(0.5)
# Run the simulation as a player (10 games)
faircoin_player.Simulate(20, 10)

# Initialize an uneven 45-65 game (45% chance of heads)
unfaircoin_player = Game(0.45)
# Run the simulation as a casino owner (1000 games)
unfaircoin_player.Simulate(20, 10)

# Print the expected change in reward and clarifications
print("Problem 2:")
print_comparative_outcomes_transientstate(unfaircoin_player, faircoin_player)
print("As previously mentioned, a decreased chance of heads is in the player's favor. Thus, the reward for the player will on average increase in this scenario. However, given that the player only plays the game 10 times, there is still a good chance of the player losing money as indicated by the calculated prediction interval.")

