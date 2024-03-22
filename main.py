from c import *
from engine import *
from items import *
from skills import *
from effects import *

'''
Helpful tips for designing
Enemies are initialised as:
<name> = Enemy([hp, ap, dp, sp, mp, cc, cd, <name>, level, quotes])
resolveCombat returns True or False for a win or a loss
Entity.restoreStats() will fully restore an entities stats to the default
'''

healpotion = healPotion()
critpotion = critPotion()

fireball = Fireball()

bleed1 = bleed(1)
bleed2 = bleed(2)
bleed3 = bleed(3)
bleed4 = bleed(4)
bleed5 = bleed(5)

me = Player()
me.restoreStats()

me.giveItem(healpotion)
me.giveItem(critpotion)

me.learnSpell(fireball)

m01 = Enemy([2, 3, 1, 0, 0, 25, 1.5, "M01 OBLIVIOUS", 2])
m02 = Enemy([8, 1, 2, 0, 0, 0, 1.0, "M02 CARDINAL", 2])


story("It was a quiet day. Too quiet. The small village was in total silence, with only your footsteps to be heard.")
story("You held your makeshift sword in your hands and looked around curiously, looking for anything to do.")
story("But there seemed to be nothing. When, out of nowhere, you felt the ground start to rumble.")
story("That probably isnt a good sign.. Something told you that you should get out of there.")
storydecision("What would you like to do?", "Leave the village [l] or Stay and watch [s]?", ["l","s"])
# story encounter, decision does not matter.
story("As you stand there contemplating, you realise with a shudder that something huge is standing behind you.")
story("You turn around to find an massive metallic construction, standing there laughing.")
speech("HELLO THERE LOSER! IT LOOKS LIKE YOU ARE STANDING BETWEEN ME, AND THIS VILLAGE. GET OUT OF MY WAY, OR ILL KILL YOU ON THE SPOT!","???")
speech("NOTHING TO SAY? EXACTLY WHAT I EXPECTED. NOW MOVE, BRAT, OR ILL DO IT FOR YOU.", "???")
speech("IM JUST KIDDING. I WANT TO WATCH YOU SCREAM!! NOW, PREPARE THE PIE!! oh. i mean uh, PREPARE TO DIE!", "???")

mecha_buster_x = mbuster()
metalFace = Boss([800, 5, 1, 0, 0, 20, 2, "Metal Face", 20])
metalFace.learnSpell(mecha_buster_x)

resolveCombat([me, m01, m02, metalFace])
