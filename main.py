from Func import *

# Main program
if __name__ == "__main__":
    thread = startEyeControlledMouse()

    try:
        while isRunning.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        stopEyeControlledMouse(thread)