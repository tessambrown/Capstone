# this code prompts the user to choose a canvas size and returns the canvas size

# class to store canvas info
class Canvas:
    def __init__(self, name, width, height):
        self.name = name

        # in px 
        self.width = width
        self.height = height


insta_story = Canvas("Insta Story", 1080, 1920)
insta_post = Canvas("Insta Post", 1080, 1080)
flyer = Canvas("Flyer", 2550, 3300) # 8.5x11
poster = Canvas("Poster", 3300, 5100) # 11x17

canvas_sizes = []
canvas_sizes.append(insta_story)
canvas_sizes.append(insta_post)
canvas_sizes.append(flyer)
canvas_sizes.append(poster)



def getSize():

    # print the choices for canvas size
    # change into a button in the final code 
    print("Canvas types to choose from: ")

    i = 1
    for sizes in canvas_sizes:
        print(f"{i}. {sizes.name}")
        i += 1
    
    choice = int(input("choose a canvas type: "))
    selected_canvas = canvas_sizes[choice-1]
    return selected_canvas.width, selected_canvas.height