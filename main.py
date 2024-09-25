from Func import *

# Main program
if __name__ == "__main__":
    thread = startEyeControlledMouse()
    isRunning.set()  # Set the flag to True

    try:
        while isRunning.is_set():
            if keyboard.is_pressed('del'):  # Check if 'del' key is pressed
                isRunning.clear()  # Clear the flag to exit the loop
            time.sleep(0.1)
    except KeyboardInterrupt:
        stopEyeControlledMouse(thread)