# this file contains functions that use the vader library 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# this function returns the 10 most emotional lines
def getKeyLyricLines(lyrics, threshold=0.2):

    important_lines = []

    # step 1: change the lyrics into a list of lines
    if isinstance(lyrics, dict):
        all_lines = []

        for _, lines in lyrics.items():

            for item in lines:

                split_lines = str(item).split("\n")
                for line in split_lines:
                    cleaned = line.strip()
                    if cleaned:
                        all_lines.append(cleaned)

    # step 2: run vader on each line
    for line in all_lines:
        scores = analyzer.polarity_scores(line)
        emotional_strength = abs(scores["compound"])

        if emotional_strength > threshold:
            important_lines.append((line, emotional_strength))

    # step 3: sort by emotional strength 
    important_lines.sort(key = lambda x: x[1], reverse = True)

    # step 4: remove any instances of repeated lyrics and return them
    top_lines = []
    seen = set()

    for line, score in important_lines:
        normalized = line.lower().strip()

        if normalized not in seen:
            seen.add(normalized)
            top_lines.append((line, score))

        if len(top_lines) == 10:
            break

    return [line for line, _ in top_lines]

# this function returns a timeline of emotions a song
def getEmotionalTimeline(lyrics):
    timeline = []

    if not isinstance(lyrics, dict):
        return timeline

    for _, lines in lyrics.items():

        # change the text into one text block
        section_text = ""
        if isinstance(lines, list):
            for item in lines:
                section_text += " " + str(item)
        else:
            section_text = str(lines)

        score = analyzer.polarity_scores(section_text)["compound"]

        if score > 0.3:
            mood = "hopeful / joyful"
        elif score < -0.3:
            mood = "sad / intense"
        else:
            mood = "neutral / reflective"

        timeline.append({"score": score, "mood": mood})

    return timeline

# summarize the timeline so it's easy for the prompt
def getSummarizedTimeline(timeline):
    moods = [item["mood"] for item in timeline]
    return " + ".join(moods)

# this function returns a visual tag based on the avg score
# change to different tags after testing
def getVisualTags(lyrics):
    total_score = 0
    section_count = 0

    for _, lines in lyrics.items():

        section_text = ""
        if isinstance(lines, list):
            for item in lines:
                section_text += " " + str(item)
        else:
            section_text = str(lines)

        score = analyzer.polarity_scores(section_text)["compound"]
        print("Section score: ",score)

        total_score += score
        section_count += 1

    if section_count == 0:
        return "neutral tones, balanced lighting"

    avg_score = total_score/section_count
    print("average song score: ", avg_score)

    if avg_score > 0.25: #if the song is high net positive return this visual tag
        print("Visual tag of the song: warm lighting")
        return "light tones"
    elif avg_score < -0.25: #if the song is low net negative return this visual tag
        print("Visual tag of the song: dark tones")
        return "dark tones"
    else:
        print("Visual tag of the song: muted tones")
        return "muted tones"
