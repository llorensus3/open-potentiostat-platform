# System architecture

## Main blocks

- **Analog front-end**
  - reference electrode buffer
  - control amplifier / servo stage
  - transimpedance amplifier
  - current range switching
- **ESP32**
  - experiment sequencing
  - DAC control
  - ADC acquisition
  - relay control
  - fault detection
- **Raspberry Pi**
  - GUI
  - logging
  - plotting
  - experiment configuration
  - post-processing

## Recommended communication

Use **USB serial with JSON messages** for the first versions.
