G90 (Absolute)
G0 X0 Y0 (Go to Origin)
G0 Z10 (Move spindle up by 10mm for testing, remove this when done)
M0 (Pause Program)

M3 (Start Spindle)
F750 (Set Feed Speed)
M0 (Pause Program)
G1 X0 Y293 (Go to the top of the first column)
G1 X10 (Move over to Next Column)
G1 Y0 (Go back to the bottom)
M5 (Stop Spindle)

M30 (End Program)