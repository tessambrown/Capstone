# This file returns the number of colors based on loudness of the song



def getLoudness(loudness):

    colors = 0

    if loudness >= -10:
        colors = 5
        return colors   
    elif loudness <= -30:
        colors = 3
        return colors
    else:
        colors = 4
        return colors 