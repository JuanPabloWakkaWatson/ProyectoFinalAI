﻿# ProyectoFinalAI

Este proyecto trata de crear una herramienta experimental para crear música automáticamente a partir de la evolución de autómatas celulares. El sistema permite crear composiciones MIDI, visualizarlas mediante GIFs animados y analizarlas gráficamente. 

Instrucciones de uso:
1. Clonar este repositorio e instalar todas las dependencias descritas en requirements.txt (pip install -r requirements.txt)
2. Correr el main de nombre pipeline.py (python pipeline.py)
3. Elegir instrumentos para 3 canales y el tempo deseado, así como la cantidad de sesiones musicales
4. Por detrás, las visualizaciones de los autómatas se procesan con la regla 90, GOL1 y GOL2; se analizan las métricas musicales, y se generan gráficas
5. Consultar el audio final en formato .wav (sólo para Linux), y los resultados en la carpeta compositions

Estructura general:
composer/ – Lógica para generación musical y archivos MIDI.
visualizer/ – Generación de GIFs animados para las evoluciones de autómatas celulares (incluye scripts para GoL, Regla90 y evolución 1D).
analyzer/ – Análisis y visualización de métricas musicales.
daw_output/ – Renderizado de audio usando FluidSynth (solo Linux).
compositions/ – Carpeta donde se almacenan las composiciones y sus resultados (MIDI, WAV, GIFs, gráficas).
pipeline.py – Script principal que coordina todo el proceso.

Detalles adicionales: 
Visualización: Los GIFs se generan con coloración especial para destacar cambios recientes en la evolución (por ejemplo, rojo para cambios en Regla 90).
Interactividad: Al ejecutar los scripts de visualización, se puede seleccionar la composición o carpeta a procesar.

Requisitos:
- Python 3.7+
- Paquetes: numpy, matplotlib, pillow
- Linux para renderizado de audio con FluidSynth (opcional)

Visualización:
Ejecutar los scripts directamente para generar las animaciones GIF a partir de los archivos .npy generados ->
- visualizer/visualizar_evolucion.py — Para GoL bidimensional
visualizer/visualizar_evolucion_1d.py — Para evolución 1D (Regla 90)
- visualizer/generar_gif_gol.py — Para múltiples variantes de GoL y Regla 90 (integrado en pipeline)


Presentación:
[Presentación Final](https://itam2-my.sharepoint.com/:p:/g/personal/maria_cobacho_itam_mx/EVYs4tVlmSNCtMTacW2k9vQBfplCnTKKZYPjk4pTbN7SRg?rtime=pjwk_7OX3Ug)
