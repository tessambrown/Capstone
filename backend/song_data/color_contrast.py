from backend.song_data.helper_functions import contrastRatio, randColor
from itertools import combinations
from backend.errors import appError

# The higher the energy the higher the contrast level
def getColorContrast(energy):
    if energy is None:
        raise appError("Song energy was found", 404)

    if energy >= 66:
        return "high"
    elif energy <=33:
        return "low"
    else:
        return "medium" 


def getPaletteContrast(palette, contrast_level, num_colors):
    # validate inputs
    if not palette:
        raise appError("Color palette is empty or missing", 500)

    if not isinstance(palette, list):
        raise appError("Color palette must be a list", 500) 

    if contrast_level not in ("high", "medium", "low"):
        raise appError(f"Invalid contrast level: {contrast_level}", 400)
    
    if not isinstance(num_colors, int) or num_colors <= 0:
        raise appError("Number of colors must be a positive integer", 400)

    # set the color palette (based on key) to selected_colors
    selected_colors = palette

    high = []
    medium = []
    low = []
 
    for c1, c2 in combinations(selected_colors, 2):
        # calculates the contrast ratio between two colors
        ratio = contrastRatio(c1, c2)

        # validate ratio
        if ratio is None:
            raise appError(f"contrastRatio() returned None for colors {c1}, {c2}", 500)

        # sort the colors into the correct array
        if ratio >= 7:
            high.append(c1)
            high.append(c2)
        elif ratio >= 4.5:
            medium.append(c1)
            medium.append(c2)
        else:
            low.append(c1)
            low.append(c2)

    # remove any duplicates
    high = list(set(high))
    medium = list(set(medium))
    low = list(set(low))

    # if there isn't enough colors in the color palette this is plan b
    if contrast_level == "high":
        priority = [high, medium, low]
    elif contrast_level == "medium":
        priority = [medium, high, low]
    else:
        priority = [low, medium, high]

    selected = []

    # loops through groups first then moves on by priority
    for group in priority:
        # loop through the color inside the group
        for color in group:
            # check to make sure the color isn't in selected
            if color not in selected:
                # if it's not a duplicate add it to the array
                selected.append(color)
            # break out of the loop if there is enough colors in the group
            if len(selected) >= num_colors:
                break
        # if the reconstructed palette has enough colors break out of the loop
        if len(selected) >= num_colors:
            break 

    if not selected:
        raise appError("No colors could be selected from the palette", 500)
    
    # if there's more colors than num colors randomly remove colors
    if len(selected) > num_colors:
        selected = randColor(selected, num_colors)

    # final sanity check
    if not selected or len(selected) == 0:
        raise appError("Palette contrast selection returned an empty result", 500)
    
    # return the color palette
    return selected

