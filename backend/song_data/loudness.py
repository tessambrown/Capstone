# For local deployment
from backend.errors import appError

# For Render deployment
# from errors import appError

# input the loudness and return colors, louder = more colors
def getLoudness(loudness):

    if loudness is None:
        raise appError("Failed to find loudness", 404)

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