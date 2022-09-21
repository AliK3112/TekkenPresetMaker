import os


charIDs = {
    0: "Paul",
    1: "Law",
    2: "King",
    3: "Yoshimitsu",
    4: "Hwoarang",
    5: "Xiayou",
    6: "Jin",
    7: "Bryan",
    8: "Heihachi",
    9: "Kazuya",
    10: "Steve",
    11: "JACK7",
    12: "Asuka",
    13: "Devil Jin",
    14: "Feng",
    15: "Lili",
    16: "Dragunov",
    17: "Leo",
    18: "Lars",
    19: "Alisa",
    20: "Claudio",
    21: "Katarina",
    22: "Chloe",
    23: "Shaheen",
    24: "Josie",
    25: "Gigas",
    26: "Kazumi",
    27: "Devil Kazumi",
    28: "Nina",
    29: "Master Raven",
    30: "Lee",
    31: "Bob",
    32: "Akuma",
    33: "Kuma",
    34: "Panda",
    35: "Eddy",
    36: "Eliza",
    37: "Miguel",
    38: "Soldier",
    39: "Young Kazuya",
    40: "JACK4",
    41: "Young Heihachi",
    42: "Dummy",
    43: "Geese",
    44: "Noctis",
    45: "Anna",
    46: "Lei",
    47: "Marduk",
    48: "Armor King",
    49: "Julia",
    50: "Negan",
    51: "Zafina",
    52: "Ganryu",
    53: "Leroy",
    54: "Fahk",
    55: "Kuni",
    56: "Lidia",
    75: "NONE"
}

three_letter_initials = {
    0: "pau",
    1: "law",
    2: "kin",
    3: "yos",
    4: "hwo",
    5: "xia",
    6: "jin",
    7: "bry",
    8: "hei",
    9: "kaz",
    10: "ste",
    11: "jac",
    12: "ask",
    13: "dvj",
    14: "fen",
    15: "lil",
    16: "dra",
    17: "leo",
    18: "lar",
    19: "asa",
    20: "ita",
    21: "ltn",
    22: "dnc",
    23: "arb",
    24: "mut",
    25: "crz",
    26: "kzm",
    27: "bs7",
    28: "nin",
    29: "frv",
    30: "lee",
    31: "bob",
    32: "mrx",
    33: "kum",
    34: "pan",
    35: "edd",
    36: "elz",
    37: "mig",
    38: "zak",
    39: "ykz",
    40: "ja4",
    41: "yhe",
    42: "dek",
    43: "mry",
    44: "mrz",
    45: "ann",
    46: "lei",
    47: "mar",
    48: "aki",
    49: "jul",
    50: "nsa",
    51: "zaf",
    52: "gan",
    53: "nsb",
    54: "nsc",
    55: "knm",
    56: "nsd",
}

forbiddenChars = [27, 38, 39, 40, 41, 42, 75]


def pushEmptyToEnd(arr):
    n = len(arr)
    count = 0
    for i in range(n):
        if arr[i] != "":
            arr[count] = arr[i]
            count += 1
    while count < n:
        arr[count] = ""
        count += 1
    return arr


def Char(id: int) -> str:
    return charIDs.get(id, "none")


def toBytes(x: int, size=8):
    return x.to_bytes(size, 'little')


def parseLine(line: str, fileData: dict):
    if line[0] == '#':
        return
    values = line.split('=')
    fileData[values[0]] = values[1]
    if values[0] == 'character_ids':
        character_ids = values[1].split(',')
        fileData[values[0]] = []
        for id in character_ids:
            fileData[values[0]].append(int(id))
    return


def isTekken7Path(fullpath):
    for file in os.listdir(fullpath):
        if file == "TEKKEN 7.exe":
            return True
    return False


if __name__ == '__main__':
    fileData = {}
    filename = 'presets1.ini'
    try:
        with open(filename, 'r') as fd:
            lines = fd.readlines()
            lines = [line.rstrip() for line in lines]
    except:
        print('"%s" file not found. Make sure it is present in same directory' % filename)
        exit(1)

    for line in lines:
        parseLine(line, fileData)
    print(fileData['character_ids'])
