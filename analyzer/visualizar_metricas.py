import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Este códgio genera gráficas para analizar visualmente la evolución 
# de las métricas por sesi´n y por modelo a partir de metadata_summary.json

def visualizar_metricas(composicion_path):
    resumen_path = os.path.join(composicion_path, "metadata_summary.json")
    if not os.path.exists(resumen_path):
        print(f"❌ No se encontró: {resumen_path}")
        return

    with open(resumen_path) as f:
        data = json.load(f)

    output_dir = os.path.join(composicion_path, "graficas_metricas")
    os.makedirs(output_dir, exist_ok=True)

    # Convertir en DataFrame
    filas = []
    for sesion, modelos in data.items():
        for modelo, metricas in modelos.items():
            fila = {"sesion": sesion, "modelo": modelo}
            fila.update(metricas)
            filas.append(fila)
    df = pd.DataFrame(filas)

    # Gráficas de líneas por métrica
    for metrica in ["entropia", "densidad", "variacion", "simetria"]:
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, x="sesion", y=metrica, hue="modelo", marker="o")
        plt.title(f"{metrica.capitalize()} por sesión")
        plt.xlabel("Sesión"); plt.ylabel(metrica.capitalize())
        plt.xticks(rotation=45); plt.grid(True); plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{metrica}_lineplot.png"))
        plt.close()

    # Boxplots por métrica
    for metrica in ["entropia", "densidad", "variacion", "simetria"]:
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df, x="modelo", y=metrica)
        plt.title(f"Distribución de {metrica}")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{metrica}_boxplot.png"))
        plt.close()

    # Heatmaps por modelo
    for modelo in ["gol1", "gol2", "regla90"]:
        subdf = df[df["modelo"] == modelo][["entropia", "densidad", "variacion", "simetria"]]
        plt.figure(figsize=(6, 5))
        corr = subdf.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title(f"Matriz de correlación - {modelo}")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{modelo}_correlacion.png"))
        plt.close()

    print(f"📊 Todas las gráficas guardadas en: {output_dir}")

# === MAIN ===
if __name__ == "__main__":
    base = "compositions"
    composiciones = sorted([d for d in os.listdir(base) if d.startswith("composicion_")])
    if not composiciones:
        print("❌ No se encontraron composiciones.")
        exit()

    for i, name in enumerate(composiciones):
        print(f"{i + 1}. {name}")
    choice = int(input("Selecciona una composición por número: ")) - 1
    seleccionada = os.path.join(base, composiciones[choice])

    visualizar_metricas(seleccionada)
