# 🧪 Chronoamperometry Laboratory Practice 

## Overview

This laboratory session introduces **chronoamperometry (CA)** using the Open Potentiostat Platform.

Students apply a **potential step** and analyze the resulting **current–time response**, linking experimental observations with electrochemical theory and instrumentation behavior.

---

## 🎯 Learning Objectives

* Understand chronoamperometric measurements
* Interpret current transients ( I(t) )
* Distinguish between:

  * capacitive current
  * faradaic current
* Identify diffusion-controlled behavior
* Validate experimental data using **Cottrell law**
* Evaluate instrumentation limitations

---

## ⚙️ Experimental Setup

### Instrumentation

* Open Potentiostat Platform (ESP32 + Raspberry Pi)
* Analog front-end:

  * RE buffer
  * servo amplifier
  * transimpedance amplifier (TIA)
* Host software for acquisition and logging

### Electrochemical Cell

* Working Electrode (WE)
* Reference Electrode (RE)
* Counter Electrode (CE)

---

## 🔌 System Architecture

<p align="center">
  <img src="../../images/open_potentiostat_architecture.svg" width="800"/>
</p>

---

## ⚡ Experimental Principle

A potential step is applied:

[
E(t) =
\begin{cases}
E_1 & t < 0 \
E_2 & t \ge 0
\end{cases}
]

The measured current is:

[
I(t) = I_c(t) + I_f(t)
]

Where:

* ( I_c(t) ): capacitive current (double-layer charging)
* ( I_f(t) ): faradaic current (electrochemical reaction)

---

## 📉 Diffusion-Controlled Behavior

Under diffusion-limited conditions, the current follows the **Cottrell equation**:

[
I(t) = \frac{n F A C \sqrt{D}}{\sqrt{\pi t}}
]

Thus:

[
I \propto t^{-1/2}
]

---

## 🧪 Experimental Procedure

1. Connect WE, RE, and CE
2. Set initial potential ( E_1 )
3. Apply step to ( E_2 )
4. Record current for 5–20 s
5. Repeat experiment (≥3 times)

### Suggested Parameters

| Parameter | Value     |
| --------- | --------- |
| (E_1)     | 0 V       |
| (E_2)     | 0.5–1.2 V |
| Duration  | 10 s      |
| Sampling  | 1–10 ms   |

---

## 📊 Expected Results

### Current vs Time

* High initial current
* Fast decay (capacitive + faradaic)
* Slower long-time decay (diffusion-controlled)

```text
I
│\
│ \
│  \
│   \
│    \__
│       \___
└────────────── t
```

---

## 📈 Data Analysis

### 1. Plot ( I(t) )

Main experimental curve.

---

### 2. Plot ( I ) vs ( t^{-1/2} )

* Should be approximately linear if diffusion-controlled
* Deviations indicate non-ideal behavior

---

## 🧠 Physical Interpretation

| Region       | Interpretation                  |
| ------------ | ------------------------------- |
| Early time   | Double-layer charging dominates |
| Intermediate | Faradaic reaction + diffusion   |
| Long time    | Diffusion-limited regime        |

---

## ⚠️ Instrumentation Considerations

* TIA saturation
* ADC resolution
* DAC stability
* Sampling rate limitations
* Noise floor
* Control loop stability

---

## ❓ Questions

1. Why does current decrease over time?
2. What is the role of the reference electrode?
3. Why should the RE ideally draw no current?
4. Under what conditions does Cottrell law apply?
5. What causes deviations from ideal behavior?
6. How does sampling rate affect results?
7. What happens if current range is incorrect?
8. How to distinguish electrochemical vs instrumental effects?

---

## 🔬 Advanced Tasks (Optional)

* Compare multiple potentials
* Change current range
* Fit experimental data to Cottrell equation
* Compare with commercial potentiostat (Gamry)
* Evaluate noise vs resolution

---

## 📁 Suggested Data Format

```csv
time_s,voltage_v,current_a
0.000,0.50,1.2e-4
0.010,0.50,7.8e-5
0.020,0.50,6.1e-5
```

---

## 🚀 Integration with Platform

This experiment validates:

* DAC setpoint generation
* ADC acquisition
* TIA current measurement
* Firmware timing accuracy
* Data streaming protocol

---

## 📌 Conclusion

Chronoamperometry provides insight into:

* electrochemical kinetics
* diffusion processes
* instrumentation performance

It is a fundamental technique for both:

* **research validation**
* **advanced engineering education**
