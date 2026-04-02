import json
from backend.errors import appError
import os
# class to store the key and associated color palatte
class keyToColor:
    def __init__(self, key, mode, colors):
        self.key = key
        self.mode = mode
        self.colors = colors


# builds the path relative to this file, not the working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PALETTE_PATH = os.path.join(BASE_DIR, "key_palettes.json")

try:
    with open(PALETTE_PATH) as f:
        KEY_COLOR_PALETTES = json.load(f)

    if not KEY_COLOR_PALETTES:
        raise appError("Color palettes file is empty", 500)

except FileNotFoundError:
    raise appError(f"Color palettes file not found at: {PALETTE_PATH}", 500)
except json.JSONDecodeError:
    raise appError("Color palettes file is not valid JSON", 500)



# enharmonic equivalents seperated by mode
THEORETICAL_KEY_MAP = {
    "major": {
        "G#": "Ab",
        "D#": "Eb",
        "A#": "Bb",
        "E#": "F",
        "B#": "C#",
        "Cb": "B",
        "Fb": "E",
        "F#": "Gb",
    },
    "minor": {
        "E#": "F",
        "A#": "Bb",
        "G#": "Ab",
        "Ab": "G#",
        "Db": "C#",
        "D#": "Eb",
    },
}

# return the correct color palette
def get_palette(root:str, mode: str) -> list[str]:

    # combine to look for the palette
    key = f"{root} {mode}"
    # raise the error if no palette is found
    if key not in KEY_COLOR_PALETTES:
        raise appError(f"No palette for: {key}", 404)
    # return the found color palette
    return KEY_COLOR_PALETTES[key]


# if the song is in a rare/theoretical key return the enharmonic equivalent
def normalizeTheoreticalKeys(key: str, mode: str) -> str:
    return THEORETICAL_KEY_MAP.get(mode, {}).get(key, key)

# driver of finding a color palette
def getColors (key: str, mode: str) -> list[str] | None:
    print(f"finding color from: {key}, {mode}")

    # normalize theoretical key if needed
    key = normalizeTheoreticalKeys(key, mode)
    lookup = f"{key} {mode}"

    # normalize the key 
    key_id = (key.lower(), mode.lower())
    print("Key id for the song: ", key_id)

    # lookup color palette
    if lookup in KEY_COLOR_PALETTES:
        return KEY_COLOR_PALETTES[lookup]
    
    # if the key can't be found return none
    print(f"No palette found for: {key} {mode}")
    return None
