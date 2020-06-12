//
// Created by ukasz on 06.06.2020.
//

#ifndef ZADANIE_3_SERVER_TASK_H
#define ZADANIE_3_SERVER_TASK_H


void schedule_task(mqd_t message_queue, char command[], int is_periodic, unsigned long time);


#endif //ZADANIE_3_SERVER_TASK_H