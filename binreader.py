import struct
import os

class BinaryReader:
    def __init__(self, filepath, OpenFile=False):
        self.__filepath = filepath
        self.__fd = None
        self.__fileIsOpen = False
        if OpenFile:
            self.openFile()

    def __del__(self):
        self.__fd.close()

    def openFile(self):
        try:
            self.__fd = open(self.__filepath, 'rb')
        except FileNotFoundError:
            self.__fileIsOpen = False
        if self.__fd != None:
            self.__fileIsOpen = True
        return self.__fileIsOpen

    def closeFile(self):
        self.__fileIsOpen = False
        self.__fd.close()

    def isOpen(self):
        return self.__fd != None

    def getFileSize(self):
        return os.path.getsize(self.__filepath)

    def __read(self, addr:int, size:int, flag:str, base=0, endian='little'):
        # Checks
        if self.__fd == None:
            return "FILE NOT OPEN"
        if type(addr) != int:
            raise TypeError("'address' must be 'int'")
        if type(size) != int:
            raise TypeError("'size' must be 'int'")
        if type(flag) != type(""):
            raise TypeError("'flag' must be 'str'")
        if type(base) != int:
            raise TypeError("'base' must be 'int'")
        if endian != 'little' and endian != 'big':
            raise ValueError("'endian' must be literal ['big', 'little']")

        # Storing original position
        original_position = self.__fd.tell()
        # Setting position to given address
        if addr != -1:
            self.__fd.seek(addr+base)
        # Setting endian + struct flag
        str = '>'+flag if endian == 'big' else '<'+flag
        # Reading value
        try:
            val = struct.unpack(str, self.__fd.read(size))[0]
        except Exception:  # raise Exception
            val = None
        # Restoring position to original
        if addr != -1:
            self.__fd.seek(original_position)
        # Returning bytes
        return val

    def __readBytes(self, addr=-1, size=1):
        if self.__fd == None:
            return "FILE NOT OPEN"
        # Storing original position
        x = self.__fd.tell()
        # Setting position to given address
        if addr != -1:
            self.__fd.seek(addr)
        # Reading bytes
        bytes = self.__fd.read(size)
        # Restoring position to original
        if addr != -1:
            self.__fd.seek(x)
        # Returning read bytes
        return bytes

    def readString(self, addr=-1, offset=0):
        if self.__fd == None:
            return "FILE NOT OPEN"
        if addr == -1:
            addr = self.__fd.tell()
        if offset != 0:
            return self.__readBytes(addr, offset).decode("ascii")
        while True:
            c = self.__readBytes(addr + offset, 1)
            if c == b'\x00' or c == b'':
                break
            offset += 1
        return self.__readBytes(addr, offset).decode("ascii")

    def readChar(self, addr=-1, endian='little', base=0):  # byte
        result = self.__read(addr, 1, 'c', base, endian)
        return result.decode('ascii') if result != None else result
    
    def readByte(self, addr=-1, endian='little', base=0):  # byte
        return self.__read(addr, 1, 'b', base, endian)

    def readInt8(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 1, 'b', base, endian)

    def readUInt8(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 1, 'B', base, endian)

    def readShort(self, addr=-1, endian='little', base=0):  # int16
        return self.__read(addr, 2, 'h', base, endian)

    def readInt16(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 2, 'h', base, endian)

    def readUInt16(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 2, 'H', base, endian)

    def readInt(self, addr=-1, endian='little', base=0):  # int32
        return self.__read(addr, 4, 'i', base, endian)

    def readInt32(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 4, 'i', base, endian)

    def readUInt32(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 4, 'I', base, endian)

    def readLong(self, addr=-1, endian='little', base=0):  # int64
        return self.__read(addr, 8, 'q', base, endian)

    def readInt64(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 8, 'q', base, endian)

    def readUInt64(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 8, 'Q', base, endian)

    def readFloat(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 4, 'f', base, endian)

    def readDouble(self, addr=-1, endian='little', base=0):
        return self.__read(addr, 8, 'd', base, endian)

    # END OF CLASS

if __name__ == "__main__":
    br = BinaryReader('test.bin', True)
    print(br.readInt32())
    print(br.readInt32())
    print(br.readInt16())
    print(br.readString())