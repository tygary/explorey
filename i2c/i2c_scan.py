"""
Run this to find what I2C addresses are visible on the bus and through the multiplexer.
"""
import board
import adafruit_tca9548a

i2c = board.I2C()

print("=== Direct I2C scan ===")
while not i2c.try_lock():
    pass
try:
    devices = i2c.scan()
    if devices:
        for addr in devices:
            print(f"  Found device at 0x{addr:02x}")
    else:
        print("  No devices found")
finally:
    i2c.unlock()

print("\n=== Scan through TCA9548A channels ===")
try:
    tca = adafruit_tca9548a.TCA9548A(i2c)
    for channel in range(8):
        ch = tca[channel]
        while not ch.try_lock():
            pass
        try:
            devices = ch.scan()
            filtered = [d for d in devices if d != 0x70]
            if filtered:
                for addr in filtered:
                    print(f"  Channel {channel}: 0x{addr:02x}")
        finally:
            ch.unlock()
except Exception as e:
    print(f"  Could not reach multiplexer: {e}")
