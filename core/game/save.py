import json
import os

class SaveManager:
    def __init__(self, save_file='savegame.json'):
        self.save_file = save_file

    def save_game(self, game):
        save_data = {
            "level": game.level_manager.current_world.name,
            "player_position": [game.player.rect.x, game.player.rect.y],
            "health": game.player.health,
            "inventory": game.player.inventory.get_save_data()  # You can define this in your inventory class
        }

        with open(self.save_file, 'w') as file:
            json.dump(save_data, file, indent=4)
        print("Game saved.")

    def load_game(self, game):
        if not os.path.exists(self.save_file):
            print("No save file found.")
            return

        with open(self.save_file, 'r') as file:
            save_data = json.load(file)

        game.level_manager.load_world(save_data["level"])
        game.player.rect.x, game.player.rect.y = save_data["player_position"]
        game.player.health = save_data["health"]
        game.player.inventory.load_save_data(save_data["inventory"])
        print("Game loaded.")
