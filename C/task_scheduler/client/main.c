#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <netdb.h>
#include "sock.h"


int create_socket();
void connect_to_server(int sockfd);
void report(const char *msg, int terminate);
void write_message(int sockfd, char* buffer);
void read_message(int sockfd, char* buffer);


int main() {

    puts("Connected to server...");

    while (1) {

        int sockfd = create_socket();
        connect_to_server(sockfd);

        char text[] = "What do you want to do?\n"
                      "0 - schedule task\n"
                      "1 - get task info\n"
                      "2 - cancel task\n"
                      "3 - exit\n";

        fprintf(stderr,"%s", text);

        char answer[2];
        scanf("%[^\n]", answer);
        char c;
        scanf("%c", &c);

        if(!strcmp(answer, "0"))
        {
//            char path[BUFF_SIZE];   // hardcoded for ease of use
//            strcpy(path, "/home/ukasz/Desktop/main.exe");
            char path[BUFF_SIZE];
            char args[BUFF_SIZE], time[BUFF_SIZE], repeat[BUFF_SIZE], tmp[BUFF_SIZE];
            char request[BUFF_SIZE];
            strcpy(request, "schedule_task");
            fprintf(stderr,"path:");
            scanf("%[^\n]", path);
            scanf("%c", &c);
            fprintf(stderr,"args:");
            scanf("%[^\n]", args);
            scanf("%c", &c);
            fprintf(stderr,"time:");
            scanf("%[^\n]", time);
            scanf("%c", &c);
            fprintf(stderr,"repeat? (0 - no, 1 - yes):");
            scanf("%[^\n]", repeat);
            scanf("%c", &c);

            strcat(path, " ");
            strcat(path, args);

            write_message(sockfd, request);
            read_message(sockfd, tmp);
            write_message(sockfd, path);
            read_message(sockfd, tmp);
            write_message(sockfd, time);
            read_message(sockfd, tmp);
            write_message(sockfd, repeat);
            read_message(sockfd, tmp);

            fprintf(stderr,"Task scheduled\n");
        }
        else if(!strcmp(answer, "1"))
        {
            fprintf(stderr,"Requesting task info...\n");
            char request[BUFF_SIZE];
            strcpy(request, "get_info");
            write_message(sockfd, request);
            char response[BUFF_SIZE];
            read_message(sockfd, response);
            read_message(sockfd, response);
            fprintf(stderr,"TASK INFO: %s\n", response);
        }
        else if(!strcmp(answer, "2"))
        {
            char id[6];
            fprintf(stderr,"Type task id:");
            scanf("%[^\n]", id);
            scanf("%c", &c);
            fprintf(stderr,"Cancelling task with id %s:\n\n", id);
            char request[BUFF_SIZE];
            strcpy(request, "cancel_task");
            write_message(sockfd, request);
            char tmp[BUFF_SIZE];
            read_message(sockfd, tmp);
            write_message(sockfd, id);
        }
        else if(!strcmp(answer, "3"))
        {
            break;
        }

        close(sockfd);
    }

    puts("Closing client...");

    return 0;
}

int create_socket()
{
    /* fd for the socket */
    int sockfd = socket(AF_INET, /* versus AF_LOCAL */
                        SOCK_STREAM, /* reliable, bidirectional */
                        0); /* system picks protocol (TCP) */
    if (sockfd < 0) report("socket", 1); /* terminate */

    return sockfd;
}

void connect_to_server(int sockfd)
{
    /* get the address of the host */
    struct hostent *hptr = gethostbyname(HOST); /* localhost: 127.0.0.1 */
    if (!hptr) report("gethostbyname", 1); /* is hptr NULL? */
    if (hptr->h_addrtype != AF_INET) /* versus AF_LOCAL */
        report("bad address family", 1);

    /* connect to the server: configure server's address 1st */
    struct sockaddr_in saddr;
    memset(&saddr, 0, sizeof(saddr));
    saddr.sin_family = AF_INET;
    saddr.sin_addr.s_addr =
            ((struct in_addr *) hptr->h_addr_list[0])->s_addr;
    saddr.sin_port = htons(PORT_NUMBER); /* port number in big-endian */
    if (connect(sockfd, (struct sockaddr *) &saddr, sizeof(saddr)) < 0)
        report("connect", 1);
}

void report(const char *msg, int terminate) {
    perror(msg);
    if (terminate) exit(-1); /* failure */
}

void write_message(int sockfd, char* buffer)
{
    if (write(sockfd, buffer, BUFF_SIZE) <= 0) {
        fprintf(stderr,"ERROR WRITE\n");
    }
}

void read_message(int sockfd, char* buffer)
{
    memset(buffer, '\0', BUFF_SIZE);
    if (read(sockfd, buffer, BUFF_SIZE ) <= 0)
    {
        fprintf(stderr,"ERROR READ\n");
    }
//    puts(buffer);
}
