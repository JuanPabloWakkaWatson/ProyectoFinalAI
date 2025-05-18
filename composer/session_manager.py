# composer/session_manager.py

import os
import sys
import numpy as np
from mido import MidiFile, MidiTrack, Message
from datetime import datetime

# Importar funciones de generación
sys.path.append(os.path.abspath("GoL"))
from automaton_gol_mutated import generar_gol
sys.path.append(os.path.abspath("Regla90"))
from generar_regla90_mutada import generar_regla90

# Importar utilidades MIDI
from utils_midi import pitch_from_x, ticks_from_frame, quantize_to_scale

# ==== Función para una sesión completa ====
def generar_sesion(session_dir: str):
    os.makedirs(session_dir, exist_ok=True)

    # Generar evoluciones y guardarlas dentro de la sesión
    path_gol1 = generar_gol(output_dir=os.path.join(session_dir, "gol1"))
    path_gol2 = generar_gol(output_dir=os.path.join(session_dir, "gol2"))
    path_r90  = generar_regla90(output_dir=os.path.join(session_dir, "regla90"))

    # Cargar evoluciones
    evo_gol1 = np.load(path_gol1)
    evo_gol2 = np.load(path_gol2)
    evo_r90 = np.load(path_r90)

    # Crear archivo MIDI
    ticks_per_beat = 480
    subdivision = 4
    mid = MidiFile(ticks_per_beat=ticks_per_beat)
    track1 = MidiTrack(); mid.tracks.append(track1)
    track2 = MidiTrack(); mid.tracks.append(track2)
    track3 = MidiTrack(); mid.tracks.append(track3)

    def agregar_gol_a_track(evolution, track, canal, pitch_range):
        width = evolution.shape[2]
        for t, frame in enumerate(evolution):
            tick = ticks_from_frame(t, ticks_per_beat, subdivision)
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

    def agregar_r90_a_track(evolution, track, canal, pitch_range):
        width = evolution.shape[1]
        for t, row in enumerate(evolution):
            tick = ticks_from_frame(t, ticks_per_beat, subdivision)
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

    agregar_gol_a_track(evo_gol1, track1, canal=0, pitch_range=(40, 60))
    agregar_gol_a_track(evo_gol2, track2, canal=1, pitch_range=(70, 90))
    agregar_r90_a_track(evo_r90,  track3, canal=2, pitch_range=(50, 75))

    # Guardar el archivo MIDI
    mid_path = os.path.join(session_dir, "ambient_combinado.mid")
    mid.save(mid_path)
    print(f"✅ Sesión guardada en: {session_dir}")

# ==== Ejecutar múltiples sesiones ====
# ==== Ejecutar múltiples sesiones dentro de una composición ====
def generar_multiples_sesiones(n=5):
    base_root = "compositions"
    os.makedirs(base_root, exist_ok=True)

    # Buscar siguiente número de composición disponible
    existing = [d for d in os.listdir(base_root) if d.startswith("composicion_")]
    num = 1
    while f"composicion_{num:03d}" in existing:
        num += 1

    composicion_dir = os.path.join(base_root, f"composicion_{num:03d}")
    os.makedirs(composicion_dir)

    print(f"\n🎼 Generando {n} sesiones en: {composicion_dir}\n")

    for i in range(1, n + 1):
        session_dir = os.path.join(composicion_dir, f"session_{i}")
        generar_sesion(session_dir)

# === Entry point ===
if __name__ == "__main__":
    N = int(input("¿Cuántas sesiones quieres generar?: "))
    generar_multiples_sesiones(N)

