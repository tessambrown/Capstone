# This file takes in the color palette and finds contrast levels
from backend.personalization.helper_functions import contrastRatio, randColor
from itertools import combinations

def getColorContrast(energy):
    if energy >= 66:
        return "high"
    elif energy <=33:
        return "low"
    else:
        return "medium" 

def getPaletteContrast(palette, contrast_level, num_colors):
    selected_colors = palette

    high = []
    medium = []
    low = []

    for c1, c2 in combinations(selected_colors, 2):
        ratio = contrastRatio(c1, c2)

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

    for group in priority:
        for color in group:
            if color not in selected:
                selected.append(color)
            if len(selected) >= num_colors:
                break
        if len(selected) >= num_colors:
            break 

    if len(selected) > num_colors:
        selected = randColor(selected, num_colors)
    
    return selected

    # if contrast_level == "high":
    #     high_colors = randColor(high, num_colors)
    #     return high_colors
    # elif contrast_level == "medium":
    #     medium_colors = randColor(medium, num_colors)
    #     return medium_colors
    # elif contrast_level == "low":
    #     low_colors = randColor(low, num_colors)
    #     return low_colors

