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

