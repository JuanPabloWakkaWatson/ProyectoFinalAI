# composer/session_manager.py

import os
import sys
import numpy as np
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from datetime import datetime

# Importar funciones de generación
sys.path.append(os.path.abspath("GoL"))
from automaton_gol_mutated import generar_gol
sys.path.append(os.path.abspath("Regla90"))
from generar_regla90_mutada import generar_regla90

# Importar utilidades MIDI
from utils_midi import pitch_from_x, ticks_from_frame, quantize_to_scale

# ==== Utilidades de instrumentación y tempo ====

instrumentos = {
    0: "Acoustic Grand Piano",
    10: "Glockenspiel",
    40: "Violin",
    41: "Viola",
    42: "Cello",
    48: "String Ensemble 1",
    50: "Synth Strings 1",
    81: "Lead 2 (sawtooth)",
    89: "Pad 2 (warm)",
    90: "Pad 3 (polysynth)",
    91: "Pad 4 (choir)"
}

def elegir_instrumento(canal):
    print(f"\n🎹 Instrumentos disponibles para canal {canal}:")
    for prog, name in instrumentos.items():
        print(f"  {prog:>3}: {name}")
    while True:
        try:
            elegido = int(input(f"Selecciona un instrumento (program number) para canal {canal}: "))
            if elegido in instrumentos:
                return elegido
            print("❌ Número inválido. Intenta de nuevo.")
        except ValueError:
            print("❌ Entrada inválida. Escribe un número.")

def elegir_tempo():
    while True:
        try:
            bpm = int(input("🎼 Tempo deseado (BPM, sugerido 60-120): "))
            if 20 <= bpm <= 300:
                return bpm2tempo(bpm)
            print("❌ BPM fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("❌ Entrada inválida. Escribe un número.")

# ==== Lógica de generación de tracks ====

def agregar_gol_a_track(evolution, track, canal, pitch_range, ticks_per_beat, subdivision):
    width = evolution.shape[2]
    delta_time = ticks_per_beat // subdivision

    for frame in evolution:
        note = None
        for x in range(frame.shape[0]):
            for y in range(frame.shape[1]):
                if frame[x, y] == 1:
                    note = quantize_to_scale(pitch_from_x(y, width, *pitch_range))
                    break
            if note: break

        if note:
            track.append(Message('note_on', note=note, velocity=64, time=delta_time, channel=canal))
            track.append(Message('note_off', note=note, velocity=64, time=0, channel=canal))

def agregar_r90_a_track(evolution, track, canal, pitch_range, ticks_per_beat, subdivision):
    width = evolution.shape[1]
    delta_time = ticks_per_beat // subdivision

    for row in evolution:
        note = None
        for i, cell in enumerate(row):
            if cell == 1:
                note = quantize_to_scale(pitch_from_x(i, width, *pitch_range))
                break

        if note:
            track.append(Message('note_on', note=note, velocity=64, time=delta_time, channel=canal))
            track.append(Message('note_off', note=note, velocity=64, time=0, channel=canal))

# ==== Generación de una sesión ====

def generar_sesion(session_dir: str, instr1, instr2, instr3, tempo):
    os.makedirs(session_dir, exist_ok=True)

    path_gol1 = generar_gol(steps=128, output_dir=os.path.join(session_dir, "gol1"))
    path_gol2 = generar_gol(steps=128, output_dir=os.path.join(session_dir, "gol2"))
    path_r90 = generar_regla90(steps=128, output_dir=os.path.join(session_dir, "regla90"))

    evo_gol1 = np.load(path_gol1)
    evo_gol2 = np.load(path_gol2)
    evo_r90 = np.load(path_r90)

    ticks_per_beat = 480
    subdivision = 4
    mid = MidiFile(ticks_per_beat=ticks_per_beat)

    meta_track = MidiTrack(); mid.tracks.append(meta_track)
    meta_track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    track1 = MidiTrack(); mid.tracks.append(track1)
    track2 = MidiTrack(); mid.tracks.append(track2)
    track3 = MidiTrack(); mid.tracks.append(track3)

    track1.append(Message('program_change', program=instr1, channel=0, time=0))
    track2.append(Message('program_change', program=instr2, channel=1, time=0))
    track3.append(Message('program_change', program=instr3, channel=2, time=0))

    agregar_gol_a_track(evo_gol1, track1, canal=0, pitch_range=(40, 60), ticks_per_beat=ticks_per_beat, subdivision=subdivision)
    agregar_gol_a_track(evo_gol2, track2, canal=1, pitch_range=(70, 90), ticks_per_beat=ticks_per_beat, subdivision=subdivision)
    agregar_r90_a_track(evo_r90, track3, canal=2, pitch_range=(50, 75), ticks_per_beat=ticks_per_beat, subdivision=subdivision)

    track1.append(MetaMessage('end_of_track', time=0))
    track2.append(MetaMessage('end_of_track', time=0))
    track3.append(MetaMessage('end_of_track', time=0))

    mid_path = os.path.join(session_dir, "ambient_combinado.mid")
    mid.save(mid_path)
    print(f"✅ Sesión guardada en: {session_dir}")

# ==== Múltiples sesiones ====

def generar_multiples_sesiones(n, instr1, instr2, instr3, tempo):
    base_root = "compositions"
    os.makedirs(base_root, exist_ok=True)

    existing = [d for d in os.listdir(base_root) if d.startswith("composicion_")]
    num = 1
    while f"composicion_{num:03d}" in existing:
        num += 1

    composicion_dir = os.path.join(base_root, f"composicion_{num:03d}")
    os.makedirs(composicion_dir)

    print(f"\n🎼 Generando {n} sesiones en: {composicion_dir}\n")

    for i in range(1, n + 1):
        session_dir = os.path.join(composicion_dir, f"session_{i}")
        generar_sesion(session_dir, instr1, instr2, instr3, tempo)

# ==== MAIN ====

if __name__ == "__main__":
    N = int(input("¿Cuántas sesiones quieres generar?: "))
    instr1 = elegir_instrumento(1)
    instr2 = elegir_instrumento(2)
    instr3 = elegir_instrumento(3)
    tempo = elegir_tempo()
    generar_multiples_sesiones(N, instr1, instr2, instr3, tempo)
