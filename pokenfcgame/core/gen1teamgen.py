# https://github.com/pkmn/randbats/blob/main/data/gen1randombattle.json
import random
import json

def badson_to_goodson(name, badson):
    badson = badson[name]
    # # "Bulbasaur": {"level": 89, "moves": ["Body Slam", "Razor Leaf", "Sleep Powder", "Swords Dance"]},
    # # "Alakazam": {"level": 68, "moves": ["Counter", "Psychic", "Recover", "Reflect", "Seismic Toss", "Thunder Wave"], "evs": {"atk": 0}, "ivs": {"atk": 2}},
    # # print(badson)
    # goodson = json.loads("""{ "name": "", "species": "", "moves": [] }""")
    # try:
    #     for ev in badson["evs"]:
    #         goodson["evs"][ev] = badson["evs"][ev]
    # except:
    #     pass
    # try:
    #     for iv in badson["ivs"]:
    #         goodson["ivs"][iv] = badson["ivs"][iv]
    # except:
    #     pass
    # for move in badson["moves"]:
    #     goodson["moves"].append(move)
    # random.shuffle(goodson["moves"])
    # while len(goodson["moves"]) > 4:
    #     goodson["moves"].pop()
    # goodson["name"] = goodson["species"] = name
    # goodson["moves"] = sorted(goodson["moves"])
    # goodson["level"] = badson["level"]
    # Exeggutor
    # Ability: No Ability
    # - Double-Edge
    # - Explosion
    # - Hyper Beam
    # - Mega Drain
    r = ""
    r += f"{name}\n"
    moves = badson["moves"]
    random.shuffle(moves)
    while len(moves) > 4:
        # print("pop")
        moves.pop()
    for move in moves:
        r += f"- {move}\n"
    # r += "\n"
    # print(r)
    return r

def genteams():
    j = json.loads(open("gen1randombattle.json", "r").read())
    # print(j)
    available = [
        # "Slowbro",
        # "Slowbro",
        # "Diglett",
        # "Diglett",
        "Slowpoke",
        "Oddish",
        "Charmander",
        "Tentacool",
        "Squirtle",
        "Pidgey",
        "Muk",
        "Clefairy",
    ]
    potential = []
    for e in available:
        potential += [badson_to_goodson(e, j)]
    random.shuffle(potential)
    t1 = potential[:4] + [badson_to_goodson("Slowbro", j)] + [badson_to_goodson("Diglett", j)]
    t2 = potential[4:] + [badson_to_goodson("Slowbro", j)] + [badson_to_goodson("Diglett", j)]
    return ["\n".join(t1), "\n\n".join(t2)]

if __name__ == "__main__":
    genteams()
