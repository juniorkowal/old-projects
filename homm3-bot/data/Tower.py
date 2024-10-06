from data.city import City
from data.habitats_cities import *
from data.city_buildings import city_mage_guild, city_city_hall, city_fort, city_marketplace, city_rescource_silo, \
    city_tavern, city_blacksmith, Artifact_Merchants_T, Library, Lookout_Tower, Wall_of_Knowledge, Sculptor_Wings
from data.building import MageGuild, Fort, Marketplace, Tavern, ResourceSilo, Building, CityHall
from data.hero import Hero
from copy import deepcopy


class Tower(City):
    def __init__(self,
                 name: str = "Tower",
                 mage_guild: MageGuild = city_mage_guild,
                 city_hall: CityHall = city_city_hall,
                 fort: Fort = city_fort,
                 marketplace: Marketplace = city_marketplace,
                 tavern: Tavern = city_tavern,
                 resource_silo: ResourceSilo = city_rescource_silo,
                 blacksmith: Building = city_blacksmith,
                 t1: Habitat = Workshop,
                 t2: Habitat = Parapet,
                 t3: Habitat = Golem_Factory,
                 t4: Habitat = Mage_Tower,
                 t5: Habitat = Altar_of_Wishes,
                 t6: Habitat = Golden_Pavilion,
                 t7: Habitat = Cloud_Temple,
                 merch: Building = Artifact_Merchants_T,
                 lib: Building = Library,
                 lookout: Building = Lookout_Tower,
                 wall: Building = Wall_of_Knowledge,
                 wings: Building = Sculptor_Wings,
                 graal: bool = False,
                 upper_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 lower_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 owned_by: str = 'neutral'):
        """
        A class representing Tower city

        :param name: Name of the given city
        :param mage_guild: mage guild object
        :param city_hall: City hall object
        :param fort: Fort object
        :param marketplace: Marketplace object
        :param tavern: Tavern object
        :param resource_silo: Resource silo object
        :param blacksmith: Blacksmith object
        :param t1: 1st level habitat - Workshop
        :param t2: 2nd level habitat - Parapet
        :param t3: 3rd level habitat - Golem factory
        :param t4: 4th level habitat - Mage tower
        :param t5: 5th level habitat - Altar of wishes
        :param t6: 6th level habitat - Golden pavilon
        :param t7: 7th level habitat - Cloud Temple
        :param merch: Artifact merchant object
        :param lib: Library object
        :param lookout: Lookout tower object
        :param wall: Wall of knowledge object
        :param wings: Sculptor Wings object
        :param graal: Boolean True - graal, False - no graal
        :param upper_hero: Hero object that is present in the higher row of the city slot bar
        :param lower_hero: Hero object that is present in the lower row of the city slot bar
        :param owned_by: Which player owns the building
        """

        super().__init__(mage_guild, fort, city_hall, tavern, marketplace, resource_silo, blacksmith, graal, upper_hero,
                         lower_hero, owned_by)
        self.name = name
        self.creature_dwellings = [deepcopy(t1), deepcopy(t2), deepcopy(t3), deepcopy(t4), deepcopy(t5), deepcopy(t6), deepcopy(t7)]
        self.artifact_merchant = merch
        self.library = lib
        self.lookout_tower = lookout
        self.wall_of_knowledge = wall
        self.sculptor_wings = wings

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

        # Library
        print('Library')
        img_copy = img[453:453 + h, 982:982 + w]
        result = 'Library', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.library.built = True

        # Wall of Knowledge
        print('Wall of Knowledge')
        img_copy = img[453:453 + h, 1176:1176 + w]
        result = 'Wall of Knowledge', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.wall_of_knowledge.built = True

        # Artifact Merchant
        print("Artifact Merchant")
        img_copy = img[557:557 + h, 691:691 + w]
        result = "Artifact Merchant", super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.artifact_merchant.built = True

        # Lookout Tower
        print("Lookout Tower")
        img_copy = img[557:557 + h, 1079:1079 + w]
        result = "Lookout Tower", super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.lookout_tower.built = True

        # Sculptor's wings
        print("Sculptor's wings")
        img_copy = img[557:557 + h, 1079:1079 + w]
        result = "Sculptor's wings", super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.sculptor_wings.built = True

        # t1
        print('t1')
        result = super().crop_t1(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'workshop':
            self.creature_dwellings[1-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[1-1].lvl = 1
        else:
            self.creature_dwellings[1-1].lvl = 2
            self.creature_dwellings[1-1].built = True

        # t2
        print('t2')
        result = super().crop_t2(img)
        result_array.append(result)
        name = result[0].lower()
        if name == "parapet":
            self.creature_dwellings[2-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[2-1].lvl = 1
        else:
            self.creature_dwellings[2-1].lvl = 2
            self.creature_dwellings[2-1].built = True

        # t3
        print('t3')
        result = super().crop_t3(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'golem factory':
            self.creature_dwellings[3-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[3-1].lvl = 1
        else:
            self.creature_dwellings[3-1].lvl = 2
            self.creature_dwellings[3-1].built = True

        # t4
        print('t4')
        result = super().crop_t4(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'mage tower':
            self.creature_dwellings[4-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[4-1].lvl = 1
        else:
            self.creature_dwellings[4-1].lvl = 2
            self.creature_dwellings[4-1].built = True

        # t5
        print('t5')
        result = super().crop_t5(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'altar of wishes':
            self.creature_dwellings[5-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[5-1].lvl = 1
        else:
            self.creature_dwellings[5-1].lvl = 2
            self.creature_dwellings[5-1].built = True

        # t6
        print('t6')
        result = super().crop_t6(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'golden pavilion':
            self.creature_dwellings[6-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[6-1].lvl = 1
        else:
            self.creature_dwellings[6-1].lvl = 2
            self.creature_dwellings[6-1].built = True

        # t7
        print('t7')
        result = super().crop_t7(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'cloud temple':
            self.creature_dwellings[7-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[7-1].lvl = 1
        else:
            self.creature_dwellings[7-1].lvl = 2
            self.creature_dwellings[7-1].built = True

        return result_array
