# Decisiones - Etapa 1

## 1. Audio por ALSA del sistema
Se usa `arecord` y `aplay` en lugar de librerías Python de audio.

### Motivo
- menor complejidad inicial
- menos dependencias Python
- mejor alineado con Linux/Raspberry
- permite aislar problemas de hardware y drivers

## 2. Arquitectura por puertos y adaptadores
La aplicación depende de contratos abstractos (`AudioInputPort`, `AudioOutputPort`).

### Motivo
- facilita cambiar de hardware
- facilita cambiar de implementación de audio
- prepara el sistema para STT/TTS/LLM

## 3. WAV como formato inicial
Se guarda audio en WAV.

### Motivo
- formato simple
- compatible con herramientas ALSA
- útil para debug y trazabilidad

## 4. Etapa 1 sin OpenAI
La integración con OpenAI queda fuera de esta etapa.

### Motivo
- separar riesgo de audio local y riesgo de integración remota