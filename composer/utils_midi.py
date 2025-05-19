# utils_midi.py

# Este código contiene funciones utilitarias para mapear celdas del 
# autómata celular a notas MIDI y cuantizarlas a una escala musical, 
# generando así armonías coherentes en lugar de ruido aleatorio.

def pitch_from_x(x, width, low=40, high=80):
    """Convierte la posición horizontal x en una nota MIDI dentro del rango."""
    scale_range = high - low
    return low + int((x / width) * scale_range)

# Calcular el tiempo en ticks MIDI
def ticks_from_frame(frame_idx, ticks_per_beat, subdivision):
    return frame_idx * (ticks_per_beat // subdivision)

# Obtener escalas mayores y menores
def scale_major(): return [0, 2, 4, 5, 7, 9, 11]
def scale_minor(): return [0, 2, 3, 5, 7, 8, 10]

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
