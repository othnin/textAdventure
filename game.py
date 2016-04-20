from player import Player
import world
from collections import OrderedDict  
    
    
def room_items_takeable(room):
    if len(room.ground) > 0:
        for item in enumerate(room.ground):
            if item[1].takeable == True:
                return True
    return False

def action_adder(actions_dict, hotkey, action, name):
    actions_dict[hotkey.lower()] = action
    actions_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey,name))
 
    
def get_available_actions(room, player):
    actions = OrderedDict()
    print("Choose an action: ")
    if player.inventory:
        action_adder(actions, 'i', player.print_inventory, "Print Inventory")
        action_adder(actions, 'd',player.drop_item, "Drop item from Inventory")
    if room_items_takeable(room):
        action_adder(actions, 'g', player.get_item, "Get item(s) in room")
    if isinstance(room, world.TraderTile):
        action_adder(actions, 't',player.trade, "Trade")
    if isinstance(room, world.EnemyTile) and not room.enemy.is_alive():
        action_adder(actions, 'l', player.loot_corpse, "Loot corpse")
    
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Attack")
    else:
        if world.tile_at(room.x, room.y-1):
            action_adder(actions, 'n', player.move_north, "Go North")
        if world.tile_at(room.x, room.y+1):
            action_adder(actions, 's', player.move_south, "Go South")
        if world.tile_at(room.x+1, room.y): 
            action_adder(actions, 'e', player.move_east, "Go East")
        if world.tile_at(room.x-1, room.y):
            action_adder(actions, 'w', player.move_west, "Go West")
        if player.hp < 100:
            action_adder(actions, 'h', player.heal, "Heal")
    return actions


def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = raw_input("Action:" )
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid action")
        
                        
def play():
    print("Escape from terror cave!")
    world.parse_world_dsl() 
    player = Player()
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print(room.intro_text())
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            choose_action(room, player)
        elif not player.is_alive():
            print("Your journey has come to an early end!")

if __name__ == "__main__":
    play()