"""
Standalone diagnostic for FT232RL RS485 DMX stick.
Run directly: python3 dmx_ft232_test.py
Adjust PORT below if needed.
"""
import serial
import time

PORT = "/dev/ttyUSB0"
FIXTURES = [10, 20, 30]  # DMX start channels for each fixture

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

# Build a frame with proper RF1/RF4 values for each fixture.
# Sending 200 to every channel hits strobe (CH2) and macro (CH9) which
# suppress color output — this sets them correctly.
data = bytearray(513)  # index 0 = start code, rest = channels
for ch in FIXTURES:
    data[ch + 0] = 255  # CH1: Dimmer full
    data[ch + 1] = 0    # CH2: Strobe off
    data[ch + 2] = 255  # CH3: Red full
    data[ch + 3] = 0    # CH4: Green
    data[ch + 4] = 0    # CH5: Blue
    data[ch + 5] = 0    # CH6: White
    data[ch + 6] = 0    # CH7: Amber
    data[ch + 7] = 0    # CH8: UV
    data[ch + 8] = 0    # CH9: Macro off (manual color mode)
    data[ch + 9] = 0    # CH10: Speed
frame = bytes(data)

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
