import enemies, npc, items
import random

class MapTile(object):
    
    def __init__(self, x,y, enemy=None):
        self.x = x
        self.y = y
        self.ground = []
        self.enemy_que = []
    #    self.enemy = []
        if not enemy == None:
            self.enemy_que.append(enemy)
     #       self.enemy = enemy

            
        
            
        
    def intro_text(self):
        raise NotImplementedError("Do not call directly. Implement a subclass")
    
    def modify_player(self, player):
        pass  
    
    def enemy_text(self):
        text = ""
        if len(self.enemy_que) > 0:
            for bad_guy in self.enemy_que:
                text += bad_guy.alive_text if bad_guy.is_alive() else bad_guy.dead_text
        return text
    
class StartTile(MapTile):
    def __init__(self, x, y):
        super(StartTile, self).__init__(x, y)
            
    def intro_text(self):
        text =  """
        You find yourself in a cave with flickering torch on the wall.
        You can make out four paths, each equally dark and forboding\n
        """
        return text + self.enemy_text()
            
class BoringTile(MapTile):
    def __init__(self, x, y):
        super(BoringTile, self).__init__(x, y,)
   
    def intro_text(self):
        text =  """
        This is a very boring part of the cave\n
        """
        return text + self.enemy_text()
        
        
class VictoryTile(MapTile):
    def __init__(self, x, y):
        super(VictoryTile, self).__init__(x, y)
            
    def intro_text(self):
        text = """
        You see a bright light in the distanc...
        It grows as you get closer! It's the sunlight!
        
        Victory is yours!\n
        """
        return text + self.enemy_text()
    
    def modify_player(self, player):
        player.victory = True
        
class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super(FindGoldTile, self).__init__(x,y)
        self.ground = [items.CrustyBread(), items.Statue()]
      

    
    def intro_text(self):
        if self.gold_claimed:
            room_text = "Another unremarkable part of the cave. You must forge onwards."
        else:
            room_text = "Someone has dropped some gold. You pick it up"
        if len(self.ground) > 0:
            room_text += "\nAlso of interest in the room:\n"
            for item in self.ground:
                room_text += '* ' + item.name  + "\n"
        return room_text
    
    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print("+{} gold added".format(self.gold))
            


class TigerDenTile(MapTile):
    def __init__(self,x,y):
        #self.enemy = enemies.Tiger(x,y)
        super(TigerDenTile, self).__init__(x,y, enemies.Tiger(x,y))
        
    def intro_text(self):
        text = "A 10 by 25 foot cell with bones of dead animals and a large hole on the far wall. This looks an animal den of some kind.\n"
        return text + self.enemy_text()


class EnemyTile(MapTile):
    
    def __init__(self, x, y): 
        
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider(x,y)
        elif r < 0.80:
            self.enemy = enemies.Ogre(x,y)
        elif r < 0.95:
            self.enemy = enemies.BatColony(x,y)
        else:
            self.enemy = enemies.RockMonster(x,y)       
        super(EnemyTile, self).__init__(x, y, self.enemy)

    def intro_text(self):
        text = "This is a generic monster tile.\n"
        return text + self.enemy_text()
            
            
            
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
            user_input = input()
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
            user_input = input("Choose an item or press Q to exit: ")
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
|EN|FG|EN|  |TT|
|TT|  |ST|TD|EN|
|FG|  |EN|  |FG|
"""         
                   
world_map = []

tile_type_dict = {"VT": VictoryTile, 
                  "EN": EnemyTile, 
                  "ST": StartTile,
                  "FG": FindGoldTile,
                  "TT": TraderTile,
                  "BT": BoringTile,
                  "TD": TigerDenTile,
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
