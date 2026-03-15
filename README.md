```
+--------------------------------------------------------------+
|                      Voice Agent MVP                         |
+--------------------------------------------------------------+

   [ Usuario ]
       |
       | habla
       v
+-------------------+
| ReSpeaker Mic In  |
+-------------------+
       |
       v
+------------------------------+
| Audio Input Adapter          |
| - selecciona device input    |
| - graba audio                |
| - guarda archivo             |
+------------------------------+
       |
       v
+------------------------------+
| Use Case: Record Audio       |
+------------------------------+
       |
       +------------------------------+
       |                              |
       | Etapa 1                      | Etapa 2
       v                              v
+----------------------+    +------------------------------+
| Audio Output Adapter |    | STT Adapter (OpenAI)         |
| - reproduce archivo  |    | - envía audio                |
| - usa ReSpeaker out  |    | - recibe texto               |
+----------------------+    +------------------------------+
       |                              |
       v                              v
 [ Usuario escucha ]          [ Terminal muestra texto ]
                                      |
                                      | Etapa 3
                                      v
                           +------------------------------+
                           | TTS Adapter (OpenAI)         |
                           | - envía texto                |
                           | - recibe/genera audio        |
                           +------------------------------+
                                      |
                                      v
                           +------------------------------+
                           | Audio Output Adapter         |
                           | - reproduce audio generado   |
                           +------------------------------+
                                      |
                                      v
                              [ Usuario escucha ]


```

# voice-agent

PoC/MVP de agente de voz en Python.

## Etapa 1
- grabar audio desde un dispositivo ALSA/ReSpeaker
- guardar un archivo WAV
- reproducir ese mismo archivo

## Etapa 2
- tomar un archivo WAV
- enviarlo a OpenAI STT
- mostrar la transcripción en terminal

## Requisitos del sistema
- Python 3.12
- Linux
- alsa-utils instalado

## Configuración rápida

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env


# voice-agent

PoC/MVP de agente de voz en Python.

## Etapa 1
- grabar audio desde un dispositivo ALSA/ReSpeaker
- guardar un archivo WAV
- reproducir ese mismo archivo

## Etapa 2
- tomar un archivo de audio
- enviarlo a OpenAI STT
- mostrar la transcripción en terminal

## Etapa 3
- tomar un texto
- enviarlo a OpenAI TTS
- guardar un archivo de audio generado

## Requisitos del sistema
- Python 3.12
- Linux
- alsa-utils instalado

## Configuración rápida

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env


# voice-agent

PoC/MVP de agente de voz en Python.

## Etapa 1
- grabar audio desde un dispositivo ALSA/ReSpeaker
- guardar un archivo WAV
- reproducir ese mismo archivo

## Etapa 2
- tomar un archivo de audio
- enviarlo a OpenAI STT
- mostrar la transcripción en terminal

## Etapa 3
- tomar un texto
- enviarlo a OpenAI TTS
- guardar un archivo de audio generado

## Etapa 4
- grabar audio del usuario
- transcribirlo
- consultar al LLM
- sintetizar la respuesta
- reproducir el audio generado

## Requisitos del sistema
- Python 3.12
- Linux
- alsa-utils instalado

## Configuración rápida

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env