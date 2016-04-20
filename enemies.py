from __builtin__ import NotImplementedError
import items


class Enemy(object):  
    def __str__(self):
        return self.name
    
    def __init__(self):
        raise NotImplementedError("Do not create raw Enemy objects")
#        I get an error with the above line ???
#        pass
               
    def is_alive(self):
        return self.hp > 0
    
       
class GiantSpider(Enemy):
    def __init__(self):
        self.name = "Giant Spider"
        self.hp = 10
        self.damage = 2
        self.gold = 2
        self.goldTaken = False
        
class Ogre(Enemy):
    def __init__(self):
        self.name = "Ogre"
        self.hp = 30
        self.damage = 10
        self.gold = 6
        self.goldTaken = False
        
class BatColony(Enemy):
    def __init__(self):
        self.name = "Colony of Bats"
        self.hp = 100
        self.damage = 4
        self.gold = 1
        self.goldTaken = False
        self.possessions =[items.BatTeeth(), items.CrustyBread()]
        
class RockMonster(Enemy):
    def __init__(self):
        self.name = "Rock Monster"
        self.hp = 80
        self.damage = 15
        self.gold = 13
        self.goldTaken = False