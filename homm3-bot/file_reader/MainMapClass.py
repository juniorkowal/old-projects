from file_reader.MainMapClassVaraibles import MapVariables
from file_reader.FileReader import FileReader
from file_reader.MapConstants import Version, IntGlobals, Victory, Loss, HeroesConstants, TileType, Objects, QuestMission,\
    RewardType
import numpy as np
from file_reader.OtherClasses import ObjectTemplate
import json


class Map(MapVariables):

    def __init__(self):
        super().__init__()
        self.reader = FileReader('')
        self.terrain_map = None
        self.objects_map = None
        self.road_map = None
        self.object_templates = []
        self.object_list = []

    def read_map(self, filename: str):
        """
        Main function for reading map. Use only this one.
        :param filename: Map filename
        :return: Map of objects, terrain, road
        """
        self.reader = FileReader(filename)
        print('Reading header')
        self.read_header()
        print('Reading player info')
        self.read_player_info()
        print('Reading victory condition')
        self.victory_condition()
        print('Reading loss condition')
        self.loss_condition()
        print('Reading teams')
        self.teams()
        print('Reading free heroes')
        self.free_heroes()
        print('Reading HOTA map extra')
        self.reader.skip(31)
        self.HOTA_map_extra()
        print('Reading artifacts')
        self.artifacts()
        print('Reading allowed spells and artifacts')
        self.allowed_spells_artifacts()
        print('Reading rumours')
        self.rumours()
        print('Reading predefined heroes')
        self.read_predefined_heroes()
        print('Reading terrain')
        self.read_terrain()
        print('Reading objects definitions')
        self.read_def_info()
        print('Reading objects')
        self.read_objects()
        print('Reading events')
        self.read_events()

        return self.objects_map, self.terrain_map, self.road_map

    def read_header(self):
        """
        Read the map header
        """
        self.version = Version(self.reader.read_uint32())
        if self.version == Version.HOTA:
            self.hota_subversion = self.reader.read_uint32()
            if self.hota_subversion >= 1:
                sprite_mirror = self.reader.read_uint8()
                hota_arena = self.reader.read_uint8()
            if self.hota_subversion >= 2:
                terrain_count = self.reader.read_uint32()
        else:
            self.hota_subversion = 0

        hero_any_on_map = self.reader.read_bool()

        self.map_size = self.reader.read_uint32()
        
        if self.map_size!=72:
            raise Exception('Wrong map size!')

        self.underground = self.reader.read_uint8()

        if self.underground:
            raise Exception('Underground not implemented!')        

        self.terrain_map = np.empty((self.underground + 1, self.map_size, self.map_size), dtype=object)
        self.road_map = np.empty((self.underground + 1, self.map_size, self.map_size), dtype=object)
        self.objects_map = np.empty((self.underground + 1, self.map_size, self.map_size), dtype=object)

        map_name = self.reader.read_string()
        description = self.reader.read_string()
        difficulty = self.reader.read_uint8()

        if self.version != Version.ROE:
            hero_lvl_cap = self.reader.read_uint8()

    def read_player_info(self):
        """
        Read player info
        """
        for i in range(IntGlobals.PLAYER_SUM):
            human = self.reader.read_bool()
            ai = self.reader.read_bool()

            if not human and not ai:
                if self.version == Version.ROE:
                    self.reader.skip(6)
                elif self.version == Version.AB:
                    self.reader.skip(12)
                else:
                    self.reader.skip(13)
                continue
            behaviour = self.reader.read_uint8()
            if self.version >= Version.SOD:
                town_owned_is_set = self.reader.read_uint8()

            if self.version != Version.ROE:
                towns = self.reader.read_uint16()
            else:
                towns = self.reader.read_uint8()

            is_random_town = self.reader.read_uint8()
            has_main_town = self.reader.read_uint8()

            if has_main_town:
                if self.version != Version.ROE:
                    hero_at_main = self.reader.read_uint8()
                    generate_hero = self.reader.read_uint8()

                town_pos = [self.reader.read_uint8(), self.reader.read_uint8(), self.reader.read_uint8()]

            random_hero = self.reader.read_uint8()
            main_hero_type = self.reader.read_uint8()
            if main_hero_type != IntGlobals.HNONE:
                hero_id = self.reader.read_uint8()
                hero_name = self.reader.read_string()

            if self.version != Version.ROE:
                placeholder = self.reader.read_uint8()
                hero_count = self.reader.read_uint8()
                self.reader.skip(3)
                for j in range(hero_count):
                    hero_id = self.reader.read_uint8()
                    hero_name = self.reader.read_string()

    def free_heroes(self):
        """
        Read disabled heroes
        """
        if self.version == Version.ROE:
            heroes = 16
        elif self.version in (Version.AB, Version.SOD, Version.WOG):
            heroes = 20
        else:
            heroes = 23

        if self.version == Version.HOTA:
            limit = self.reader.read_uint32()

        self.reader.skip(heroes)  # Heroes mask

        if self.version != Version.ROE:
            placeholder = self.reader.read_uint32()
            for i in range(placeholder):
                idx = self.reader.read_uint8()

        if self.version >= Version.SOD:
            hero_custom_count = self.reader.read_uint8()
            for i in range(hero_custom_count):
                print(i)
                idx = self.reader.read_uint8()
                face = self.reader.read_uint8()
                name = self.reader.read_string()
                mask = self.reader.read_uint8()

    def HOTA_map_extra(self):
        """
        Read extra things that HOTA adds
        :return:
        """
        if self.version != Version.HOTA:
            return

        mon_plague_week = self.reader.read_uint32()
        if self.hota_subversion >= 1:
            art_combined = self.reader.read_uint32()
            if art_combined:
                art_comb_num = int(np.ceil(art_combined / 8))
                self.reader.skip(art_comb_num)

            if self.hota_subversion >= 3:
                combat_count_limit = self.reader.read_uint32()

    def artifacts(self):
        """
        Read artifacts
        """
        if self.version != Version.ROE:
            if self.version == Version.AB:
                bytes = 17
            elif self.version != Version.HOTA:
                bytes = 18
            else:
                art_count = self.reader.read_uint32()
                bytes = int(np.ceil(art_count / 8))

            self.reader.skip(bytes)  # Idx of artifacts

    def allowed_spells_artifacts(self):
        """
        Read allowed spells and artifacts
        """
        if self.version >= Version.SOD:
            self.reader.skip(9)  # Ids of spells
            self.reader.skip(4)  # Ids of skills

    def rumours(self):
        """
        Read rumours
        """
        rumours_count = self.reader.read_uint32()
        for i in range(rumours_count):
            name = self.reader.read_string()
            desc = self.reader.read_string()

    def victory_condition(self):
        """
        Read victory condition
        """
        vic_cond = self.reader.read_uint8()

        if vic_cond != Victory.NONE:
            self.reader.read_uint8() # allow normal victory
            self.reader.read_uint8() # applies to AI

        if vic_cond == Victory.NONE:
            pass
        elif vic_cond == Victory.ARTIFACT:
            art = self.reader.read_uint8()
            if self.version != Version.ROE:
                self.reader.skip(1)
        elif vic_cond == Victory.ACCUMULATE_CREATURES:
            mon_id = self.reader.read_uint8()
            if self.version != Version.ROE:
                self.reader.skip(1)
            unit_count = self.reader.read_uint32()
        elif vic_cond == Victory.ACCUMULATE_RESOURCES:
            resource = self.reader.read_uint8()
            resource_count = self.reader.read_uint32()
        elif vic_cond == Victory.UPGRADE_TOWN:
            coords = [self.reader.read_uint8(), self.reader.read_uint8(), self.reader.read_uint8()]
            hall_lvl = self.reader.read_uint8()
            castle_lvl = self.reader.read_uint8()
        elif vic_cond == Victory.BUILD_GRAIL:
            coord = [self.reader.read_uint8(), self.reader.read_uint8(), self.reader.read_uint8()]
        elif vic_cond == Victory.DEFEAT_HERO:
            coord = [self.reader.read_uint8(), self.reader.read_uint8(), self.reader.read_uint8()]
        elif vic_cond == Victory.CAPTURE_TOWN:
            coord = [self.reader.read_uint8(), self.reader.read_uint8(), self.reader.read_uint8()]
        elif vic_cond == Victory.KILL_MONSTER:
            coord = [self.reader.read_uint8(), self.reader.read_uint8(), self.reader.read_uint8()]
        elif vic_cond == Victory.FLAG_DWELLINGS:
            pass
        elif vic_cond == Victory.FLAG_MINES:
            pass
        elif vic_cond == Victory.TRANSPORT_ARTIFACT:
            art = self.reader.read_uint8()
            coord = [self.reader.read_uint8(), self.reader.read_uint8(), self.reader.read_uint8()]
        elif vic_cond == Victory.ELIMINATE_MONSTERS:
            pass
        elif vic_cond == Victory.SURVIVE_TIME:
            time = self.reader.read_uint32()

    def loss_condition(self):
        """
        Read loss condition
        """
        loss_condition = self.reader.read_uint8()

        if loss_condition == Loss.NONE:
            pass
        elif loss_condition == Loss.TOWN:
            coords = [self.reader.read_uint8(), self.reader.read_uint8(), self.reader.read_uint8()]
        elif loss_condition == Loss.HERO:
            coords = [self.reader.read_uint8(), self.reader.read_uint8(), self.reader.read_uint8()]
        elif loss_condition == Loss.TIME:
            time = self.reader.read_uint16()

    def teams(self):
        """
        Read teams of each player
        """
        count = self.reader.read_uint8()
        for i in range(IntGlobals.PLAYER_SUM):
            teams = self.reader.read_uint8() if count != 0 else 0

    def load_artifacts_of_hero(self):
        """
        Load artifacts of a hero
        :return: Artifacts of a hero
        """
        art_set = self.reader.read_uint8()
        artifacts = []
        if art_set:
            for j in range(16):
                if self.version == Version.ROE:
                    artid = self.reader.read_uint8()
                else:
                    artid = self.reader.read_uint16()
                artifacts.append(artid)
            if self.version >= Version.SOD:  # machine 4
                if self.version == Version.ROE:
                    artid = self.reader.read_uint8()
                else:
                    artid = self.reader.read_uint16()
                artifacts.append(artid)

            if self.version == Version.ROE:  # Spellbook
                artid = self.reader.read_uint8()
            else:
                artid = self.reader.read_uint16()
            artifacts.append(artid)

            if self.version == Version.ROE:  # misc5
                artid = self.reader.read_uint8()
            else:
                artid = self.reader.read_uint16()
            artifacts.append(artid)

            amount = self.reader.read_uint16()  # Bag artifacts
            for j in range(amount):
                if self.version == Version.ROE:
                    artid = self.reader.read_uint8()
                else:
                    artid = self.reader.read_uint16()
                artifacts.append(artid)
        return artifacts

    def read_predefined_heroes(self):
        """
        Read predefined heroes
        """
        limit = 156
        if self.version == Version.HOTA:
            limit = self.reader.read_uint32()
        if self.version in (Version.SOD, Version.WOG, Version.HOTA):
            for i in range(limit):
                custom = self.reader.read_uint8()
                if not custom:
                    continue

                has_exp = self.reader.read_uint8()
                if has_exp:
                    exp = self.reader.read_uint32()

                has_sec_skills = self.reader.read_uint8()
                if has_sec_skills:
                    count = self.reader.read_uint32()
                    for j in range(count):
                        name = self.reader.read_uint8()
                        lvl = self.reader.read_uint8()

                self.load_artifacts_of_hero()

                has_custom_bio = self.reader.read_uint8()
                if has_custom_bio:
                    bio = self.reader.read_string()

                sex = self.reader.read_uint8()
                custom_spells = self.reader.read_uint8()
                if custom_spells:
                    self.reader.skip(9)

                custom_pri_skills = self.reader.read_uint8()
                if custom_pri_skills:
                    self.reader.skip(4)

    def read_terrain(self):
        """
        Read terrain
        """
        for z in range(self.underground + 1):
            for y in range(self.map_size):
                for x in range(self.map_size):
                    surface = HeroesConstants.TerrainType[self.reader.read_uint8()]
                    self.reader.skip(3)
                    road = HeroesConstants.RoadType[self.reader.read_uint8()]
                    self.reader.skip(2)
                    self.terrain_map[z][y][x] = surface
                    self.road_map[z][y][x] = road

    def read_def_info(self):
        """
        Read definitions info. That is read every object that exists in the map and define its available
        and blocked spaces and save them as ObjectTemplate objects to an array
        """
        object_templates_number = self.reader.read_uint32()
        for _ in range(object_templates_number):
            animation = self.reader.read_string()
            block_mask = np.empty(6, dtype=int)
            visit_mask = np.empty(6, dtype=int)
            used_tiles = np.full((6, 8), TileType.FREE)
            for j in range(6):
                block_mask[j] = self.reader.read_uint8()
            for j in range(6):
                visit_mask[j] = self.reader.read_uint8()

            for i in range(6):  # rows (x-axis)
                for j in range(8):  # columns (y-axis)
                    tile = TileType.FREE
                    if ((visit_mask[i] >> j) & 1) != 0:
                        tile = TileType.ACCESSIBLE
                    elif ((block_mask[i] >> j) & 1) == 0:
                        tile = TileType.BLOCKED
                    if tile != TileType.FREE:
                        used_tiles[5-i][7-j] = tile

            self.reader.skip(2)  # landscape
            self.reader.skip(2)  # allowed terrain for object

            idx = self.reader.read_uint32()
            if idx == 140:
                a=0
            subidx = self.reader.read_uint32()

            self.reader.skip(2)  # type and print

            obj_template = ObjectTemplate(idx, subidx, used_tiles)

            self.reader.skip(16)

            self.object_templates.append(obj_template)

    def read_resources(self):
        """
        Inside function for reading resources
        :return: Resources
        """
        resources = []
        for i in range(7):
            res = self.reader.read_uint32()
            resources.append(res)
        return resources

    def read_creature_set(self, number):
        """
        Inside function for reading garrisons
        :param number: Number of creature sets
        :return: Creatures
        """
        version = self.version > Version.ROE
        max_id = 0xFFFF if version else 0xFF
        units = []
        for i in range(number):
            creature_id = self.reader.read_uint16() if version else self.reader.read_uint8()
            count = self.reader.read_uint16()
            if creature_id == max_id:  # Empty slot
                continue
            if creature_id > (max_id - 0x0F):
                # This will happen when random object has random army
                creature_id = (max_id - creature_id - 1) + 1000  # arbitrary 1000 for extension of monster ids
            try:
                units.append({HeroesConstants.Monster[creature_id]: count})
            except:
                units.append({HeroesConstants.MonsterWOG[creature_id]: count})
        return units

    def read_message_and_guards(self):
        """
        Read message and guards of an objects
        :return: that message and guards
        """
        has_message = self.reader.read_uint8()
        mag = []
        if has_message:
            message = self.reader.read_string()
            mag.append(message)
            has_guards = self.reader.read_uint8()
            if has_guards:
                stack = self.read_creature_set(7)
                mag.append(stack)
            self.reader.skip(4)
        return mag

    def read_spells(self):
        """
        Read spells
        :return: Spells
        """
        spells = []
        for i in range(9):
            byte = self.reader.read_uint8()
            for n in range(8):
                if (byte & (1 << n)) != 0:
                    spells = HeroesConstants.SpellID[i*8 + n]
        return spells

    def read_hero(self):
        """
        Read hero
        """
        if self.version > Version.ROE:
            uid = self.reader.read_uint32()

        player_color = self.reader.read_uint8()
        sub_id = self.reader.read_uint8()
        has_name = self.reader.read_uint8()
        if has_name:
            name = self.reader.read_string()
        else:
            name = HeroesConstants.Heroes[sub_id]
        if self.version > Version.AB:
            has_exp = self.reader.read_uint8()
            if has_exp:
                exp = self.reader.read_uint32()
        else:
            exp = self.reader.read_uint32()
        has_portrait = self.reader.read_uint8()
        if has_portrait:
            portrait = self.reader.read_uint8()
        has_sec_skills = self.reader.read_uint8()
        skills = []
        if has_sec_skills:
            how_many = self.reader.read_uint32()
            for i in range(how_many):
                skill = HeroesConstants.SecondarySkill[self.reader.read_uint8()]
                lvl = HeroesConstants.SecSkillLevel[self.reader.read_uint8()]
                skills.append(lvl + ' ' + skill)

        has_garrison = self.reader.read_uint8()
        if has_garrison:
            army = self.read_creature_set(7)

        formation = self.reader.read_uint8()
        artifacts = self.load_artifacts_of_hero()
        patrol = self.reader.read_uint8()

        if self.version > Version.ROE:
            has_custom_biography = self.reader.read_uint8()
            if has_custom_biography:
                bio = self.reader.read_string()
            sex = self.reader.read_uint8()

        if self.version > Version.AB:
            has_custom_spells = self.reader.read_uint8()
            if has_custom_spells:
                spells = self.read_spells
        elif self.version == Version.AB:
            buff = self.reader.read_uint8()

        primary_skills = []
        if self.version > Version.AB:
            has_custom_prim_skills = self.reader.read_uint8()
            if has_custom_prim_skills:
                for j in range(4):
                    primary_skills.append(self.reader.read_uint8())
        self.reader.skip(16)

    def read_quest(self):
        """
        Read quests
        """
        task_id = self.reader.read_uint8()

        if task_id == QuestMission.NONE:
            pass
        elif task_id == QuestMission.PRIMARY_STAT:
            for i in range(4):
                value = self.reader.read_uint8()
        elif task_id == QuestMission.LEVEL:
            level = self.reader.read_uint32()
        elif task_id == QuestMission.KILL_HERO:
            hero = self.reader.read_uint32()
        elif task_id == QuestMission.KILL_CREATURE:
            creature = self.reader.read_uint32()
        elif task_id == QuestMission.ART:
            art_number = self.reader.read_uint8()
            for i in range(art_number):
                artifact = self.reader.read_uint16()
        elif task_id == QuestMission.ARMY:
            type_no = self.reader.read_uint8()
            for i in range(type_no):
                monster = self.reader.read_uint16()
                count = self.reader.read_uint16()
        elif task_id == QuestMission.RESOURCES:
            for i in range(7):
                count = self.reader.read_uint32()

        elif task_id == QuestMission.HERO:
            hero = self.reader.read_uint8()
        elif task_id == QuestMission.PLAYER:
            player = self.reader.read_uint8()
        elif task_id == QuestMission.HOTA_EXTRA:
            if self.hota_subversion >= 3:
                hota_quest_id = self.reader.read_uint32()
                if hota_quest_id == QuestMission.HOTA_CLASS:
                    class_count = self.reader.read_uint32()
                    if class_count:
                        class_avail = int(np.ceil(class_count/8))
                        for i in range(class_avail):
                            class_mask = self.reader.read_uint8()

                elif hota_quest_id == QuestMission.HOTA_NOTBEFORE:
                    return_after = self.reader.read_uint32()

        limit = self.reader.read_uint32()
        text_first = self.reader.read_string()
        text_after = self.reader.read_string()
        text_done = self.reader.read_string()

    def read_reward(self):
        """
        Read rewards
        """
        reward_id = self.reader.read_uint8()

        if reward_id == RewardType.EXPERIENCE:
            value = self.reader.read_uint32()
        elif reward_id == RewardType.MANA_POINTS:
            value = self.reader.read_uint32()
        elif reward_id == RewardType.MORALE_BONUS:
            value = self.reader.read_uint8()
        elif reward_id == RewardType.LUCK_BONUS:
            value = self.reader.read_uint8()
        elif reward_id == RewardType.RESOURCES:
            id = self.reader.read_uint8()
            count = self.reader.read_uint32()
        elif reward_id == RewardType.PRIMARY_SKILL:
            id = self.reader.read_uint8()
            value = self.reader.read_uint8()
        elif reward_id == RewardType.SECONDARY_SKILL:
            id = self.reader.read_uint8()
            value = self.reader.read_uint32()
        elif reward_id == RewardType.ARTIFACT:
            if self.version == Version.ROE:
                artifact = self.reader.read_uint8()
            else:
                artifact = self.reader.read_uint16()
        elif reward_id == RewardType.SPELL:
            idx = self.reader.read_uint8()
        elif reward_id == RewardType.CREATURE:
            if self.version == Version.ROE:
                artifact = self.reader.read_uint8()
            else:
                artifact = self.reader.read_uint16()
            value = self.reader.read_uint16()

    def read_seer_hut(self):
        """
        Read quests and rewards of the seer hut
        :return: Just a message for everyone to absolutely not enter this building
        """
        if self.version > Version.ROE:
            num_quest = 1
            if self.hota_subversion >= 3:
                num_quest = self.reader.read_uint32()
            for i in range(num_quest):
                self.read_quest()
                self.read_reward()
        else:
            art_id = self.reader.read_uint8()
            self.read_reward()

        # HOTA extra - multiple/cycled quests
        if self.hota_subversion >= 3:
            num_quest = self.reader.read_uint32()
            for i in range(num_quest):
                self.read_quest()
                self.read_reward()
        self.reader.skip(2)
        return "Quests - don't touch"

    def read_town(self):
        """
        Read town
        """
        if self.version > Version.ROE:
            uid = self.reader.read_uint32()

        owner = self.reader.read_uint8()
        player = HeroesConstants.PlayersColors[owner]

        has_name = self.reader.read_uint8()
        name = 'Random'
        if has_name:
            name = self.reader.read_string()
        stack = []
        has_garrison = self.reader.read_uint8()
        if has_garrison:
            stack = self.read_creature_set(7)
        formation = self.reader.read_uint8()

        has_custom_buildings = self.reader.read_uint8()
        if has_custom_buildings:
            self.reader.skip(12)
        else:
            has_fort = self.reader.read_uint8()

        spells_always = []  # Not implemented
        if self.version > Version.ROE:
            for i in range(9):
                spell = self.reader.read_uint8()

        spells_random = []  # Not implemented
        for i in range(9):
            spell = self.reader.read_uint8()

        if self.hota_subversion >= 1:
            self.reader.skip(1)  # spell research

        events_num = self.reader.read_uint32()
        for j in range(events_num):
            name = self.reader.read_string()
            message = self.reader.read_string()
            res = self.read_resources()
            players = self.reader.read_uint8()
            if self.version > Version.AB:
                human = self.reader.read_uint8()
            computer_affected = self.reader.read_uint8()
            first_occurrence = self.reader.read_uint16() + 1
            next_occurrence = self.reader.read_uint8()
            self.reader.skip(17)
            for n in range(6):  # buildings
                self.reader.read_uint8()
            for n in range(7):  # monsters
                self.reader.read_uint16()
            self.reader.skip(4)

        if self.version > Version.AB:
            alignment = self.reader.read_uint8()
        self.reader.skip(3)

    def read_objects(self):
        """
        Read every object in the game, check it in the definitions and save to the object map as its string name, its id
        and some additional information (for example number of resources or guards or messages)
        """
        object_num = self.reader.read_uint32()

        for i in range(object_num):
            x = self.reader.read_uint8()
            y = self.reader.read_uint8()
            z = self.reader.read_uint8()

            defnum = self.reader.read_uint32()
            curr_object = self.object_templates[defnum]
            object_idx = curr_object.id

            object_more_info = []

            self.reader.skip(5)

            if object_idx in (Objects.EVENT, Objects.PANDORAS_BOX):
                message_stack = self.read_message_and_guards()
                gained_exp = self.reader.read_uint32()
                mana_diff = self.reader.read_uint32()
                morale_diff = self.reader.read_uint8()
                luck_diff = self.reader.read_uint8()
                resources = self.read_resources()

                primary_skills = []
                for j in range(4):
                    primary_skills.append(self.reader.read_uint8())

                secondary_skills = []
                secondary_skills_num = self.reader.read_uint8()
                for j in range(secondary_skills_num):
                    skill = HeroesConstants.SecondarySkill[self.reader.read_uint8()]
                    lvl = HeroesConstants.SecSkillLevel[self.reader.read_uint8()]
                    secondary_skills.append(lvl + ' ' + skill)

                artifacts = []
                artifact_number = self.reader.read_uint8()
                for j in range(artifact_number):
                    if self.version == Version.ROE:
                        art_id = self.reader.read_uint8()
                    else:
                        art_id = self.reader.read_uint16()
                    artifact = HeroesConstants.Artifacts[art_id]
                    artifacts.append(artifact)

                spells = []
                spell_num = self.reader.read_uint8()
                for j in range(spell_num):
                    spells.append(HeroesConstants.SpellID[self.reader.read_uint8()])

                cr_num = self.reader.read_uint8()
                creatures = self.read_creature_set(cr_num)

                self.reader.skip(8)

                if object_idx == Objects.EVENT:
                    available_for = self.reader.read_uint8()
                    computer_activate = self.reader.read_uint8()
                    remove_after_visit = self.reader.read_uint8()
                    if self.hota_subversion >= 3:
                        human_activate = self.reader.read_uint8()
                    else:
                        human_activate = 1
                    self.reader.skip(4)
                    object_more_info.append((message_stack, gained_exp, mana_diff, morale_diff, luck_diff, resources,
                                             primary_skills, secondary_skills, artifacts, spells, creatures,
                                             available_for, computer_activate, remove_after_visit, human_activate))
                    continue

                object_more_info.append((message_stack, gained_exp, mana_diff, morale_diff, luck_diff, resources,
                                         primary_skills, secondary_skills, artifacts, spells, creatures))

            elif object_idx in (Objects.HERO, Objects.RANDOM_HERO, Objects.PRISON):
                self.read_hero()  # May cause errors if there is hero in town gate

            elif object_idx in (Objects.MONSTER, Objects.RANDOM_MONSTER, Objects.RANDOM_MONSTER_L1,
                                Objects.RANDOM_MONSTER_L2, Objects.RANDOM_MONSTER_L3, Objects.RANDOM_MONSTER_L4,
                                Objects.RANDOM_MONSTER_L5, Objects.RANDOM_MONSTER_L6, Objects.RANDOM_MONSTER_L7):
                if self.version > Version.ROE:
                    uid = self.reader.read_uint32()

                if object_idx == Objects.MONSTER:
                    name = HeroesConstants.Monster[curr_object.subid]
                else:
                    name = 'random'
                count = self.reader.read_uint16()
                character = HeroesConstants.MonChar[self.reader.read_uint8()]  # Will join or not

                has_message = self.reader.read_uint8()
                if has_message:
                    message = self.reader.read_string()
                    resources = self.read_resources()
                    if self.version == Version.ROE:
                        artid = self.reader.read_uint8()
                    else:
                        artid = self.reader.read_uint16()  # It could give some artifacts but not implementing that

                never_flees = self.reader.read_uint8()
                not_growing_team = self.reader.read_uint8()
                self.reader.skip(2)

                if self.hota_subversion >= 3:
                    character_spec = self.reader.read_uint32()
                    money_join = self.reader.read_uint8()
                    percent_join = self.reader.read_uint32()
                    upgraded_stack = self.reader.read_uint32()  # upgraded stack in not upgraded monster 0/1/ffffffff
                    stacks_count = self.reader.read_uint32()  # 00=one more, ffffffff=def,
                                                             # fdffffff=avg, fdffffff=on less or num

                object_more_info.append((name, count))

            elif object_idx in (Objects.OCEAN_BOTTLE, Objects.SIGN):
                text = self.reader.read_string()
                self.reader.skip(4)
                object_more_info.append(text)

            elif object_idx == Objects.SEER_HUT:
                object_more_info.append(self.read_seer_hut())

            elif object_idx == Objects.WITCH_HUT:
                if self.version > Version.ROE:
                    for j in range(4):
                        allowed = self.reader.read_uint8()

            elif object_idx == Objects.SCHOLAR:
                bonus_type = self.reader.read_uint8()
                bonus_id = self.reader.read_uint8()
                self.reader.skip(6)
                object_more_info.append((bonus_type, bonus_id))

            elif object_idx in (Objects.GARRISON, Objects.GARRISON2):
                owner = self.reader.read_uint8()
                self.reader.skip(3)
                monsters = self.read_creature_set(7)
                if self.version > Version.ROE:
                    removable_units = self.reader.read_uint8()
                else:
                    removable_units = 1
                self.reader.skip(8)
                object_more_info.append(monsters)

            elif object_idx in (Objects.ARTIFACT, Objects.RANDOM_ART, Objects.RANDOM_TREASURE_ART,
                                Objects.RANDOM_MINOR_ART, Objects.RANDOM_MAJOR_ART, Objects.RANDOM_RELIC_ART,
                                Objects.SPELL_SCROLL):

                stack = self.read_message_and_guards()
                if object_idx == Objects.SPELL_SCROLL:
                    spell_id = self.reader.read_uint32()
                    artifact = curr_object.name + ': ' + HeroesConstants.SpellID[spell_id]
                elif object_idx == Objects.ARTIFACT:
                    artifact = HeroesConstants.Artifacts[curr_object.subid]
                else:
                    artifact = curr_object.name
                object_more_info.append((artifact, stack))

            elif object_idx in (Objects.RANDOM_RESOURCE, Objects.RESOURCE):
                stack = self.read_message_and_guards()
                amount = self.reader.read_uint32()
                self.reader.skip(4)
                object_more_info.append((amount, stack))

            elif object_idx in (Objects.TOWN, Objects.RANDOM_TOWN):  # Not sure where the town coords will be
                self.read_town()

            elif object_idx in (Objects.MINE, Objects.ABANDONED_MINE):
                owner = self.reader.read_uint8()  # resource mask for abandoned mine, not implemented
                self.reader.skip(3)

            elif object_idx in (Objects.CREATURE_GENERATOR1, Objects.CREATURE_GENERATOR2,
                                Objects.CREATURE_GENERATOR3, Objects.CREATURE_GENERATOR4):
                owner = self.reader.read_uint8()
                self.reader.skip(3)
            elif object_idx in (Objects.SHRINE_OF_MAGIC_GESTURE, Objects.SHRINE_OF_MAGIC_THOUGHT,
                                Objects.SHRINE_OF_MAGIC_INCANTATION):
                spell_id = self.reader.read_uint8()
                self.reader.skip(3)
                object_more_info.append(('Spell id', spell_id))
            elif object_idx == Objects.GRAIL:
                if self.hota_subversion >= 3:
                    if 1000 <= curr_object.subid <= 1003:  # Grail not allowed
                        continue
                radius = self.reader.read_uint32()
            elif object_idx in (Objects.RANDOM_DWELLING, Objects.RANDOM_DWELLING_LVL,
                                Objects.RANDOM_DWELLING_FACTION):
                player = self.reader.read_uint32()
                if object_idx in (Objects.RANDOM_DWELLING, Objects.RANDOM_DWELLING_LVL):
                    uid = self.reader.read_uint32()
                    if not uid:
                        castles_1 = self.reader.read_uint8()
                        castles_2 = self.reader.read_uint8()
                if object_idx in (Objects.RANDOM_DWELLING, Objects.RANDOM_DWELLING_FACTION):
                    min_lvl = max(self.reader.read_uint8(), 1)
                    max_lvl = min(self.reader.read_uint8(), 7)

            elif object_idx == Objects.QUEST_GUARD:
                self.read_quest()

            elif object_idx == Objects.SHIPYARD:
                owner = self.reader.read_uint32()

            elif object_idx == Objects.HERO_PLACEHOLDER:
                tile_owner = self.reader.read_uint8()
                hero_id = self.reader.read_uint8()
                if hero_id == IntGlobals.HNONE:
                    power = self.reader.read_uint8()

            elif object_idx == Objects.BORDER_GATE:
                if self.hota_subversion >= 3:
                    if curr_object.subid == 1000:
                        self.read_quest()

            elif object_idx in (Objects.BORDER_GUARD, Objects.KEY_MASTER, Objects.PYRAMID):
                pass

            elif object_idx == Objects.LIGHTHOUSE:
                owner = self.reader.read_uint32()

            elif object_idx in (Objects.CREATURE_BANK, Objects.DERELICT_SHIP, Objects.DRAGON_UTOPIA,
                                Objects.CRYPT, Objects.SHIPWRECK):
                if self.hota_subversion >= 3:
                    variant = self.reader.read_uint32()
                    upgraded = self.reader.read_uint8()
                    artnum = self.reader.read_uint32()
                    artifacts = []
                    for j in range(artnum):
                        art_id = self.reader.read_uint32()
                        if art_id == 0xffffffff:
                            artifacts.append('Random')
                        else:
                            artifacts.append(HeroesConstants.Artifacts[art_id])
                    object_more_info.append({'variant': variant, 'upgraded': upgraded, 'artifacts': artifacts})
            try:
                self.object_list.append((curr_object, object_more_info, (x, y, z)))
                self.objects_map[z][y][x] = (curr_object, object_more_info)
            except:
                a=0

    def read_events(self):
        """
        Read events
        """
        number_of_events = self.reader.read_uint32()
        for i in range(number_of_events):
            name = self.reader.read_string()
            message = self.reader.read_string()
            resources = self.read_resources()
            players = self.reader.read_uint8()
            if self.version > Version.AB:
                human_able = self.reader.read_uint8()
            ai_able = self.reader.read_uint8()
            first = self.reader.read_uint16() + 1
            interval = self.reader.read_uint16()
            self.reader.skip(16)

    def write_objects_to_file(self, path: str):
        with open(path, "w") as f:
            content = []
            for obj in self.object_list:
                json_dict = obj[0].to_json()
                json_dict["more"] = obj[1]
                json_dict["pos"] = obj[2]
                content.append(json_dict)
            to_write = json.dumps(content)
            f.write(to_write)


if __name__ == '__main__':
    m = Map()
    m.read_map("test_files/Map_test.h3m")

    a = m.objects_map
    b = m.terrain_map
    c = m.road_map

    test = 0



