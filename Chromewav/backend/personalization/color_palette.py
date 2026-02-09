# this file prompts the user to select a color palette and returns 5 hex codes

class colorPalette:
    def __init__(self, name, colors):
        self.colors = colors
        self.name = name


# change when we choose color palettes
palette_1 = colorPalette("Palette 1", ["#0A3323", "#839958", "#F7F4D5", "#D3968C", "#105666"])
palette_2 = colorPalette("Palette 2", ["#45151B", "#EA9DAE", "#FBDE9C", "#F99256", "#C74E51"])
palette_3 = colorPalette("Palette 3", ["#6C0820", "#F2AEBC", "#F2DCDB", "#5A86CB", "#3D5D91"])
palette_4 = colorPalette("Palette 4", ["#475B35", "#F5F9E5", "#E19184", "#C63E4E", "#620607"])
palette_5 = colorPalette("Palette 5", ["#4C3D19", "#354024", "#889063", "#CFBB99", "#E5D7C4"])

color_palettes = []
color_palettes.append(palette_1)
color_palettes.append(palette_2)
color_palettes.append(palette_3)
color_palettes.append(palette_4)
color_palettes.append(palette_5)

def getColor ():

    print("Color palettes to choose from:")
    i = 1
    for colors in color_palettes:
        print(f"{i}. {colors.name}")
        i += 1

    choice = int(input("choose a color palette: "))
    selected_color = color_palettes[choice - 1]
    return selected_color.name, selected_color.colors
