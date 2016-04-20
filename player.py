import items
import world

class Player:
    def __init__(self):
        self.inventory = [items.Rock(), items.Dagger(), items.CrustyBread()]
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
        enemy = room.enemy
        print("You used {} againt {}!".format(best_weapon, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You kill {}!".format(enemy.name))
        else:
            print("{} HP is {}. ".format(enemy.name, enemy.hp))
        
    def move(self,dx, dy):
        self.x += dx
        self.y += dy
        
    def move_north(self):
        self.move(dx=0, dy=-1) 
        
    def move_south(self):
        self.move(dx=0, dy=1)
        
    def move_east(self):
        self.move(dx=1, dy=0)
        
    def move_west(self):
        self.move(dx=-1, dy=0)
        
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
                
            
#            itemChosen = getable_items[int(choice)-1]
#            self.inventory.append(itemChosen)
#            room.ground.remove(itemChosen) 
#            print("You picked up: {}".format(itemChosen))
#        except(ValueError, IndexError):
#            print("Invalid Choice")
            
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
        if room.enemy.goldTaken == True:
            print("You find no gold.")
        else:
            print("You find {} gold".format(room.enemy.gold))
            self.gold += room.enemy.gold
            room.enemy.goldTaken = True
        if room.enemy.possessions == []:
            print("...and nothing")
        else:
            print("After more searching you find:")
            for i, item in enumerate(room.enemy.possessions, 1):
                print("{} - {}".format(i, item))
            try:
                choice = raw_input("Take it (a)ll or select the number to take: ")
                if choice in ['a','A']:
                    self.inventory.extend(room.enemy.possessions)
                    print("You picked up: ")
                    print(", ".join([str(x)for x in room.enemy.possessions]))
                    room.enemy.possessions = []
                else:
                    self.inventory.append(room.enemy.possessions[int(choice)-1])
                    print("You picked up {}.".format(room.enemy.possessions[int(choice)-1]))
                    room.enemy.possessions.remove(room.enemy.possessions[int(choice)-1])
            except(ValueError, IndexError):
                print("Invalid choice")
        