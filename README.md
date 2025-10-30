# 🛰️ LICEO AERONÁUTICO MILITAR  
## PROMOCIÓN 46 – PROYECTO SONAR

![Liceo Aeronáutico Militar - Encabezado](./8c0b0588-dedc-46f6-8166-4742f694d874.png)

---

### 🧑‍🚀 GRUPO DE TRABAJO  
**CAD II Año Cicolini, CAD II Año Franchi, CAD II Año Méndez y CAD II Año Santacroce**

---

## 📡 Descripción del Proyecto

El **Proyecto SONAR** es una iniciativa académica desarrollada en el marco de la **Promoción 46 del Liceo Aeronáutico Militar (LAM)**, orientada a la **visualización de distancias y detección de objetos en tiempo real** mediante el uso de un sensor ultrasónico **HC-SR04**, un **servo SG90** y una interfaz gráfica desarrollada en **Python**.

El sistema realiza un **barrido angular de 0° a 180°**, midiendo distancias con precisión y generando un **radar visual** con sonido e interfaz gráfica, que representa los ecos detectados con puntos en movimiento.

---

## ⚙️ Componentes Utilizados

| Componente | Descripción |
|-------------|--------------|
| 🧠 **Arduino UNO** | Microcontrolador principal encargado de controlar el servo y leer las distancias del sensor. |
| 📶 **Sensor ultrasónico HC-SR04** | Mide la distancia al objeto mediante pulsos de sonido. |
| ⚙️ **Servo SG90** | Gira el sensor entre 0° y 180° para realizar el barrido. |
| 💡 **LED y buzzer** | Indican alertas cuando el objeto está a menos de 20 cm. |
| 💻 **Python (Matplotlib + PySerial)** | Programa que recibe los datos del Arduino y muestra el radar en tiempo real. |

---

## 🔬 Esquema de Funcionamiento

```text
HC-SR04 → mide distancia
↓
Arduino → envía “ángulo,distancia” por COM3
↓
Python (sonar_realtime.py) → muestra radar + sonidos
↓
Servo → sincronizado con el barrido visual
