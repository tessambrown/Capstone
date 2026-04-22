# For local deployment
from backend.api.lyrics import getLyrics
from backend.song_data.helper_functions import getRatio
from backend.song_data.canvas_size import getSize
from backend.api.spotify import getTrackID, getTrackAnalysis, getAudioFeatures
from backend.song_data.loudness import getLoudness
from backend.song_data.key import getColors
from backend.song_data.color_contrast import getColorContrast, getPaletteContrast
from backend.errors import appError

# For Render deployment
# from api.lyrics import getLyrics
# from song_data.helper_functions import getRatio
# from song_data.canvas_size import getSize
# from api.spotify import getTrackID, getTrackAnalysis, getAudioFeatures
# from song_data.loudness import getLoudness
# from song_data.key import getColors
# from song_data.color_contrast import getColorContrast, getPaletteContrast
# from errors import appError

# a class that stores all of the personlization variables
class songData():
    def __init__(self):
        self.artist = None
        self.song = None
        self.lyrics = None
        self.canvas_width = None
        self.canvas_height = None 
        self.ratio = None
        self.color = None
        self.id = None 
        self.track_analysis = None
        self.audio_features = None
        self.key = None
        self.mode = None
        self.tempo = None
        self.energy = None
        self.loudness = None
        self.num_colors = None
        self.contrast = None
        self.palette = None
        self.happiness = None
    
    def is_complete(self):
        return all([
            self.artist,
            self.song,
            self.lyrics,
            self.ratio,
            self.contrast,
            self.palette,
            self.tempo,
            self.canvas_width,
            self.canvas_height,
            self.mode,
            self.happiness
        ])
    
    def __repr__(self):
        return (
            f"SongPersonlizations(\n"
            f"  Artist: {self.artist}\n"
            f"  Song: {self.song}\n"
            f"  Sections: {len(self.lyrics)}\n"
            f"  Canvas: {self.canvas_width}, {self.canvas_height}\n"
            f"  Ratio: {self.ratio}\n" 
            f"  Contrast: {self.contrast}\n"
            f"  Palette: {self.palette}\n"
        )


# finds data based on inputted song 
def songMetadata(name, song, canvas_choice):
    # inputs validated in main.py

    # intilize an empty songPersonlization object 
    new_song = songData()

    try:
        # get the lyrics for the song sorted in sections
        result = getLyrics(name, song)

        # if getLyrics needs confirmation, bubble it up
        if isinstance(result, dict) and result.get("needs_confirmation"):
            return result
        
        lyrics, artist, song_title = result

        # if there isn't any lyrics set to an empty string
        if lyrics is None:
            lyrics = "No lyrics found"

        # add artist name to object 
        new_song.artist = artist
        
        # add song to object
        new_song.song = song_title

        # add the lyrics to the object 
        new_song.lyrics = lyrics

        # get the track id for the song from the Spotify API
        new_song.id = getTrackID(new_song.song, new_song.artist)
        print("ID from inputted song:", new_song.id);

        # get the metadata for the song
        new_song.track_analysis = getTrackAnalysis(new_song.id)

        # sort through and return specfic audio features
        features = getAudioFeatures(new_song.track_analysis)
        print("Features:", features)

        # set the song's features from getAudioFeatures() to the corresponding object
        new_song.key = features.get("key")
        new_song.mode = features.get("mode")
        new_song.tempo = features.get("tempo")
        new_song.energy = features.get("energy")
        new_song.loudness = features.get("loudness")
        new_song.happiness = features.get("happiness")
        

        # input loudness of the song return num colors
        new_song.num_colors = getLoudness(new_song.loudness)

        # get the color palette associated with the key + mode of the song
        new_song.color = getColors(new_song.key, new_song.mode)

        # get colors that match contrast levels
        new_song.contrast = getColorContrast(new_song.energy)

        # palette based on the color contrast, number of colors, and the song's color palette 
        new_song.palette = getPaletteContrast(new_song.color, new_song.contrast, new_song.num_colors)

        # input user's choice and return the width and hight of the canavs
        width, height = getSize(canvas_choice)
        new_song.canvas_width = width
        new_song.canvas_height = height

        # translate the canvas size into an aspect ratio
        new_song.ratio = getRatio(new_song.canvas_width, new_song.canvas_height)

        # make sure everything is complete
        if not new_song.is_complete():
            raise appError("Song data is incomplete", 500)
        
        return new_song
    except appError:
        raise
    except Exception as e:
        print(e)
        raise appError("Failed to process song metadata", 500)