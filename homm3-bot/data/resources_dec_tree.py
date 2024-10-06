"""Script containing functions responsible for choosing which type of resources to choose"""
from data.player_data import Player


def resources_dec_tree(player: Player, resources: dict, day: int):
    """
    Choosing resources decision tree.
    :param player: Player object
    :param resources: Resources that we own (dict)
    :param day: Current day (int)
    :return: "gold" | "wood" | "ore" | "exp" | "crystal" | "gems" | "sulfur" | "mercury"
    """
    if day < 14:
        if player.gold < 15000:
            if "gold" in resources:
                if resources["gold"] > 999:
                    return "gold"
                else:
                    if "wood" in resources:
                        if player.wood <= player.ore:
                            return "wood"
                        else:
                            if "ore" in resources:
                                return "ore"
                    else:
                        if "ore" in resources:
                            return "ore"
                        else:
                            if "exp" in resources:
                                return "exp"
                            else:
                                if "mercury" in resources:
                                    return "mercury"
                                else:
                                    if "sulfur" in resources:
                                        return "sulfur"
                                    else:
                                        if "crystal" in resources:
                                            return "crystal"
                                        else:
                                            if "gems" in resources:
                                                return "gems"
            else:
                if "wood" in resources:
                    if player.wood <= player.ore:
                        return "wood"
                    else:
                        if "ore" in resources:
                            return "ore"
                else:
                    if "ore" in resources:
                        return "ore"
                    else:
                        if "exp" in resources:
                            return "exp"
                        else:
                            if "mercury" in resources:
                                return "mercury"
                            else:
                                if "sulfur" in resources:
                                    return "sulfur"
                                else:
                                    if "crystal" in resources:
                                        return "crystal"
                                    else:
                                        if "gems" in resources:
                                            return "gems"
                                        else:
                                            return False
        else:
            if "wood" in resources:
                if player.wood <= player.ore:
                    return "wood"
                else:
                    if "ore" in resources:
                        return "ore"
            else:
                if "ore" in resources:
                    return "ore"
                else:
                    if "gold" in resources:
                        return "gold"
                    else:
                        if "exp" in resources:
                            return "exp"
                        else:
                            if "mercury" in resources:
                                return "mercury"
                            else:
                                if "sulfur" in resources:
                                    return "sulfur"
                                else:
                                    if "crystal" in resources:
                                        return "crystal"
                                    else:
                                        if "gems" in resources:
                                            return "gems"
    else:
        if player.gold < 15000:
            if "gold" in resources:
                if resources["gold"] > 999:
                    return "gold"
                else:
                    if "wood" in resources:
                        if player.wood <= player.ore:
                            return "wood"
                        else:
                            if "ore" in resources:
                                return "ore"
                    else:
                        if "ore" in resources:
                            return "ore"
                        else:
                            if "exp" in resources:
                                return "exp"
                            else:
                                if "mercury" in resources:
                                    return "mercury"
                                else:
                                    if "sulfur" in resources:
                                        return "sulfur"
                                    else:
                                        if "crystal" in resources:
                                            return "crystal"
                                        else:
                                            if "gems" in resources:
                                                return "gems"
            else:
                if "wood" in resources:
                    if player.wood <= player.ore:
                        return "wood"
                    else:
                        if "ore" in resources:
                            return "ore"
                else:
                    if "ore" in resources:
                        return "ore"
                    else:
                        if "exp" in resources:
                            return "exp"
                        else:
                            if "mercury" in resources:
                                return "mercury"
                            else:
                                if "sulfur" in resources:
                                    return "sulfur"
                                else:
                                    if "crystal" in resources:
                                        return "crystal"
                                    else:
                                        if "gems" in resources:
                                            return "gems"
                                        else:
                                            return False
        else:
            if "wood" in resources:
                if player.wood <= player.ore:
                    return "wood"
                else:
                    if "ore" in resources:
                        return "ore"
            else:
                if "ore" in resources:
                    return "ore"
                else:
                    if "gold" in resources:
                        return "gold"
                    else:
                        if "exp" in resources:
                            return "exp"
                        else:
                            if "mercury" in resources:
                                return "mercury"
                            else:
                                if "sulfur" in resources:
                                    return "sulfur"
                                else:
                                    if "crystal" in resources:
                                        return "crystal"
                                    else:
                                        if "gems" in resources:
                                            return "gems"


def gold_or_exp(hero, player):
    """
    Function deciding if player needs exp or gold.
    :param hero: Hero object
    :param player: Player object
    :return: "gold" | "exp"
    """
    if hero.herotype == "main":
        if player.gold < 2000:
            return "gold"
        else:
            return "exp"
    else:
        if player.gold > 25000:
            return "exp"
        else:
            return "gold"
