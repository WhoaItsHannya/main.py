from random import *


def c(prompt="Press Enter to continue. [OK]"):
    input(prompt)


def speech(speechtext, speaker):
    print(" ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    print(f"<< {speaker} >> :")
    nlcount = 0
    for n in range(len(speechtext)):
        nlcount += 1
        if nlcount > 60:
            nlcount = 0
            print("")
        print(speechtext[n], end="")
    print("")
    print(" ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    c()


def displayHP_DMG(entity, damage):
    print(f"====== {entity._name} =======")
    health = (entity._hp / entity._nhp) * 50
    ndamage = (damage * 50) / entity._nhp
    print("[", end="")
    for n in range(50):
        if n < health - ndamage:
            print("■", end="")
        elif n < health:
            print("￭", end="")
        else:
            print("□", end="")
    a = entity._hp - damage
    if a < 0: a = 0
    print(f" {a} of {entity._nhp} remains!]")


class Entity():
    # an Entity class will represent any playable entity.
    # wether it is controlled by player or not, it needs the following:
    # TakeCombatTurn function to take a turn in combat
    # HandleInteraction if interacted with
    def __init__(self):
        # this is where the core stats will go
        # core stats for all entities:
        # int hp + nhp - norm/health points
        # int ap + nap - norm/attack points
        # int dp + ndp - norm/defence points
        # int sp + nsp - norm/speed points
        # int mp + nmp - norm/madness points
        # int cc - crit chance - represented as a percentage (0/100 = 0% crit, 100/100 = 100% crit)
        # float cd - crit damage - 1.5 is the base crit damage mutliplier.
        self._hp = 1  # hit points
        self._nhp = 1  # normal hit points

        self._ap = 1  # attack points
        self._nap = 1  # normal attack points

        self._dp = 1  # defense points
        self._ndp = 1  # normal defense points

        self._sp = 1  # speed points
        self._nsp = 1  # normal speed points

        self._mp = 1  # madness points
        self._nmp = 1  # normal madness points

        self._cc = 5  # crit chance
        self._ncc = 5  # normal crit chance

        self._cd = 1.5  # crit damage
        self._ncd = 1.5  # normal crit damage

        self._questItems = []  # List of held quest items
        self._usableItems = []  # List of held combat items e.g. potions
        self._combatItems = []  # List of usable items e.g. Sword to boost ATK
        self._otherItems = []  # Useless trinkets to collect

        self._name = ""  # Entity name

        self._level = 1  # Entity level
        self._exp = 0  # Entity EXP. For players this indicates progress to levels, for enemies this shows how much
        # exp gained from defeating.
        self._nlevelexp = 10

        self._type = "UNASSIGNED_TYPE"  # type to signify if entity represents a Player, NPC, or Enemy

        self._skills = []

        self._effects = []

    def takeTurn(self, combatEntities):
        return False

    def startTurn(self, effects, combatEntities):
        for effect in effects:
            if effect._evaluateOrder == "TURN_START":
                e = effect.evaluate(self, combatEntities)
                if effect._needsConfirm:
                    c()
                if not e:
                    effects.remove(effect)

    def endTurn(self, effects, combatEntities):
        for effect in effects:
            if effect._evaluateOrder == "TURN_FINISH":
                e = effect.evaluate(self, combatEntities)
                if effect._needsConfirm:
                    c()
                if not e:
                    effects.remove(effect)

    def applyEffect(self, effect, duration=None):
        if duration is not None:
            effect._duration = duration
        self._effects.append(effect)
        print(f"{self._name} recieves effect {effect._effectName} [{effect._effectSymbol}]")

    def giveItem(self, item):
        if item._itemType == "quest":
            self._questItems.append(item)
        if item._itemType == "usable":
            self._usableItems.append(item)
        if item._itemType == "combat":
            self._combatItems.append(item)
        else:
            self._otherItems.append(item)

    def learnSpell(self, spell):
        self._skills.append(spell)

    def restoreStats(self):
        self._hp = self._nhp
        self._ap = self._nap
        self._dp = self._ndp
        self._sp = self._nsp
        self._mp = self._nmp
        self._cc = self._ncc
        self._cd = self._ncd

    def takeDamage(self, enemy, damage, ignoreDefence=0):
        if type(enemy) not in [Player, Friendly, Enemy, Boss]:
            damage = damage - (self._dp - (self._dp * (ignoreDefence / 100)))
            if damage < 1: damage = 1
            print(f"{enemy._type} deals {damage} damage to {self._name}!")
        else:
            # ignoreDefence is a % value of how much our attack penetrates the enemy defence.
            print(f"{enemy._name} attacks {self._name}!")
            # First we calculate damage
            damage = damage - (self._dp - (self._dp * (ignoreDefence / 100)))
            if damage < 1:
                damage = 1
            # Now for crit chance
            if randint(0, 100) < enemy._cc:
                damage *= enemy._cd
                print(f"{enemy._name} landed a critical hit on {self._name}! Damage x{enemy._cd}")
            print(f"{enemy._name} deals {damage} damage to {self._name}!")
        displayHP_DMG(self, damage)
        self._hp -= damage
        if self._hp <= 0:
            return False
        else:
            return True


class Friendly(Entity):
    # Friendly signifies a controllable NPC that joins the player,s party.
    def __init__(self):
        super().__init__()
        self._type = "friendly"


class Player(Entity):
    def __init__(self):
        super().__init__()
        self._dpcooldown = 0
        self._type = "player"
        print("Choose a player name.")
        done = False
        while not done:
            self._name = input(" ~ ")
            if input(f"Confirm your name to be {self._name}? [ y / n ]\n ~ ") == "y":
                done = True
            else:
                print("Choose a player name.")
        print('''
Note that the Maximum value stated here is not the game maximum,
but instead the maximum it can be based on your Player. The actual
stats can be edited in a battle but will return to the default
value post battle. As an example, a Critical Chance of 5% of 5% means
that your crit rate is as normal. However if a monster debuffed you
to lower your crit rate you may see 0% of 5%. But you can upgrade your
crit rate past this \'maximum\' value, it is just to show you during
combat how your player stands.
        ''')

        if input("Start game normally, or start in Expert Mode? [ n / e ]\n ~ ") != 'e':
            self.levelUp(10)

    def levelUp(self, pts):
        print('Congratulations, you levelled up! You may now apply stat changes.')
        ptsRemaining = pts
        while ptsRemaining > 0:
            print(f'''
You have {ptsRemaining} points remaining to spend.
{self.printStats()}
Select a stat to upgrade by inputting the Attribute ID.
        ''')
            statChoice = input(' ~ ')
            done = False
            ptstoAdd = 0
            while not done:
                print(f"How many of your {ptsRemaining} points would you like to add to this stat?")
                print(f"Press Return to choose 1, 0 to cancel, or enter a number to select an amount.")
                ptstoAdd = input(" ~ ")
                if ptstoAdd != "":
                    try:
                        ptstoAdd = int(ptstoAdd)
                        if ptstoAdd > ptsRemaining:
                            print("You dont have enough points to do that.")
                        else:
                            done = True
                        if ptstoAdd < 0:
                            print("Cannot add less than 1 point.")
                            done = False
                    except Exception as e:
                        print("That isnt a valid number, try again.")
                else:
                    ptstoAdd = 1
                    done = True
            ptsRemaining -= ptstoAdd
            match statChoice:
                case 'HP':
                    self._hp += ptstoAdd
                    self._nhp += ptstoAdd
                case 'AP':
                    self._ap += ptstoAdd
                    self._nap += ptstoAdd
                case 'DP':
                    self._dp += ptstoAdd
                    self._ndp += ptstoAdd
                case 'SP':
                    self._sp += ptstoAdd
                    self._nsp += ptstoAdd
                case 'MP':
                    self._mp += ptstoAdd
                    self._nmp += ptstoAdd
                case 'CC':
                    if self._cc >= 100:
                        print("You cannot increase your Critical Chance higher than 100%.")
                        ptsRemaining += ptstoAdd
                    else:
                        if self._cc + ptstoAdd * 5 > 100:
                            print("You cannot increase your Critical Chance higher than 100%.")
                            ptsRemaining += ptstoAdd
                        else:
                            self._cc += ptstoAdd * 5
                            self._ncc += ptstoAdd * 5
                case 'CD':
                    self._cd += ptstoAdd * 0.25
                    self._ncd += ptstoAdd * 0.25
                case _:
                    ptsRemaining += ptstoAdd
                    print("That ID was not recognised as an attribute. Try again.")
        print("Done levelling up. Your new stats are:")
        print(self.printStats())

    def printStats(self):
        if len(self._effects) == 0:
            z = "No Effects"
        else:
            z = ""
            for w in range(len(self._effects)):
                z = z + f"[{self._effects[w]._effectSymbol}~{self._effects[w]._duration}t] "
        a = (f'''
Player {self._name}: Level {self._level} [{self._exp} of {self._nlevelexp} to next level]
~ Attribute Name ~ ID ~ Current Value -- Maximum Value ~
Hitpoints          HP   {self._hp:<11}   of {self._nhp}
Attack power       AP   {self._ap:<11}   of {self._nap}
Defense power      DP   {self._dp:<11}   of {self._ndp}
Speed              SP   {self._sp:<11}   of {self._nsp}
Madness            MP   {self._mp:<11}   of {self._nmp}
Critical Chance    CC   {str(self._cc) + '%':<11}   of {self._ncc}%
Critical Damage    CD   {str(self._cd) + 'x':<11}   of {self._ncd}x

Special Effects: {z}
        ''')
        return a

    def printItems(self, itemTypes):
        pass

    def takeTurn(self, combatEntities):
        self.startTurn(self._effects, combatEntities)
        combatFinished = False
        if self._mp < self._nmp:
            self._mp += 1
        self._dpcooldown -= 1
        if self._dpcooldown < 3:
            self._dp = self._ndp
        if self._dpcooldown < 0:
            self._dpcooldown = 0
        print(f"{self._name}, it,s your turn!")
        print(self.printStats())
        print(f"Current opponents:")
        print('~ Opponent name ~ Opponent HP ~ Opponent ID ~ Opponent Level ~ Opponent Special Effects')
        id = 0
        for n in combatEntities:
            if n._type == "enemy" or n._type == "boss":
                if len(n._effects) == 0:
                    z = "No Effects"
                else:
                    z = ""
                    for w in range(len(n._effects)):
                        z = z + f"[{n._effects[w]._effectSymbol}~{n._effects[w]._duration}t] "

                print(f'{n._name:<17} {n._hp:<10}    {id:<10}    {n._level:<10}       {z}')
            id += 1
        print(f"What action would you like to take?")
        print('''
~ Action name ~ ID ~ Description ~                    
 Attack         AT   Attack one enemy.                   
 Use Item       UI   Use an item in your inventory            
 Defend         DF   Prepare yourself to defend against an enemies next attack.
 Use Special    SP   Use a Special Attack on the enemy. Requires Madness Points (MP)
 View help      H?   Open the Help dialogue.
                            ''')
        done = False
        while not done:
            choice = input(" ~ ")
            done = True
            match choice:
                case "AT":
                    # attack
                    print("Choose an opponent to attack.")
                    print('~ Opponent name ~ Opponent HP ~ Opponent ID ~ Opponent Level')
                    id = 0
                    opponents = []
                    for n in combatEntities:
                        if n._type == "enemy" or n._type == "boss":
                            print(f'{n._name:<10}        {n._hp:<10}    {id:<10}    {n._level:<10}')
                            opponents.append(id)
                        id += 1
                    opponent = -1
                    while opponent not in opponents:
                        print("Enter your target,s ID.")
                        try:
                            opponent = int(input(" ~ "))
                            if opponent not in opponents:
                                raise ValueError
                        except Exception as e:
                            print("That is not a valid target.")
                    # now we have an opponent selected, it is time to penetrate them
                    them = combatEntities[opponent]
                    damage = self._ap
                    them.takeDamage(self, damage)
                    if them._hp <= 0:
                        combatEntities.remove(them)
                        print(f'''

~ Enemy ,,{them._name},, defeated! ~ 

        ''')
                        for item in them._combatItems:
                            self._combatItems.append(item)
                            them._combatItems.remove(item)
                            print(f"GET ITEM! {item._name}")
                        for item in them._questItems:
                            self._questItems.append(item)
                            them._questItems.remove(item)
                            print(f"GET ITEM! {item._name}")
                        for item in them._usableItems:
                            self._usableItems.append(item)
                            them._usableItems.append(item)
                            print(f"GET ITEM! {item._name}")
                        for item in them._otherItems:
                            self._otherItems.append(item)
                            them._otherItems.append(item)
                            print(f"GET ITEM! {item._name}")
                        combatFinished = True
                        for m in combatEntities:
                            if m._type == "enemy":
                                combatFinished = False
                        self._exp += them._level
                    c()
                case "UI":
                    if self._combatItems == []:
                        print("You have no items to use.")
                        done = False
                    print("Select the Item ID of the item you wish to use.")
                    itemID = 0
                    validIDs = []
                    print("Item ID   ~ Item name")
                    for item in self._combatItems:
                        validIDs.append(itemID)
                        print(f"{itemID:<10}: {item._name}")
                        itemID += 1
                    choice = -1
                    while int(choice) not in validIDs:
                        choice = input(" ~ ")
                        try:
                            choice = int(choice)
                        except Exception as e:
                            print("That is not a valid item ID.")
                        if choice not in validIDs: print("That item ID is not one in the list.")
                    self._combatItems[choice].useItem(self)
                    c()
                    self._combatItems.remove(self._combatItems[choice])
                case "DF":
                    if self._dpcooldown < 1:
                        print("You prepare to receive an enemy attack. You gain a bonus to")
                        print("your defence.")
                        self._dp += 3
                        self._dpcooldown = 6
                        c()
                    else:
                        print("Defense option is on cooldown.")
                        done = False
                case "SP":
                    print("Choose a special skill to use by entering it,s ID.")
                    print('Skill name ~ MP Cost ~ Skill ID')
                    spellID = 0
                    validSpells = []
                    for spell in self._skills:
                        validSpells.append(spellID)
                        print(f'{spell._name:<10}   {spell._mpcost:<10}{spellID}')
                        spellID += 1
                    choice = -1
                    while choice not in validSpells:
                        try:
                            choice = int(input(" ~ "))
                            if choice not in validSpells: raise ValueError
                        except Exception as e:
                            print("That is not a valid ID.")
                    self._skills[choice].useSpell(self, combatEntities)

                case "H?":
                    print("Now viewing Help.")
                    print("Your turn will continue as usual.")
                    print(f"""
Please select an option from the Help menu to proceed with viewing help.                    
Option ID code ~ Option description
LL               View help about levelling up          
SP               View help about Special Attacks
SE               View help about Special Effects
Enter any other input to exit this menu.
                    """)
                    choice = input(" ~ ")
                    match choice:
                        case "LL":
                            print("""
When you level up, you will gain some Stat Points to spend on yourself.
Choose what to spend them on wisely.
HP will boost your health, letting you take more hits.
AP will boost your attack, letting you deal more damage.
DP will boost your defence, meaning you take less damage.
SP will increase your speed, making you more likely to act first.
MP will boost your Madness. Madness is a measure of how hyped up you are
    during a combat. This increases by 1 every turn until you reach your
    maximum, defined by the MP stat. You can spend MP to use Special Skills.
    Levelling up Madness is crucial as it will let you use more powerful
    skills in the future.
CC will boost your % likelyhood of landing a Critical Hit.
CD will boost the multiplier that increases damage on a Critical Hit.
                            """)
                        case "SP":
                            print("""
A Special Attack is a move you learn during your journey. Special Attacks
have a variety of desirable attributes that you will want to use them for.
In order to use a Special Attack, you have to have the Madness to have the
will to use it. 
Some cool features of Special Attacks that mean you should focus on getting
them include:
- Some special attacks ignore enemy Defense capabilities
- Some special attacks inflict Special Effects to you or your enemy.
- Some special attacks are very strong and can help take out multiple enemies.
You will have to have a Madness Power of at LEAST the Special Attacks requirement
in order to use it!
                            """)
                        case "SE":
                            print("""
Special Effects are effects that have certain positive or negative changes on
how turns are evaluated. They will all have a Duration, and effects can vary
from boosting your Defense to granting you immortality.
Below is a list of all Special Effects, ID tags, and descriptions.

Effect name ~ Effect Eval Symbol ~ Effect description at Level I
Bleed         Bl                   Deals a fixed 5 damage at the end of the turn.           
                            
Higher level effects will provide scaling to the Duration and in some cases Damage of 
effects that are applied. For example, Bleed I inflicts 5 damage per turn, but 
Bleed VI inflicts 30 damage per turn. An effect can only scale up to level VI.
                            """)
                        case _:
                            print("Quitting Help menu.")
                    c()
                    print("Choose an action to take.")
                    done=False

                case _:
                    "Selection not recognised. Try again."
                    done = False
        self.endTurn(self._effects, combatEntities)
        return combatFinished


class Enemy(Entity):
    def __init__(self, stats, items=None, quotes=None):
        super().__init__()
        if items is None:
            items = []
        self._type = "enemy"
        self._hp = stats[0]
        self._nhp = stats[0]
        self._ap = stats[1]
        self._nap = stats[1]
        self._dp = stats[2]
        self._ndp = stats[2]
        self._sp = stats[3]
        self._nsp = stats[3]
        self._mp = stats[4]
        self._nmp = stats[4]
        self._cc = stats[5]
        self._ncc = stats[5]
        self._cd = stats[6]
        self._ncd = stats[6]
        self._name = stats[7]
        self._level = stats[8]
        for item in items:
            if item._itemType == "quest":
                self._questItems.append(item)
            elif item._itemType == "combat":
                self._combatItems.append(item)
            elif item._itemType == "usable":
                self._usableItems.append(item)
            else:
                self._otherItems.append(item)
        if quotes is not None:
            self._quotes = quotes
        else:
            self._quotes = []

    def takeTurn(self, combatEntities):
        self.startTurn(self._effects, combatEntities)
        print(f"{self._name}, it,s your turn!")
        if self._quotes != []:
            speech(choice(self._quotes), self._name)
        # enemy needs to decide best course of action on its turn.
        # If its DEF is significantly lower than the player, use its Defense option
        # enemy defence option is different and grants a permanent buff for the rest of
        # the battle to aid in balancing in underlevelled enemy fights
        # the enemy shoudl always attack a random choice from the player or allies
        targets = []
        for possible in combatEntities:
            if possible._type == "player" or possible._type == "friendly":
                targets.append(possible)
        target = choice(targets)
        print(f"The enemy {self._name} attacks {target._name}!")
        if self._ndp < (target._ndp - 3):
            self._ndp += 3
        # now that we have selected an enemy to target, attack them
        damage = self._ap
        target.takeDamage(self, damage)
        if target._hp <= 0:
            combatEntities.remove(target)
            print(f'''


~ The enemy ,,{self._name},, finished off ,,{target._name},,!! ~


                                ''')
            if target._type == "player":
                return True
        c()
        self.endTurn(self._effects, combatEntities)
        return False


class Boss(Enemy):
    # a boss monster,s elite skills are handled by the engine as spells.
    def __init__(self, stats, items=None, quotes=None):
        super().__init__(stats, items)
        self._type = "boss"
        self._intention = None  # Intention indicates the next Elite Skill that the boss wants to use
        self._intentionTarget = None
        self._quotes = quotes

    def takeTurn(self, combatEntities):
        self.startTurn(self._effects, combatEntities)
        self._l = []
        print(f"{self._name}, it,s your turn!")
        for entity in combatEntities:
            if entity._type in ['enemy','boss']:
                combatEntities.remove(entity)
                self._l.append(entity)
        if self._quotes is not None:
            speech(choice(self._quotes),self._name)
        self._mp += 4
        if self._intention is None:
            self._intention = choice(self._skills)
            self._intentionTarget = choice(combatEntities)
            print("You get a bad omen...")
            print(f'''
~ Warning! ~
            
<< {self._name} >>   ==>   {self._intentionTarget._name}

~ {self._intention._name} | {self._intention._damage} dmg ~

~ Warning! ~
''')
            input("Press Enter to continue. [OK]")
        if self._intention._mpcost <= self._mp:
            self._intention.useSpell(self, combatEntities)  # resolve intention
        else:
            damage = self._ap
            self._intentionTarget.takeDamage(self, damage)
            if self._intentionTarget._hp <= 0:
                combatEntities.remove(self._intentionTarget)
                print(f'''


~ The enemy ,,{self._name},, finished off ,,{self._intentionTarget._name},,!! ~


                                    ''')
                if self._intentionTarget._type == "player":
                    return True
            c()

        combatEntities.append(self)
        for entity in self._l:
            combatEntities.append(entity)
        self.endTurn(self._effects, combatEntities)
        return False


