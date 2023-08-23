import sys
import random
import operator

def rollDice(numDice, sides):
    diceRollTotal = 0
    for i in range(numDice):
        diceRollTotal = diceRollTotal + random.randint(1, sides)
    return diceRollTotal

class PlayerCharacter:
    def __init__(self, playerName):
        self.name = playerName
        self.level = 1
        self.HP = 8 + rollDice(self.level, 8)
        self.ATK = 2
        self.DEF = 12
        self.SPD = rollDice(1, 20) + 2
        self.NPC = False

class EnemyGoblin:
    def __init__(self):
        self.name = "Goblin"
        self.HP = rollDice(2, 6)
        self.ATK = 2
        self.DEF = 15
        self.SPD = rollDice(1, 20)
        self.NPC = True
        self.actions = [scimitar, shortbow]

class Ability:
    def __init__(self, abilityName, dType, aHit, bDamage, diceNum, diceType, aDescription):
        self.name = abilityName
        self.damageType = dType
        self.hit = aHit
        self.baseDamage = bDamage
        self.diceRolls = diceNum
        self.diceSides = diceType
        self.description = aDescription

scimitar = Ability("Scimitar", "Slashing", 4, 2, 1, 6, "%s slashes with a scimitar.")
shortbow = Ability("Shortbow", "Piercing", 4, 2, 1, 6, "%s fires an arrow with a shortbow.")

player = PlayerCharacter("Mr. Hatfield")
goblin = EnemyGoblin()
playerAction = ""
diceRoll = 0
damageDealt = 0

combatants = [player, goblin]
combatants = sorted(combatants, key=operator.attrgetter('SPD'))

print("A goblin appears!")
if combatants[0].NPC == True:
    print("You were caught offguard!")

while 1:

    """
    for combatant in combatants:
        if combatant.NPC == True:
            print("is NPC")
        else:
            print("is not NPC")
    """ 
    print("What will you do?")
    print("1. Attack 2. Magic 3. Item 4. Examine 5. Flee")
    playerAction = str(sys.stdin.readline()).lower().strip()
    if playerAction == "1" or playerAction == "attack":
        print("%s attacks the goblin!" % player.name)
        diceRoll = rollDice(1, 20)
        if diceRoll == 20:
            damageDealt = (player.ATK + rollDice(1, 4))* 2
            print("CRITICAL HIT!")
        if diceRoll == 1:
            damageDealt = 0
            print("Critical Miss!")
        if diceRoll + player.ATK >= goblin.DEF:
            damageDealt = player.ATK + rollDice(1, 4)
        else:
            damageDealt = 0
            print("%s's attack misses!" % player.name)
        if damageDealt > 0:
            goblin.HP = goblin.HP - damageDealt
            print("The goblin takes %s points of damage!" % damageDealt)
        if goblin.HP <= 0:
            print("The goblin is defeated!")
            print("You win!")
            break
    else:
        print("That is not a valid action! Whoops!")
    print(goblin.actions[random.randint(0, 1)].description % goblin.name)
    diceRoll = rollDice(1, 20)
    if diceRoll == 20:
        player.HP = player.HP - 4
        print("CRITICAL HIT!")
        print("You take 4 points of damage!")
    if diceRoll == 1:
        print("Critical Miss!")
        player.HP = player.HP - 0
    if diceRoll + goblin.ATK >= player.DEF:
        player.HP = player.HP - 2
        print("You take 2 points of damage!")
    else:
        player.HP = player.HP - 0
        print("The goblin's attack misses.")
    if player.HP <= 0:
        print("You are defeated!")
        print("You lose!")
        break
    
