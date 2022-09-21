import json
import os
import sys
from binreader import BinaryReader
from utils import *
from orig import original_preset_list


class PresetList:
    def __init__(self, path: str):
        self.__filename = os.path.basename(path)
        self.reader = BinaryReader(path, True)
        if not self.reader.isOpen():
            raise FileNotFoundError("Failed to Open File %s" % self.__filename)
        self.preset_dict = {}
        self.__readPresets()

    def __del__(self):
        self.reader.__del__()

    def __readPresets(self):
        if not self.reader.isOpen():
            return
        self.paths_addr = self.reader.readInt64(0)
        self.num_chars = self.reader.readInt64(8)
        base = 0x10
        for i in range(self.num_chars):
            charID = self.reader.readInt64(i * 0x198, base=base) + 256
            # Setting Preset Dictionary
            self.preset_dict[Char(charID)] = {
                'char_id': charID, 'count': 0, 'presets': []}
            # Reading all presets
            for j in range(50):
                addr = i * 0x198 + j * 8
                cosOffset = self.reader.readInt64(addr, base=0x18)
                cosTitle = self.reader.readString(cosOffset)
                if cosTitle != '':
                    self.preset_dict[Char(charID)]['count'] += 1
                self.preset_dict[Char(charID)]['presets'].append(cosTitle)
        return

    def __getCharPresetInfo(self, char_id):
        if char_id in forbiddenChars:
            return None
        for char in self.preset_dict:
            if self.preset_dict[char]['char_id'] == char_id:
                return self.preset_dict[char]
        return None

    def addPreset(self, char_id=-1, preset_name='', save=True) -> bool:
        if char_id == -1:
            return False, "No Character ID provided"

        if preset_name == '' or preset_name == None:
            return False, "No Preset Name Passed"

        char_info = self.__getCharPresetInfo(char_id)

        if char_info == None:
            return False, "Invalid Character ID passed"

        count = char_info['count']
        if count + 1 > 50:
            return False, "Preset limit reached (50)"

        if preset_name[0:3] != three_letter_initials[char_id]:
            preset_name = three_letter_initials[char_id] + '_' + preset_name

        char_info['presets'][count] = preset_name
        char_info['count'] += 1

        if save:
            return self.saveFile(), "OK"
        else:
            return True, "OK"

    def removePreset(self, char_id=-1, preset_name='', save=True):
        if char_id == -1:
            return False, "No Character ID provided"

        if preset_name == '' or preset_name == None:
            return False, "No Preset Name Passed"

        char_info = self.__getCharPresetInfo(char_id)

        if char_info == None:
            return False, "Invalid Character ID passed"

        if char_info['count'] - 1 < 0:
            return False, "Character already has no presets"

        if preset_name[0:3] != three_letter_initials[char_id]:
            preset_name = three_letter_initials[char_id] + '_' + preset_name

        idx = -1
        for i, preset in enumerate(char_info['presets']):
            if preset == preset_name:
                idx = i
                break

        if idx == -1:
            return False, "No Preset with this name exists"

        char_info['presets'][idx] = ""
        char_info['count'] -= 1
        pushEmptyToEnd(char_info['presets'])
        if save:
            return self.saveFile(), "OK"
        else:
            return True, "OK"

    def printPresets(self, char_id=None):
        dict = self.preset_dict
        for i, char in enumerate(dict):
            if char_id != None and dict[char]['char_id'] != char_id:
                continue
            print(char, end=':\n')
            for i, preset in enumerate(dict[char]['presets']):
                if preset == '':
                    break
                print("\t%-3d %-25s" % (i, preset))
            print()
        return

    def saveFile(self, path='./'):
        # path = r'F:\Steam\steamapps\common\TEKKEN 7\TekkenGame\Content\Binary\list'
        file = self.__filename
        if path == './':
            file = '%s_new.bin' % self.__filename.split('.')[0]
        return self.__writeFile(path, file)

    def __writeFile(self, path, file):
        with open("%s/%s" % (path, file), 'wb') as f:
            f.write(toBytes(self.paths_addr))
            f.write(toBytes(self.num_chars))
            # Fill bytes all the way, occupying character slots
            for _ in range(2601):
                f.write(toBytes(0))
            # Parent String
            f.write(b'customize_preset_table_cs_s3\0\0')
            zero_addr = f.tell() - 1
            # Character strings
            for char_name in self.preset_dict:
                self.preset_dict[char_name]['preset_offsets'] = []
                char_info = self.preset_dict[char_name]
                for preset in char_info['presets']:
                    if preset == '':
                        char_info['preset_offsets'].append(zero_addr)
                    else:
                        char_info['preset_offsets'].append(f.tell())
                        f.write(bytes(preset+'\0', 'ascii'))
            # Going back to write these offsets
            f.seek(0x10)
            for char_name in self.preset_dict:
                char_info = self.preset_dict[char_name]
                char_id: int = char_info['char_id'] - 256
                f.write(char_id.to_bytes(8, 'little', signed=True))
                for preset_offset in char_info['preset_offsets']:
                    f.write(toBytes(preset_offset))
        return True

    def restoreOriginal(self):
        self.preset_dict = original_preset_list
        return self.saveFile()


def main(char_id: int, preset_name: str, flag: str):
    obj = PresetList("./customize_preset_table_cs_s3.bin")

    if char_id == "restore":
        obj.restoreOriginal()
        print('Everything restored to original.')
        print('File created: "customize_preset_table_cs_s3_new.bin"')
        return

    char_id = int(char_id)

    if flag:
        fn = obj.removePreset
        label = "removed from"
    else:
        fn = obj.addPreset
        label = "added to"

    success, msg = fn(char_id, preset_name)

    if success:
        print('Preset "%s" successfully %s character # %d %s' %
              (preset_name, label, char_id, Char(char_id)))
    else:
        print("Failed! Reason: " + msg)

    return


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'restore':
        main("restore", None, None)
        exit(0)
    if len(sys.argv) < 3:
        print('Not enough arguments\nArgument details are as follow')
        print('1 - Character ID')
        print('  1.1 - Alternatively, Type "restore" to remove all presets and restore originals\n  E.g; python presets.py restore')
        print('2 - Preset Name')
        print(
            '3 - Flag to indicate that you want to delete a preset. Needs to be ANY value')
        print('Preset Name can be with or without prefix')
        print('For example, "kaz_tatoo_shirt" and "tatoo_shirt" are both correct')
        print('Prefix will be added automatically')
        exit(0)
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError:
        main(sys.argv[1], sys.argv[2], None)
