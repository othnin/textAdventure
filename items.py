from __builtin__ import NotImplementedError


#############################################################################
class Weapon:
    def __str__(self):
        return self.name
    
    def __init__(self):
        raise NotImplementedError("Do not create raw weapons objects")
    


class Rock(Weapon):
    def __init__(self):
        self.name = "Rock"
        self.description = "A fist sized rock suitable for bludgeoning."
        self.damage = 5
        self.value = 1
        self.takeable = True
    
    
class Dagger(Weapon):
    def __init__(self):
        self.name = "Dagger"
        self.description = "A small dagger with some rust. Somewhat more dangerous that a rock."
        self.damage = 10
        self.value = 20
        self.takeable = True

    
class RustySword(Weapon):
    def __init__(self):
        self.name = "Rusty Sword"
        self.description = "This sword is showing its age, but still has some fight left in it."
        self.damage = 20
        self.value = 100
        self.takeable = True
######################################################################################################
class Consumable(object):
    def __init__(self):
        raise NotImplementedError("Do not create raw consumables objects.")
    
    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)
    
class CrustyBread(Consumable):
    def __init__(self):
        self.name = "Crusty Bread"
        self.healing_value = 10
        self.value = 12
        self.takeable = True
        
class HealingPotion(Consumable):
    def __init__(self):
        self.name = "Healing Potion"
        self.healing_value = 50
        self.value = 60
        self.takeable = True
############################################################################        
class Booty(object):
    def __str__(self):
        return self.name
    
    def __init__(self):
        raise NotImplementedError("Do not create raw booty objects")
        
    
class BatTeeth(Booty):
    def __init__(self):
        self.name = "bat teeth"
        self.description = "Some teeth pulled out of a bat"
        self.value = 2
        self.takeable = True
#######################################################################################################################
class Armor(object):
    def __str__(self):
        return self.name
    
    def __init__(self):
        raise NotImplementedError("Do not create raw armor objects")          
    
    
class LeatherArmor(Armor):
    def __init__(self):
        self.name = "leather armor"
        self.description = "Some decent leather armor. Strong enough for to take a dagger but that's about it"
        self.ac = 3
        self.takeable = True
 
###########################################################################################################     
class Statue(object):
    def __init__(self):
        self.name = "A large statue"
        self.takeable = False
