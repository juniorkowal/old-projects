"""Script containing Dungeon city class"""

from data.city import City
from data.habitats_cities import *
from data.city_buildings import city_mage_guild, city_city_hall, city_fort, city_marketplace, city_rescource_silo, \
    city_tavern, city_blacksmith, Artifact_Merchants_D, Portal_of_Summoning, Mana_Vortex, Battle_Scholar_Academy, \
    Mushroom_Rings
from data.hero import Hero
from data.building import *

class Dungeon(City):
    def __init__(self,
                 name: str = "Dungeon",
                 mage_guild: MageGuild = city_mage_guild,
                 city_hall: CityHall = city_city_hall,
                 fort: Fort = city_fort,
                 marketplace: Marketplace = city_marketplace,
                 tavern: Tavern = city_tavern,
                 resource_silo: ResourceSilo = city_rescource_silo,
                 blacksmith: Building = city_blacksmith,
                 t1: Habitat = Warren,
                 t2: Habitat = Harpy_Loft,
                 t3: Habitat = Pillar_of_Eyes,
                 t4: Habitat = Chapel_of_Stilled_Voices,
                 t5: Habitat = Labyrinth,
                 t6: Habitat = Manticore_Lair,
                 t7: Habitat = Dragon_Cave,
                 merch: Building = Artifact_Merchants_D,
                 portal: Building = Portal_of_Summoning,
                 mana: Building = Mana_Vortex,
                 scholar: Building = Battle_Scholar_Academy,
                 rings: Building = Mushroom_Rings,
                 graal: bool = False,
                 upper_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 lower_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 owned_by: str = 'neutral'):
        """

        A class representing Dungeon city

        :param name: Name of the given city
        :param mage_guild: Mage guild object
        :param city_hall: City hall object
        :param fort: Fort object
        :param marketplace: Marketplace object
        :param tavern: Tavern object
        :param resource_silo: Resource silo object
        :param blacksmith: Blacksmith object
        :param t1: 1st level habitat - Warren
        :param t2: 2nd level habitat - Harpy Loft
        :param t3: 3rd level habitat - Pillar of Eyes
        :param t4: 4th level habitat - Chapel of Stilled Voices
        :param t5: 5th level habitat - Labyrynth
        :param t6: 6th level habitat - Manticore Lair
        :param t7: 7th level habitat - Dragon Cave
        :param merch: Artifact merchant object
        :param portal: Portal of Summoning object
        :param mana: Mana Vortex object
        :param scholar: Battle Scholar Academy object
        :param rings: Mushroom Rings object
        :param graal: Boolean True - graal, False - no graal
        :param upper_hero: Hero object that is present in the higher row of the city slot bar
        :param lower_hero: Hero object that is present in the lower row of the city slot bar
        :param owned_by: Which player owns the building
        """
        super().__init__(mage_guild, fort, city_hall, tavern, marketplace, resource_silo, blacksmith, graal, upper_hero,
                         lower_hero, owned_by,t1,t2,t3,t4,t5,t6,t7)
        self.name = name
        self.artifact_merchant = merch
        self.portal_of_summoning = portal
        self.mana_vortex = mana
        self.battle_scholar_academy = scholar
        self.mushroom_rings = rings


    def end_week(self, player):
        """
        Checking lvl of fort building to estimate growth multiplier for given unit generator
        """
        # we are checking lvl of fort building to estimate growth multiplier (we are ignoring habitat influence (at least for now)) TODO: castle specyfic buildings
        multiplier = 1
        if self.fort.lvl == 2:
            multiplier = 1.5
        elif self.fort.lvl == 3:
            multiplier = 2

        for habitat in self.creature_dwellings:
            if habitat.lvl > 0:
                habitat.unit_ready += habitat.growth * multiplier

    def __repr__(self):
        return self.name + f' value: ({str(self.value)})'

    def __str__(self):
        return self.name + f' value: ({str(self.value)})'

    def crop_building_names(self):
        """
        Reads and fills town object with adequate buildings in a given town
        """
        img = super().take_screenshot()
        result_array = []
        w = self.textbox_width
        h = self.textbox_height
        textbox_width = 150
        textbox_height = 16
        # City hall
        print('city hall')
        result = super().crop_city_hall(img)
        result_array.append(result)

        if result[0] == 'Town Hall':
            self.city_hall.lvl = 0
        elif result[0] == 'City Hall':
            self.city_hall.lvl = 1
        elif result[1] != 'yellow':
            self.city_hall.lvl = 2
        else:
            self.city_hall.lvl = 3
            self.city_hall.built = True

        # Citadel
        print('citadel')
        result = super().crop_citadel(img)
        result_array.append(result)

        if result[0] == 'Fort':
            self.fort.lvl = 0
        elif result[0] == 'Citadel':
            self.fort.lvl = 1
        elif result[0] == 'Castle' and result[1] != 'yellow':
            self.fort.lvl = 2
        else:
            self.fort.lvl = 3
            self.fort.built = True

        # Tavern
        print('tavern')
        result = super().crop_tavern(img)
        result_array.append(result)

        if result[1] == 'yellow':
            self.tavern.built = True

        # Blacksmith
        print('Blacksmith')
        result = super().crop_blacksmith(img)
        result_array.append(result)

        if result[1] == 'yellow':
            self.blacksmith.built = True

        # Marketplace
        print('Marketplace')
        img_copy = img[453:453 + h, 594:594 + w]
        result = super().give_text_and_color(img_copy)
        result_array.append(result)

        if result[0] == 'Marketplace':
            self.marketplace.built = False
        elif result[1] != 'yellow':
            self.marketplace.built = True
        else:
            self.resource_silo.built = True
            self.marketplace.built = True

        # Mage guild
        print('Mage guild')
        img_copy = img[453:453 + h, 788:788 + w]
        result = super().give_text_and_color(img_copy)
        result_array.append(result)

        if result[0] == 'Mage Guild Level 1':
            self.mage_guild.lvl = 0
        elif result[0] == 'Mage Guild Level 2':
            self.mage_guild.lvl = 1
        elif result[0] == 'Mage Guild Level 3' and result[1] != 'yellow':
            self.mage_guild.lvl = 2
        elif result[0] == 'Mage Guild Level 3' and result[1] == 'yellow':
            self.mage_guild.lvl = 3
        elif result[0] == 'Mage Guild Level 4' and result[1] != 'yellow':
            self.mage_guild.lvl = 3
        elif result[0] == 'Mage Guild Level 4' and result[1] == 'yellow':
            self.mage_guild.lvl = 4
        elif result[0] == 'Mage Guild Level 5' and result[1] != 'yellow':
            self.mage_guild.lvl = 4
        elif result[0] == 'Mage Guild Level 5' and result[1] == 'yellow':
            self.mage_guild.lvl = 5
            self.mage_guild.built = True

        # Mana Vortex

        print("Mana Vortex")
        img_copy = img[453:453 + h, 1176:1176 + w]
        result = "Mana Vortex", super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.mana_vortex.built = True

        # Portal of Summoning
        print("Portal of Summoning")
        img_copy = img[453:453 + h, 1176:1176 + w]
        result = "Portal of Summoning", super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.portal_of_summoning.built = True

        # Artifact Merchant
        print('Artifact Merchant')
        img_copy = img[557:557 + h, 691:691 + w]
        result = 'Artifact Merchant', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.artifact_merchant.built = True

        # Battle Scholar Academy
        print('Battle Scholar Academy')
        img_copy = img[557:557 + h, 885:885 + w]
        result = 'Battle Scholar Academy', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.battle_scholar_academy.built = True

        # Mushroom Rings
        print('Mushroom Rings')
        img_copy = img[557:557 + h, 1079:1079 + w]
        result = 'Mushroom Rings', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.mushroom_rings.built = True

        # t1
        print('t1', end=" ")
        result = super().crop_t1(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'warren':
            self.creature_dwellings[1-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[1-1].lvl = 1
        else:
            self.creature_dwellings[1-1].lvl = 2
            self.creature_dwellings[1-1].built = True
        print(self.creature_dwellings[1-1].lvl)

        # t2
        print('t2', end=" ")
        result = super().crop_t2(img)
        result_array.append(result)
        name = result[0].lower()
        if name == "harpy loft":
            self.creature_dwellings[2-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[2-1].lvl = 1
        else:
            self.creature_dwellings[2-1].lvl = 2
            self.creature_dwellings[2-1].built = True
        print(self.creature_dwellings[2-1].lvl)

        # t3
        print('t3', end=" ")
        result = super().crop_t3(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'pillar of eyes':
            self.creature_dwellings[3-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[3-1].lvl = 1
        else:
            self.creature_dwellings[3-1].lvl = 2
            self.creature_dwellings[3-1].built = True
        print(self.creature_dwellings[3-1].lvl)

        # t4
        print('t4', end=" ")
        result = super().crop_t4(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'chapel of stilled voices':
            self.creature_dwellings[4-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[4-1].lvl = 1
        else:
            self.creature_dwellings[4-1].lvl = 2
            self.creature_dwellings[4-1].built = True
        print(self.creature_dwellings[4-1].lvl)

        # t5
        print('t5', end=" ")
        result = super().crop_t5(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'labyrinth':
            self.creature_dwellings[5-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[5-1].lvl = 1
        else:
            self.creature_dwellings[5-1].lvl = 2
            self.creature_dwellings[5-1].built = True
        print(self.creature_dwellings[5-1].lvl)

        # t6
        print('t6', end=" ")
        result = super().crop_t6(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'manticore lair':
            self.creature_dwellings[6-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[6-1].lvl = 1
        else:
            self.creature_dwellings[6-1].lvl = 2
            self.creature_dwellings[6-1].built = True
        print(self.creature_dwellings[6-1].lvl)

        # t7
        print('t7', end=" ")
        result = super().crop_t7(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'dragon cave':
            self.creature_dwellings[7-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[7-1].lvl = 1
        else:
            self.creature_dwellings[7-1].lvl = 2
            self.creature_dwellings[7-1].built = True
        print(self.creature_dwellings[7-1].lvl)

        return result_array
