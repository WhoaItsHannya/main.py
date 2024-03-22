
def c(prompt="Press Enter to continue. [OK]"):
    input(prompt)

def displayHP_DMG(entity, damage):
    print(f"====== {entity._name} =======")
    health = entity._hp
    mhealth = entity._nhp
    multiplier = 0
    m = False
    while health > 60:
        multiplier += 1
        mhealth -= 60
        health -= 60
        m = True
    print("[",end="")
    for n in range(60):
        if n < health - damage:
            print("■", end="")
        elif n < health:
            print("￭", end="")
        else:
            print("□", end="")
    if m: print(f"x{multiplier}",end="")
    print("]")


def resolveCombat(entities=None):
    print('''
    
    
~ Combat Start! ~
    
    
    ''')
    if entities is None:
        print("You win! You beat... nothing. Well done.")
        return -1
    me = None
    entities.sort(key = lambda x: x._nsp, reverse=True)
    for entity in entities:
        if entity._type == "player":
            me = entity
    combatFinished = False
    while me._hp > 0 and not combatFinished:
        for entity in entities:
            match entity._type:
                case "player":
                    combatFinished = entity.takeTurn(entities)
                case "enemy":
                    combatFinished = entity.takeTurn(entities)
                case "friendly":
                    combatFinished = entity.takeTurn(entities)
                case "boss":
                    combatFinished = entity.takeTurn(entities)
                case _:
                    pass
    print('''
    
~ Combat finish! ~
    
    ''')
    if me._exp >= me._nlevelexp:
        me._level += 1
        me._exp -= me._nlevelexp
        print(f"You levelled up from this combat! You are now level {me._level}.")
        print(f"You have {me._exp} EXP remaining.")
        pointsToEarn = me._level + 2
        me._nlevelexp = me._nlevelexp + 10
        if pointsToEarn > 15: pointsToEarn = 15
        me.levelUp(pointsToEarn)
    if me._hp <= 0:
        return False
    else:
        return True

def story(storytext):
    print(" ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    nlcount = 0
    for n in range(len(storytext)):
        nlcount += 1
        if nlcount > 60:
            nlcount = 0
            print("")
        print(storytext[n], end="")
    print("")
    print(" ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    c()


def storydecision(storytext, decisiontext, decisionoptions):
    print(" ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    nlcount = 0
    for n in range(len(storytext)):
        nlcount += 1
        if nlcount > 60:
            nlcount = 0
            print("")
        print(storytext[n], end="")
    print("")
    print(" ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    nlcount = 0
    for n in range(len(decisiontext)):
        nlcount += 1
        if nlcount > 60:
            nlcount = 0
            print("")
        print(decisiontext[n], end="")
    print("")
    decision = -1
    print("[ ",end="")
    for n in range(len(decisionoptions)-1):
        print(f"{decisionoptions[n]} / ", end="")
    print(f"{decisionoptions[len(decisionoptions)-1]} ]", end="")
    print("")
    while decision not in decisionoptions:
        decision = input(" ~ ")
    return decision