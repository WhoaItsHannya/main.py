class Item():
    def __init__(self, itemType, rarity, name):
        self._itemType = itemType
        self._rarity = rarity
        self._name = name

    def useItem(self, target):
        pass

class healPotion(Item):
    def __init__(self):
        super().__init__("combat", "common", "Potion of Healing")

    def useItem(self, target):
        target._hp += 5
        if target._hp > target._nhp:
            target._hp = target._nhp
        print("You heal 5 HP!")

class critPotion(Item):
    def __init__(self):
        super().__init__("combat", "common", "Potion of Criticals")

    def useItem(self, target):
        target._cc += 30
        if target._cc > 100:
            target._cc = 100
        target._cd += 1.5
        print("You gain 30% crit rate and 1.5x bonus crit damage!")

