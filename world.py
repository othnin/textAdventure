import enemies, npc, items
import random

class MapTile(object):
    
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.ground = []
        
    def intro_text(self):
        raise NotImplementedError("Do not call directly. Implement a subclass")
    
    def modify_player(self, player):
        pass
    
class StartTile(MapTile):
        
    def intro_text(self):
        return """
        You find yourself in a cave with flickering torch on the wall.
        You can make out four paths, each equally dark and forboding
        """
            
class BoringTile(MapTile):
   
    def intro_text(self):
        return """
        This is a very boring part of the cave
        """
        
class VictoryTile(MapTile):
       
    def intro_text(self):
        return """
        You see a bright light in the distanc...
        It grows as you get closer! It's the sunlight!
        
        Victory is yours!
        """
    def modify_player(self, player):
        player.victory = True
        
class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super(FindGoldTile, self).__init__(x,y)
        self.ground.append(items.CrustyBread())
        self.ground.append(items.Statue())
        self.ground.append(items.RustySword())

    
    def intro_text(self):
        if self.gold_claimed:
            room_text = "Another unremarkable part of the cave. You must forge onwards."
        else:
            room_text = "Someone has dropped some gold. You pick it up"
        if len(self.ground) > 0:
            room_text += "\nAlso of interest in the room:\n"
            for item in self.ground:
                room_text += '* ' + item.name  + "\n"
            #    room_text += item.Name  str(item)
        return room_text
    
    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print("+{} gold added".format(self.gold))
            
    
class EnemyTile(MapTile):
    
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant spider jumps down from it's web in front of you!"
            self.dead_text = "The corpse of a giant spider rots on the ground"
        if r < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "An orge is blocking your path!"
            self.dead_text = "A dead ogre reminds you of your triumpg"
        if r < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squeaking noise growing louder ...suddenly you are lost in a swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground"
        else:
            self.enemy = enemies.RockMonster()       
            self.alive_text = "You've distured a rock monster from his slumber!"
            self.dead_text = "Defeated, the monster has reverted into an ordinary rock"
        super(EnemyTile, self).__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text
            
    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, player.hp))
            
class TraderTile(MapTile):

    def __init__(self, x,y):
        self.trader = npc.Trader()
        super(TraderTile, self).__init__(x,y)

    def intro_text(self):
        return """
        A frail not-quite-juman, not-quite-creature squates in the corner clinking his gold coins together. He looks willing to trade
        """
        
    def check_if_trade(self, player): 
        while True:
            print("Would you like to (B)uy (S)ell or (Q)uit: ")
            user_input = raw_input()
            if user_input in ['q', 'Q']:
                return
            elif user_input in ['B','b']:
                print("Here's whats available to buy: ")
                self.trade(buyer= player, seller=self.trader)
            elif user_input in ['S', 's']:
                print("Here's whats available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice")
                
    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("Thats too expensive")
            return
        print(item)
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print("Trade Complete")
            
    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Gold".format(i, item.name, item.value))
        while True:
            user_input = raw_input("Choose an item or press Q to exit: ")
            if user_input in ['q', 'Q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice -1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Invalid Choice")

                    
            
        
            
world_dsl = """
|EN|EN|VT|EN|EN|
|EN|  |  |  |EN|
|EN|FG|BT|  |TT|
|TT|  |ST|FG|BT|
|FG|  |EN|  |FG|
"""         
                   
world_map = []

tile_type_dict = {"VT": VictoryTile, 
                  "EN": EnemyTile, 
                  "ST": StartTile,
                  "FG": FindGoldTile,
                  "TT": TraderTile,
                  "BT": BoringTile,
                  "  ":None}

def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False
    return True

start_tile_location = None

def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")
    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]
    
    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x,y
            row.append(tile_type(x, y) if tile_type else None)
        world_map.append(row)
  

    
def tile_at(x,y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None