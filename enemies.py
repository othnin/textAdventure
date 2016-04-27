from __builtin__ import NotImplementedError
import items, world
from movement import Movement
from random import randint


class Enemy(Movement):  
    def __str__(self):
        return self.name
 
    def __init__(self, x,y):
        self.x = x
        self.y = y  
        self.possessions = [] 
               
    def is_alive(self):
        return self.hp > 0
            
    def modify_player(self, player):
        if self.is_alive():
            if player.armor == []:
                player.hp = player.hp - self.damage
                print("The () does {} damage. You have {} HP remaining.".format(self.name, self.damage, player.hp))
            else:
                if player.armor.ac <  self.damage:
                    damageToPlayer = self.damage - player.armor.ac
                else:
                    damageToPlayer = 1
                player.hp = player.hp - damageToPlayer
                print("The {} does {} damage. You have {} HP remaining.".format(self.name, damageToPlayer, player.hp))
    
    def pursue_player(self, player_direction):
        self.r = randint(1,100)
        if self.r < self.pursuit:
            print("The {} is after you! Heading {}".format(self.name, player_direction))
            room = world.tile_at(self.x, self.y)
            room.enemy_que.remove(self)        
            direction = getattr(self, player_direction)
            direction()
            room = world.tile_at(self.x, self.y)
            room.enemy_que.append(self)
            
       
class GiantSpider(Enemy):
    def __init__(self, x,y):
        self.name = "Giant Spider"
        self.hp = 10
        self.damage = 2
        self.gold = 2
        self.pursuit = 0
        super(GiantSpider, self).__init__(x,y)
        self.alive_text = "A giant spider jumps down from it's web in front of you!\n"
        self.dead_text = "The corpse of a giant spider rots on the ground\n"
        self.possessions =[items.BatTeeth(), items.CrustyBread()]
        
class Ogre(Enemy):
    def __init__(self,x, y):
        self.name = "Ogre"
        self.hp = 30
        self.damage = 10
        self.gold = 6
        self.pursuit = 0
        super(Ogre, self).__init__(x,y)
        self.alive_text = "A large, smelly, Ogre looms over you. Reading for battle\n"
        self.dead_text = "A large mound of dead Ogre lays in the room\n"
        self.possessions =[items.BatTeeth(), items.CrustyBread()]
        
class BatColony(Enemy):
    def __init__(self, x, y):
        self.name = "Colony of Bats"
        self.hp = 100
        self.damage = 4
        self.gold = 1
        self.pursuit = 0
        super(BatColony, self).__init__(x,y)
        self.alive_text = "The squeaking in the room alerts you to a clould of nasty flying bats\n"
        self.dead_text = "A dozen bat corpses litter the ground\n"
        self.possessions =[items.BatTeeth(), items.CrustyBread()]
        
class RockMonster(Enemy):
    def __init__(self, x,y):
        self.name = "Rock Monster"
        self.hp = 80
        self.damage = 15
        self.gold = 13
        self.putsuit = 10
        super(RockMonster, self).__init__(x,y)
        self.alive_text = "A rock monster approaches from behind a pile of rusted armor\n"
        self.dead_text = "The rock monster falls down and turns into an iron lump\n"
        self.possessions =[items.BatTeeth(), items.CrustyBread()]
        
class Tiger(Enemy):
    def __init__(self, x,y):
        self.name = "Giant Tiger"
        self.hp = 10
        self.damage = 18
        self.gold = 13
        self.pursuit = 100
        self.alive_text = "A snarling tiger approaches\n"
        self.dead_text = "A dead tiger corpse lies here\n"
        super(Tiger, self).__init__(x,y)
        self.possessions = [items.BatTeeth(), items.CrustyBread()]
        
        
    def modify_player(self, player):
        if self.is_alive():
            if player.armor == []:
                player.hp = player.hp - self.damage
                print("Tiger slashing does {} damage. You have {} HP remaining.".format(self.damage, player.hp))
            else:
                if player.armor.ac <  self.damage:
                    damageToPlayer = self.damage - player.armor.ac
                else:
                    damageToPlayer = 1
                player.hp = player.hp - damageToPlayer
                print("Tiger slashing does {} damage. You have {} HP remaining.".format(damageToPlayer, player.hp))
