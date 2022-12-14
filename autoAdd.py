import sys
from time import sleep
from presets import PresetList
from utils import *


class AutoAdd:
    def __init__(self, filename):
        self.__filename = filename
        self.__read_ini()
        if isTekken7Path(self.__path):  # Append path to binary file if it's T7 path
            self.__path += "\\TekkenGame\\Content\\Binary\\list\\"
        self.__presetlist = PresetList(self.__path + self.__filename)

    def __read_ini(self):
        fileData = {}
        with open('presets.ini', 'r') as fd:
            lines = fd.readlines()
            lines = [line.replace(' ', '') for line in lines]

        for line in lines:
            parseLine(line, fileData)

        try:
            self.__path = fileData['path']
            if self.__path.startswith('\"') and self.__path.endswith('\"'):
                self.__path = self.__path[1:-1]
        except:
            self.__path = "./"

        try:
            self.__preset_name = fileData['preset_name']
            if self.__preset_name.startswith('\"') and self.__preset_name.endswith('\"'):
                self.__preset_name = self.__preset_name[1:-1]
        except:
            self.__preset_name = None

        try:
            self.__character_ids = fileData['character_ids']
        except:
            self.__character_ids = [-1]

    def addPresets(self):
        for id in self.__character_ids:
            success, msg = self.__presetlist.addPreset(
                id, self.__preset_name, False)
            if success:
                print("Successfully added preset \"%s\" for character \"%s\"" %
                      (self.__preset_name, Char(id)))
            else:
                print("Couldn't add preset \"%s\" for character \"%s\".\nReason: %s" % (
                    self.__preset_name, Char(id), msg))
        if self.__presetlist.saveFile(self.__path):
            print("File successfully saved in folder \"%s\"" % self.__path)

    def removePresets(self):
        for id in self.__character_ids:
            success, msg = self.__presetlist.removePreset(
                id, self.__preset_name, False)
            if success:
                print("Successfully removed preset \"%s\" from character \"%s\"" % (
                    self.__preset_name, Char(id)))
            else:
                print("Couldn't add remove \"%s\" from character \"%s\".\nReason: %s" % (
                    self.__preset_name, Char(id), msg))
        if self.__presetlist.saveFile(self.__path):
            print("File successfully saved in folder \"%s\"" % self.__path)


def main():
    print(sys.argv)
    if len(sys.argv) < 2:
        print("Parameters not provided. 0 = Add. 1 = Remove")
        sleep(3)
        return
    autoAdd = AutoAdd("customize_preset_table_cs_s3.bin")
    if sys.argv[1] == '0':
        # print("read ini file and add presets")
        autoAdd.addPresets()
    elif sys.argv[1] == '1':
        # print("read ini file and remove presets")
        autoAdd.removePresets()
    else:
        print("Invalid parameters. 0 = Add. 1 = Remove")
    # sleep(3)
    return


if __name__ == '__main__':
    main()
