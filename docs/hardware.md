# Hardware notes

Recommended board separation:
- analog front-end board
- digital control board

## Analog front-end

Suggested functional blocks:
- RE high-impedance buffer
- servo amplifier for CE drive
- TIA with switched feedback resistors
- optional differential measurement channel

## Design priorities

- low leakage
- stable loop compensation
- careful grounding
- low-noise analog rails
- protection for RE, WE, and CE connectors
