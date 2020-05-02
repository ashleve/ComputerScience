#include <stdio.h>
#include <stdlib.h>
#include <signal.h>


int main(int argc, char **argv)
{
    pid_t process_id;
    int signal_number;
    union sigval signal_data;

    if(argc < 4)
    {
        printf("Error: incorrect number of arguments.");
        return -1;
    }

    process_id = strtol(argv[1], NULL, 10);
    signal_number = strtol(argv[2], NULL, 10);
    signal_data.sival_int = strtol(argv[3], NULL, 10);

    if(process_id < 0 || signal_number < 0){
        printf("Error: incorrect arguments.");
        return -1;
    }

    sigqueue(process_id, signal_number, signal_data);
    printf("Do procesu o id %d wyslano  sygnal %d i dane: %d", process_id, signal_number, signal_data.sival_int);

    return 0;
}
