# Open Potentiostat Platform

Open electrochemical instrumentation platform for **research** and **master-level teaching**.

## Overview

This repository contains the foundations of a modular open potentiostat platform designed for:

- **research validation and comparison** against commercial instruments
- **master-level teaching** in electrochemistry, instrumentation, embedded systems, and data acquisition
- **project-based learning** for laboratory courses, MSc theses, and research prototypes

The platform is based on a hybrid architecture:

- **ESP32** as the embedded experiment controller
- **Raspberry Pi** as the host for GUI, logging, plotting, and advanced processing
- a dedicated **analog front-end** for RE buffering, servo control, and TIA current measurement

## Educational goals

Students should be able to:

- understand the role of **WE, RE, and CE**
- analyze the operation of a **potentiostat control loop**
- study the function of the **reference buffer**, **TIA**, and **servo amplifier**
- perform **chronoamperometry (CA)** and **cyclic voltammetry (CV)**
- understand the basis of **electrochemical impedance spectroscopy (EIS)**
- compare open instrumentation with commercial systems such as **Gamry**

## Research goals

This platform is intended as a starting point for:

- validation against commercial potentiostats
- battery characterization
- electrolyzer and hydrogen-related measurements
- corrosion and sensor experiments
- development of reproducible laboratory workflows

## Current status

This repository is a **starter framework**. It is not yet a validated scientific instrument.

Implemented or scaffolded:

- repository structure
- documentation skeleton
- ESP32 firmware skeleton
- Raspberry Pi host skeleton
- serial JSON protocol definition
- starter examples and teaching materials

Not yet complete:

- validated hardware design
- calibrated acquisition chain
- full safety and fault management
- auto-ranging
- robust EIS acquisition pipeline

## Repository structure

```text
open-potentiostat-platform/
├── docs/
├── hardware/
├── firmware/
├── software/
├── protocols/
├── examples/
├── data/
├── images/
└── .github/
```

## Quick start

### 1. Hardware
Build or adapt:
- analog front-end board
- ESP32 control board
- Raspberry Pi host

### 2. Firmware
Use PlatformIO for the ESP32 firmware:

```bash
cd firmware/esp32
pio run
pio run -t upload
pio device monitor
```

### 3. Raspberry Pi host
Install Python dependencies and run the host tools:

```bash
cd software/raspberry
pip install -r requirements.txt
python example_run.py
```

## Roadmap

- **v0.1**: CA basic acquisition
- **v0.2**: CV basic acquisition
- **v0.3**: range switching and saturation detection
- **v0.4**: calibration workflow
- **v0.5**: GUI integration
- **v1.0**: basic EIS support

## Safety notice

This project is intended for **laboratory development and teaching only**.

It is **not** a certified instrument. Always validate:
- loop stability
- current and voltage limits
- input protection
- isolation strategy
- measurement accuracy

Read [`docs/safety.md`](docs/safety.md) before using the platform in a lab.

## Citation

If you use this repository in teaching materials, projects, or publications, please cite it using the metadata in [`CITATION.cff`](CITATION.cff).

## Contributing

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening issues or pull requests.
