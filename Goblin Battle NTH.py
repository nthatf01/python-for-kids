import sys
import random
import operator
import time

def rollDice(numDice, sides, advantage="None"):
    diceRollTotal = 0
    for i in range(numDice):
        diceRollTotal = diceRollTotal + random.randint(1, sides)
    if advantage == "Advantage":
        for i in range(numDice):
            advDiceRollTotal = advDiceRollTotal + random.randint(1, sides)
        if advDiceRollTotal > diceRollTotal:
            diceRollTotal = advDiceRollTotal
    elif advantage == "Disadvanage":
        for i in range(numDice):
            disDiceRollTotal = disDiceRollTotal + random.randint(1, sides)
        if disDiceRollTotal < diceRollTotal:
            diceRollTotal = disDiceRollTotal
    return diceRollTotal

def printText(text_to_print):
    time.sleep(.20)
    for char in text_to_print:
        print(char, end="", flush=True)
        time.sleep(.025)
    print("\n")
    time.sleep(.3)

class PlayerCharacter:
    def __init__(self, playerName, playerClass):
        self.name = playerName
        self.pcClass = playerClass
        self.level = 1
        self.HP = 8 + rollDice(self.level, 8)
        self.ATK = 2
        self.DEF = 12
        self.SPD = rollDice(1, 20) + 2
        self.NPC = False
        self.actions = [vicious_mockery, healing_word]
        self.advantage = "None"

    def castSpell(self, chosenSpell):
        spell = next((action for action in self.actions if action.name.lower() == chosenSpell), None)
        printText(spell.description % self.name)
        if spell.damageType == "Healing":
            recoveredHP = rollDice(spell.diceRolls, spell.diceSides)
            self.HP = self.HP + recoveredHP
            printText("{0} regains {1} HP.".format(self.name, recoveredHP))
        else:
            damageDealt = spell.baseDamage + rollDice(spell.diceRolls, spell.diceSides)
            goblin.HP = goblin.HP - damageDealt
            printText("The goblin takes %s points of damage!" % damageDealt)
        if spell.effect == "Disadvantage":
            goblin.advantage = "Disadvantage"
            printText("{0} is affected with Disadvantage.".format(goblin.name))

class EnemyGoblin:
    def __init__(self):
        self.name = "Goblin"
        self.HP = rollDice(2, 6)
        self.ATK = 2
        self.DEF = 15
        self.SPD = rollDice(1, 20)
        self.NPC = True
        self.actions = [scimitar, shortbow]
        self.advantage = "None"

    def useRandomAbility(self):
        damageDealt = 0
        chosenAbility = self.actions[random.randint(0, len(self.actions)-1)]
        printText(chosenAbility.description % self.name)
        diceRoll = rollDice(1, 20, self.advantage)
        self.advantage = "None"
        if diceRoll == 20:
            printText("CRITICAL HIT!")
            damageDealt = (chosenAbility.baseDamage + rollDice(chosenAbility.diceRolls, chosenAbility.diceSides)) * 2
            printText("{0} takes {1} points of damage!".format(player.name, damageDealt))
        elif diceRoll == 1:
            printText("Critical Miss!")
            damageDealt = 0
        elif diceRoll + goblin.ATK >= player.DEF:
            damageDealt = chosenAbility.baseDamage + rollDice(chosenAbility.diceRolls, chosenAbility.diceSides)
            printText("{0} takes {1} points of damage!".format(player.name, damageDealt))
        else:
            damageDealt = 0
            printText("The goblin's attack misses.")
        player.HP = player.HP - damageDealt
        
class Ability:
    def __init__(self, abilityName, dType, aHit, bDamage, diceNum, diceType, aDescription, aEffect = ""):
        self.name = abilityName
        self.damageType = dType
        self.hit = aHit
        self.baseDamage = bDamage
        self.diceRolls = diceNum
        self.diceSides = diceType
        self.description = aDescription
        self.effect = aEffect

scimitar = Ability("Scimitar", "Slashing", 4, 2, 1, 6, "%s slashes with a scimitar.")
shortbow = Ability("Shortbow", "Piercing", 4, 2, 1, 6, "%s fires an arrow with a shortbow.")
vicious_mockery = Ability("Vicious Mockery", "Psychic", 0, 0, 1, 4, "%s mocks the enemy.", "Disadvantage")
healing_word = Ability("Healing Word", "Healing", 0, 0, 1, 4, "%s recovers from damage.")

player = PlayerCharacter("Mr. Hatfield", "Bard")
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
    
    for combatant in combatants:
        if combatant.NPC == True:
            goblin.useRandomAbility()
            if player.HP <= 0:
                printText("You are defeated!")
                printText("You lose!")
                break
        else:
            printText("What will you do?")
            print("1. Attack 2. Magic 3. Item 4. Examine 5. Flee")
            playerAction = str(sys.stdin.readline()).lower().strip()
            if playerAction == "1" or playerAction == "attack":
                printText("%s attacks the goblin!" % player.name)
                diceRoll = rollDice(1, 20)
                if diceRoll == 20:
                    damageDealt = (player.ATK + rollDice(1, 4))* 2
                    printText("CRITICAL HIT!")
                elif diceRoll == 1:
                    damageDealt = 0
                    printText("Critical Miss!")
                elif diceRoll + player.ATK >= goblin.DEF:
                    damageDealt = player.ATK + rollDice(1, 4)
                else:
                    damageDealt = 0
                    printText("%s's attack misses!" % player.name)
                if damageDealt > 0:
                    goblin.HP = goblin.HP - damageDealt
                    printText("The goblin takes %s points of damage!" % damageDealt)

            elif playerAction == "2" or playerAction == "magic":
                i = 0
                printText("Which spell do you cast?")
                for spell in player.actions:
                    i += 1
                    print("{0}. {1} ".format(i, player.actions[i-1].name), end="", flush=True)
                print("\n")
                playerSpell = str(sys.stdin.readline()).lower().strip()
                player.castSpell(playerSpell)
                
            elif playerAction == "4" or playerAction == "examine":
                printText("{0} the {1} has {2} HP remaining.".format(player.name, player.pcClass, player.HP))
                printText("{0} has {1} HP remaining.".format(goblin.name, goblin.HP))
            else:
                print("That is not a valid action! Whoops!")
            if goblin.HP <= 0:
                printText("The goblin is defeated!")
                print("You win!")
                break
    if player.HP <= 0 or goblin.HP <= 0:
        break
    
