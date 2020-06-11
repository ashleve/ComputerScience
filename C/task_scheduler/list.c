//
// Created by ukasz on 11.06.2020.
//

#include "list.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>


struct node *head = NULL;


//display the list
void printList() {
    struct node *ptr = head;
    fprintf(stderr,"Current tasks: [ ");

    //start from the beginning
    while(ptr != NULL) {
        fprintf(stderr,"(pid: %d, is_periodic: %d), ",ptr->key,ptr->data);
        ptr = ptr->next;
    }

    fprintf(stderr," ]\n");
}


void insertFirst(int key, int data) {
    //create a link
    struct node *link = (struct node*) malloc(sizeof(struct node));

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

    for(current = head; current != NULL; current = current->next) {
        length++;
    }

    return length;
}

//find a link with given key
struct node* find(int key) {

    //start from the first link
    struct node* current = head;

    //if list is empty
    if(head == NULL) {
        return NULL;
    }

    //navigate through list
    while(current->key != key) {

        //if it is last node
        if(current->next == NULL) {
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
struct node* delete(int key) {

    //start from the first link
    struct node* current = head;
    struct node* previous = NULL;

    //if list is empty
    if(head == NULL) {
        return NULL;
    }

    //navigate through list
    while(current->key != key) {

        //if it is last node
        if(current->next == NULL) {
            return NULL;
        } else {
            //store reference to current link
            previous = current;
            //move to next link
            current = current->next;
        }
    }

    //found a match, update the link
    if(current == head) {
        //change first to point to next link
        head = head->next;
    } else {
        //bypass the current link
        previous->next = current->next;
    }

    return current;
}


//int main() {
//    insertFirst(1,10);
//    insertFirst(2,20);
//    insertFirst(3,30);
//    insertFirst(4,1);
//    insertFirst(5,40);
//    insertFirst(6,56);
//
//    printf("Original List: ");
//
//    //print list
//    printList();
//
//    while(!isEmpty()) {
//        struct node *temp = deleteFirst();
//        printf("\nDeleted value:");
//        printf("(%d,%d) ",temp->key,temp->data);
//    }
//
//    printf("\nList after deleting all items: ");
//    printList();
//    insertFirst(1,10);
//    insertFirst(2,20);
//    insertFirst(3,30);
//    insertFirst(4,1);
//    insertFirst(5,40);
//    insertFirst(6,56);
//
//    printf("\nRestored List: ");
//    printList();
//    printf("\n");
//
//    struct node *foundLink = find(4);
//
//    if(foundLink != NULL) {
//        printf("Element found: ");
//        printf("(%d,%d) ",foundLink->key,foundLink->data);
//        printf("\n");
//    } else {
//        printf("Element not found.");
//    }
//
//    delete(4);
//    printf("List after deleting an item: ");
//    printList();
//    printf("\n");
//    foundLink = find(4);
//
//    if(foundLink != NULL) {
//        printf("Element found: ");
//        printf("(%d,%d) ",foundLink->key,foundLink->data);
//        printf("\n");
//    } else {
//        printf("Element not found.");
//    }
//
//    printf("\n");
//    sort();
//
//    printf("List after sorting the data: ");
//    printList();
//
//    reverse(&head);
//    printf("\nList after reversing the data: ");
//    printList();
//
//    return 0;
//}