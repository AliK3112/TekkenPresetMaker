import struct
import os


class BinaryReader:
    def __init__(self, filepath, OpenFile=False):
        self.filepath = filepath
        self.fd = None
        self.__fileIsOpen = False
        if OpenFile:
            self.openFile()

    def openFile(self):
        try:
            self.fd = open(self.filepath, 'rb')
        except FileNotFoundError:
            self.__fileIsOpen = False
        if self.fd != None:
            self.__fileIsOpen = True
        return self.__fileIsOpen

    def closeFile(self):
        self.__fileIsOpen = False
        self.fd.close()

    def isOpen(self):
        return self.fd != None

    def getFileSize(self):
        return os.path.getsize(self.filepath)

    def __read(self, addr, size, flag, base=0, endian='little'):
        if self.fd == None:
            return "FILE NOT OPEN"
        # Storing original position
        original_position = self.fd.tell()
        # Setting position to given address
        self.fd.seek(addr+base)
        # Setting endian + struct flag
        str = '>'+flag if endian == 'big' else '<'+flag
        # Reading value
        try:
            val = struct.unpack(str, self.fd.read(size))[0]
        except Exception:  # raise Exception
            val = None
        # Restoring position to original
        self.fd.seek(original_position)
        # Returning bytes
        return val

    def __readBytes(self, addr, size):
        if self.fd == None:
            return "FILE NOT OPEN"
        # Storing original position
        x = self.fd.tell()
        # Setting position to given address
        self.fd.seek(addr)
        # Reading bytes
        bytes = self.fd.read(size)
        # Restoring position to original
        self.fd.seek(x)
        # Returning read bytes
        return bytes

    def readString(self, addr, offset=0):
        if self.fd == None:
            return "FILE NOT OPEN"
        if offset != 0:
            return self.__readBytes(addr, offset).decode("ascii")
        while self.__readBytes(addr + offset, 1) != b'\x00':
            offset += 1
        return self.__readBytes(addr, offset).decode("ascii")

    def readByte(self, addr, endian='little', base=0):  # byte
        return self.__read(addr, 1, 'b', base, endian)

    def readInt8(self, addr, endian='little', base=0):
        return self.__read(addr, 1, 'b', base, endian)

    def readUInt8(self, addr, endian='little', base=0):
        return self.__read(addr, 1, 'B', base, endian)

    def readShort(self, addr, endian='little', base=0):  # int16
        return self.__read(addr, 2, 'h', base, endian)

    def readInt16(self, addr, endian='little', base=0):
        return self.__read(addr, 2, 'h', base, endian)

    def readUInt16(self, addr, endian='little', base=0):
        return self.__read(addr, 2, 'H', base, endian)

    def readInt(self, addr, endian='little', base=0):  # int32
        return self.__read(addr, 4, 'i', base, endian)

    def readInt32(self, addr, endian='little', base=0):
        return self.__read(addr, 4, 'i', base, endian)

    def readUInt32(self, addr, endian='little', base=0):
        return self.__read(addr, 4, 'I', base, endian)

    def readLong(self, addr, endian='little', base=0):  # int64
        return self.__read(addr, 8, 'q', base, endian)

    def readInt64(self, addr, endian='little', base=0):
        return self.__read(addr, 8, 'q', base, endian)

    def readUInt64(self, addr, endian='little', base=0):
        return self.__read(addr, 8, 'Q', base, endian)

    def readFloat(self, addr, endian='little', base=0):
        return self.__read(addr, 4, 'f', base, endian)

    def readDouble(self, addr, endian='little', base=0):
        return self.__read(addr, 8, 'd', base, endian)

    # END OF CLASS

# if __name__ == "__main__":
# 	br = BinaryReader('mota_8.bin', True)
# 	header = br.readString(0)
# 	print(header)
# 	endianInt = br.readUInt32(4)
# 	endian = 'big' if endianInt == 256 else 'little'
# 	print(endianInt)
# 	print(br.readByte(8, endian))
# 	print(br.readUInt32(12, endian))
# 	print(br.readUInt32(16, endian))
