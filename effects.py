class effect:
    def __init__(self):
        self._evaluateOrder = "NOEVALUATE"
        self._effectName = "NONAME"
        self._effectSymbol = "??"
        self._description = "NODESCRIPTION"
        self._type = "NO_TYPE"
        self._duration = 0
        self._level = 0
        self._needsConfirm = False

    def evaluate(self, target, combatEntities=None):
        pass

mapping = ["0", "I", "II", "III", "IV", "V", "VI"]

class bleed(effect):
    def __init__(self, level):
        super().__init__()
        self._evaluateOrder = "TURN_FINISH"
        self._effectName = "Bleed"
        self._description = "Inflicts fixed amount of Bleed damage at the end of a turn."
        self._type = "Bleed"
        self._duration = 2
        self._level = level
        self._effectSymbol = "Bl " + mapping[level]
        self._needsConfirm = True
    def evaluate(self, target, combatEntities=None):
        if combatEntities is None:
            print("Error: An effect evaluate which requires CombatEntites was not given the argument.")
            raise KeyboardInterrupt
        target.takeDamage(self, 5*self._level, ignoreDefence=25)
        if target._hp <= 0:
            combatEntities.remove(target)
        self._duration -= 1
        if self._duration == 0:
            return False
        else:
            return True


class atkup(effect):
    def __init__(self, level):
        super().__init__()
        self._evaluateOrder = "TURN_FINISH"
        self._effectName = "Attack Up"
        self._description = "Boosts your AP to over your maximum temporarily."
        self._type = "Attack Up"
        self._duration = 3
        self._startDuration = 3
        self._level = level
        self._effectSymbol = "AP UP " + mapping[level]

    def evaluate(self, target, combatEntities=None):
        if self._duration == self._startDuration:
            target._ap += 6*self._level
        self._duration -= 1
        if self._duration == 0:
            target._ap -= 6*self._level
            return False
        else:
            return True

