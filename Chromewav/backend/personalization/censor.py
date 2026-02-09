# This file takes in lyrics from lyrics.py and censors them
# what this file does:
    # 1. cleans the banned words
    # 2. cleans the lyrics
    # 3. censor banned words
    # 4. return lyrics with censors

# check for banned words in lyrics and censor them
def getCensoredLyrics(lines):
    
    # array of banned words that AI API won't take
    # Why are some of them so funny lol 
    banned_words = ["blood", "twerk", "making love", "voluptuous", "naughty", "wincest", "orgy", "no clothes", "au naturel", "no shirt", 
                    "decapitate", "bare", "nude", "barely dressed", "bra", "risque", "scantily clad", "cleavage", "stripped", "infested", 
                    "full frontal", "unclothed", "invisible clothes", "wearing nothing", "lingerie", "naked", "without clothes on", 
                    "negligee", "zero clothes", "gruesome", "fascist", "nazi", "prophet mohammed", "slave", "coon", "honkey", "cocaine"
                    "heroin", "meth", "crack", "kill", "belle delphine", "hitler", "jinping", "lolita", "president xi", "toture", "disturbing"
                    "farts", "fart", "poop", "infected", "warts", "shit", "brown pudding", "bunghole", "vomit", "seductive", "sperm", "sexy"
                    "sadist", "sensored", "censored", "silenced", "deepfake", "inappropriate", "waifu", "succubus", "slaughter", "surgery"
                    "reproduce", "crucified", "seductively", "explicit", "large bust", "wang", "teratoma", "intimate", "see through", "tryphophobia",
                    "bloodbath", "wound", "cronenberg", "khorne", "cannibal", "cannibalism", "visceral", "guts", "bloodshot", "gory", "killing",
                    "crucifixion", "vivisection", "massacre", "hemoglobin", "suicide", "arse", "labia", "ass", "mammeries", "badonlers", "bloody",
                    "minge", "big ass", "mommy milker", "booba", "nipple", "oppai", "booty", "organs", "bosom", "overies", "flesh", "breasts", 
                    "penis", "busty", "phallus", "clunge", "sexy female", "crotch", "skimpy", "dick", "thick", "bruises", "girth", "titty", 
                    "honkers", "vagina", "hooters", "veiny", "lnob", "ahegao", "pinup", "ballgag", "car crash", "playboy", "bimbo", "pleasure",
                    "pleasures", "bodily fluids", "boudoir", "rule34", "brothel", "seducing", "dominatrix", "corpse", "seductive", "fuck", "sensual",
                    "hardcore", "sexy", "hentai", "shag", "horny", "shibari", "incest", "smut", "jav", "succubus", "jerk off king at pic", "thot",
                    "kinbaku", "lefs spread", "sensuality", "belly button", "porn", "patriotic", "bleed", "excrement", "petite", "seduction", "mccurry",
                    "provocative", "sultry", "erected", "camisole", "tight white", "arrest", "see-through", "feces", "anus", "revealing clothing", 
                    "vein", "loli", "-edge", "boobs", "-backed", "tied up", "zedong", "bathing", "jail", "reticulum", "rear end", "sakimichan", 
                    "behind bars","shirtless", "sakimichan", "seductive", "sexi", "sexualiz", "sexual"]


    # clean banned words (just in case)
    banned_set = set(word.lower() for word in banned_words)

    censored_lines = []

    for line in lines:
        
        if line.strip() == " ":
            censored_lines.append(line)
            continue

        censored_words = []
        original_words = line.split()

        for word in original_words:
            cleaned_word = word.lower()
            
            for char in [".", "!", "?", "(", ")", ",", "-"]:
                cleaned_word = cleaned_word.replace(char, "")

            # check for banned words
            if cleaned_word in banned_set:
                censored_words.append("***")
            else:
                censored_words.append(cleaned_word)

        # rebuild lyric lines
        censored_line = " ".join(censored_words)
        censored_lines.append(censored_line)
    print("\ncensored lines: ", censored_lines)
    return censored_lines