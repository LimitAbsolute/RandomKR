import random
import unicodedata
from collections import deque

'''
pack: 
pyinstaller -F random_kr_en.py -n KR_Series_Random_Challenge_en -i E:\编程作业\Python\RandomKR\pic\icon.png
Configuration Instructions: 
hero: Hero array
tower: Defense Tower Array
level: Level array
'''
# constant definition
GAME_MODES = {
    '1': 'kr',
    '2': 'krf',
    '3': 'kro',
    '4': 'krv',
    '5': 'kra'
}
CHALLENGE_TYPES = ('Heroic Challenge', 'Iron Challenge')
# The number of challenges for one-time output
CHALLENGES_COUNT = 5

# Game configuration
GAME_CONFIG = {
    'kr': {
        'hero': ['Sir. Gerald Lightseeker', 'Alleria Swiftwind', 'Malik Hammerfury', 'Bolin Farslayer', 'Magnus Spellbane',
                 'Ignus', 'King Denas', 'Elora Wintersong', 'Ingvar Bearclaw', 'Hacksaw',
                 'Oni', 'Thor', "Ten'Shí"],
        'level': ['1.Southport', '2.The Farmlands', '3.Pagras', '4.Twin Rivers', '5.Silveroak Forest',
                  '6.The Citadel', '7.Coldstep Mines', '8.Icewind Pass', '9.Stormcloud Temple', '10.The Wastes',
                  '11.Forsaken Valley', '12.The Dark Tower', "13.Sarelgaz's Lair", '14.Ruins of Acaroth', '15.Rotten Forest',
                  '16.Hushwood', "17.Bandit's Lair", '18.Glacial Heights', "19.Ha'Kraj Plateau", '20.Pit of Fire',
                  '21.Pandaemonium', '22.Fungal Forest', '23.Rotwick', '24.Ancient Necropolis', '25.Nightfang Swale',
                  '26.Castle Blackburn'],
        'selection_rules': {
            'hero': {'count': 1, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    },
    'krf': {
        'hero': ['Alric', 'Mirage', 'Captain Blackthorne', 'Cronan', 'Bruxa',
                 'Nivus', 'Dierdre', 'Grawl', "Sha'tra", 'Ashbite',
                 'Karkinos', 'Kutsao', 'Dante', 'Bonehart', 'Kahz',
                 'Saitam'],
        'level': ['1.Hammerhold', '2.Sandhawk Hamlet', '3.Sape Oasis', '4.Dunes of Despair', "5.Buccaneer's Den",
                  "6.Nazeru's Gates", '7.Crimson Valley', '8.Snapvine Bridge', '9.Lost Jungle', "10.Ma'qwa Urqu",
                  '11.Temple of Saqra', '12.The Underpass', "13.Beresad's Lair", '14.The Dark Descent', '15.Emberspike Depths',
                  '16.Port Tortuga', '17.Storm Atoll', '18.The Sunken Citadel', '19.Bonesburg', '20.Desecrated Grove',
                  '21.Dusk Chateau', '22.Darklight Depths'],
        'selection_rules': {
            'hero': {'count': 1, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    },
    'kro': {
        'hero': ['Eridan', 'Arivan', 'Catha', "Reg'son", 'Prince Denas',
                 'Razz and Rags', 'Bravebark', "Vez'nan", 'Xin', 'Phoenix',
                 'Durax', 'Lynn', 'Bruce', 'Lilith', 'Wilbur',
                 'Faustus'],
        'level': ['1.Gray Ravens', '2.The High Cross', '3.Waterfalls Trail', '4.Redwood Stand', '5.Royal Gardens',
                  '6.Gryphon Point', '7.Rockhenge', '8.Grimmsburg', '9.The Crystal Lake', '10.Neverwonder',
                  '11.The Unseelie Court', '12.The Ascent', '13.Arcane Quarters', "14.Mactans' Retreat", '15.Shrine of Elynie',
                  "16.Galadrian's Wall", '17.Blood Quarry', "18.Beheader's Seat", '19.Duskwood Outpost', '20.Duredhel Outskirts',
                  '21.Dwaraman Gates', '22.Tainted Pit'],
        'selection_rules': {
            'hero': {'count': 1, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    },
    'krv': {
        'hero': ['Veruk', 'Asra', 'Oloch', 'Margosa', 'Mortemis',
                 'Tramin', 'Jigou', 'Beresad', 'Doom Tank SG-11', "Jun'Pai",
                 'Eiskalt', 'Murglun', "Jack O'Lantern", 'Dianyun', 'Grosh',
                 'Isfet', 'Lucerna'],
        'tower': ['Shadow Archers', 'Orc Warriors Den', 'Infernal Mage', 'Rocket Riders', 'Dark Knights',
                  'Melting Furnace', 'Specters Mausoleum', 'Goblirangs', 'Bone Flingers', 'Elite Harassers',
                  'Orc Shaman', 'Grim Cemetery', 'Rotten Forest', 'Wicked Sisters', 'Blazing Gem',
                  'Goblin War Zeppelin', "Deep Devil's Reef", 'Swamp Thing', 'Shaolin Temple', 'Ignis Altar',
                  'Sandworm Hollow', 'Ogre Shipwreck'],
        'level': ["1.Dwarven Gate", '2.Corridors of the Old City', '3.Kazan Mines', '4.Golden Brewery', '5.Clockwork Factory',
                  "6.Bolgur's Throne", "7.Northerners' Outpost", '8.Frozen Rapids', "9.Northerners' Village", "10.Dragons' Boneyard",
                  "11.Jokull's Nest", '12.Otil Farmlands', '13.Silveroak Outpost', '14.City of Lozagon', '15.Lightseeker Camp',
                  "16.Denas's Castle", '17.Maginicia Shores', '18.Anurian Plaza', '19.Pond of the Sage', '20.Breaking the Ice',
                  '21.Into the Mountains', '22.The Frozen Throne', '23.Ancient Gate', '24.City of Rivers', "25.Dragon's Power",
                  '26.Back To The Rotten Forest', '27.A Night In The Swamp', '28.The Ancient Ghosts', '29.Excavation Gateway', '30.Lost Passage',
                  '31.The Original World', "32.Wizard's Landing", '33.Sape Oasis', '34.The Lost Empire', '35.Hammerhold Streets',
                  '36.The Grand Arena', '37.Corsairs Brotherhood', '38.Monkey Island', '39.Sharkpool Reef', '40.Skullwreck Bay',
                  '41.Treasure Island'],
        'selection_rules': {
            'hero': {'count': 1, 'memory_size_range': (1, 10)},
            'tower': {'count': 5, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    },
    'kra': {
        'hero': ['Vesper', 'Raelyn', 'Nyru', 'Torres', 'Anya',
                 'Grimson', 'Broden', 'Therien', 'Onagro', 'Warhead',
                 'Lumenir', 'Kosmyr', 'Stregi', 'Kratoa', 'Bonehart',
                 'Sylvara', 'Spydyr', 'Sun Wukong'],
        'tower': ['Royal Archers', 'Paladin Covenant', 'Arcane Wizard', 'Tricannon', 'Ballista Outpost',
                  'Arborean Emissary', 'Demon Pit', 'Battle Brewmasters', 'Necromancer', 'Elven Stargazers',
                  'Dwarven Flamespitter', 'Dune Sentinels', 'Rocket Gunners', 'Eldritch Channeler', 'Grim Wraiths',
                  'Twilight Longbows', 'Bog Hermit', 'Cannoneer Squad', 'Surge Colossus', 'Bamboo Masters'],
        'level': ['1.Sea of Trees', '2.The Guardian Gate', '3.The Heart of the Forest', '4.Emerald Treetops', '5.Ravaged Outskirts',
                  '6.The Wildbeast Den', '7.Bleak Valley', '8.Carmine Mines', '9.Wicked Crossing', '10.Temple Courtyard',
                  '11.Canyon Plateau', '12.Blighted Farmlands', '13.Desecrated Temple', '14.Corruption Valley', '15.The Eyesore Tower',
                  "16.Hunger's Peak", '17.Misty Ruins', '18.Deepleaf Outpost', '19.Temple of the Fallen', '20.Arborean Hamlet',
                  '21.The Sunken Ruins', '22.Starving Hollow', '23.Darksteel Gates', '24.Frantic Assembly', '25.Colossal Core',
                  '26.Replication Chamber', '27.Dominion Dome', '28.Defiled Temple', '29.Breeding Chamber', '30.The Forgotten Throne',
                  '31.', '32.', '33.', '34.', '35.'],
        'selection_rules': {
            'hero': {'count': 2, 'memory_size_range': (1, 10)},
            'tower': {'count': 5, 'memory_size_range': (1, 10)},
            'level': {'count': 1, 'memory_size_range': (1, 10)}
        }
    }
}


class PoolManager:
    """Short term Memory Pool Manager"""

    def __init__(self, item, select_count, memory_size):
        if select_count > len(item):
            raise Exception(f'Selecting quantity {select_count} exceeds pool size {len(item)} ({", ".join(item)})')
        self.original_pool = item.copy()
        self.select_count = select_count
        self.memory = deque(maxlen=memory_size)

    def get_selection(self):
        """Obtain a random selection to exclude recent memories"""
        # Exclude recently used elements
        available = [i for i in self.original_pool if i not in self.memory]

        # If there are insufficient available elements, clear the memory and try again
        if len(available) < self.select_count:
            self.memory.clear()
            available = self.original_pool.copy()

        # Randomly select and update memory
        selected = random.sample(available, self.select_count)
        self.memory.extend(selected)
        return selected


def get_display_width(string):
    """Calculate string display width"""
    return sum(2 if unicodedata.east_asian_width(c) in ('F', 'W') else 1 for c in string)


class GameManager:
    """Game Explorer"""

    def __init__(self, config_name):
        self.config = GAME_CONFIG[config_name]
        self.memory_sizes = {}
        self.pools = self._init_pools()

    def _init_pools(self):
        """Initialize all selection pools"""
        pools = {}
        for key, rule in self.config['selection_rules'].items():
            memory_size = random.randint(*rule['memory_size_range'])
            pools[key] = PoolManager(
                item=self.config[key],
                select_count=rule['count'],
                memory_size=memory_size  # Dynamically generate memory pool size
            )
            self.memory_sizes[key] = memory_size  # Record the size of the memory pool
        return pools

    def generate_challenge(self):
        """Generate a complete challenge"""
        result = {key: pool.get_selection() for key, pool in self.pools.items()}
        result.update({'challenge_type': random.choice(CHALLENGE_TYPES)})
        return result

    def generate_multiple_challenges(self, count=5):
        """Generate multiple challenges"""
        return [self.generate_challenge() for _ in range(count)]


def print_memory_sizes(managers):
    """Print detailed information on the memory pool size for each game mode"""
    print('*Memory Pool Capacity Configuration')
    for mode, manager in managers.items():
        result = f'{GAME_MODES[mode].upper()} Mode (Hero Pool: {manager.memory_sizes["hero"]}, '
        if 'tower' in manager.memory_sizes:
            result += f'Defense Tower Pool: {manager.memory_sizes["tower"]}, '
        result += f'Level Pool: {manager.memory_sizes["level"]})'
        print(result)
    print()


def print_star_box(selections):
    """Format output with borders"""
    lines = [f'[RANDOM HERO] {", ".join(selections["hero"])}']
    # KR1-3 generation does not have tower selection function
    if 'tower' in selections:
        lines.append(f'[RANDOM DEFENSE TOWER] {", ".join(selections["tower"])}')
    lines.append(f'[RANDOM LEVEL] {selections["level"][0]}')
    lines.append(f'[WHY NOT GIVE IT A TRY] {selections["challenge_type"]}')

    max_width = max(get_display_width(line) for line in lines)
    border = '=' * max_width
    print(border)
    print('\n'.join(lines))
    print(f'{border}\n')


def print_multiple_challenges(challenges):
    """Generate multiple random challenges at once"""
    for i in challenges:
        print_star_box(i)


if __name__ == '__main__':
    # Initialize Game Manager
    # Only initialize the configured game modes
    managers = {
        num: GameManager(mode)
        for num, mode in GAME_MODES.items()
        if mode in GAME_CONFIG
    }
    # Print detailed information on memory pool size
    print_memory_sizes(managers)
    while True:
        choice = input(f'Enter 1-5 to generate {CHALLENGES_COUNT} corresponding KR series challenges, enter 0 to exit: ')
        if choice == '0':
            print('The program has exited!')
            break
        elif choice in managers:
            game_manager = managers[choice]
            challenges = game_manager.generate_multiple_challenges(count=CHALLENGES_COUNT)
            print_multiple_challenges(challenges)
        else:
            print('Invalid input, please re-enter!\n')
