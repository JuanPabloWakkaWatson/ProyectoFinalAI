# utils_midi.py
def pitch_from_x(x, width, low=40, high=80):
    """Convierte la posición horizontal x en una nota MIDI dentro del rango."""
    scale_range = high - low
    return low + int((x / width) * scale_range)

def ticks_from_frame(frame, ticks_per_beat=480, subdivision=4):
    """Convierte un frame a ticks MIDI (1/subdivision nota por frame)."""
    return int((frame * ticks_per_beat) / subdivision)

def pentatonic_scale():
    """Devuelve los grados de la escala pentatónica menor."""
    return [0, 3, 5, 7, 10]

def quantize_to_scale(note, base=40, scale=None):
    """Cuantiza una nota al grado más cercano de una escala dentro del rango."""
    if scale is None:
        scale = pentatonic_scale()
    octave = (note - base) // 12
    degree = min(scale, key=lambda x: abs((base + x + 12 * octave) - note))
    return base + degree + 12 * octave
