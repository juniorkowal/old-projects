import math
import random

import numpy as np


# DMGf = DMGb × (1 + I1 + I2 + I3 + I4 + I5) × (1 - R1) × (1 - R2 - R3) × (1 - R4) × (1 - R5) × (1 - R6) × (1 - R7) × (1 - R8)

# BASE DAMAGE - DMGb

# Damage range for a single unit type is displayed in its stats. Base damage for a stack of creatures is calculated as such:
def baseDamage(minDamage,maxDamage,numberOfUnits):
    dmg=0
# If there are less than or equal to 10 creatures in a stack then a random integer is chosen in a damage range for each creature,
# and they are added up.
    if numberOfUnits<=10:
        for i in range(numberOfUnits):
            if minDamage == maxDamage:  dmg+= minDamage
            else:                       dmg+=np.random.randint(minDamage,maxDamage)
        return dmg
# If there are more than 10 creatures in a stack, 10 random integers are chosen in a damage range of the creature and added up.
# The result is multiplied by N/10, where N is the number of creatures in the stack, and rounded down.
    else:
        for i in range(10):
            if minDamage == maxDamage:  dmg += minDamage
            else:                       dmg += np.random.randint(minDamage, maxDamage)
        return math.floor(dmg*(numberOfUnits/10))


# ATTACK-DEFENSE DIFFERENCE (I1 AND R1)

# It is calculated as the difference between the attacker's attack value and the defender's defense value.
# These are determined by adding up the attack skill of the attacking hero and of the attacking creature type,
# and by adding up defense skill of the defending hero and defending creature type. Spells and creature abilities
# that affect attack or defense values, such as Bloodlust or disease, are also taken into account in this part of the formula,
# as are any bonuses from native terrain or hero's creature specialties.

def attackDefenseDifference(heroLevel,creatureLevel,attackHero,attackCreature,defenseHero,defenseCreature,nativeTerrain=0,
                            spellAttack=0,spellDefense=0,creatureAbilityAttack=0,creatureAbilityDefense=0,creatureSpecialty=False):
    creatureSpecialtyAttack = 0
    creatureSpecialtyDefense = 0
    if creatureSpecialty:
        creatureSpecialtyAttack=math.ceil(math.floor(heroLevel/creatureLevel)*attackCreature/20)
        creatureSpecialtyDefense=math.ceil(math.floor(heroLevel/creatureLevel)*defenseCreature/20)

    attack=attackHero+attackCreature+nativeTerrain+spellAttack+creatureAbilityAttack+creatureSpecialtyAttack
    defense=defenseHero+defenseCreature+nativeTerrain+spellDefense+creatureAbilityDefense+creatureSpecialtyDefense

    return attack-defense


# SECONDARY SKILL FACTORS - VARIABLES I2 AND I3

#I2
def archeryOffense(archeryLevel=0,offenseLevel=0,ranged=False):
    archery=[0,0.10,0.25,0.50]
    if ranged:
        return archery[archeryLevel]
    else:
        return offenseLevel*0.10

#I3
def heroSpecialization(heroLevel,archeryLevel=0,offenseLevel=0,heroName='',ranged=False):
    specialHeroes=['Orrin','Gundula','Crag Hack']
    if heroName in specialHeroes:
        if heroName == specialHeroes[0] and ranged:
            return 0.05*heroLevel*archeryOffense(archeryLevel,offenseLevel,ranged)
        elif (heroName==specialHeroes[1] or heroName==specialHeroes[2]) and ranged==False:
            return 0.05*heroLevel*archeryOffense(archeryLevel,offenseLevel,ranged)
        else:
            return 0
    else:
        return 0


# LUCK - I4 //todo: more modifiers affecting luck

def luck(luckSkillLevel=0):
    luckyStrike = None
    luckyVar=luckSkillLevel

    if luckyVar==0:
        luckyStrike=random.choices([0,1],(1-1/24,1/24),k=1)
    elif luckyVar==1:
        luckyStrike=random.choices([0,1],(1-2/24,2/24),k=1)
    elif luckyVar>=3:
        luckyStrike=random.choices([0,1],(1-3/24,3/24),k=1)

    return luckyStrike


# CREATURE ABILITIES - I5

def creatureAbilities(creatureName,attackedCreatureName,heroLevel,squaresTravelled=0):

    if creatureName=='Dread Knight':
        return random.choices([0,1],(1-1/5,1/5),k=1)
    elif creatureName=='Ballista' or creatureName=='Cannon':
        # The I5 variable is also 1.00 for a ballista or cannon (Horn of the Abyss) whose shots deal double (base) damage,
        # and 2.00 for cannon's triple damage.
        # But it doesn't specify when ballista or cannon deals double or triple damage.
        return 0
    elif creatureName=='Angel' and attackedCreatureName=='Devil' or creatureName=='Devil' and attackedCreatureName=='Angel':
        return 0.5
    elif creatureName=='Titan' and attackedCreatureName=='Black Dragon' or creatureName=='Black Dragon' and attackedCreatureName=='Titan':
        return 0.5
    elif creatureName=='Genie' and attackedCreatureName=='Efreeti' or creatureName=='Efreeti' and attackedCreatureName=='Genie':
        return 0.5
    elif creatureName=='Fire Elemental' and attackedCreatureName=='Water Elemental' or creatureName=='Water Elemental' and attackedCreatureName=='Fire Elemental':
        return 1
    elif creatureName=='Air Elemental' and attackedCreatureName=='Earth Elemental' or creatureName=='Earth Elemental' and attackedCreatureName=='Air Elemental':
        return 1
    elif creatureName=='Cavalier' or creatureName=='Champion' and attackedCreatureName!='Pikeman' or attackedCreatureName!='Halberdier':
        return 0.05*heroLevel*squaresTravelled
    else:
        return 0


# DEFENSE VARIABLES

#R2 and R3

def armorerVariables(heroName,attackingCreature,heroLevel,armorerLevel=0):
    armorer=[0,0.05,0.10,0.15]
    if heroName in ['Mephala','Neela','Tazar']:
        if attackingCreature=='Arrow_Tower':
            return -armorer[armorerLevel]+0.05*heroLevel*armorer[armorerLevel]
        else:
            return armorer[armorerLevel]+0.05*heroLevel*armorer[armorerLevel]
    else:
        if attackingCreature=='Arrow_Tower':
            return -armorer[armorerLevel]
        else:
            return armorer[armorerLevel]

#R4

def magicShields(shield=False,shieldLevel=0,airShield=False,airShieldLevel=0,ranged=False):
    shieldValues=[0.15,0.30,0.30]
    airShieldValues=[0.25,0.50,0.50]
    if ranged==False:
        if shield:
            return shieldValues[shieldLevel]
        else:
            return 0
    else:
        if airShield:
            return airShieldValues[airShieldLevel]
        else:
            return 0


#R5

def rangeMeleePenalty(distance,goldenBow=False,bowOfTheSharpshooter=False,ranged=False,creatureName=''):
    if goldenBow or bowOfTheSharpshooter or creatureName=='Sharpshooter':
        return 0
    if ranged:
        if distance>=10 or distance==0:
            if creatureName in ['Beholder','Evil_Eye','Medusa','Medusa_Queen','Magi','Arch_Magi','Zealot','Enchanter','Titan']:
                return 0
            return 0.50
    else:
        return 0


#R6

def obstaclePenalty(creatureName,goldenBow=False,bowOfTheSharpshooter=False,behindWall=False):
    if creatureName in ['Magi','Arch_Magi','Enchanter','Sharpshooter'] or goldenBow or bowOfTheSharpshooter:
        return 0
    if behindWall:
        return 0.50
    else:
        return 0

#R7

def mindSpells(blind=False):
    if blind:
        return 0.50
    else:
        return 0

#R8

def creatureSpecialties(paralysed=False,petrified=False,creatureName='',attackedCreature=''):
    if creatureName=='Psychic_Elemental' and (attackedCreature=='Giant' or attackedCreature=='Undead'):
        return 0.50
    if creatureName=='Magic_Elemental' and (attackedCreature=='Magic_Elemental' or attackedCreature=='Black_Dragon'):
        return 0.50
    if petrified:
        return 0.50
    if paralysed:
        return 0.25
    else:
        return 0



def creatureStackDmg(attackingCreature,attackingHero,attackedCreature,attackedHero,nativeTerrain=False,spellAttack=0,spellDefense=0,creatureAbilityAttack=0,
                creatureAbilityDefense=0,creatureSpecialty=False,ranged=False,archeryLevel=0,offenseLevel=0,squaresTravelled=0,attackedHeroArmorerLevel=0,attackedShield=False,
            attackedShieldLevel=0,attackedAirShield=False,attackedAirShieldLevel=0,distanceBetweenAttackingAndAttacked=5,goldenBow=False,bowOfTheSharpshooter=False,blind=False,
                behindWall=False,paralysed=False,petrified=False):

    dmgb=baseDamage(attackingCreature.type.damage[0],attackingCreature.type.damage[1],attackingCreature.quantity)
    i1=attackDefenseDifference(attackingHero.lvl,attackingCreature.type.lvl,attackingHero.attack,attackingCreature.type.attack,attackedHero.defense,attackedCreature.type.defense,
                                                    nativeTerrain,spellAttack,spellDefense,creatureAbilityAttack,creatureAbilityDefense,creatureSpecialty)
    i2=archeryOffense(archeryLevel,offenseLevel,ranged)
    i3=heroSpecialization(attackingHero.lvl,archeryLevel,offenseLevel,attackingHero.name,ranged)
    i4=luck(attackingHero.luck)
    i5=creatureAbilities(attackingCreature.type.name,attackedCreature.type.name,attackingHero.lvl,squaresTravelled)
    
    r2_and_r3=armorerVariables(attackedHero.name,attackingCreature.type.name,attackedHero.lvl,attackedHeroArmorerLevel)
    r4=magicShields(attackedShield,attackedShieldLevel,attackedAirShield,attackedAirShieldLevel,ranged)
    r5=rangeMeleePenalty(distanceBetweenAttackingAndAttacked,goldenBow,bowOfTheSharpshooter,ranged,attackingCreature.type.name)
    r6=obstaclePenalty(attackingCreature.type.name,goldenBow,bowOfTheSharpshooter,behindWall)
    r7=mindSpells(blind)
    r8=creatureSpecialties(paralysed,petrified,attackingCreature.type.name,attackedCreature.type.name)

    r1=0
    if i1>0:
        i1=0.05*i1
    elif i1<0:
        r1=abs(i1)*0.025
    
    if i1>60: i1=60
    if i1<-28:
        i1=0
        r1=-28

    damage=math.ceil(dmgb*(1+i1+i2+i3+i4+i5)*(1-r2_and_r3)*(1-r4)*(1-r5)*(1-r6)*(1-r7)*(1-r8))

    if damage<0:
        damage=0

    return damage

# To use the above function, you need to provide:
# attackingCreature - the creature stack which attacks
# attackingHero - attacking creature stack's hero
# attackedCreature - creature stack that is about to be attacked
# attackedHero - self expalnatory
# nativeTerrain - whether the attacking stack is on its native terrain (True/False)
# spellAttack - any bonuses from spells which add to attack
# spellDefense - any bonuses from spells which add to defense
# creatureAbilityAttack - any bonuses from creature abilities which add to attack
# creatureAbilityDefense - any bonuses from creature abilities which add to defense
# creatureSpecialty - whether hero specializes in a creature (True/False)
# ranged - whether the creature stack is making a ranged attack
# archeryLevel - level of the archery skill of the attacking hero
# offenseLevel - level of the offense skill of the attacking hero
# squaresTravelled - how many squares has the creature stack travelled to make an attack
# attackedHeroArmorerLevel - level of the armorer level of the attacked hero
# attackedShield - whether attacked creature is under the effects of the shield spell
# attackedShieldLevel - level of the shield spell
# attackedAirShield - whether attacked creature is under the effects of the air shield spell
# attackedAirShieldLevel - level of the air shield spell
# distanceBetweenAttackingAndAttacked - distance between battling creatures, used to apply ranged penalties
# goldenBow - whether the attacking hero has the goldenbow artifact
# bowOfTheSharpshooter - whether the attacking hero has the bowofthesharpshooter artifact
# blind - whether attacked creature is blind
# behindWall - whether attacked creature is behind an obstacle/wall
# paralysed - whether attacked creature is paralysed
# petrified - whether attacked creature is petrified

