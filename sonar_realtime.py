# ===============================================================
#  SONAR REALTIME LAM - Lectura en vivo desde Arduino
#  
#  LICEO AERONÁUTICO MILITAR - PROMOCIÓN 46
#  Proyecto SONAR 2025
#  Autor: Cicolini - Franchi - Méndez - Santacroce
#
# ===============================================================

import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sounddevice as sd
from datetime import datetime

# ------------------ CONFIGURACIÓN ------------------
PUERTO = 'COM3'        # ⚠️ Cambiar según tu PC (ej: 'COM4' o '/dev/ttyUSB0')
BAUDIOS = 9600
TIMEOUT = 1
RANGO_MAX = 200         # cm
FS = 44100              # frecuencia de muestreo para sonido

# ------------------ FUNCIONES DE SONIDO ------------------
def sonar_ping(frecuencia=1000, duracion=0.08, volumen=0.5):
    """Ping agudo corto estilo radar USAF"""
    try:
        t = np.linspace(0, duracion, int(FS * duracion), False)
        onda = np.sin(frecuencia * 2 * np.pi * t) * volumen
        sd.play(onda, FS, blocking=False)
    except Exception as e:
        print("⚠️ Error en sonar_ping:", e)

def beep_objeto(frecuencia=1400, duracion=0.2, volumen=0.8):
    """Beep fuerte estilo contacto radar"""
    t = np.linspace(0, duracion, int(FS * duracion), False)
    onda = np.sin(frecuencia * 2 * np.pi * t) * volumen
    sd.play(onda, FS, blocking=True)

def timestamp_militar():
    """Devuelve timestamp en formato militar (DTG)."""
    ahora = datetime.utcnow()
    return ahora.strftime("%d%H%MZ %b %y").upper()

# ------------------ CONEXIÓN SERIAL ------------------
try:
    arduino = serial.Serial(PUERTO, BAUDIOS, timeout=TIMEOUT)
    time.sleep(2)
    print(f"✅ Conectado al Arduino en {PUERTO}")
except Exception as e:
    print("❌ No se pudo conectar al Arduino:", e)
    exit()

# ------------------ INTERFAZ GRÁFICA ------------------
fig = plt.figure(figsize=(18, 12), facecolor="black")
fig.canvas.manager.set_window_title("LAM SONAR - REALTIME")

# --- RADAR POLAR ---
ax = fig.add_axes([0.05, 0.05, 0.9, 0.7], polar=True)
ax.set_theta_offset(0)
ax.set_theta_direction(1)
ax.set_thetamin(0)
ax.set_thetamax(180)
ax.set_rlim(0, RANGO_MAX)
ax.set_facecolor("black")
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)

# --- GRILLA VERDE ---
for r in np.linspace(40, RANGO_MAX, 5):
    ax.plot(np.linspace(0, np.pi, 300), [r]*300, color="lime", linestyle="--", linewidth=0.5)
for angle in np.linspace(0, np.pi, 9):
    ax.plot([angle, angle], [0, RANGO_MAX], color="lime", linestyle="--", linewidth=0.5)

# --- ENCABEZADO ---
plt.figtext(0.5, 0.97, "LICEO AERONÁUTICO MILITAR",
            ha="center", va="top", fontsize=24, color="lime", fontweight="bold")
plt.figtext(0.5, 0.92, "PROMOCIÓN 46",
            ha="center", va="top", fontsize=18, color="lime")
plt.figtext(0.5, 0.88,
            "GRUPO: CAD II AÑO Cicolini, CAD II Franchi, CAD II Méndez y CAD II Santacroce",
            ha="center", va="top", fontsize=12, color="lime")

# --- LOGOS (opcional) ---
imagenes = [
    "images.png",
    "Flag_of_Argentina.svg.png",
    "LAM_Cuerpo_de_Cadetes_1982_FAA_parche.png"
]
posiciones = [0.33, 0.5, 0.70]

for img_path, pos in zip(imagenes, posiciones):
    try:
        img = mpimg.imread(img_path)
        ax_img = fig.add_axes([pos - 0.08, 0.70, 0.16, 0.1])
        ax_img.imshow(img)
        ax_img.axis("off")
    except:
        pass

# --- PANEL DE CONTACTOS (parte inferior derecha) ---
ax_panel = fig.add_axes([0.80, 0.02, 0.23, 0.7])
ax_panel.set_facecolor("black")
ax_panel.axis("off")

texto_titulo = ax_panel.text(0, 1.0, "CONTACTOS: 0",
                             ha="left", va="top",
                             fontsize=14, color="lime",
                             family="monospace")

texto_log = ax_panel.text(0, 0.95, "",
                          ha="left", va="top",
                          fontsize=10, color="lime",
                          family="monospace")

# --- VARIABLES DE RASTRO ---
linea_barrido = None
rastros = []
max_rastro = 80
log_contactos = []

# ------------------ LOOP PRINCIPAL ------------------
while True:
    # Barrido simulado (el ángulo viene desde Arduino)
    try:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode().strip()
            if "," in data:
                angulo, distancia = map(int, data.split(","))
                theta = np.radians(angulo)

                # Reproducir ping cada cierto ángulo
                if angulo % 10 == 0:
                    sonar_ping()

                # Limpiar línea previa
                if linea_barrido:
                    linea_barrido.remove()

                # Dibujar línea de barrido
                linea_barrido, = ax.plot([theta, theta], [0, RANGO_MAX],
                                         color="lime", linewidth=2, alpha=0.6)

                # Rastro visual
                rastro = ax.fill_between([theta - 0.02, theta], 0, RANGO_MAX,
                                         color="lime", alpha=0.1)
                rastros.append(rastro)
                if len(rastros) > max_rastro:
                    rastros[0].remove()
                    rastros.pop(0)

                # Dibujar punto detectado
                if 0 < distancia < RANGO_MAX:
                    ax.plot(theta, distancia, 'ro', markersize=8)
                    beep_objeto()
                    registro = f"{timestamp_militar()} | BRG {angulo:03d}° RNG {distancia}cm"
                    log_contactos.append(registro)
                    if len(log_contactos) > 40:
                        log_contactos.pop(0)

                # Actualizar panel lateral
                texto_titulo.set_text(f"CONTACTOS: {len(log_contactos)}")
                texto_log.set_text("\n".join(log_contactos[-20:]))  # muestra los últimos

                plt.pause(0.001)

    except KeyboardInterrupt:
        print("\n🛑 Simulación interrumpida por el usuario.")
        break
    except Exception as e:
        print("⚠️ Error en lectura:", e)
