from dao.game_dao import GameDao
class GameService:
    def __init__(self):
        self.game_dao = GameDao()
        def create_game(self, player_name: str, min_x: int, max_x: int, min_y: int, max_y: int, min_z: int, max_z: int) -> int: 
            game = Game()
            battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
            game.add_player(Player(player_name, battle_field))
            return self.game_dao.create_game(game)
        def join_game(self, game_id: int, player_name: str) -> bool:
            game=Game()
            game.add_player(Player(player_name, game_id))
            return self.game_dao.join_game(game)
        def get_game(self, game_id: int) -> Game:
            game=Game(game_id)
            return game_dao.get_game(game)

        def add_vessel(self, game_id: int, player_name: str, vessel_type: str, x: int, y: int, z: int) -> bool:
            game = Game()
            vessel = Vessel(vessel_type: str, x: int, y: int, z: int)
            game.Player(player_name, game_id, vessel)
            return game_dao.add_vessel(game)
