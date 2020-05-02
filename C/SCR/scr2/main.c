#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <mqueue.h>
#include <string.h>
#include <sys/mman.h>
#include <time.h>
#include <semaphore.h>

#define SEMAPHORE_NAME "the_semaphore"
#define MEMORY_NAME  "the_memory"
#define QUEUE_NAME  "/the_queue"    // this needs to have slash at the beginning


void run_server(mqd_t m_queue);
void run_client(mqd_t m_queue);
void sort_arr(int *addr, int size);

struct msg_buffer {
    int size;           // size of shared memory
    char text[100];     // name id of shared memory
} message;


int main(void) {
    printf("Program just started...!\n");

    // unlink just in case...
    mq_unlink(QUEUE_NAME);

    struct mq_attr attr;
    attr.mq_flags = 0;
    attr.mq_maxmsg = 8;
    attr.mq_curmsgs = 0;
    attr.mq_msgsize = sizeof(message);

    // creates a message queue
    mqd_t m_queue = mq_open(QUEUE_NAME, O_RDWR | O_CREAT, 0777, &attr);


    if (fork() != 0) {
        run_server(m_queue);
    } else {
        run_client(m_queue);
    }

    return EXIT_SUCCESS;
}


void sort_arr(int *addr, int size) {
    for (unsigned int i = 0; i < size; i++) {
        for (unsigned int j = 0; j < size; j++) {
            if (addr[j] < addr[j + 1]) {
                addr[j] += addr[j + 1];
                addr[j + 1] = addr[j] - addr[j + 1];
                addr[j] -= addr[j + 1];
            }
        }
    }
}


void run_server(mqd_t m_queue) {
    printf("(SERVER): start!\n");

    printf("(SERVER): waiting for message...\n");
    mq_receive(m_queue, (char *) &message, sizeof(message), 0);
    printf("(SERVER): message received, size=%d, text='%s'\n", message.size, message.text);
    int mem_size = message.size;

    printf("(SERVER): memory mapping...\n");
    int fd = shm_open(MEMORY_NAME, O_RDWR | O_CREAT, 0777);
    ftruncate(fd, mem_size * sizeof(int));  // truncate size of shared memory to the given value
    int *addr = (int *) mmap(0, mem_size * sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0); // map memory
//    printf("%p", addr);

    printf("(SERVER): sorting data...\n");
    sort_arr(addr, mem_size);

    printf("(SERVER): releasing memory access...\n");
    sem_t *sem = sem_open(SEMAPHORE_NAME, O_CREAT, 0600, 0);
    sem_post(sem);   // release client

    printf("(SERVER): collecting garbage...\n");
//    munmap(addr, mem_size * sizeof(int));
    mq_close(m_queue);
    mq_unlink(QUEUE_NAME);
    sem_close(sem);
    sem_unlink(SEMAPHORE_NAME);

    printf("(SERVER): server closed!\n");
}


void run_client(mqd_t m_queue) {
    printf("(CLIENT): start!\n");

    printf("(CLIENT): initializing shared memory...\n");
    size_t mem_size = 10;
    int fd = shm_open(MEMORY_NAME, O_RDWR | O_CREAT, 0777); // create shared memory
    ftruncate(fd, mem_size * sizeof(int));  // truncate size of shared memory to the given value
    int *addr = (int *) mmap(0, mem_size * sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0); // map memory
//    printf("%p", addr);

    printf("(CLIENT): writing data to the shared memory...\n");
    printf("data: ");
    srand(time(NULL));
    for (unsigned int i = 0; i < mem_size; i++) {
        addr[i] = rand() % 11;  // random integer between 0 and 10
        printf("%d ", addr[i]);
    }
    printf("\n");

    message.size = mem_size;
    strcpy(message.text, MEMORY_NAME);
    printf("(CLIENT): sending message, size=%d, text='%s'\n", message.size, message.text);
    mq_send(m_queue, (char *) &message, sizeof(message), 1);

    printf("(CLIENT): waiting for memory access...\n");
    sem_t *sem = sem_open(SEMAPHORE_NAME, O_CREAT, 0600, 0);
    sem_wait(sem);   // waits until server does sem_post()

    printf("(CLIENT) reading data...\n");
    printf("data: ");
    for (unsigned int i = 0; i < mem_size; i++)
        printf("%d ", addr[i]);
    printf("\n");

    printf("(CLIENT) collecting garbage...\n");
    munmap(addr, mem_size * sizeof(int));
    mq_close(m_queue);
    mq_unlink(QUEUE_NAME);
    sem_close(sem);
    sem_unlink(SEMAPHORE_NAME);

    printf("(CLIENT): client closed!\n");
}