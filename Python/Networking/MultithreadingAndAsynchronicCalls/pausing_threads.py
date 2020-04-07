from threading import Thread, Event
from time import sleep


class ThreadWithPause:

    def __init__(self, thread_nr):
        # started thread is suspended by default
        self.event = Event()
        self.thread_nr = 0 if thread_nr == 10 else thread_nr

    def function(self):
        while True:
            self.event.wait()

            for i in range(65, 91):
                message = "" + chr(i) + str(self.thread_nr)
                print(message)

            sleep(1)

    def pause(self):
        self.event.clear()

    def resume(self):
        self.event.set()


def resume_threads(threads, first, last):
    for i in range(first-1, last):
        threads[i].resume()


def pause_threads(threads, first, last):
    for i in range(first-1, last):
        threads[i].pause()


def main():
    threads = []
    for i in range(1, 11):
        t = ThreadWithPause(thread_nr=i)
        Thread(target=t.function, args=()).start()
        threads.append(t)

    print("All threads are suspended.")

    print("Available commands:\n"
          "start x\n"
          "stop x\n"
          "start x-y\n"
          "stop x-y\n")

    while True:
        in_str = input("Type command: ")

        if in_str.find(" ") == -1:
            print("Incorrect command.")
            continue

        splitted = in_str.split(" ")
        first_arg = splitted[0]
        second_arg = splitted[1]

        if second_arg.find("-") != -1:
            t_numbers = splitted[1].split("-")
            first_t_nr = int(t_numbers[0])
            last_t_nr = int(t_numbers[1])
        else:
            first_t_nr = int(second_arg)
            last_t_nr = first_t_nr

        if first_t_nr < 1 or first_t_nr > 10 or last_t_nr < 1 or last_t_nr > 10 or last_t_nr < first_t_nr:
            print("Incorrect command.")
            continue

        if first_arg == "start":
            resume_threads(threads, first_t_nr, last_t_nr)
        elif first_arg == "stop":
            pause_threads(threads, first_t_nr, last_t_nr)
        else:
            print("Incorrect command.")


if __name__ == "__main__":
    main()
