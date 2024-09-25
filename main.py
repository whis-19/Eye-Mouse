from Func import *

# Main program
if __name__ == "__main__":
    thread = startEyeControlledMouse()
    isRunning.set() 

  
    listener_thread = threading.Thread(target=inputBuffer)
    listener_thread.start()

    try:
        while isRunning.is_set():
            time.sleep(0.1)  
    except KeyboardInterrupt:
        stopEyeControlledMouse(thread)

    listener_thread.join()  