# Firmware notes

The ESP32 firmware should:
- parse JSON commands from serial
- configure experiment modes
- execute deterministic acquisition loops
- stream measurements back to the host

Suggested states:
- IDLE
- RUN_CA
- RUN_CV
- RUN_CP
- FAULT
