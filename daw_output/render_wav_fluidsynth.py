import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

# Este código automatiza la conversión de archivos MIDI generados por 
# el sistema (ambient_combinado.mid) a archivos de audio .wav 
# utilizando FluidSynth y un soundfont .SF2.

# Este módulo sólo será usado si el sistema operativo es Linux

SOUNDFONT = os.path.expanduser("~/soundfonts/FluidR3_GM2-2.SF2")
BASE_DIR = "compositions"

def render_sesion(session_path):
    midi_path = os.path.join(session_path, "ambient_combinado.mid")
    wav_path = os.path.join(session_path, "render.wav")
    if not os.path.exists(midi_path):
        print(f"❌ No se encontró MIDI en: {session_path}")
        return
    command = [
        "fluidsynth",
        "-ni",
        SOUNDFONT,
        "-o", "synth.polyphony=2048",
        "-o", "audio.period-size=4096",
        "-o", "audio.periods=4",
        midi_path,
        "-F", wav_path,
        "-r", "44100"
    ]
    print(f"🎧 Renderizando: {session_path}")
    subprocess.run(command)

def render_composicion(composicion_path):
    sesiones = [
        os.path.join(composicion_path, s)
        for s in sorted(os.listdir(composicion_path))
        if os.path.isdir(os.path.join(composicion_path, s))
    ]

    with ProcessPoolExecutor() as executor:
        executor.map(render_sesion, sesiones)

if __name__ == "__main__":
    composiciones = sorted([f for f in os.listdir(BASE_DIR) if f.startswith("composicion_")])
    if not composiciones:
        print("❌ No hay composiciones.")
        exit()

    for i, name in enumerate(composiciones):
        print(f"{i+1}. {name}")
    choice = int(input("Selecciona una composición por número: ")) - 1
    seleccionada = os.path.join(BASE_DIR, composiciones[choice])

    render_composicion(seleccionada)
