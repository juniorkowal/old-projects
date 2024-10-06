import pickle
import gzip


def save_object(obj, filename):
    """
    function to compress and save object of our class

    :param obj: object to save
    :param filename: path to file
    :return:
    """
    object = pickle.dumps(obj,pickle.HIGHEST_PROTOCOL)
    compressed = gzip.compress(object)
    with open(filename, 'wb') as outp:
        outp.write(compressed)


def load_object(filename):
    """

    function to load and uncompress object of our class

    :param filename: path to file to load
    :return: object from file specified in input
    """
    with open(filename, 'rb') as inp:
        compressed = inp.read()
        uncompressed = gzip.decompress(compressed)
        return pickle.loads(uncompressed)


def load_advai(filename):
    """

    function to load adventure ai object and return both adventure ai and player objects

    :param filename: path to file
    :return: adventure ai object and player object
    """
    with open(filename, 'rb') as inp:
        compressed = inp.read()
        uncompressed = gzip.decompress(compressed)
        advai = pickle.loads(uncompressed)
        player = advai.player
        return advai, player
