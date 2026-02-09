# this file controls personlization for the backend files

# import files for personlization 
from backend.api.lyrics import getLyrics
from backend.personalization.vader import getKeyLyricLines, getEmotionalTimeline, getSummarizedTimeline, getVisualTags
from backend.personalization.censor import getCensoredLyrics
from backend.personalization.lyric_selection import getSelection
from backend.personalization.helper_functions import checkChar, getRatio, formatColor 
from backend.personalization.canvas_size import getSize
from backend.personalization.color_palette import getColor
from backend.personalization.emotion import getEmotions
from backend.api.spotify import getTrackID, getTrackAnalysis, getAudioFeatures
from backend.personalization.loudness import getLoudness
from backend.personalization.key import getColors
from backend.personalization.color_contrast import getColorContrast, getPaletteContrast
from backend.generation.prompt_builder import getTempoTier, getRatioModifiers, getChaosBehavior

# a class that stores all of the personlization variables
class songPersonlizations():
    def __init__(self):
        self.artist = None
        self.song = None
        self.lyrics = None
        self.key_lyrics = None
        self.timeline = None
        self.summarized_timeline = None
        self.visual_tag = None
        self.censored = None
        self.selected = None
        self.selected_censored = None
        self.canvas_width = None
        self.canvas_height = None 
        self.ratio = None
        self.color_name = None
        self.color = None
        self.format_color = None
        self.emotion = None
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
        self.tempo_tier = None
        self.ratio_modifier = None
        self.tempo_level = None
        self.chaos = None
    
    # validation functions
    def has_basic_info(self):
        return bool(self.artist and self.song)
    
    def has_lyrics(self):
        return isinstance(self.lyrics, dict) and len(self.lyrics) > 0
    
    def is_complete(self):
        return all([
            self.artist,
            self.song,
            self.lyrics,
            self.ratio,
            self.contrast,
            self.palette,
            self.tempo_tier,
            self.ratio_modifier,
            self.canvas_width,
            self.canvas_height,
            self.chaos
        ])
    
    def __repr__(self):
        return (
            f"SongPersonlizations(\n"
            f"  Artist: {self.artist}\n"
            f"  Song: {self.song}\n"
            f"  Sections: {len(self.lyrics) if self.lyrics else 0}\n"
            f"  Canvas: {self.canvas_width}, {self.canvas_height}\n"
            f"  Ratio: {self.ratio}\n"   
        )

# initalize choices for canvas size, color, and emotions to change later!!!!!

def personlizations():
    # intilize an empty songPersonlization object 
    new_song = songPersonlizations()

    print("\nrunning in personlization_state.py\n")

    while True:
        name = input("Enter artist name: ")
        if name == "":
            continue

        song = input("Enter song name: ")
        if song == "":
            continue

        # get the lyrics for the song sortted in sections
        lyrics = getLyrics(name, song)

        if lyrics is None:
            print("\nSong or artist not found. Please try again.\n")
            continue
        
        print("\nSong found processing lyrics\n")
        break
    
    # add artist name to object 
    new_song.artist = name
    
    # add song to object
    new_song.song = song

    # add lyrics to the object
    new_song.lyrics = lyrics
    # print("\nLyrics: ", new_song.lyrics)

    # new_song.key_lyrics = getKeyLyricLines(new_song.lyrics)

    new_song.id = getTrackID(new_song.song, new_song.artist)
    print("Track ID: ", new_song.id)

    new_song.track_analysis = getTrackAnalysis(new_song.id)

    # sort through and return specfic audio features
    features = getAudioFeatures(new_song.track_analysis)
    new_song.key = features.get("key")
    new_song.mode = features.get("mode")
    new_song.tempo = features.get("tempo")
    new_song.energy = features.get("energy")
    new_song.loudness = features.get("loudness")
    print("Key of the song: ", new_song.key)
    print("Mode of the song: ", new_song.mode)
    print("Loudness of the song: ", new_song.loudness)

    # input loudness of the song return num colors
    new_song.num_colors = getLoudness(new_song.loudness)
    print("Number of colors: ", new_song.num_colors)

    # get the color palette associated with the key+mode of the song
    new_song.color = getColors(new_song.key, new_song.mode)
    print("Colors for the song: ", new_song.color)

    # get colors that match contrast levels
    new_song.contrast = getColorContrast(new_song.energy)
    print("Color contrast based on the song: ", new_song.contrast)


    # palette based on the color contrast 
    new_song.palette = getPaletteContrast(new_song.color, new_song.contrast, new_song.num_colors)
    print("Color palette based on color contrast: ", new_song.palette)

    # get tempo tier for prompt
    tempo_level, tempo_tier = getTempoTier(new_song.tempo)
    new_song.tempo_level = tempo_level
    new_song.tempo_tier = tempo_tier
    print("Tempo tier from the song: ", new_song.tempo_tier, "And tempo level: ", new_song.tempo_level)

    new_song.chaos = getChaosBehavior(new_song.tempo_level)
    print("Chaos behavior of the song: ", new_song.chaos)
    
    # prompt the user to select a canvas size and return the canvas size in px 
    width, height = getSize()
    new_song.canvas_width = width
    new_song.canvas_height = height

    # translate the canvas size into a ratio for prompt 
    new_song.ratio = getRatio(new_song.canvas_width, new_song.canvas_height)

    new_song.ratio_modifier = getRatioModifiers(new_song.ratio)

    # return all of the personlizations for the prompt builder
    # validate that personlization is complete 
    if not new_song.is_complete():
        print("Parts of new song object: ", new_song)
        return None
    else:
        print("Personlizations complete")
        return new_song