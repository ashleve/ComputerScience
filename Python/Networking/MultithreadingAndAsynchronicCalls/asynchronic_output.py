import asyncio


async def print_message(nr):
    nr = 0 if nr == 10 else nr
    for i in range(65, 91):
        message = "" + chr(i) + str(nr)
        print(message)


async def repeat(nr):
    while True:
        await print_message(nr=nr)
        await asyncio.sleep(1)


async def controller(tasks):
    print("Available commands:\n"
          "delete x\n"
          "delete x-y\n")

    while True:
        await asyncio.sleep(1)

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

        if first_arg == "delete":
            delete_tasks(tasks, first_t_nr, last_t_nr)
        else:
            print("Incorrect command.")


def delete_tasks(tasks, first, last):
    for i in range(first-1, last):
        tasks[i].cancel()


def main():
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(1, 11):
        task = loop.create_task(repeat(nr=i))
        tasks.append(task)

    loop.create_task(controller(tasks))

    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
