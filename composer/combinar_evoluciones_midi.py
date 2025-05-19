import os
import sys
import numpy as np
from mido import MidiFile, MidiTrack, Message
from utils_midi import pitch_from_x, ticks_from_frame, quantize_to_scale
from datetime import datetime
from automaton_gol_mutated import generar_gol
from generar_regla90_mutada import generar_regla90

# Este código fusiona evoluciones del GOL mutado y Regla 90 
# en una sola pieza MIDI de múltiples canales

# Generar evoluciones directamente
path_gol1 = generar_gol()
path_gol2 = generar_gol()
path_r90 = generar_regla90()

# Luego cargas los .npy y haces el MIDI como ya tienes
evo_gol1 = np.load(path_gol1)
evo_gol2 = np.load(path_gol2)
evo_r90 = np.load(path_r90)

# ==== Configuración MIDI ====
ticks_per_beat = 480
subdivision = 4
mid = MidiFile(ticks_per_beat=ticks_per_beat)
track1 = MidiTrack(); mid.tracks.append(track1)  # GoL 1 → Canal 0
track2 = MidiTrack(); mid.tracks.append(track2)  # GoL 2 → Canal 1
track3 = MidiTrack(); mid.tracks.append(track3)  # Regla 90 → Canal 2

# ==== Mapear evolución GoL ====
def agregar_gol_a_track(evolution, track, canal, pitch_range, offset_time=0):
    width = evolution.shape[2]
    for t, frame in enumerate(evolution):
        tick = ticks_from_frame(t + offset_time, ticks_per_beat, subdivision)
        events = []
        for x in range(frame.shape[0]):
            for y in range(frame.shape[1]):
                if frame[x, y] == 1:
                    pitch = quantize_to_scale(pitch_from_x(y, width, *pitch_range))
                    velocity = 50
                    dur = int(ticks_per_beat / subdivision)
                    events.append((tick, Message('note_on', note=pitch, velocity=velocity, time=0, channel=canal)))
                    events.append((tick + dur, Message('note_off', note=pitch, velocity=velocity, time=0, channel=canal)))
        events.sort(key=lambda e: e[0])
        last_tick = tick
        for t_, msg in events:
            delta = t_ - last_tick
            msg.time = delta
            track.append(msg)
            last_tick = t_

# ==== Mapear evolución Regla 90 ====
def agregar_r90_a_track(evolution, track, canal, pitch_range, offset_time=0):
    width = evolution.shape[1]
    for t, row in enumerate(evolution):
        tick = ticks_from_frame(t + offset_time, ticks_per_beat, subdivision)
        events = []
        for i, cell in enumerate(row):
            if cell == 1:
                pitch = quantize_to_scale(pitch_from_x(i, width, *pitch_range))
                velocity = 50
                dur = int(ticks_per_beat / subdivision)
                events.append((tick, Message('note_on', note=pitch, velocity=velocity, time=0, channel=canal)))
                events.append((tick + dur, Message('note_off', note=pitch, velocity=velocity, time=0, channel=canal)))
        events.sort(key=lambda e: e[0])
        last_tick = tick
        for t_, msg in events:
            delta = t_ - last_tick
            msg.time = delta
            track.append(msg)
            last_tick = t_

# ==== Aplicar las capas ====
agregar_gol_a_track(evo_gol1, track1, canal=0, pitch_range=(40, 60))
agregar_gol_a_track(evo_gol2, track2, canal=1, pitch_range=(70, 90))
agregar_r90_a_track(evo_r90, track3, canal=2, pitch_range=(50, 75))

# Crear carpeta de sesión
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
session_dir = os.path.join("composiciones", f"session_{timestamp}")
os.makedirs(session_dir, exist_ok=True)

# Generar evoluciones directamente DENTRO DE session_dir
path_gol1 = generar_gol(output_dir=os.path.join(session_dir, "gol1"))
path_gol2 = generar_gol(output_dir=os.path.join(session_dir, "gol2"))
path_r90 = generar_regla90(output_dir=os.path.join(session_dir, "regla90"))


# Guardar el archivo MIDI con nombre identificable
mid_path = os.path.join(session_dir, "ambient_combinado.mid")
mid.save(mid_path)

print(f"\n✅ Composición guardada en: {mid_path}")