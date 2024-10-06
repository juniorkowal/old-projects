"""Script containing building objects for every city"""

from data.building import *

# city
city_tavern = Tavern("Tavern", False, Cost(500, 5, 0, 0, 0, 0, 0))
city_fort = Fort(0, "Fort", False, (Cost(5000, 20, 20, 0, 0, 0, 0), Cost(2500, 0, 5, 0, 0, 0, 0), Cost(5000, 10, 10, 0, 0, 0, 0)))
city_mage_guild = MageGuild(0, "Mage_Guild", Spells("Placeholder"), (Cost(2000, 5, 5, 0, 0, 0, 0), Cost(1000, 5, 5, 4, 4, 4, 4), Cost(1000, 5, 5, 6, 6, 6, 6), Cost(1000, 5, 5, 8, 8, 8, 8),Cost(1000, 5, 5, 10, 10, 10, 10)), built=False)
city_city_hall = CityHall(0, "City_Hall", True, (Cost(2500, 0, 0, 0, 0, 0, 0), Cost(5000, 0, 0, 0, 0, 0, 0), Cost(10000, 0, 0, 0, 0, 0, 0)))
city_marketplace = Marketplace("Marketplace", False, Cost(500, 5, 0, 0, 0, 0, 0))
city_blacksmith = Building("Blacksmith", False, Cost(1000, 5, 0, 0, 0, 0, 0))
city_rescource_silo = ResourceSilo("Resource_Silo", False, Cost(5000, 0, 5, 0, 0, 0, 0), income=Cost(0, 1, 1, 0, 0, 0, 0))

# Castle unique buildings
Stables = Building("Stables", False, Cost(2000, 10, 0, 0, 0, 0, 0))
Griffin_Bastion = Building("Griffin_Bastion", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Brotherhood_of_the_Sword = Building("Brotherhood_of_the_Sword", False, Cost(500, 5, 0, 0, 0, 0, 0))
Lighthouse = Building("Lighthouse", False, Cost(2000, 0, 10, 0, 0, 0, 0))

# Rampart unique buildings
Dendroid_Saplings = Building("Dendroid_Saplings", False, Cost(2000, 0, 0, 0, 0, 0, 0))
Treasury = Building("Treasury", False, Cost(5000, 5, 10, 0, 0, 0, 0))
Fountain_of_Fortune = Building("Fountain_of_Fortune", False, Cost(1500, 0, 0, 0, 0, 10, 0))
Miners_Guild = Building("Miners_Guild", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Mystic_Pond = Building("Mystic_Pond", False, Cost(2000, 2, 2, 2, 2, 2, 2))

# Tower unique buildings
Artifact_Merchants_T = Building("Artifact_Merchants", False, Cost(10000, 0, 0, 0, 0, 0, 0))
Library = Building("Library", False, Cost(1500, 5, 5, 5, 5, 5, 5))
Lookout_Tower = Building("Lookout_Tower", False, Cost(1000, 5, 0, 0, 0, 0, 0))
Sculptor_Wings = Building("Sculptor_Wings", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Wall_of_Knowledge = Building("Wall_of_Knowledge", False, Cost(1000, 0, 5, 0, 0, 0, 0))

# Inferno unique buildings
Order_of_Fire = Building("Order_of_Fire", False, Cost(1000, 5, 0, 0, 0, 0, 0))
Castle_Gate = Building("Castle_Gate", False, Cost(10000, 5, 5, 0, 0, 0, 500))
Cages = Building("Cages", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Brimstone_Stormclouds = Building("Brimstone_Stormclouds", False, Cost(1000, 0, 0, 0, 4, 0, 0))
Birthing_Pools = Building("Birthing_Pools", False, Cost(1000, 0, 0, 0, 0, 0, 0))

# Necropolis unique buildings
Necromancy_Amplifier = Building("Necromancy_Amplifier", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Cover_of_Darkness = Building("Cover_of_Darkness", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Skeleton_Transformer = Building("Skeleton_Transformer", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Unearthed_Graves = Building("Unearthed_Graves", False, Cost(1000, 0, 0, 0, 0, 0, 0))

# Dungeon unique buildings
Artifact_Merchants_D = Building("Artifact_Merchants_D", False, Cost(10000, 0, 0, 0, 0, 0, 0))
Portal_of_Summoning = Building("Portal_of_Summoning", False, Cost(2500, 0, 5, 0, 0, 0, 0))
Mana_Vortex = Building("Mana_Vortex", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Battle_Scholar_Academy = Building("Battle_Scholar_Academy", False, Cost(1000, 5, 5, 0, 0, 0, 0))
Mushroom_Rings = Building("Mushroom_Rings", False, Cost(1000, 0, 0, 0, 0, 0, 0))

# Stronghold unique buildings
Ballista_Yard = Building("Ballista_Yard", False, Cost(1000, 5, 0, 0, 0, 0, 0))
Freelancers_Guild = Building("Freelancers_Guild", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Mess_Hall = Building("Mess_Hall", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Escape_Tunnel = Building("Escape_Tunnel", False, Cost(2000, 5, 5, 0, 0, 0, 0))
Hall_of_Valhalla = Building("Hall_of_Valhalla", False, Cost(1000, 0, 0, 0, 0, 0, 0))

# Fortress unique buildings
Blood_Obelisk = Building("Blood_Obelisk", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Cage_of_Warlords = Building("Cage_of_Warlords", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Captains_Quarters = Building("Captains_Quarters", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Glyphs_of_Fear = Building("Glyphs_of_Fear", False, Cost(1000, 0, 0, 0, 0, 0, 0))

# Conflux unique buildings
Magic_University = Building("Magic_University", False, Cost(5000, 10, 10, 0, 0, 0, 0))
Artifact_Merchants_C = Building("Artifact_Merchants_C", False, Cost(10000, 0, 0, 0, 0, 0, 0))
Garden_of_Life = Building("Garden_of_Life", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Vault_of_Ashes = Building("Vault_of_Ashes", False, Cost(5000, 0, 0, 5, 0, 0, 0))

# Cove unique buildings
Pub = Building("Pub", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Roost = Building("Roost", False, Cost(1000, 0, 0, 0, 0, 0, 0))
Grotto = Building("Grotto", False, Cost(7500, 15, 15, 0, 0, 0, 0))
Thieves_Guild = Building("Thieves_Guild", False, Cost(500, 5, 0, 0, 0, 0, 0))
