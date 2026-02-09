# lyric selection file
# this file has a function that returns selected lyrics

def getSelection(sections, sections_censored):

    i = 1
    for section in sections:
        print(f"{i}. {section}")
        i += 1

    choice = int(input("Which lyric section you want to choose: "))

    # convert dict keys to a list
    section_names = list(sections.keys())
    section_names_censored = list(sections_censored.keys())

    # adjust because lists start at 0
    selected_section = section_names[choice - 1]
    selected_section_censored = section_names_censored[choice -1]
    return sections[selected_section], sections_censored[selected_section_censored]

        