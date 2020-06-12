//
// Created by ukasz on 06.06.2020.
//

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>
#include <mqueue.h>

#include "task.h"
#include "msg.h"

#define CLOCKID CLOCK_REALTIME
#define SIG SIGRTMIN


char* command;
int periodic;
mqd_t m_queue;


static void handler(int sig, siginfo_t *si, void *uc)
{
    /* Note: calling printf() from a signal handler is not safe
       (and should not be done in production programs), since
       printf() is not async-signal-safe; see signal-safety(7).
       Nevertheless, we use printf() here as a simple way of
       showing that the handler was called. */

//    printf ("Executing %s\n", command);
    system (command);

    if(!periodic)
    {
        // send info to the server that the task has completed
        struct msg_buffer msg;
        pid_t pid = getpid();
        msg.id = (int)pid;
        int err = mq_send(m_queue, (char *) &msg, sizeof(msg), 1);

//        if(err == -1)
//        {
//            fprintf(stderr, "ERROR %i", err);
//        }
    }
}


void schedule_task(mqd_t message_queue, char path_to_exe_with_args[], int is_periodic, unsigned long time)
{
//    fprintf(stderr,"Scheduling task: %s\n", path_to_exe_with_args);

    command = path_to_exe_with_args;
    periodic = is_periodic;
    m_queue = message_queue;

    struct sigevent sev;
    sev.sigev_notify = SIGEV_SIGNAL;
    sev.sigev_signo = SIG;
    timer_t timerid;
    sev.sigev_value.sival_ptr = &timerid;

    struct itimerspec its;
    its.it_value.tv_sec = time / 1000000000;
    its.it_value.tv_nsec = time % 1000000000;
    if (is_periodic)
    {
        its.it_interval.tv_sec = time / 1000000000;
        its.it_interval.tv_nsec = time % 1000000000;
    }
    else
    {
        its.it_interval.tv_sec= 0;
        its.it_interval.tv_nsec = 0;
    }

    struct sigaction sa;
    sa.sa_flags = SA_SIGINFO;
    sa.sa_sigaction = handler;
    sigemptyset(&sa.sa_mask);

    if (sigaction(SIG, &sa, NULL) == -1)
    {
        printf("ERROR1");
    }

    if (timer_create(CLOCKID, &sev, &timerid) == -1)
    {
        printf("ERROR2");
    }

    if (timer_settime(timerid, 0, &its, NULL) == -1)
    {
        printf("ERROR3");
    }
}
