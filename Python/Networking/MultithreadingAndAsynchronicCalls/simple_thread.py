import threading


def f():
    print("Hello World!")


x = threading.Thread(target=f, args=())
x.start()
x.join()
