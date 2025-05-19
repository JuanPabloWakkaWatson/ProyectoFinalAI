# pipeline.py
import os
import time
import platform
from composer.session_manager import (
    elegir_instrumento, elegir_tempo,
    generar_una_sesion_directa, generar_multiples_sesiones
)
from visualizer.generate_gifs_by_session import procesar_composicion as generar_gifs
from analyzer.analyze_sessions import analizar_composicion
from analyzer.visualizar_metricas import visualizar_metricas

# Render opcional en Linux
def renderizar_audio(session_path):
    from daw_output.render_wav_fluidsynth import render_sesion
    render_sesion(session_path)

# Verifica existencia de un archivo con espera
def esperar_archivo(path, intentos=10, delay=0.2):
    for _ in range(intentos):
        if os.path.exists(path):
            return True
        time.sleep(delay)
    return False

IS_LINUX = platform.system() == "Linux"
IS_WINDOWS = platform.system() == "Windows"

def main():
    print("🎼 Generación de sesión(es) con análisis y visualización\n")

    # Entrada de usuario
    try:
        num_sesiones = int(input("¿Cuántas sesiones quieres generar? (1 o más): "))
        assert num_sesiones >= 1
    except:
        print("❌ Valor inválido. Se generará solo 1 sesión.")
        num_sesiones = 1

    instr1 = elegir_instrumento(1)
    instr2 = elegir_instrumento(2)
    instr3 = elegir_instrumento(3)
    tempo = elegir_tempo()

    # Generación de sesiones
    if num_sesiones == 1:
        print("\n🚀 Generando 1 sesión...")
        session_path = generar_una_sesion_directa(instr1, instr2, instr3, tempo)
        composicion_dir = os.path.dirname(session_path)
        sesiones = [session_path]
    else:
        print(f"\n🚀 Generando {num_sesiones} sesiones...")
        composicion_dir = generar_multiples_sesiones(num_sesiones, instr1, instr2, instr3, tempo)
        sesiones = [
            os.path.join(composicion_dir, d)
            for d in sorted(os.listdir(composicion_dir))
            if os.path.isdir(os.path.join(composicion_dir, d)) and d.startswith("session_")
        ]

    # Verificación de archivos antes de generar GIFs
    print("\n🖼️ Generando visuales (GIFs)...")
    todos_listos = True
    for path in sesiones:
        gol1_path = os.path.join(path, "gol1", "gol.npy")
        gol2_path = os.path.join(path, "gol2", "gol.npy")
        r90_path = os.path.join(path, "regla90", "regla90.npy")
        if all(esperar_archivo(p) for p in [gol1_path, gol2_path, r90_path]):
            print(f"🧩 Archivos detectados en {path}")
        else:
            print(f"⚠️ Archivos faltantes en {path}")
            todos_listos = False

    if todos_listos:
        print("📽️ Generando todos los GIFs...")
        generar_gifs(composicion_dir)
    else:
        print("⚠️ No se generaron GIFs por sesiones incompletas.")

    # Análisis de métricas
    print("\n📊 Analizando métricas...")
    analizar_composicion(composicion_dir)

    # Gráficas
    print("\n📈 Generando gráficas...")
    visualizar_metricas(composicion_dir)

    # Render opcional
    if IS_LINUX:
        print("\n🎧 Renderizando audio con FluidSynth...")
        for path in sesiones:
            renderizar_audio(path)
    else:
        print("\n🎵 Saltando render de audio. Puedes usar los archivos .mid en FL Studio.")

    print(f"\n✅ Todo listo. Carpeta generada: {composicion_dir}")

if __name__ == "__main__":
    main()
