# This file returns the hex codes of a color palette based on key + mode of the song

# class to store the key and associated color palatte
class keyToColor:
    def __init__(self, key, mode, colors):
        self.key = key
        self.mode = mode
        self.colors = colors

# initilizing color palettes
c_major = keyToColor("C", "major", ["#fae29c", "#f0bb52", "#d28030", "#f2f1f1", "#c1ddda", "#c6e0a6", "#fbdacd", "#eb9dae", "#b34568", "#591427"])
c_minor = keyToColor("C", "minor", ["#bcb3d1", "#8783b2", "#3a345b", "#cf75af", "#8f306a", "#4b1635", "#b7c1d5", "#556c93", "#1c2b48", "#0c1b34"])
c_sharp_major = keyToColor("C#", "major", ["#edb5d3", "#ef59a0", "#f2e6b8", "#f2cca6", "#f28695", "#fccd57", "#10878d", "#6da2d7", "#7858a2", "#b6b1d8"])
c_sharp_minor = keyToColor("C#", "minor", ["#b7c1d5", "#8280bd", "#241f60", "#d9b8d0", "#a47097", "#5f214d", "#42124b", "#70a3b1", "#40809a", "#0d3846"])
d_flat_major = keyToColor("Db", "major", ["#9fb1cd", "#536187", "#1b314c", "#0c1926", "#c7c7c6", "#6b797d", "#4e6e79", "#394a56", "#2c4042", "#1d3539"])
d_major = keyToColor("D", "major", ["#f2dbb6", "#eece73", "#9b7135", "#824a1f", "#b2606f", "#8f2f30", "#6e1410", "#cee6f2", "#4b81ac", "#263677"])
d_minor = keyToColor("D", "minor", ["#f2aebc", "#d06a86", "#a63561", "#8a2245", "#2f111a", "#5973ad", "#243f90", "#21205d", "#161a32", "#0b0e17"])
d_sharp_minor = keyToColor("D#", "minor", ["#d3d2d0", "#929aad", "#3c3e4a", "#9eadcd", "#193960", "#131625", "#768956", "#303d21", "#17160f", "#3b2c20"])
e_flat_major = keyToColor("Eb", "major", ["#f2d3d3", "#e67e7f", "#a13374", "#81194e", "#a32f3c", "#711011", "#2e1010", "#7a70b3", "#41386b", "#2c274f"])
e_major = keyToColor("E", "major", ["#eee4ba", "#feea55", "#fccd57", "#f6b61d", "#f15c22", "#aed79e", "#8fb680", "#ee4994", "#ed196f", "#bc1e62"])
e_minor = keyToColor("E", "minor", ["#af8eab", "#683c68", "#502a50", "#432033", "#ffe0bc", "#a9cadf", "#385988", "#172d55", "#414159", "#28283d"])
b_major = keyToColor("B", "major", ["#eb9dae", "#591427", "#3c1215", "#c18d36", "#f2dbb6", "#a81f23", "#5e0e12", "#8fb680", "#3e5026", "#052623"])
b_minor = keyToColor("B", "minor", ["#fce0d9", "#f1c0a3", "#e3cfe5", "#ca9dc8", "#96cde7", "#60b0df", "#223662", "#a7b7ab", "#a3b568", "#233f41"])
f_major = keyToColor("F", "major", ["#f8dfc0", "#fdd295", "#e6a43f", "#b24a37", "#a32738", "#8b181b", "#710f13", "#c6e0a6", "#818d47", "#3d4422"])
f_minor = keyToColor("F", "minor", ["#d3d2d0", "#8694a4", "#536187", "#1b314c", "#0c1926", "#92504e", "#792e29", "#5b1918", "#291910", "#070806"])
f_sharp_major = keyToColor("F#", "major", ["#96d0cf", "#10878d", "#016d5e", "#d62887", "#843293", "#f0b127", "#f6d73e", "#f4753d", "#f16051", "#a6ca53"])
f_sharp_minor = keyToColor("F#", "minor", ["#e6a43f", "#b24a37", "#5b1918", "#8694a4", "#4e6573", "#2b4367", "#1b314c", "#172531", "#202221", "#070806"])
g_major = keyToColor("G", "major", ["#beaed5", "#7a70b3", "#4b4167", "#322341", "#9c3259", "#6c1a34", "#3868b2", "#1a3854", "#6b9877", "#46684f"])
g_minor = keyToColor("G", "minor", ["#9eadcd", "#668ca9", "#394a56", "#1b314c", "#1f2244", "#111630", "#a15561", "#630c16", "#471116", "#321316"])
a_flat_major = keyToColor("Ab", "major", ["#f7f6f9", "#d5b4d6", "#4b4167", "#a6b8d1", "#305ba7", "#1a3854", "#192342", "#0c1926", "#f7e59f", "#c78439"])
a_flat_minor= keyToColor("Ab", "minor", ["#68bc98", "#257772", "#145666", "#d5e0c5", "#164230", "#052623", "#124643", "#deaec1", "#943b5c", "#6b1f3b"])
a_major = keyToColor("A", "major", ["#efbcd7", "#ec579f", "#da1b5d", "#6b1f3b", "#ccd533", "#f6d73e", "#f04b27", "#b41f24", "#c0dff3", "#3b53a4"])
a_minor = keyToColor("A", "minor", ["#edaac3", "#f17db1", "#943b5c", "#411528", "#76172c", "#ab3a41", "#8b181b", "#aedccf", "#6bb1ad", "#145666"])
b_flat_major = keyToColor("Bb", "major", ["#f7e59f", "#f6d73e", "#fcb527", "#f37d78", "#f16051", "#f38292", "#aedccf", "#8fc1e8", "#305ba7", "#22416e"])
b_flat_minor = keyToColor("Bb", "minor", ["#bcb3d1", "#683c68", "#502a50", "#aa4b54", "#8b181b", "#710f13", "#b7c1d5", "#556c93", "#1c2b48", "#0c1b34"])

# add the color palettes to the array
color_palettes = []
color_palettes.append(c_major)
color_palettes.append(c_minor)
color_palettes.append(c_sharp_minor)
color_palettes.append(c_sharp_major)
color_palettes.append(d_flat_major)
color_palettes.append(d_major)
color_palettes.append(d_minor)
color_palettes.append(d_sharp_minor)
color_palettes.append(e_flat_major)
color_palettes.append(e_major)
color_palettes.append(e_minor)
color_palettes.append(b_major)
color_palettes.append(b_minor)
color_palettes.append(f_major)
color_palettes.append(f_minor)
color_palettes.append(f_sharp_major)
color_palettes.append(f_sharp_minor)
color_palettes.append(g_major)
color_palettes.append(g_minor)
color_palettes.append(a_flat_major)
color_palettes.append(a_flat_minor)
color_palettes.append(a_major)
color_palettes.append(a_minor)
color_palettes.append(b_flat_major)
color_palettes.append(b_flat_minor)

palette_lookup = {
    (p.key.lower(), p.mode.lower()): p.colors
    for p in color_palettes
}

def getColors (key, mode):

    key_id = (key.lower(), mode.lower())
    print("Key id for the song: ", key_id)

    # if key_id not in palette_lookup:
    #     print("Missing key in palette_lookup: ", key_id)
    #     return ["#ffffff"]
    print("Palette look up: ", palette_lookup[key_id])
    return palette_lookup[key_id]    

