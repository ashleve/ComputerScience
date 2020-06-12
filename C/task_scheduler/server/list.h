//
// Created by ukasz on 11.06.2020.
//

#ifndef ZADANIE_3_SERVER_LIST_H
#define ZADANIE_3_SERVER_LIST_H


struct node {
    int data;
    int key;
    struct node *next;
};

struct node *head;

int length();
void printList();
void get_task_info(char *buffer);
void insertFirst(int key, int data);
struct node* find(int key);
struct node* delete(int key);


#endif //ZADANIE_3_SERVER_LIST_H
