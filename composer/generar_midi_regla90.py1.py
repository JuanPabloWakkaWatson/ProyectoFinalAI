# Regla90/generar_midi_regla90.py

import numpy as np
from mido import Message, MidiFile, MidiTrack
import os
import sys

# Agregar path raíz para importar utils_midi
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from composer.utils_midi import pitch_from_x, ticks_from_frame, quantize_to_scale

# ==== SELECCIÓN DE CARPETA ====
base_dir = os.path.join("Regla90", "evoluciones_1d")
folders = sorted([f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))])

if not folders:
    raise FileNotFoundError(f"No se encontraron carpetas en {base_dir}")

print("Carpetas disponibles:")
for i, folder in enumerate(folders):
    print(f"{i + 1}. {folder}")

choice = int(input("Selecciona una carpeta por número: ")) - 1
selected_folder = os.path.join(base_dir, folders[choice])
npy_path = os.path.join(selected_folder, "evolution.npy")

if not os.path.exists(npy_path):
    raise FileNotFoundError(f"No se encontró evolution.npy en {selected_folder}")

# ==== CARGAR EVOLUCIÓN 1D ====
evolution = np.load(npy_path)  # shape: (frames, width)
output_dir = selected_folder
mid_path = os.path.join(output_dir, "ambient_regla90.mid")

# ==== CONFIGURACIÓN MIDI ====
ticks_per_beat = 480
subdivision = 4
mid = MidiFile(ticks_per_beat=ticks_per_beat)
track = MidiTrack()
mid.tracks.append(track)

width = evolution.shape[1]

# ==== CONVERTIR A NOTAS ====
for t, line in enumerate(evolution):
    time_tick = ticks_from_frame(t, ticks_per_beat, subdivision)
    events = []

    for i, cell in enumerate(line):
        if cell == 1:
            pitch = pitch_from_x(i, width)
            pitch = quantize_to_scale(pitch)
            velocity = 50
            duration = int(ticks_per_beat / subdivision)
            events.append((time_tick, Message('note_on', note=pitch, velocity=velocity, time=0)))
            events.append((time_tick + duration, Message('note_off', note=pitch, velocity=velocity, time=0)))

    # Insertar ordenado por tiempo
    events.sort(key=lambda ev: ev[0])
    last_time = time_tick
    for tick, msg in events:
        delta = tick - last_time
        msg.time = delta
        track.append(msg)
        last_time = tick

# ==== GUARDAR MIDI ====
mid.save(mid_path)
print(f"✅ Archivo MIDI guardado en: {mid_path}")
