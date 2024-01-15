class DoomMetadataPacket:
    def __init__(self):
        # Initialize variables to store game state
        self.player_position = None
        self.walls = []
        self.doors = []
        self.enemies = []
        self.player_health = None
        self.player_actions = {
            'forward': False,
            'left': False,
            'right': False,
            'stop': False,
            'shoot': False,
            'open_door': False
        }
        # ... other relevant state variables ...

    def update_game_state(self):
        """
        Update the game state by interfacing with the game.
        """
        self.player_position = self.get_player_position()
        self.walls = self.get_walls()
        self.doors = self.get_doors()
        self.enemies = self.get_enemies()
        self.player_health = self.get_player_health()
        # ... update other state variables ...

    def get_player_position(self):
        # Code to get player's position
        pass

    def get_walls(self):
        # Code to get wall positions
        pass

    def get_doors(self):
        # Code to get door positions and states
        pass

    def get_enemies(self):
        # Code to get enemy positions and states
        pass

    def get_player_health(self):
        # Code to get player's health
        pass

    def update_player_actions(self, actions):
        """
        Update the player actions.

        :param actions: Dictionary of player actions.
        """
        self.player_actions = actions

    def create_metadata_packet(self):
        """
        Create a metadata packet that includes both the environment and player data.
        """
        self.update_game_state()
        metadata = {
            'player_position': self.player_position,
            'walls': self.walls,
            'doors': self.doors,
            'enemies': self.enemies,
            'player_health': self.player_health,
            'player_actions': self.player_actions
            # ... include other state information ...
        }
        return metadata

# Example usage
metadata_packet_creator = DoomMetadataPacket()
# Assume 'current_actions' is obtained from the game action encoder
metadata_packet_creator.update_player_actions(current_actions)
metadata_packet = metadata_packet_creator.create_metadata_packet()
