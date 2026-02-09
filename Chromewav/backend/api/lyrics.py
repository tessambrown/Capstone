# lyricgenius api file
# what this file does:
    # 1. calls lyric genius api
    # 2. passes token through geniusClient
    # 3. checks that the artist exists
    # 4. sort the lyrics into sections
    # 5. return section
   
import lyricsgenius
genius = lyricsgenius.Genius("8pJMW8vLXb-goqxfDF9tu2kWGiAnmEDLqbiEd8cDM-tO4Q0-N1Hoq7ex9WOCwe07")

def getLyrics(name, song):

    artist = genius.search_artist(name, max_songs=0)
    genius.verbose = False
    genius.remove_section_headers = False
    song = genius.search_song(song, artist.name) #use user input and artist name to retrive song lyrics

    lyrics_lines = song.lyrics.split("\n")

    sections = {} # stores arrays for each section
    current_section = None # tracks which section you're in

    # Iterate through lines in song.lyrics to find and sort by section headers 
    for line in lyrics_lines:
        # detect section headers
        if line.startswith("[") and line.endswith("]"):
            # remove brackets by replacing them
            header = line.replace("[", "").replace("]", "")

            current_section = header

            if current_section not in sections:
                sections[current_section] = []
            
            continue

        # store lyric lines (including the blank lines)
        if current_section is not None:
            sections[current_section].append(line)

    return sections