import gzip


class FileReader:
    def __init__(self, filename: str = ''):
        if not filename:  # This is just so it can be called without filename for hints annotations
            return
        if self.is_map_gzipped(filename):
            self.file = gzip.open(filename, 'rb')
        else:
            self.file = open(filename, 'rb')
        self.testing = self.file.read()
        self.file.seek(0)

    def is_map_gzipped(self, filepath: str):
        """
        Check if map is gzipped
        :param filepath: filename
        :return: is map gzipped
        """
        with gzip.open(filepath, 'rb') as gz_f:
            try:
                self.file = gz_f.read(1)
                return True
            except gzip.BadGzipFile:
                return False

    def read_uint8(self):
        """
        Read 1 byte as uint
        :return: That 1 byte as int
        """
        self.testing = self.testing[1:]
        return int.from_bytes(self.file.read(1), "little", signed=False)

    def read_uint16(self):
        """
        Read 2 bytes as uint
        :return: That 2 bytes as int
        """
        self.testing = self.testing[2:]
        return int.from_bytes(self.file.read(2), "little", signed=False)

    def read_uint32(self):
        """
        Read 4 bytes as uint
        :return: That 4 bytes as int
        """
        self.testing = self.testing[4:]
        return int.from_bytes(self.file.read(4), "little", signed=False)

    def read_bool(self):
        """
        Read 1 byte as bool
        :return: That 1 byte as bool
        """
        self.testing = self.testing[1:]
        return int.from_bytes(self.file.read(1), "little", signed=False) != 0

    def read_uint_custom(self, byte_number):
        """
        Read custom amount of bytes as bool
        :return: That custom amount of bytes as bool
        """
        self.testing = self.testing[byte_number:]
        return int.from_bytes(self.file.read(byte_number), "little", signed=False)

    def read_string(self):
        """
        Read a string by reading 4 bytes first that show that string length in bytes and the reading that many bytes
        :return: Read string
        """
        self.testing = self.testing[4:]
        string_length = int.from_bytes(self.file.read(4), "little", signed=False)
        self.testing = self.testing[string_length:]
        return self.file.read(string_length).decode("utf-8")

    def skip(self, number: int):
        """
        Skip a certain amount of bytes in the file
        :param number: How many bytes to skip
        """
        self.testing = self.testing[number:]
        self.file.read(number)
       #  self.file.seek(number, 1)


