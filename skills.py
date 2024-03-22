# Spell type should be what you want the name to appear as in damage calculations
from effects import *

class skill():
    def __init__(self, type, cost, name):
        self._type = type
        self._mpcost = cost
        self._name = name

    def useSpell(self, me, combatEntities):
        pass

class Fireball(skill):
    def __init__(self):
        super().__init__("Fireball", 4, "Fireball")

    def useSpell(self, me, combatEntities):
        if me._mp < 0:
            print("You dont have enough Madness Points to cast that spell.")
            print("As you try to cast the fireball, only sad sparks emerge.")
            return 0
        tpk = []
        for entity in combatEntities:
            if entity != me:
                modifier = me._mp - entity._mp
                if modifier < 0: modifier = 0
                damage = 7 + modifier
                entity.takeDamage(self, damage, ignoreDefence=100)
                if entity._hp <= 0:
                    tpk.append(entity)
                    print(f"{entity._name} burnt to death.")
        for s in tpk:
            combatEntities.remove(s)
        if tpk != []:
            print("Seeing everyone burning fills you with strenth.")
            if len(tpk) > 6: p = 6
            else: p = len(tpk)
            e = atkup(p)
            me.applyEffect(e)
        print("The fireball engulfs all your enemies, and friends too!")
        me._mp -= self._mpcost

# Enemy Elite Skills here

class mbuster(skill):
    def __init__(self):
        super().__init__("Mecha Buster IV", 12, "Mecha Buster IV")
        self._damage = 40
    def useSpell(self, me, combatEntities):
        me._mp -= self._mpcost
        for target in combatEntities:
            if target is not me:
                print("Metal Face uses Mecha Buster IV!")
                print(f'''
<< {me._name} >>   ->   {me._intentionTarget._name}

~ {self._name} -> {self._damage} dmg ~
''')
                target.takeDamage(self, self._damage, ignoreDefence=100)
                if target._hp <= 0:
                    target._hp = 0
                    combatEntities.remove(target)
                    print(f"{target._name} was annhilated by Metal Face.")
