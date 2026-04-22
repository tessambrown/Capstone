# For local deployment
from backend.errors import appError

# For Render deployment
# from errors import appError

# class to store canvas info
class Canvas:
    def __init__(self, name, width, height):
        self.name = name

        # in px 
        self.width = width
        self.height = height

# add each canvas size info to a Canvas class
phone_screen = Canvas("Phone Screen", 1290, 2796)
phone = Canvas("Phone", 1080, 1350)
poster = Canvas("Poster", 2550, 3300) # 8.5x11

# add each canvas size to the array
canvas_sizes = []
canvas_sizes.append(phone_screen)
canvas_sizes.append(phone)
canvas_sizes.append(poster)

# take user choice and return it as the height and width
def getSize(user_choice):
    print("User choice inside getSize():", user_choice)
    try:
        if user_choice == "phone_screen":
            phone_screen = canvas_sizes[0]
            return phone_screen.width, phone_screen.height
        elif user_choice == "phone":
            phone = canvas_sizes[1]
            return phone.width, phone.height
        elif user_choice == "poster":
            poster = canvas_sizes[2]
            return poster.width, poster.height
        else:
            return ("Invalid canvas selection")
        
    except (ValueError, TypeError):
        raise appError("Invalid canvas selection. Must be a number", 400)

    except IndexError:
        raise appError("Canvas selection out of range", 404)