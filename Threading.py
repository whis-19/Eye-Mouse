from Imports import *

def threadFunction(func, *args, **kwargs):
    print(f"Thread initialized for {func.__name__} with arguments: {args} {kwargs}")
    result = func(*args, **kwargs)
    print(f"Thread for {func.__name__} has finished. Result: {result}")

def runInThread(func, *args, **kwargs):
    thread = threading.Thread(target=threadFunction, args=(func,) + args, kwargs=kwargs)
    thread.start()
    return thread