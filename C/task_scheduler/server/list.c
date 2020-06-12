//
// Created by ukasz on 11.06.2020.
//

#include "list.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>


struct node *head = NULL;


void printList() {
    struct node *ptr = head;
    fprintf(stderr, "Current tasks: [ ");

    //start from the beginning
    while (ptr != NULL) {
        fprintf(stderr, "(pid: %d, is_periodic: %d), ", ptr->key, ptr->data);
        ptr = ptr->next;
    }

    fprintf(stderr, " ]\n");
}


void get_task_info(char *buffer) {
    struct node *ptr = head;

    memset(buffer, '\0', 1000);
    strcpy(buffer, "Current tasks: [ ");

    //start from the beginning
    while (ptr != NULL) {

        int length = snprintf( NULL, 0, "%d", ptr->key );
        char* str = malloc( length + 1 );
        snprintf( str, length + 1, "%d", ptr->key );
        strcat(buffer, "(id : ");
        strcat(buffer, str);
        free(str);

        length = snprintf( NULL, 0, "%d", ptr->data );
        str = malloc( length + 1 );
        snprintf( str, length + 1, "%d", ptr->data );
        strcat(buffer, ", periodic: ");
        strcat(buffer, str);
        strcat(buffer, "), ");
        free(str);

        ptr = ptr->next;
    }

    strcat(buffer, " ]\n");
}


void insertFirst(int key, int data) {
    //create a link
    struct node *link = (struct node *) malloc(sizeof(struct node));

    link->key = key;
    link->data = data;

    //point it to old first node
    link->next = head;

    //point first to new first node
    head = link;
}


int length() {
    int length = 0;
    struct node *current;

    for (current = head; current != NULL; current = current->next) {
        length++;
    }

    return length;
}

//find a link with given key
struct node *find(int key) {

    //start from the first link
    struct node *current = head;

    //if list is empty
    if (head == NULL) {
        return NULL;
    }

    //navigate through list
    while (current->key != key) {

        //if it is last node
        if (current->next == NULL) {
            return NULL;
        } else {
            //go to next link
            current = current->next;
        }
    }

    //if data found, return the current Link
    return current;
}

//delete a link with given key
struct node *delete(int key) {

    //start from the first link
    struct node *current = head;
    struct node *previous = NULL;

    //if list is empty
    if (head == NULL) {
        return NULL;
    }

    //navigate through list
    while (current->key != key) {

        //if it is last node
        if (current->next == NULL) {
            return NULL;
        } else {
            //store reference to current link
            previous = current;
            //move to next link
            current = current->next;
        }
    }

    //found a match, update the link
    if (current == head) {
        //change first to point to next link
        head = head->next;
    } else {
        //bypass the current link
        previous->next = current->next;
    }

    return current;
}
