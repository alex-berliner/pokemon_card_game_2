from poke_env import AccountConfiguration, ShowdownServerConfiguration
from poke_env.teambuilder import Teambuilder
from poke_env.player import Player, RandomPlayer
import pprint
import asyncio
import json
import sys
sys.path.append('../build/proto')
sys.path.append('../util')
import pokemon_interface_pb2
import socket
import sys
import time
from hardware_listener import *
from gen1teamgen import *

from poke_env.player.battle_order import (
    BattleOrder,
    DefaultBattleOrder,
    DoubleBattleOrder,
)

class MaxDamagePlayer(Player):
    def __init__(self, battle_format, name, queue, evl, team=None, account_configuration=None, server_configuration=None,):
        super().__init__(battle_format=battle_format, team=team, account_configuration=account_configuration, server_configuration=server_configuration)
        self.name = name
        self.queue = queue
        self.evl = evl

    # self._data = GenData.from_gen(gen) # # Species related attributes # self._ability: Optional[str] = None # self._active: bool # self._base_stats: Dict[str, int] # self._current_hp: Optional[int] = 0 # self._effects: Dict[Effect, int] = {} # self._first_turn: bool = False # self._gender: Optional[PokemonGender] = None # self._heightm: int # self._item: Optional[str] = self._data.UNKNOWN_ITEM # self._last_details: str = "" # self._last_request: Optional[Dict[str, Any]] = {} # self._level: int = 100 # self._max_hp: Optional[int] = 0 # self._moves: Dict[str, Move] = {} # self._must_recharge: bool = False # self._possible_abilities: List[str] # self._preparing_move: Optional[Move] = None # self._preparing_target = None # self._protect_counter: int = 0 # self._revealed: bool = False # self._shiny: Optional[bool] = False # self._species: str = "" # self._status_counter: int = 0 # self._status: Optional[Status] = None # self._terastallized_type: Optional[PokemonType] = None # self._terastallized: bool = False # self._type_1: PokemonType # self._type_2: Optional[PokemonType] = None # self._weightkg: int
    # TODO: utility NFCs stored in hand that let you poll for stats of pokemon
    def pokemon_status(self, pokemon, available_moves):
        o = ""
        # /home/pi/code/pokemon/poke-env/src/poke_env/environment/pokemon.py

        o += ("Active" if pokemon._active else "Inactive").ljust(10)

        status_cond = ""
        if pokemon._status:
            status_cond = f"({pokemon._status.name.capitalize()})"
        o += f"{pokemon._species.capitalize()} {status_cond} ".ljust(18)

        # hp
        hp  = f"{pokemon._current_hp}".ljust(3) + " / "
        hp += f"{pokemon._max_hp}".ljust(6)
        o += hp
        # TODO: hack: move exists if first four of _moves exists in avail
        if pokemon._current_hp > 0:
            if pokemon._active and available_moves is not None:
                move_names = "".join([str(x).split(" ")[-1].capitalize().ljust(13) for x in available_moves])
                o += f"{move_names} "
            else:
                move_name_arr = [(f"{pokemon._moves[x]._id},").ljust(13) for x in pokemon._moves]
                move_names = "".join(move_name_arr).ljust(13)
                o += f"{move_names} "
            for e in pokemon._effects:
                o += f"{e.name}, ".ljust(13)
        return o.strip().rstrip(",")

    def get_pokemon_active(self, battle):
        return [battle.team[x] for x in battle.team if battle.team[x]._active][0]

    def get_pokemon_inactive(self, battle):
        return sorted([battle.team[x] for x in battle.team if not battle.team[x]._active], key=lambda x: x._species)

    def display_turn_start(self, battle, available_moves):
        print(f"Player {self.name}'s turn")
        print("Opponent's Pokemon:")
        print(self.pokemon_status(battle.opponent_active_pokemon, None))
        print()
        print(f"Your Pokemon:{' '*27}Red{' '*10}Yellow{' '*7}Blue{' '*9}Grey")
        print(self.pokemon_status(self.get_pokemon_active(battle), available_moves))
        # print("Inactive:")
        for e in self.get_pokemon_inactive(battle):
            print(self.pokemon_status(e, available_moves))
        for i in range(self.name):
            print("="*30)

    def ui_update(self, split_messages):
        print("\n"*20)
        for i in range(len(split_messages)):
            sm = split_messages[i]
            for i in range(len(sm)):
                handled = False
                try:
                    m = json.loads(sm[i])
                    """
                    {'forceSwitch': [True],
                    'side': {'name': 'MaxDamagePlayer 1',
                    'id': 'p1',
                    'pokemon': [{'ident': 'p1: Diglett',
                    'details': 'Diglett',
                    ...
                     """
                    if "forceSwitch" in m:
                        plid = m["side"]["id"]
                        pokemon = m["side"]["pokemon"][0]["details"]
                        print(f"{plid}'s {pokemon} fainted!")
                        handled = True
                    # else:
                    #     print(m)

                except:
                    pass
            if len(sm) >= 2 and "move" in sm[1]:
                # ['', 'move', 'p1a: Slowpoke', 'Thunder Wave', 'p2a: Slowbro']
                player = sm[2][:2]
                pokemon = sm[2].split(":")[-1].strip()
                move = sm[3]
                opponent = sm[4][:2]
                target = sm[4].split(":")[-1].strip()
                print(f"{player}'s {pokemon} used {move} on {opponent}'s {target}")
            if len(sm) >= 2 and "switch" in sm[1]:
                # print(sm)
                # # ['', 'move', 'p1a: Slowpoke', 'Thunder Wave', 'p2a: Slowbro']
                player = sm[2][:2]
                pokemon = sm[2].split(":")[-1].strip()
                print(f"{player} switched to {pokemon}")
            # if not handled:
            #     print(sm)
    def wait(self):
        time.sleep(2)
        print("Pass the device to your opponent!")
        t=3
        for i in range(t):
            print(t-i)
            time.sleep(1)
    def choose_move(self, battle):
        # {battle._anybody_inactive}") {battle._available_moves}") {battle._available_switches}") {battle._battle_tag}") {battle._can_dynamax}") {battle._can_mega_evolve}") {battle._can_tera}") {battle._can_z_move}") {battle._data}") {battle._dynamax_turn}") {battle._fields}") {battle._finished}") {battle._force_switch}") {battle._format}") {battle.in_team_preview}") {battle._max_team_size}") {battle._maybe_trapped}") {battle._move_on_next_request}") {battle._opponent_can_dynamax}") {battle._opponent_can_mega_evolve}") {battle._opponent_can_terrastallize}") {battle._opponent_can_z_move}") {battle._opponent_dynamax_turn}") {battle._opponent_rating}") {battle._opponent_side_conditions}") {battle._opponent_team}") {battle._opponent_username}") {battle._player_role}") {battle._player_username}") {battle._players}") {battle._rating}") {battle._reconnected}") {battle._replay_data}") {battle._rqid}") {battle.rules}") {battle._reviving}") {battle._save_replays}") {battle._side_conditions}") {battle._team_size}") {battle._team}") {battle._teampreview_opponent_team}") {battle._teampreview}") {battle._trapped}") {battle._turn}") {battle._wait}") {battle._weather}") {battle._won}") {battle.logger}")
        available_switches = [BattleOrder(available_switches) for available_switches in battle.available_switches]
        available_moves = [BattleOrder(move) for move in battle.available_moves]
        # self.evl.switch_player(self.name-1)
        self.display_turn_start(battle, available_moves)
        # r = self.choose_random_move(battle)
        # print("choose: ", str(r), "\n\n\n")
        # return r
        for _ in range(self.queue.qsize()):
            self.queue.get()
        # print(self.queue.qsize())
        # for e in available_moves:
        #     print(e)
        # failsafe for continuing game when no moves are available
        if not any(available_switches + available_moves):
            print("jumpstarting game state after disconnect. sorry!")
            return self.choose_random_move(battle)
        while True:
            for i in range(self.queue.qsize()):
                message = self.queue.get()
                if len(message.pokemon_name) > 0:
                    for e in battle.available_switches:
                        if e._species.lower() == message.pokemon_name.lower() and e._current_hp > 0: # TODO: change to faint check
                            print(f"Switching to {message.pokemon_name.capitalize()}")
                            self.wait()
                            return BattleOrder(e)
                elif self.get_pokemon_active(battle)._current_hp < 1:
                    # print("Your pokemon has fainted!")
                    time.sleep(0.5)
                    for _ in range(self.queue.qsize()):
                        self.queue.get()
                    time.sleep(0.5)
                elif self.get_pokemon_active(battle)._current_hp > 0:
                    move_id = message.attack
                    if move_id >= len(available_moves):
                        print(f"Invalid move id! {move_id}")
                        for e in available_moves:
                            print(e)
                        time.sleep(0.5)
                        for _ in range(self.queue.qsize()):
                            self.queue.get()
                        time.sleep(0.5)
                        input()
                        continue
                    move = str(available_moves[move_id]).split(" ")[-1]
                    print(f"Using {move}")
                    self.wait()
                    return available_moves[move_id]

        return self.choose_random_move(battle)

class PlayerTeamManager(Teambuilder):
    def __init__(self, teams):
        self.team = self.join_team(self.parse_showdown_team(teams.pop()))

    def yield_team(self):
        return self.team

def genouteam():
    return ["""
    Gengar
- Hypnosis
- Thunderbolt
- Night Shade
- Explosion

Chansey
- Ice Beam
- Thunderbolt
- Thunder Wave
- Soft-Boiled

Snorlax
- Body Slam
- Earthquake
- Hyper Beam
- Self-Destruct

Exeggutor
- Sleep Powder
- Stun Spore
- Psychic
- Explosion

Tauros
- Body Slam
- Earthquake
- Hyper Beam
- Blizzard

Lapras
- Blizzard
- Thunderbolt
- Body Slam
- Confuse Ray
    """
    # Starmie
    # Ability: Illuminate
    # - Blizzard
    # - Psychic
    # - Thunder Wave
    # - Recover

    # Exeggutor
    # Ability: Chlorophyll
    # - Sleep Powder
    # - Psychic
    # - Double-Edge
    # - Explosion

    # Alakazam
    # Ability: Synchronize
    # - Psychic
    # - Seismic Toss
    # - Thunder Wave
    # - Recover

    # Chansey
    # Ability: Natural Cure
    # - Ice Beam
    # - Thunderbolt
    # - Thunder Wave
    # - Soft-Boiled

    # Snorlax
    # Ability: Immunity
    # - Body Slam
    # - Reflect
    # - Hyper Beam
    # - Rest

    # Tauros
    # Ability: Intimidate
    # - Body Slam
    # - Hyper Beam
    # - Blizzard
    # - Earthquake
]
async def itsanonlinegame(event_listener):
    player = MaxDamagePlayer(
        battle_format = "gen1ou",
        account_configuration=AccountConfiguration("allocsb1", ""),
        server_configuration=ShowdownServerConfiguration,
        team = PlayerTeamManager(genouteam()),
        name = 1,
        queue = event_listener.queue,
        evl = event_listener,
        # queue = event_listener.queue,
        # evl = event_listener,
    )
    # player = RandomPlayer(
    #     account_configuration=AccountConfiguration("allocsb1", ""),
    #     server_configuration=ShowdownServerConfiguration,

    # )

    # Sending challenges to 'your_username'
    await player.send_challenges("allocsb2", n_challenges=1)

async def offlinegame(event_listener):
    start = time.time()
    teams = genteams()
    print(teams[0])
    max_damage_player_1 = MaxDamagePlayer(
        name = 1,
        battle_format = "gen1ou",
        team = PlayerTeamManager(teams),
        queue = event_listener.queue,
        evl = event_listener
    )
    # max_damage_player_2 = MaxDamagePlayer(
    #     name = 2,
    #     battle_format = "gen1ou",
    #     team = PlayerTeamManager(teams),
    #     queue = event_listener.queue,
    #     evl = event_listener
    # )
    max_damage_player_2 = MaxDamagePlayer(
        name = 2,
        battle_format = "gen1ou",
        team = PlayerTeamManager(teams),
        queue = event_listener.queue,
        evl = event_listener
    )

    await max_damage_player_1.battle_against(max_damage_player_2, n_battles=1)

    print(
        "Max damage player 1 won %d / 1 battles [this took %f seconds]"
        % (
            max_damage_player_1.n_won_battles, time.time() - start
        )
    )

async def main():
    event_listener = HardwareListener()
    # await offlinegame(event_listener)
    await itsanonlinegame(event_listener)
    # TODO: removing this causes the interpreter to shut down without the
    # HL server shutting down. These should be shutting down at the same time.
    while True:
        time.sleep(0.1)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
