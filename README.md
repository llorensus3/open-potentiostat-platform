# 🧪 Electrochemical Characterization of Supercapacitors (Gamry 600+)

This repository contains a **complete experimental and analysis workflow** for the characterization of **small supercapacitor cells (mF range)** assembled in **Swagelok cells (Ø 12 mm electrodes)**.

The workflow is designed for **master-level laboratory training** and includes:
- experimental protocols (Gamry Reference 600+)
- automated data analysis (Python)
- example datasets
- reproducible figures

---

## 🎯 Objectives

- Understand electrochemical characterization techniques:
  - Cyclic Voltammetry (CV)
  - Galvanostatic Charge/Discharge (GCD)
  - Electrochemical Impedance Spectroscopy (EIS)

- Extract key parameters:
  - Capacitance
  - Equivalent Series Resistance (ESR)
  - Frequency response

- Compare experimental methods and identify non-ideal behavior

---

## ⚙️ Experimental Setup

**Cell type:** Swagelok  
**Electrodes:** circular, Ø 12 mm  
**Configuration:** two-electrode full cell  

### Connection (Gamry 600+)

| Terminal | Connection |
|--------|----------|
| WE + WS | Positive electrode |
| CE + RE | Negative electrode |

---

## 📊 Measurement Workflow

1. Measure Open Circuit Voltage (OCV)
2. Perform **EIS** at OCV
3. Perform **CV** at low scan rate
4. Repeat CV at higher scan rates
5. Perform **GCD**
6. (Optional) Leakage / self-discharge

---

## 📁 Repository Structure

```text
docs/
  experiments/
    gamry_supercapacitor_swagelok.md

software/
  analysis/
    analyze_cv_supercap.py
    analyze_gcd_supercap.py
    analyze_eis_supercap.py

data/
  examples/
    supercap_cv_example.csv
    supercap_gcd_example.csv
    supercap_eis_example.csv
# 🔬 Open Potentiostat Platform

An open-source potentiostat platform for **electrochemical measurements**, combining:

* ⚡ **ESP32** → real-time control
* 🧠 **Raspberry Pi** → high-level processing, logging, and analysis

Designed for:

* 🎓 Advanced engineering education
* 🧪 Electrochemical research
* 🔋 Energy systems (batteries, hydrogen, sensors)

---

## 🚀 Overview

<p align="center">
  <img src="images/open_potentiostat_architecture.svg" width="950"/>
</p>

<p align="center">
  <em>Hybrid architecture separating real-time control (ESP32) and high-level processing (Raspberry Pi).</em>
</p>

---

## 🧠 System Concept

<p align="center">
  <img src="images/open_potentiostat_conceptual_electronics.svg" width="950"/>
</p>

<p align="center">
  <em>Conceptual analog front-end including RE buffer, servo amplifier, TIA current measurement, DAC/ADC interface, and electrochemical cell.</em>
</p>

---

## 🧪 Supported Techniques

* Chronoamperometry (CA)
* Cyclic Voltammetry (CV)
* (Planned) Electrochemical Impedance Spectroscopy (EIS)

---

## ⚙️ Architecture

### 🔌 Hardware

* Analog front-end:

  * RE buffer
  * Servo amplifier
  * Transimpedance amplifier (TIA)
* ESP32 control board
* Raspberry Pi host

### 💻 Firmware

* Real-time experiment control
* Timing-critical DAC/ADC handling
* Serial communication protocol

### 📡 Software (Raspberry Pi)

* Experiment orchestration
* Data logging
* Visualization and analysis

---

## 📦 Repository Structure

```text
docs/                → Documentation and experiments
hardware/            → Analog front-end and PCB design
firmware/esp32/      → Embedded control firmware
software/raspberry/  → Host tools and scripts
protocols/           → Serial communication protocol
data/examples/       → Example datasets
images/              → Diagrams and figures
```

---

## 🧪 Experiments

* [Chronoamperometry](docs/experiments/chronoamperometry.md)
* [Cyclic Voltammetry](docs/experiments/cyclic_voltammetry.md)

---
## 📈 EIS Model Fitting

- `software/analysis/fit_randles_eis.py`

Example:

```bash
python software/analysis/fit_randles_eis.py data/examples/supercap_eis_example.csv

## 📡 Communication Protocol

* [Serial Protocol Examples](protocols/serial_protocol_examples.md)

---

## 📊 Data Analysis

### Python tools

* `plot_ca.py`
* `plot_cv.py`

### Example usage

```bash
cd software/raspberry
python plot_cv.py ../../data/examples/cv_example.csv --show
```

---

## 📁 Example Data

* `data/examples/ca_example.csv`
* `data/examples/cv_example.csv`

---

## 🎯 Educational Value

This platform is designed as a **teaching tool** for:

* Electrochemistry fundamentals
* Instrumentation design
* Embedded systems (ESP32)
* Data acquisition and signal processing
* Experimental validation and analysis

---

## 🔬 Research Applications

* Battery characterization (Li-ion, LiFePO₄)
* Hydrogen production systems (electrolysis)
* Surface analysis using electrochemical methods
* Sensor development

---

## ⚠️ Limitations (Current Version)

* Not yet calibrated against commercial potentiostats
* Limited precision depending on ADC/DAC selection
* Analog front-end still under iterative design

---

## 🚧 Roadmap

* [ ] Analog front-end v1 validation
* [ ] Calibration workflow
* [ ] Comparison with Gamry reference system
* [ ] EIS implementation
* [ ] GUI for experiment control

---

## 🤝 Contributing

Contributions are welcome!

* Hardware improvements
* Firmware optimization
* New electrochemical techniques
* Data analysis tools

---

## 📜 License

MIT License

---

## 📖 Citation

If you use this project in research or teaching:

```text
Servera, L. (2026). Open Potentiostat Platform.
```

---

## ⭐ Acknowledgements

Inspired by classical potentiostat architectures and modern open hardware initiatives.

