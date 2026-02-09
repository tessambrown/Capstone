# this file prompts the user to select an emotion and returns selected emotion

class emotion ():
    def __init__(self, name):
        self.name = name 

# change when we decide what emotions we want to use
emotion_1 = emotion("Happy")
emotion_2 = emotion("Sad")
emotion_3 = emotion("Energetic")
emotion_4 = emotion("Angry")
emotion_5 = emotion("Chill")

emotions = []
emotions.append(emotion_1)
emotions.append(emotion_2)
emotions.append(emotion_3)
emotions.append(emotion_4)
emotions.append(emotion_5)

def getEmotions():

    print("Emotions to choose from:")
    i = 1
    for emotion in emotions:
        print(f"{i}. {emotion.name}")
        i += 1
    
    choice = int(input("choose an emotion you feel when listening to the song: "))
    selected_emotion = emotions[choice - 1]
    return selected_emotion.name