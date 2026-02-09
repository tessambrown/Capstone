class tempoTier:
    def _init_(self):
        self.tempo_level = None
        self.tier = None
    

def getTempoTier(tempo):
    tempo_tier = tempoTier
    
    if tempo <= 40:
        tempo_tier.tempo_level = "low"
        tempo_tier.tier = "LOW: diffuse, airy, slow “breathing” transitions; minimal structure; broad soft fields; very gentle grain."

    if tempo >= 40 and tempo <= 76:
        tempo_tier.tempo_level = "low-medium"
        tempo_tier.tier = "LOW-MEDIUM: calm harmonic layering; milky haze; soft glow; slightly more defined flows."
    
    if tempo >= 76 and tempo <= 108:
        tempo_tier.tempo_level = "medium"
        tempo_tier.tier = "MEDIUM: flowing ribbons and intersections; controlled bloom; clearer layer separation without sharp edges."
    
    if tempo >= 108 and tempo <= 120:
        tempo_tier.tempo_level = "high-medium"
        tempo_tier.tier = "HIGH-MEDIUM: energetic interference; phase shifting; warped gradients; smearing/tearing boundaries while staying cohesive."
    
    if tempo >= 120 and tempo <= 168:
        tempo_tier.tempo_level = "high"
        tempo_tier.tier = "HIGH: radiant intensity; pulsing/spiraling expansion; brighter cores and bloom; rhythmic repetition/interference without geometry."
    
    if tempo >= 168:
        tempo_tier.tempo_level = "highest"
        tempo_tier.tier = "HIGHEST: maximal compression; saturation stacking; volatile interference; blown highlights; dense layering with brief soft “breathing gaps.”"
    
    return tempo_tier.tempo_level, tempo_tier.tier

def getRatioModifiers(ratio):
    if ratio == "9:16":
        return "Strong vertical energy flow; elongated gradients; stacked layers rising and falling; avoid centered symmetry."
    elif ratio == "2:3":
        return "Vertical drift with gentle asymmetry; distribute intensity along the long axis; avoid a single central hotspot."
    elif ratio == "3:4":
        return "Portrait-balanced flow; soft vertical arcs and layered veils; moderate central cohesion without rigid centering."
    elif ratio == "4:5":
        return "Compact portrait composition; concentrated mid-frame energy with soft top and bottom falloff; maintain airy margins."
    elif ratio == "1:1":
        return "Balanced radial or orb-like distribution; even visual weight across quadrants; no dominant directional pull."
    elif ratio == "16:9":
        return "Wide lateral flow; elongated horizontal gradients; energy dispersed left to right; avoid vertical stacking dominance."
    elif ratio == "3:2":
        return "Cinematic horizontal sweep; layered bands and drifting interference across the width; keep focal intensity off-center."
    elif ratio == "4:3":
        return "Landscape-balanced dispersion; gentle lateral drift with soft diagonal currents; avoid heavy edge clustering."
    elif ratio == "21:9":
        return "Panoramic dispersion; thin layered bands and long interference waves; multiple soft intensity pockets rather than a single focus."
    elif ratio == "11:17":
        return "rising luminous currents; distribute energy along the vertical axis with soft diagonal drift to avoid rigid column structures."
    elif ratio == "17:22":
        return "layered veils and radiant arcs stretching upward and downward; allow subtle curvature and swirl to break linear stacking."
    else:
        return None

def getChaosBehavior(tempo):
    if tempo == "low":
        return "Introduce gentle instability through soft dissolves, drifting overlaps, and slow phase shifts; chaos remains atmospheric and calm."
    
    if tempo == "low-medium":
        return "Allow harmonic interference between layers, subtle asymmetry, and overlapping flows that gently disrupt uniform motion."
    
    if tempo == "medium":
        return "Introduce energetic collisions, frequency interference, and uneven energy distribution while maintaining overall flow."
    
    if tempo == "high-medium":
        return "Allow visible distortion, smearing, tearing edges, and phase breaks as layers collide and destabilize."
    
    if tempo == "high":
        return "Push chaos through saturation spikes, radiant turbulence, overlapping bursts, and unstable luminous cores."
    
    if tempo == "highest": 
        return "Embrace maximal chaos: dense compression, volatile interference, layer collapse, blown highlights, and overwhelming sensory density, balanced by brief soft gaps to avoid total visual failure."


def getPrompt(song):

    # prompt = f"""
    #     Create a fully abstract image inspired by chromesthesia—a synesthetic translation of sound into color, frequency, and emotional motion. The image must be purely non-representational: no identifiable objects, figures, symbols, environments, icons, typography, or readable marks.

    #     Treat light as an enchanted, radiant phenomenon, not a structural element. Don't add any banding, slicing, striping, or repetitive linear segmentation. Emphasize luminous bloom, soft halos, radiant cores, and gently impossible lighting. Movement should feel like magical flow—swirling energy or spell-like circulation—never mechanical repetition.

    #     Introduce controlled chaos: overlapping frequencies, uneven energy distribution, phase-shifted layers, and moments of visual tension where color fields collide, smear, or partially dissolve. Allow instability, interference, and asymmetry while maintaining cohesion and flow.

    #     Include subtle glowing particles, luminous dust, or star-like specks embedded within the color fields to enhance a sense of wonder.

    #     Contrast level: {song.contrast}
    #     Aspect ratio: {song.ratio}
    #     Composition modifier: {song.ratio_modifier}

    #     Color palette (STRICT): {", ".join(song.palette)}
    #     Use only these colors. No additional colors, neutrals, black, or white. All blends derive strictly from the palette.

    #     Core look: layered translucency, soft diffusion, internal ambient light, depth via opacity stacking only.

    #     Tempo behavior: {song.tempo_tier}
    #     Chaos behavior: {song.chaos}

    #     Keep edges soft; avoid crisp geometry. No watermarks, signatures, borders, or text.

    #     Style: ultra-abstract, contemporary painterly-digital hybrid, high resolution.
    # """

    prompt = f"""
        Create a fully abstract image inspired by chromesthesia—a synesthetic translation of sound into color, 
        frequency, and emotional motion. The image must be strictly non-representational: no identifiable objects, 
        figures, symbols, environments, typography, or readable marks.

        Treat light as an enchanted, radiant phenomenon, not a structural element. Avoid rigid banding, slicing, 
        striping, or repetitive linear segmentation. Emphasize luminous bloom, soft halos, radiant cores, and gently 
        impossible lighting. Movement should feel magical and fluid—swirling energy or spell-like circulation—never 
        mechanical.

        Apply controlled chaos according to tempo:
        Chaos behavior: {song.chaos}

        Include subtle glowing particles, luminous dust, or star-like specks embedded within the color fields.

        Contrast: {song.contrast}
        Aspect ratio: {song.ratio}
        Composition: {song.ratio_modifier}

        Color palette (STRICT): {", ".join(song.palette)}
        Use only these colors; all gradients, glow, highlights, and shadows derive strictly from the palette.

        Layered translucency, soft diffusion, internal ambient light, depth via opacity stacking only.

        Tempo behavior: {song.tempo_tier}

        No watermarks, borders, or text. Ultra-abstract painterly-digital style, high resolution.
    """

    word_count = len(prompt.split())

    if word_count > 200:
        return None

    print("Word count of the prompt: ", word_count)

    return prompt.strip()

