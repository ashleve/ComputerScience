#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <signal.h>


void * f1 (void * signal_number) {
    printf( "This is thread %lu\n", pthread_self() );

    sigset_t s;

    // make thread ignore all signals except SIGRTMIN
    sigfillset(&s);
    sigdelset(&s, SIGRTMIN);
    pthread_sigmask(SIG_SETMASK, &s, NULL);

    // create mask for signal
    sigemptyset(&s);
    sigaddset(&s, SIGRTMIN + *(int*)signal_number);

    // wait for signal
    siginfo_t info;
    sigwaitinfo(&s, & info);
    printf("%d - %d\n", info.si_signo, info.si_value.sival_int);

    return NULL;
}


int main(void) {

    // make main thread block all signals
    sigset_t set;
    sigfillset( & set);
    pthread_sigmask(SIG_SETMASK, & set, NULL);

    // create threads
    int signal1 = 1, signal2 = 2;
    pthread_t t1, t2;
    pthread_create(&t1, NULL, f1, &signal1);
    pthread_create(&t2, NULL, f1, &signal2);

    // wait for threads
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    return EXIT_SUCCESS;
}