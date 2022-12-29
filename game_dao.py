# creation de la base de donnees
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)






# creation de la classe PlayerEntity
class PlayerEntity(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship("GameEntity", back_populates="players")
    battle_field = relationship("BattlefieldEntity", back_populates="player", uselist=False, cascade="all, delete-orphan")
    


# creation de la classe GameEntity
class GameEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    players = relationship("PlayerEntity", back_populates="game",cascade="all, delete-orphan")

# creation de la classe Battlefieled
class BattlefieldEntity(Base) :
    __tablename__ = 'battlefiled'
    id = Column(Integer, primary_key=True)
    min_x = Column(Integer, nullable=True)
    min_y = Column(Integer, nullable=True)
    min_z = Column(Integer, nullable=True)
    max_x = Column(Integer, nullable=True)
    max_y = Column(Integer, nullable=True)
    max_z = Column(Integer, nullable=True)
    max_power = Column(Integer, nullable=True)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    vessel = relationship("VesselEntity", back_populates="Battlefield", uselist=False  ,cascade="all, delete-orphan")
    player = relationship("PlayerEntity", back_populates="battlefileds")


# creation de la classe VesselEntity
class VesselEntity(Base) : 
    __tablename__ = 'vessel'
    id = Column(Integer, primary_key=True)
    cord_x = Column(Integer, nullable=True)
    cord_y = Column(Integer, nullable=True)
    cord_z = Column(Integer, nullable=True)
    hits_to_be_destroyed = Column(Integer, nullable=True)
    type= Column(String, nullable=True)
    battle_filed_id = Column(Integer, ForeignKey("battlefiled.id"), nullable=False)
    weapon = relationship("WeaponEntity", back_populates="vessels", uselist=False, cascade="all, delete-orphan" )

# creation de la classe WeaponEntity
class WeaponEntity(Base) :
    __tablename__ = "weapon"
    id = Column(Integer, primary_key=True)
    ammunitions = Column(Integer, nullable=True)
    range = Column(Integer, nullable=True)
    type = Column(String, nullable=True)
    vessel_id = Column(Integer, ForeignKey("vessel.id"), nullable=False)





# class GameDao pour convertir un objet game en un objet gameEntity
class GameDao:
    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()
    def create_game(self, game: Game) -> int:
        game_entity = map_to_game_entity(game)
        self.db_session.add(game_entity)
        self.db_session.commit()
        return game_entity.id
    def find_game(self, game_id: int) -> Game:
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        return map_to_game(game_entity)


# class PlayerDao pour convertir un objet player en un objet playerEntity
class PlayerDao :
    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()  
    def create_player(self, player: Player) -> int:
        player_entity = map_to_player_entity(player)
        self.db_session.add(player_entity)
        self.db_session.commit()
        return player_entity.id
    def find_player(self, player_id: int) -> Player:
        stmt = select(PlayerEntity).where(PlayerEntity.id == player_id)
        player_entity = self.db_session.scalars(stmt).one()
        return map_to_player(player_entity)

# class VesselDao pour convertir un objet vessel en un objet vesselEntity
class VesselDao : 
    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session() 
    
    def create_vessel(self, vessel: Vessel) -> int:
        vessel_entity = map_to_vessel_entity(vessel)
        self.db_session.add(vessel_entity)
        self.db_session.commit()
        return vessel_entity.id
    
    def find_vessel(self, vessel_id: int) -> Vessel:
        stmt = select(VesselEntity).where(VesselEntity.id == vessel_id)
        vessel_entity = self.db_session.scalars(stmt).one()
        return map_to_vessel(vessel_entity)




# Définition de la fonction map_to_game_entity
def map_to_game_entity(game: Game) -> GameEntity:
    game_entity = GameEntity()
    if game.get_id() is not None:
        game_entity.id = game.get_id()
    for player in game.get_players():
        player_entity = PlayerEntity()
        player_entity.id = player.id
        player_entity.name = player.get_name()
        battlefield_entity = map_to_battlefield_entity(
            player.get_battlefield())
        vessel_entities = \
            map_to_vessel_entities(player.get_battlefield().id,
                                   player.get_battlefield().vessels)
        battlefield_entity.vessels = vessel_entities
        player_entity.battle_field = battlefield_entity
        game_entity.players.append(player_entity)
    return game_entity
# Définition de la fonction map_to_vessel_entities
def map_to_vessel_entities(battlefield_id: int, vessels: list[Vessel]) -> list[VesselEntity]:        
    vessel_entities: list[VesselEntity] = []
    for vessel in vessels:
        vessel_entity = map_to_vessel_entity(battlefield_id, vessel)
        vessel_entities.append(vessel_entity)

    return vessel_entities

# Definition de la fonction map_to_vessel_entity
def map_to_vessel_entity(battlefield_id: int, vessel: Vessel) -> VesselEntity:
    vessel_entity = VesselEntity()
    weapon_entity = WeaponEntity()
    weapon_entity.id = vessel.weapon.id
    weapon_entity.ammunitions = vessel.weapon.ammunitions
    weapon_entity.range = vessel.weapon.range
    weapon_entity.type = type(vessel.weapon).__name__
    vessel_entity.id = vessel.id
    vessel_entity.weapon = weapon_entity
    vessel_entity.type = type(vessel).__name__
    vessel_entity.hits_to_be_destroyed = vessel.hits_to_be_destroyed
    vessel_entity.coord_x = vessel.coordinates[0]
    vessel_entity.coord_y = vessel.coordinates[1]
    vessel_entity.coord_z = vessel.coordinates[2]
    vessel_entity.battle_field_id = battlefield_id
    return vessel_entity
# Définition de la fonction map_to_player_entity
def map_to_player_entity(player: Player) -> PlayerEntity:
    player_entity = PlayerEntity()
    player_entity.id = player.id
    player_entity.name = player.name
    player_entity.battle_field = map_to_battlefield_entity(
        player.get_battlefield())
    return player_entity

# Définition de la fonction map_to_battlefield_entity
def map_to_battlefield_entity(battlefield: Battlefield) -> BattlefieldEntity:
    battlefield_entity = BattlefieldEntity()
    battlefield_entity.id = battlefield.id
    battlefield_entity.max_x = battlefield.max_x
    battlefield_entity.max_y = battlefield.max_y
    battlefield_entity.max_z = battlefield.max_z
    battlefield_entity.min_x = battlefield.min_x
    battlefield_entity.min_y = battlefield.min_y
    battlefield_entity.min_z = battlefield.min_z
    battlefield_entity.max_power = battlefield.max_power
    return battlefield_entity

