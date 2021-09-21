from __future__ import division
import items, world
from movement import Movement
import random

'''
User player class
'''
class Player(Movement):
    def __init__(self):
        self.inventory = [items.Rock(), items.VorpalSword(), items.CrustyBread()]
        self.armor = items.LeatherArmor()
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.hp = 100
        self.gold = 5
        self.victory = False
        
    def print_inventory(self):
        print("Inventory: ")
        for item in self.inventory:
            print('* ' + str(item))
        print("Gold: {}".format(self.gold))
     
    def status(self):
        print("HP: {}".format(self.hp))
        print("Best Weapon: {}".format(self.most_powerful_weapon()))
        print("Armor: {}, AC: {}".format(self.armor.name, self.armor.ac))
        
    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)
            
    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            except AttributeError:
                pass
        return best_weapon
    
    def is_alive(self):
        return self.hp > 0
    
    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        for bad_guy in room.enemy_que:
            if bad_guy.is_alive():
                print("You used {} againt {}!".format(best_weapon, bad_guy.name))
                bad_guy.hp -= best_weapon.damage
                if not bad_guy.is_alive():
                    print("You kill {}!".format(bad_guy.name))
                else:
                    print("{} HP is {}. ".format(bad_guy.name, bad_guy.hp))
                break
    
    def flee(self):
        flee_choices = []
        room = world.tile_at(self.x, self.y)
        if world.tile_at(room.x, room.y-1):
            flee_choices.append("move_north")
        if world.tile_at(room.x, room.y+1):
            flee_choices.append("move_south")
        if world.tile_at(room.x+1, room.y): 
            flee_choices.append("move_east")
        if world.tile_at(room.x-1, room.y):
            flee_choices.append("move_west")
        percent_chance = 1/len(flee_choices)
        r = random.random()
        for x in range (len(flee_choices)):
            if r < percent_chance:
                flee_direction =  flee_choices[x]
                break
            else:
                percent_chance += percent_chance 
        fleeNow = getattr(self, flee_direction)
        print("You fled the monster heading {}!".format(flee_direction[5:]))
        for bad_guy in room.enemy_que:
            bad_guy.pursue_player(flee_direction)
        fleeNow()
       

    def heal(self):
        consumables = [item for item in self.inventory if isinstance(item, items.Consumable)]
        if not consumables:
            print("You don't have any items to heal you")
            return
        
        for i, item in enumerate(consumables, 1):
            print("Choose an item to heal you: ")
            print("{}. {}".format(i, item))
            
        valid = False
        while not valid:
            choice = input("")
            try:
                to_eat = consumables[int(choice) - 1]
                #self.hp = max(100, self.hp + to_eat.healing_value) This wil always return at least 100
                if self.hp + to_eat.healing_value > 100:
                    self.hp = 100
                else:
                    self.hp = self.hp + to_eat.healing_value                   
                self.inventory.remove(to_eat)
                print("Current HP: {}".format(self.hp))
                valid = True
            except(ValueError, IndexError):
                print("Invalid choice. Try again")
                
    def get_item(self):
        room = world.tile_at(self.x, self.y)        
        getable_items = [item for item in room.ground if item.takeable == True]
        for i, item in enumerate(getable_items, 1):
            print("{} - {}".format(i, item))        
        choice = raw_input("Select item to pick up: ")
        try:
            self.inventory.append(getable_items[int(choice)-1])
            print("You picked up: {}".format(getable_items[int(choice)-1]))
            room.ground.remove(getable_items[int(choice)-1])
        except(ValueError, IndexError):
            print("Invalid choice")
                
            
    def drop_item(self):
        room = world.tile_at(self.x, self.y)
        for i, item in enumerate(self.inventory, 1):
            print("{} - {}".format(i, item))            
        choice = raw_input("Select item to drop: ")
        try:
            room.ground.append(self.inventory[int(choice)-1])
            print("You dropped: {}".format(self.inventory[int(choice)-1]))
            self.inventory.remove(self.inventory[int(choice)-1])
        except(ValueError, IndexError):
            print("Invalid choice")
            
    def loot_corpse(self):
        room = world.tile_at(self.x, self.y)
        print("You search the dead {}".format(room.enemy.name))
        for bad_guy in room.enemy_que:
            if bad_guy.gold > 0:
                print("You find {} gold on the dead {}".format(bad_guy.gold, bad_guy.name))
                self.gold += bad_guy.gold
                bad_guy.gold = 0            
                
        for bad_guy in room.enemy_que:
            if bad_guy.possessions == []:
                print("...and find nothing on the {}".format(bad_guy.name))
            else:
                print("After more searching you find on the {}:".format(bad_guy.name))
                
                for i, item in enumerate(bad_guy.possessions, 1):
                    print("{} - {}".format(i, item))
                try:
                    choice = raw_input("Take it (a)ll or select the number to take: ")
                    if choice in ['a','A']:
                        self.inventory.extend(bad_guy.possessions)
                        print("You picked up: ")
                        print(", ".join([str(x)for x in bad_guy.possessions]))
                        bad_guy.possessions = []
                    else:
                        self.inventory.append(bad_guy.possessions[int(choice)-1])
                        print("You picked up {}.".format(bad_guy.possessions[int(choice)-1]))
                        bad_guy.possessions.remove(bad_guy.possessions[int(choice)-1])
                except(ValueError, IndexError):
                    print("Invalid choice")
        
