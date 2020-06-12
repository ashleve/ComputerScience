#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <mqueue.h>
#include <signal.h>
#include "config.h"
#include "task.h"
#include "list.h"
#include "msg.h"


int create_server();

int accept_client(int fd);

void report(const char *msg, int terminate);

void read_message(char *buffer, int client_fd);

void write_message(char *buffer, int client_fd);

void create_task_timer_process(mqd_t m_queue, char *buffer0, char *buffer1, char *buffer2);

void update_task_list(mqd_t m_queue);

void delete_task(int id);


int main() {

    mqd_t m_queue = create_message_queue();

    int fd = create_server();

    while (1) {
        int client_fd = accept_client(fd);
        if (client_fd < 0) {
            report("accept", 0); /* don't terminate if there's a problem */
            continue;
        }

        /* read from client */
        char buffer0[BUFF_SIZE], buffer1[BUFF_SIZE], buffer2[BUFF_SIZE], buffer3[BUFF_SIZE];
        read_message(buffer0, client_fd);
        write_message(buffer0, client_fd);

        update_task_list(m_queue);

        if (!strcmp(buffer0, "schedule_task")) {
            read_message(buffer1, client_fd);
            write_message(buffer1, client_fd);
            read_message(buffer2, client_fd);
            write_message(buffer2, client_fd);
            read_message(buffer3, client_fd);
            write_message(buffer3, client_fd);

            if (display_logs)
                fprintf(stderr, "\nNew request: %s %s %s %s\n", buffer0, buffer1, buffer2, buffer3);

            create_task_timer_process(m_queue, buffer1, buffer2, buffer3);
        } else if (!strcmp(buffer0, "cancel_task")) {
            read_message(buffer1, client_fd);
            int task_id = atoi(buffer1);
            if (display_logs)
                fprintf(stderr, "New request: %s %i\n", buffer0, task_id);
            delete_task(task_id);
        } else if (!strcmp(buffer0, "get_info")) {
            if (display_logs)
                fprintf(stderr, "New request: %s\n", buffer0);
            char resp[BUFF_SIZE];
            get_task_info(resp);
            if (display_logs)
                fprintf(stderr, "%s", resp);
            write_message(resp, client_fd);
        } else if (!strcmp(buffer0, "exit")) {
            if (display_logs)
                fprintf(stderr, "New request: %s\n", buffer0);
            close(client_fd);
            close(fd);
            break;
        }

        close(client_fd); /* break connection */
    }

    return 0;
}


int create_server() {
    int fd = socket(AF_INET, /* network versus AF_LOCAL */
                    SOCK_STREAM, /* reliable, bidirectional, arbitrary payload size */
                    0); /* system picks underlying protocol (TCP) */
    if (fd < 0)
        report("socket", 1); /* terminate */

    /* bind the server's local address in memory */
    struct sockaddr_in saddr;
    memset(&saddr, 0, sizeof(saddr)); /* clear the bytes */
    saddr.sin_family = AF_INET; /* versus AF_LOCAL */
    saddr.sin_addr.s_addr = htonl(INADDR_ANY); /* host-to-network endian */
    saddr.sin_port = htons(PORT_NUMBER); /* for listening */
    if (bind(fd, (struct sockaddr *) &saddr, sizeof(saddr)) < 0)
        report("bind", 1); /* terminate */

    /* listen to the socket */
    if (listen(fd, MAX_CONNECTS) < 0) /* listen for clients, up to MAX_CONNECTS */
        report("listen", 1); /* terminate */

    if (display_logs)
        fprintf(stderr, "Listening on port %i for clients...\n", PORT_NUMBER);

    return fd;
}

int accept_client(int fd) {
    struct sockaddr_in caddr; /* client address */
    int len = sizeof(caddr); /* address length could change */
    int client_fd = accept(fd, (struct sockaddr *) &caddr, &len); /* accept blocks */
    if (display_logs)
        fprintf(stderr, "\nClient connected...\n");
    return client_fd;
}

void report(const char *msg, int terminate) {
    if (display_logs)
        perror(msg);
    if (terminate) exit(-1); /* failure */
}

void read_message(char *buffer, int client_fd) {
    memset(buffer, '\0', BUFF_SIZE);
    if (read(client_fd, buffer, BUFF_SIZE) <= 0) {
        if (display_logs)
            fprintf(stderr, "ERROR READ\n");
    }
}

void write_message(char *buffer, int client_fd) {
    if (write(client_fd, buffer, BUFF_SIZE) <= 0) {
        if (display_logs)
            fprintf(stderr, "ERROR WRITE\n");
    } /* echo as confirmation */
}

void create_task_timer_process(mqd_t m_queue, char *buffer0, char *buffer1, char *buffer2) {
    char path_with_args[BUFF_SIZE];
    strcpy(path_with_args, buffer0);
    unsigned long time = atoi(buffer1);
    int is_periodic = atoi(buffer2);

    pid_t pid = fork();
    if (pid == -1) {
        if (display_logs)
            printf("ERROR FORK");
        exit(EXIT_FAILURE);
    } else if (pid == 0) {
        schedule_task(m_queue, path_with_args, is_periodic, time * NANOSECONDS_IN_SEC);

        if (is_periodic) {
            // timer przerywa sleepa więc trzeba go ponawiać
            while (1) {
                sleep(1000000000);
            }
        } else {
            sleep(1000000000);
            exit(0);
        }
    } else {
        insertFirst((int) pid, is_periodic);
    }
}

void update_task_list(mqd_t m_queue) {
    struct timespec tm;
    tm.tv_sec = 0;
    tm.tv_nsec = 1;
    struct msg_buffer msg;

    int err;
    do {
        err = mq_timedreceive(m_queue, (char *) &msg, sizeof(msg), NULL, &tm);

        if (err != -1) {
            // remove task from list if exists
            struct node *success = delete(msg.id);
            if (success) {
                if (display_logs)
                    fprintf(stderr, "Task with id %i removed from list\n", msg.id);
            } else {
                if (display_logs)
                    fprintf(stderr, "Removing task %i from list failed\n", msg.id);
            }
        }

    } while (err != -1);
}

void delete_task(int id) {
    // remove task from list if exists
    struct node *success = delete(id);

    // kill task timer process
    if (success) {
        kill(id, SIGKILL);
    }
}