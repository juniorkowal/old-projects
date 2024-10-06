from file_reader.MapConstants import HeroesConstants


class ObjectTemplate:
    def __init__(self, idx, subid, tiles):
        self.id = idx
        self.subid = subid
        self.tiles = tiles
        try:
            self.name = HeroesConstants.Objects[self.id]
        except:
            self.name = '?'

    def __repr__(self):
        return self.name + ', id: ' + str(self.id)

    def to_json(self):
        json = {"name": self.name, "id": self.id, "subid": self.subid, "tiles": self.tiles.tolist()}
        return json
