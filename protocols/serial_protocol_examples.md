# 📡 Serial Protocol Examples

This document contains practical examples of the JSON-based serial protocol used between the **Raspberry Pi host** and the **ESP32 controller**.

Communication is line-based:
- one JSON object per line
- UTF-8 text
- newline (`\n`) terminates each message

---

## General Format

### Command sent from host
```json
{"cmd":"ping"}
```

### Response from controller
```json
{"status":"ok","device":"potentiostat-esp32","fw":"0.1.0"}
```

---

## 1. Ping

### Request
```json
{"cmd":"ping"}
```

### Response
```json
{"status":"ok","device":"potentiostat-esp32","fw":"0.1.0"}
```

Purpose:
- verify communication
- detect firmware version
- confirm device presence

---

## 2. Read a Single Sample

### Request
```json
{"cmd":"read_once"}
```

### Response
```json
{"status":"ok","t_ms":1234,"v_re":2.4312,"v_tia":2.4981,"e_we":0.0688,"i_a":1.9e-7,"range":"1uA"}
```

Fields:
- `t_ms`: timestamp in milliseconds
- `v_re`: buffered reference electrode voltage
- `v_tia`: TIA output voltage
- `e_we`: estimated working electrode potential
- `i_a`: measured current in amperes
- `range`: active current range

---

## 3. Set Current Range

### Request
```json
{"cmd":"set_range","range":"10uA"}
```

### Response
```json
{"status":"ok","range":"10uA"}
```

Typical ranges:
- `100mA`
- `10mA`
- `1mA`
- `100uA`
- `10uA`
- `1uA`
- `100nA`

---

## 4. Set DAC Manually

### Request
```json
{"cmd":"set_dac","voltage":1.250}
```

### Response
```json
{"status":"ok","voltage":1.25}
```

Use this for:
- debugging
- calibration
- manual tests

---

## 5. Start Chronoamperometry

### Request
```json
{"cmd":"start_ca","set_voltage":1.20,"duration_s":20.0,"range":"10uA","dt_ms":20}
```

### Response
```json
{"status":"ok","mode":"CA"}
```

### Streamed data
```json
{"type":"data","t_ms":0,"v_cmd":1.20,"v_re":2.10,"v_tia":2.49,"e_we":0.40,"i_a":1.0e-7,"range":"10uA"}
{"type":"data","t_ms":20,"v_cmd":1.20,"v_re":2.11,"v_tia":2.48,"e_we":0.39,"i_a":2.0e-7,"range":"10uA"}
```

### Completion event
```json
{"type":"event","event":"experiment_complete","mode":"CA"}
```

---

## 6. Start Cyclic Voltammetry

### Request
```json
{"cmd":"start_cv","v_start":1.0,"v1":1.8,"v2":0.8,"scan_rate":0.05,"range":"100uA","dt_ms":20}
```

### Response
```json
{"status":"ok","mode":"CV"}
```

### Streamed data
```json
{"type":"data","t_ms":100,"v_cmd":1.005,"v_re":2.16,"v_tia":2.45,"e_we":0.34,"i_a":5.0e-6,"range":"100uA"}
```

### Completion event
```json
{"type":"event","event":"experiment_complete","mode":"CV"}
```

---

## 7. Stop Current Experiment

### Request
```json
{"cmd":"stop"}
```

### Response
```json
{"status":"stopped"}
```

---

## 8. Error Messages

### Bad JSON
```json
{"status":"error","code":"bad_json"}
```

### Unknown command
```json
{"status":"error","code":"unknown_command"}
```

### Invalid range
```json
{"status":"error","code":"invalid_range"}
```

### TIA saturation
```json
{"status":"error","code":"tia_saturation"}
```

### ADC fault
```json
{"status":"error","code":"adc_fault"}
```

---

## 9. Recommended Host Workflow

1. Send `ping`
2. Optionally send `read_once`
3. Set range if needed
4. Start experiment (`start_ca` or `start_cv`)
5. Read all streamed `data` packets
6. Detect final `event`
7. Save data to CSV

---

## 10. Notes for Developers

- Keep one JSON object per line
- Always terminate messages with `\n`
- Prefer explicit field names
- Include units in documentation, not in keys
- Use `type:"data"` and `type:"event"` for streamed messages

---

## 11. Example Python Send Command

```python
import json
import serial

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
payload = {"cmd":"start_ca","set_voltage":1.2,"duration_s":10,"range":"10uA","dt_ms":20}
ser.write((json.dumps(payload) + "\n").encode())
print(ser.readline().decode())
```
