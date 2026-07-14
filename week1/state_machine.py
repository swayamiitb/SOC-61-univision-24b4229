"""Week 1: an event-driven camera state machine.

Demonstrates why a vision system should react to events instead of polling,
and how a state lock plus try/finally keeps it from deadlocking on a failure.
"""
import time

camera_state = "IDLE"
frames_processed = 0
MAX_BUFFER = 5


def hardware_interrupt_detected():
    """Stand-in for a hardware-level motion sensor interrupt."""
    return True


def grab_frame_buffer():
    """Stand-in for fetching a frame from VRAM."""
    time.sleep(0.1)
    return "raw_tensor_data"


def run():
    global camera_state, frames_processed
    while frames_processed < MAX_BUFFER:
        # only query the camera when the system is actually ready
        if hardware_interrupt_detected() and camera_state == "IDLE":
            camera_state = "ACQUIRING"
            try:
                frame = grab_frame_buffer()
                frames_processed += 1
                print(f"[{frames_processed}/{MAX_BUFFER}] acquired {frame}")
            finally:
                # always release the lock, even if grabbing the frame crashes
                camera_state = "IDLE"


if __name__ == "__main__":
    run()
    print("Done. Final state:", camera_state)
