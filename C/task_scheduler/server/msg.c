//
// Created by ukasz on 11.06.2020.
//

#include "msg.h"

#include <mqueue.h>


mqd_t create_message_queue() {
    // unlink just in case...
    mq_unlink(QUEUE_NAME);

    struct mq_attr attr;
    attr.mq_flags = 0;
    attr.mq_maxmsg = 8;
    attr.mq_curmsgs = 0;
    attr.mq_msgsize = sizeof(message);
    mqd_t m_queue = mq_open(QUEUE_NAME, O_RDWR | O_CREAT, 0777, &attr);

    return m_queue;
}