# Serial JSON protocol

## Example commands

```json
{"cmd":"ping"}
{"cmd":"read_once"}
{"cmd":"start_ca","set_voltage":1.2,"duration_s":10,"range":"10uA","dt_ms":20}
{"cmd":"start_cv","v_start":1.0,"v1":1.8,"v2":0.8,"scan_rate":0.05,"range":"100uA","dt_ms":20}
{"cmd":"stop"}
```

## Example streamed data

```json
{"type":"data","t_ms":100,"v_cmd":1.2,"v_re":2.10,"v_tia":2.48,"e_we":0.40,"i_a":2e-7,"range":"10uA"}
```
