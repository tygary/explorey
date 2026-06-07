"""
Standalone diagnostic for FT232RL RS485 DMX stick.
Run directly: python3 dmx_ft232_test.py
Adjust PORT below if needed.
"""
import serial
import time

PORT = "/dev/ttyUSB0"
CHANNEL_VALUE = 200  # bright enough to see if a light responds

print(f"Opening {PORT} ...")
try:
    s = serial.Serial(
        PORT,
        baudrate=250000,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        rtscts=False,
        dsrdtr=False,
        timeout=1,
    )
except Exception as e:
    print(f"FAILED to open port: {e}")
    raise SystemExit(1)

print(f"Opened. RTS={s.rts}  CTS={s.cts}  DSR={s.dsr}")

# DMX frame: start code 0x00 + 512 channels all at CHANNEL_VALUE
frame = bytes([0] + [CHANNEL_VALUE] * 512)

print("Sending DMX frames continuously.  Watch the wireless transmitter for activity.")
print("Press Ctrl-C to stop.\n")

attempt = 0
for rts_state in [True, False]:
    s.rts = rts_state
    print(f"--- Trying RTS={rts_state} ---")

    for method in ["break_condition", "baud_switch"]:
        print(f"    Method: {method}  (10 frames) ...", end=" ", flush=True)
        for _ in range(10):
            try:
                if method == "break_condition":
                    s.break_condition = True
                    time.sleep(0.0001)
                    s.break_condition = False
                    time.sleep(0.000012)
                    s.write(frame)
                    s.flush()
                else:
                    s.baudrate = 100000
                    s.write(b'\x00')
                    s.flush()
                    s.baudrate = 250000
                    s.write(frame)
                    s.flush()
                time.sleep(0.05)
            except Exception as e:
                print(f"ERROR: {e}")
                break
        print("done")

print("\nAll combinations tried.")
print("If the transmitter showed activity for ANY of them, note which RTS + method worked.")
s.close()
