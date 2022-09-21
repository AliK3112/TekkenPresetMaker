# TEKKEN 7 Preset Maker
A tool that adds a preset entry into the preset costumes binary file `tkdata\list\customize_preset_table_cs_s3.bin`

## How to build project
- Clone or download this folder.
- Run build.bat
- Go to `./dist/TekkenPresetMaker/`
- Run the `TekkenPresetMaker.exe`

## How to run project from source code
- Clone or download this folder.
- Run command: python presets.py <char-id> <preset-name> <deletion-flag>
- Go to `./dist/TekkenPresetMaker/`
- Run the `TekkenPresetMaker.exe`

## How to run release build
#### One Time, Pre-Requisites
1. Use [Tekken 7 All Extracting Tool](https://github.com/a5tronomy/Tekken-7-Extracting-Packing-Tools) to extract all data from `tkdata.bin`. We need the decoded raw file contents so we can modify & load them.

2. In your `..TEKKEN 7/TekkenGame/Content/Binary` folder, rename `tkdata.bin` to `tkdata.bin-x` so the game doesn't find and load this.

3. Place the extracted out contents of `tkdata.bin` in this folder. We want the game to load all the stuff from here.
   - Your initial setup is complete now.
   - Your `..TEKKEN 7/TekkenGame/Content/Binary` folder should look like this:
   
   ![Binary folder](https://user-images.githubusercontent.com/83224003/190898256-99b0216b-d477-4e8f-ba9f-c0d038d6f6b7.png)

#### OPTION 1: USE CLI
1. Download a character mod that supports preset maker and paste it's contents in "~mods" folder

2. Run `TekkenPresetMaker.exe`. Follow on-screen commands to add preset to your given character.
   - Mod creators should provide you the name for the preset.
   - It's important that preset name matches correctly with uasset files, otherwise, your game will crash.
   - If you install a PAK file, your game will work, but if you just create a new entry in the preset list, without Adding the "PAK" file, you're guaranteed a crash.

3. Tool will make a new `customize_preset_table_cs_s3.bin` file with the "new" postfix (`customize_preset_table_cs_s3_new.bin`).
   - Paste this in `..TEKKEN 7/TekkenGame/Content/list` folder, where original preset binary file was located.
   - Rename the old one to `customize_preset_table_cs_s3_org.bin` and save it somewhere else (You're making a back-up).
   - Rename the new one to `customize_preset_table_cs_s3.bin` , now the game will load this one.\
   
#### OPTION 2: USE SCRIPTS
1. Put data in `presets.ini` as described below.
2. Run `addPresets.exe` or `removePresets.exe` depending on your need.
3. Follow Step 3 from OPTION 1.

## Putting data in 'presets.ini':
1. path: Your tekken 7 path. If not present, current working directory will be selected as path
2. preset_name: Self explanatory.
    Preset Name can be with or without prefix.
    If adding presets for more than 1 Character, prefix is NOT recommended.
    E.g, "kaz_tatoo_shirt" and "tatoo_shirt" are both correct
3. character_ids: Character IDs, comma seperated
    E.g, character_ids=6,8,9,13
    Character IDs are present in the text file for reference

`presets.ini` should look like this:
![presets.ini](https://user-images.githubusercontent.com/83224003/191601245-175dc8f8-b9cf-411c-8ddf-6fd6e1b0081a.png)

