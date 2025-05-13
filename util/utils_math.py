import random

def roll(threshold):
    mfChance = random.random()
    mbRollTrue = (mfChance < threshold / 100)
    return mbRollTrue