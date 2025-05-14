import random

def roll(aiThreshold, asName="roll"):
    mfChance = random.random()
    mbRollTrue = (mfChance > aiThreshold / 100)
    print(f"[ROLL] \"{asName}\" {mbRollTrue} : Rolled {int(mfChance * 100)} / {aiThreshold}")
    return mbRollTrue

def randElement(array: list):
    mfIndex = random.randrange(0, len(array) - 1)
    return array[mfIndex]