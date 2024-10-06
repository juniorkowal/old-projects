"""Script containing Castle city class"""

from data.building import MageGuild, Fort, Marketplace, Tavern, ResourceSilo, Building, CityHall
from data.city import City
from data.habitats_cities import *
from data.city_buildings import city_mage_guild, city_city_hall, city_fort, city_marketplace, city_rescource_silo, \
    city_tavern, city_blacksmith, Stables, Griffin_Bastion, Brotherhood_of_the_Sword
from data.hero import Hero


class Castle(City):
    def __init__(self,
                 name: str = "Castle",
                 mage_guild: MageGuild = city_mage_guild,
                 city_hall: CityHall = city_city_hall,
                 fort: Fort = city_fort,
                 marketplace: Marketplace = city_marketplace,
                 tavern: Tavern = city_tavern,
                 resource_silo: ResourceSilo = city_rescource_silo,
                 blacksmith: Building = city_blacksmith,
                 t1: Habitat = Guardhouse,
                 t2: Habitat = Archers_Tower,
                 t3: Habitat = Griffin_Tower,
                 t4: Habitat = Barracks,
                 t5: Habitat = Monastery,
                 t6: Habitat = Training_Grounds,
                 t7: Habitat = Portal_of_Glory,
                 stable: Building = Stables,
                 bastion: Building = Griffin_Bastion,
                 bos: Building = Brotherhood_of_the_Sword,
                 graal: bool = False,
                 upper_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 lower_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 owned_by: str = 'neutral'):
        """
        A class representing Castle object

        :param name: Name of the given city
        :param mage_guild: mage guild object
        :param city_hall: City hall object
        :param fort: Fort object
        :param marketplace: Marketplace object
        :param tavern: Tavern object
        :param resource_silo: Resource silo object
        :param blacksmith: Blacksmith object
        :param t1: 1st level habitat - Magic Lantern
        :param t2: 2nd level habitat - Altar of Air
        :param t3: 3rd level habitat - Altar of Water
        :param t4: 4th level habitat - Altar of Fire
        :param t5: 5th level habitat - Alter of Earth
        :param t6: 6th level habitat - Altar of Thought
        :param t7: 7th level habitat - Pyre
        :param stable: Stables object
        :param bastion: Griffin bastion object
        :param bos: Brotherhood of the sword object
        :param graal: Boolean True - graal, False - no graal
        :param upper_hero: Hero object that is present in the higher row of the city slot bar
        :param lower_hero: Hero object that is present in the lower row of the city slot bar
        :param owned_by: Which player owns the building
        """

        super().__init__(mage_guild, fort, city_hall, tavern, marketplace, resource_silo, blacksmith, graal, upper_hero,
                         lower_hero, owned_by, t1, t2, t3, t4, t5, t6, t7)
        self.name = name
        self.stables = stable
        self.griffin_bastion = bastion
        self.brotherhood_of_the_sword = bos

    def end_week(self,player):
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
            if habitat.lvl>0:
                habitat.unit_ready += habitat.growth*multiplier

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
        name = super().read_text(img[349:349 + self.textbox_height, 982:982 + self.textbox_width])
        result = (name, result[1])
        result_array.append(result)

        if name == 'Tavern':
            self.tavern.built = False
        elif name == 'Brotherhood of the Sword' and result[1] != 'yellow':
            self.tavern.built = True
        else:
            self.brotherhood_of_the_sword.built = True
            self.tavern.built = True

        # Blacksmith
        print('Blacksmith')
        result = super().crop_blacksmith(img)
        result_array.append(result)

        if result[1] == 'yellow':
            self.blacksmith.built = True


        # Marketplace
        print('Marketplace')
        img_copy = img[453:453+h, 691:691+w]
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
        img_copy = img[453:453+h, 885:885+w]
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

        # Shipyard 'Not implemented'
        print('Shipyard', 'Not implemented')
        # img_copy = img[453:453+h, 1079:1079+w]
        # result = super().give_text_and_color(img_copy)
        # result_array.append(result)

        # Stables
        print('Stables')
        img_copy = img[557:557+h, 788:788+w]
        result = 'Stables', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.stables.built = True

        # Griffin bastion
        print('Griffin bastion')
        img_copy = img[557:557+h, 982:982+w]
        result = 'Griffin bastion', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.griffin_bastion.built = True

        # t1

        result = super().crop_t1(img)
        result_array.append(result)

        if result[0] == 'Guardhouse':
            self.creature_dwellings[1-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[1-1].lvl = 1
        else:
            self.creature_dwellings[1-1].lvl = 2
            self.creature_dwellings[1-1].built = True
        print(f't1 {self.creature_dwellings[1-1].lvl}')
        # t2

        result = super().crop_t2(img)
        result_array.append(result)

        if result[0] == "Archer's Tower":
            self.creature_dwellings[2-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[2-1].lvl = 1
        else:
            self.creature_dwellings[2-1].lvl = 2
            self.creature_dwellings[2-1].built = True
        print(f't2 {self.creature_dwellings[2 - 1].lvl}')
        # t3

        result = super().crop_t3(img)
        result_array.append(result)

        if result[0] == 'Griffin Tower':
            self.creature_dwellings[3-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[3-1].lvl = 1
        else:
            self.creature_dwellings[3-1].lvl = 2
            self.creature_dwellings[3-1].built = True
        print(f't3 {self.creature_dwellings[3 - 1].lvl}')
        # t4

        result = super().crop_t4(img)
        result_array.append(result)

        if result[0] == 'Barracks':
            self.creature_dwellings[4-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[4-1].lvl = 1
        else:
            self.creature_dwellings[4-1].lvl = 2
            self.creature_dwellings[4-1].built = True
        print(f't4 {self.creature_dwellings[4 - 1].lvl}')
        # t5

        result = super().crop_t5(img)
        result_array.append(result)

        if result[0] == 'Monastery':
            self.creature_dwellings[5-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[5-1].lvl = 1
        else:
            self.creature_dwellings[5-1].lvl = 2
            self.creature_dwellings[5-1].built = True
        print(f't5 {self.creature_dwellings[5 - 1].lvl}')
        # t6

        result = super().crop_t6(img)
        result_array.append(result)

        if result[0] == 'Training Grounds':
            self.creature_dwellings[6-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[6-1].lvl = 1
        else:
            self.creature_dwellings[6-1].lvl = 2
            self.creature_dwellings[6-1].built = True
        print(f't6 {self.creature_dwellings[6 - 1].lvl}')
        # t7

        result = super().crop_t7(img)
        result_array.append(result)

        if result[0] == 'Portal of Glory':
            self.creature_dwellings[7-1].lvl = 0
        elif result[1] != 'yellow':
            self.creature_dwellings[7-1].lvl = 1
        else:
            self.creature_dwellings[7-1].lvl = 2
            self.creature_dwellings[7-1].built = True
        print(f't7 {self.creature_dwellings[7 - 1].lvl}')
        return result_array









