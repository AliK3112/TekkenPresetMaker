from time import sleep
from presets import PresetList
import msvcrt
from os import system, name
from utils import Char, charIDs

# define our clear function


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def main():
    return


def inputCharID():
    print('Character IDs for reference:')
    for i, id in enumerate(charIDs):
        if id == 75:
            break
        print("%-3d %-20s\t" % (id, charIDs[id]), end='')
        if (id + 1) % 4 == 0:
            print()
    print()
    while True:
        try:
            char_id = int(input('Enter character ID: '))
            if char_id not in charIDs:
                print("Invalid ID. Please Enter Valid Char ID")
            else:
                break
        except:
            print("Invalid ID. Please Enter Valid Char ID")
            return -1
    return char_id


def inputPresetName():
    print('NOTE: Character Prefix "kaz" "hei" will automatically be added if not preset:')
    return input('Enter Preset Name: ')


if __name__ == "__main__":
    try:
        presetlist = PresetList("./customize_preset_table_cs_s3.bin")
    except:
        print('Failed to Open File "customize_preset_table_cs_s3.bin"\nProgram Exiting')
        sleep(3)
        exit(1)
    while True:
        clear()
        print('Make sure binary file "customize_preset_table_cs_s3.bin" is in this same folder')
        print('What you want to do?')
        print('Press 1 - Show all presets?')
        print('Press 2 - Show preset of a certain character?')
        print('Press 3 - Add new preset to a certain character?')
        print('Press 4 - Remove a preset from a certain character?')
        print('Press 5 - Remove everything and restore original')
        print('Press 6 - Exit')
        inp = msvcrt.getch().decode()
        clear()
        #########################################################################
        if inp == '1':
            print("VIEW ALL CHARACTER PRESETS")
            presetlist.printPresets()
            print('Press any key to go back...')
            msvcrt.getch()
        #########################################################################
        elif inp == '2':
            char_id = inputCharID()
            if char_id == -1:
                continue
            print("VIEW SPECIFIC CHARACTER PRESETS")
            presetlist.printPresets(char_id)
            print('Press any key to go back...')
            msvcrt.getch()
        #########################################################################
        elif inp == '3':
            char_id = inputCharID()
            if char_id == -1:
                continue
            print("ADD CHARACTER PRESET")
            preset_name = inputPresetName()
            if (preset_name == ''):
                continue
            success, msg = presetlist.addPreset(char_id, preset_name)
            if success:
                print('Preset "%s" successfully added to character # %d %s' %
                      (preset_name, char_id, Char(char_id)))
            else:
                print("Failed! Reason: " + msg)
            print()
            presetlist.printPresets(char_id)
            print('Press any key to go back...')
            msvcrt.getch()
        #########################################################################
        elif inp == '4':
            char_id = inputCharID()
            if char_id == -1:
                continue
            print("REMOVE CHARACTER PRESET")
            preset_name = inputPresetName()
            if (preset_name == ''):
                continue
            success, msg = presetlist.removePreset(char_id, preset_name)
            if success:
                print('Preset "%s" successfully removed from character # %d %s' %
                      (preset_name, char_id, Char(char_id)))
            else:
                print("Failed! Reason: " + msg)
            print()
            presetlist.printPresets(char_id)
            print('Press any key to go back...')
            msvcrt.getch()
        #########################################################################
        elif inp == '5':
            if presetlist.restoreOriginal():
                print('Everything restored to original.')
                print('File created: "customize_preset_table_cs_s3_new.bin"')
            else:
                print('Something wrong happened')
            print('Press any key to go back...')
            msvcrt.getch()
        #########################################################################
        elif inp == '6':
            break
        #########################################################################
