
import lyricsgenius
import difflib
from dotenv import load_dotenv
import os
load_dotenv()

# For local deployment
# from backend.errors import appError

# For Render deployment
from errors import appError

# set the api key for the lyric genius API
api_key = os.getenv("LYRIC_KEY")
genius = lyricsgenius.Genius(api_key)

# helper function to return the similarity of two things
def similarity(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

# normalizes the artist string input
def normalizeArtists(artists):
    normalized = artists.lower()

    # a list of separators that the user could input
    separators = [
        " feat. ",
        " feat ",
        " ft. ",
        " ft ",
        " featuring ",
        " and ",
        " & ",
        " x ",
        " + "
    ]

    # replace any seperator in artist input with a comma
    for sep in separators:
        normalized = normalized.replace(sep, ",")

    # split the normalized string on commas
    artist_list = normalized.split(",")

    # clean any whitespace left over and remove empty entries
    return [artist.strip().title() for artist in artist_list if artist.strip()]

# find the best song match for user input
def findBestMatch(hits, song_title, artists):
    # initilize best_score and best_song
    best_score = 0
    best_song = None

    # take the array of hits from getLyrics()
    for hit in hits:
        result = hit["result"]

        # get the title and primary artist for the hit
        genius_title = result["title"]
        genius_artist = result["primary_artist"]["name"]

        # score the song title
        title_score = similarity(song_title, genius_title)

        # score the artists name
        artist_score = max((similarity(artist, genius_artist) for artist in artists), default=0)

        # song title matters more than the artist
        total_score = (title_score * 0.7) * (artist_score * 0.3)

        # if the song title contains "live" or "remix" reduce the total score
        if "live" in genius_title.lower():
            total_score -= 0.1
        if "remix" in genius_title.lower():
            total_score -= 0.1

        # if the totall score is better assign the best_song to the result in hits
        if total_score > best_score:
            best_score = total_score
            best_song = result

    # return the best score and the best song
    return best_score, best_song

# organize the lyrics into sections 
def organizeSections(lyrics):
    # split the lyrics at "\n"
    lyrics_lines = lyrics.split("\n")

    sections = {}
    current_section = None

    # iterate through the lyrics
    for line in lyrics_lines:
            
            # when it gets to "[" -> "[section]" start of a new section
            if line.startswith("[") and "]" in line:

                # assgin the new section to the header of a section of lyrics
                header = line.replace("[", "").replace("]", "")
                current_section = header

                if current_section not in sections:
                    sections[current_section] = []

                continue
            
            # if it's not the header of a section it's lyrics and add lyrics to the current_section object
            if current_section is not None:
                sections[current_section].append(line)
    
    # once the loop is done return the section
    return sections

# get the lyrics for the inputted song
# this function drives all of the other functions
def getLyrics(artists, song_title):

    # turns off status messages
    genius.verbose = False

    # don't remove the section headers 
    genius.remove_section_headers = False

    # normalized the artist input
    artists = normalizeArtists(artists)


    # try to search for each artist
    for artist_name in artists:
        print(f"Searching for: {song_title} by {artist_name}")

        # combine the artist and the song title into one string
        search_query = f"{song_title} {artist_name}"

        # returns the search result from the lyric genius API
        try:
            search_results = genius.search(search_query)
        except Exception as e:
            print(f"Search failed for {artist_name}: {e}")
            continue

        if search_results == {'hits': []}:
            raise appError("Cannot find the song from the user input", 400)

        # if the API returns something unexpected
        if not isinstance(search_results, dict):
            continue
        # top hits from the search results
        hits = search_results.get("hits", [])

        # if there isn't any hits try the next artist
        if not hits:
            continue

        # find the best match of the hits
        best_score, best_song = findBestMatch(hits, song_title, artists)
        
        # if the song has a low confidence rate ask the user if the response is correct
        if best_song and best_score < 0.1:
            potential_title = best_song["title"]
            potential_artist = best_song["primary_artist"]["name"]

            print(f"needs user confirmation: {potential_title} by {potential_artist}")

            # send to main.py that confirmation is needed
            return {
                "needs_confirmation": True,
                "potential_title": potential_title,
                "potential_artist": potential_artist
            }

        # if the top hit is close to the inputted value
        if best_song and best_score > 0.1:
            suggested_title = best_song["title"]
            suggested_artist = best_song["primary_artist"]["name"]

            print(f"Best match: {suggested_title} by {suggested_artist}")
            print(f"Match confidence: {round(best_score,2)}")

            # search for the specfic song and get its lyrics
            song = genius.search_song(suggested_title, suggested_artist)

            if song is None:
                raise appError("Cannot find the song", 500)
            
            # organize the lyrics into sections
            sections = organizeSections(song.lyrics)
            return sections, suggested_artist, suggested_title

    # if none of the artists worked 
    return None, None, None