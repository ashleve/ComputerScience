//
// Created by ukasz on 11.06.2020.
//

#ifndef ZADANIE_3_SERVER_MSG_H
#define ZADANIE_3_SERVER_MSG_H


#include <mqueue.h>

#define QUEUE_NAME  "/the_queue"

struct msg_buffer {
    int id;     // pid of finished timer process
} message;

mqd_t create_message_queue();


#endif //ZADANIE_3_SERVER_MSG_H
