import random
from backend.errors import appError
# build a class to set variables used in the prompt
class promptBuilder:
    def __init__(self):
        self.tempo_level = None
        self.tempo_tier = None
        self.chaos = None
        self.mode = None
        self.spectral_behavior = None
        self.density = None
        self.shape = None
        self.materiality = None

# use the tempo and sort into tempo levels and a tempo modifer
def getTempoTier(tempo):
    # guard to check if the tempo is a number
    if not isinstance(tempo, (int, float)):
        raise appError("Tempo must be a number", 500)

    # sort tempos and assign them tempo tiers
    if tempo <= 40:
        tempo_level = "low"
        tier = "LOW: diffuse, airy, slow “breathing” transitions; minimal structure; broad soft fields; very gentle grain."
    elif tempo >= 40 and tempo <= 76:
        tempo_level = "low-medium"
        tier = "LOW-MEDIUM: calm harmonic layering; milky haze; soft glow; slightly more defined flows."
    elif tempo >= 76 and tempo <= 108:
        tempo_level = "medium"
        tier = "MEDIUM: flowing ribbons and intersections; controlled bloom; clearer layer separation without sharp edges."
    elif tempo >= 108 and tempo <= 120:
        tempo_level = "high-medium"
        tier = "HIGH-MEDIUM: energetic interference; phase shifting; warped gradients; smearing/tearing boundaries while staying cohesive."  
    elif tempo >= 120 and tempo <= 168:
        tempo_level = "high"
        tier = "HIGH: radiant intensity; pulsing/spiraling expansion; brighter cores and bloom; rhythmic repetition/interference without geometry."
    elif tempo >= 168:
        tempo_level = "highest"
        tier = "HIGHEST: maximal compression; saturation stacking; volatile interference; blown highlights; dense layering with brief soft “breathing gaps.”"
    
    return tempo_level, tier

# input the tempo level and return a chaos modifier
def getChaosBehavior(tempo_level):
    if tempo_level == "low":
        return "Introduce gentle instability through soft dissolves, drifting overlaps, and slow phase shifts; chaos remains atmospheric and calm."
    
    if tempo_level == "low-medium":
        return "Allow harmonic interference between layers, subtle asymmetry, and overlapping flows that gently disrupt uniform motion."
    
    if tempo_level == "medium":
        return "Introduce energetic collisions, frequency interference, and uneven energy distribution while maintaining overall flow."
    
    if tempo_level == "high-medium":
        return "Allow visible distortion, smearing, tearing edges, and phase breaks as layers collide and destabilize."
    
    if tempo_level == "high":
        return "Push chaos through saturation spikes, radiant turbulence, overlapping bursts, and unstable luminous cores."
    
    if tempo_level == "highest": 
        return "Embrace maximal chaos: dense compression, volatile interference, layer collapse, blown highlights, and overwhelming sensory density, balanced by brief soft gaps to avoid total visual failure."

# based on the mode return mode modifier
def getModeBehavior(mode):
    mode = mode.lower()

    if mode == "major":
        return "major: Brighter luminous bias, open spatial expansion, smoother transitions, upward curvature."
    
    if mode == "minor":
        return "minor: Darker tonal clustering, inward pull, tighter compression, subtle shadow tension."
    
    # if a different mode is passed add a nutreal modifier
    return f"{mode}: Neutral tonal bias, balanced spatial energy."
    

# using happiness level return spectral behaviors
def getSpectralFeatures(happiness):
    # validate happiness
    if not (0 <= happiness <= 100):
        raise appError("Happiness must be between 0 and 100", 500)
    
    if happiness >= 50:
        return "sharper glow, crisp particle sparks, higher frequency shimmer"
    if happiness < 50:
        return "heavier diffusion, denser haze, softer bloom"

# return a random density
def getDensity():
    densities = ["sparse", "dense", "syncopated", "steady"]

    rand_density = random.choice(densities)
    return rand_density

# return a random shape
def getShape():
    shapes = ["radial", "wave-based", "cloud-based", "ribbon-based", "fragmentation-based", "vortex-based", "lattice-distortion-based"]

    rand_shape = random.choice(shapes)
    return rand_shape

# return a random material 
def getMateriality():
    materials = ["glasslike (clean glow, refraction feel)", "velvet (soft absorption, matte diffusion)", "liquid (flowing gradients, pooling)", "smoke/mist (wispy translucency)", "plasma (high-energy bloom, scintillation)"]

    rand_material = random.choice(materials)
    return rand_material

# enforce the word limit and cut out the lowest prioity section
def wordLimit(parts, max_words=200):
    words = lambda s: len(s.split())
    combined = "\n".join([p for p, _prio in parts])
    print("Word count: ", words(combined))

    # if the combined parts is below or equal to the word count
    if words(combined) <= max_words:
        return combined
    
    # drop the lowest prioity parts (higher number = lower importance)
    parts_sorted = sorted(parts, key=lambda x: x[1], reverse=True)
    kept = parts[:]

    for drop_part, drop_prio in parts_sorted:
        candidate = [p for p in kept if p[0] != drop_part]
        combined_candidate = "\n".join([p for p, _ in candidate])
        if words(combined_candidate) <= max_words:
            return combined_candidate
        kept = candidate
        
    # last resort manually shorten the string
    return " ".join(combined.split() [:max_words])


def getPrompt(song):
    prompt = promptBuilder()

    # validate that all song parts are there
    required = ["palette", "tempo", "mode", "happiness"]
    for attr in required:
        if not hasattr(song, attr) or getattr(song, attr) is None:
            raise ValueError(f"Song object is missing required attribute: '{attr}'")

    print("\nBuilding the prompt...\n")

    # core line that explains chromesthesia
    core_line = """
        Create a fully abstract image inspired by chromesthesia a synesthetic translation of sound into color, 
        frequency, and emotional motion. The image must be strictly non-representational: no identifiable objects, 
        figures, symbols, environments, typography, or readable marks.
    """
    
    # add the color palette and make sure it's only those colors
    palette_line = f"""
        Color palette (STRICT): {", ".join(song.palette)}
        Use only these colors; all gradients, glow, highlights, and shadows derive strictly from the palette.
    """

    # ensure there aren't any extra bits
    no_text_line = "No watermarks, borders, or text. Ultra-abstract painterly-digital style, high resolution."

    # get the tempo level and tempo tier
    tempo_level, tempo_tier = getTempoTier(song.tempo)
    prompt.tempo_level = tempo_level
    prompt.tempo_tier = tempo_tier

    # get the chaos behavior modifier
    prompt.chaos = getChaosBehavior(prompt.tempo_level)

    # add the modifer to a chaos line
    chaos_line = f"""
        Apply controlled chaos according to tempo:
        Chaos behavior: {prompt.chaos}
    """
    # get the mode behavior modifer and add it to a line
    prompt.mode = getModeBehavior(song.mode)
    mode_line = f"Mood bias: {prompt.mode}"

    # get and assign the spectral behavior modifier to the spectral behavior line
    prompt.spectral_behavior = getSpectralFeatures(song.happiness)
    spectral_behavior_line = f"Spectral character: {prompt.spectral_behavior}"

    # get and assign the density modifier to the density line
    prompt.density = getDensity()
    density_line = f"Rhythmic structure: {prompt.density}, influencing distribution and repetition of energy clusters."

    # get and assign the shape modifer to the shape line
    prompt.shape = getShape()
    shape_line = f"Shape language: emphasize {prompt.shape}."

    # get and assign the materiality modifier to the materiality line
    prompt.materiality = getMateriality()
    material_line = f"Materiality: {prompt.materiality}; all texture and glow should behave like this material."

    # add all of the lines of the prompt to the array and assign it a priority level
    # lower number is a higher priority
    parts = [
        (core_line, 0),
        (palette_line, 0),
        (no_text_line, 0),
        (tempo_tier, 0),
        (chaos_line, 0),
        (mode_line, 1),
        (shape_line, 1),
        (spectral_behavior_line, 2),
        (density_line, 2),
        (material_line, 2)
    ]

    # send all of the parts of the prompt to check and enforce the word limit
    final_prompt = wordLimit(parts)
    print("The final prompt: ", final_prompt)
    # return the final prompt
    return final_prompt