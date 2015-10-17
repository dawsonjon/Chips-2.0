/*

Copyright (C) Jonathan P Dawson 2014

list.c

Very simple list of integers

+-----+-------+----------+
|  0  | value |          |
+-----+-------+  ITEM 0  |
|  1  | next  |          |
+-----+-------+----------+
|  2  | value |          |
+-----+-------+  ITEM 1  |
|  3  | next  |          |
+-----+-------+----------+

...

+-----------+   +-----------+   +-----------+   +-----------+   +-----------+
|head       |   | item 0    |   | item 1    |   | item 2    |   | tail      |<-+
+-----------+   +-----------+   +-----------+   +-----------+   +-----------+  |
|value | o----->|value | o----->|value | o----->|value | o----->|value | o-----+
+-----------+   +-----------+   +-----------+   +-----------+   +-----------+
*/


int _data[1024];
unsigned _free = 0;
unsigned no_error = 0;
unsigned not_found = 0;
unsigned error = no_error;


/* Initialise the data area */
/* creates a list of free elements */
void list_initialise(){
    unsigned i;
    for(i=0; i<1024; i+=2){
        _data[i+1] = i+2;
    }
}

/* Get the next field of an element */
unsigned next(unsigned item)
{
    return _data[item + 1];
}

/* Get the value field of an element */
int value(unsigned item)
{
    return _data[item];
}

/* Set the next field of an element */
void set_next(unsigned item, unsigned next)
{
    _data[item + 1] = next;
}

/* Set the value field of an element */
void set_value(unsigned item, unsigned value)
{
    _data[item] = value;
}

/* Mark an element as the list tail */
void set_tail(unsigned item)
{
    _data[item + 1] = item + 1;
}

/* Determine whether an element of a list is a tail */
unsigned is_tail(unsigned item)
{
    return _data[item + 1] == item + 1;
}

/* Create a new (empty) list and return a handle to it */
unsigned new_list()
{
    unsigned head, tail;

    /* For convenience, an empty list has a head and a tail */
    /* The head and tail have no data in them */
    head = _free;
    _free = next(_free);
    tail = _free;
    _free = next(_free);

    set_next(head, tail);
    set_tail(tail);

    return head;
}

/* Set the value of the nth item in a list */
/* sets *error* to *not_found* if the list does not contain n elements */
void set_item(unsigned list, unsigned n, int value)
{
    unsigned find = next(list);
    unsigned i; 
    error = no_error;

    for(i=0; i<n; i++){
        if (is_tail(find)){
            error = not_found;
            return;
        }
        find = next(find);
    }
    set_value(find, value);
}

/* Get the value of the nth item in a list */
/* sets *error* to *not_found* if the list does not contain n elements */
int get_item(unsigned list, unsigned n)
{
    unsigned find = next(list);
    unsigned i; 
    error = no_error;

    if (is_tail(find)){
        error = not_found;
        return -1;
    }
    for(i=0; i<n; i++){
        if (is_tail(find)){
            error = not_found;
            return -1;
        }
        find = next(find);
    }
    return value(find);
}

/* insert an item imediately before nth item */
/* sets *error* to *not_found* if the list does not contain n elements */
void insert_item(unsigned list, unsigned n, int value)
{
    unsigned find = next(list);
    unsigned previous = list;
    unsigned i, new; 
    error = no_error;

    for(i=0; i<n; i++){
        if (is_tail(find)){
            error = not_found;
            return;
        }
        previous = find;
        find = next(find);
    }
    
    new = _free;
    _free = next(_free);
    set_next(previous, new);
    set_next(new, find);
    set_value(new, value);
}

/* Delete nth item */
/* sets *error* to *not_found* if the list does not contain n elements */
void delete_item(unsigned list, unsigned n)
{
    unsigned find = next(list);
    unsigned previous = list;
    unsigned i, new; 
    error = no_error;

    for(i=0; i<n; i++){
        if (is_tail(find)){
            error = not_found;
            return;
        }
        previous = find;
        find = next(find);
    }
    
    set_next(previous, next(find));
    set_next(find, _free);
    _free = find;
}

/* Append an item to the end of a list */
void append_item(unsigned list, int value)
{
    unsigned find = next(list);
    unsigned previous = list;
    unsigned i, new; 
    error = no_error;

    while (!is_tail(find)){
        previous = find;
        find = next(find);
    }

    new = _free;
    _free = next(_free);

    set_next(previous, new);
    set_next(new, find);
    set_value(new, value);
}

/* Print a list in simulation console */
void print_list(unsigned list)
{
    unsigned find = next(list);
    error = no_error;

    while (!is_tail(find)){
        report(value(find));
        find = next(find);
    }
}

/* return the length of a list */
unsigned len_list(unsigned list)
{
    unsigned find = next(list);
    unsigned i = 0;
    error = no_error;

    while (!is_tail(find)){
        i++;
        find = next(find);
    }
    return i;
}

void main()
{
    list_initialise();
    unsigned list = new_list();

    assert(len_list(list) == 0);
    append_item(list, 0);
    assert(len_list(list) == 1);
    assert(get_item(list, 0) == 0);
    append_item(list, 1);
    assert(len_list(list) == 2);
    assert(get_item(list, 0) == 0);
    assert(get_item(list, 1) == 1);
    append_item(list, 2);
    assert(len_list(list) == 3);
    assert(get_item(list, 0) == 0);
    assert(get_item(list, 1) == 1);
    assert(get_item(list, 2) == 2);
    delete_item(list, 1);
    assert(len_list(list) == 2);
    assert(get_item(list, 0) == 0);
    assert(get_item(list, 1) == 2);
    delete_item(list, 0);
    assert(len_list(list) == 1);
    assert(get_item(list, 1) == 2);
    delete_item(list, 0);
    assert(len_list(list) == 0);
    append_item(list, 0);
    append_item(list, 1);
    append_item(list, 2);
    append_item(list, 3);
    assert(get_item(list, 0) == 0);
    assert(get_item(list, 1) == 1);
    assert(get_item(list, 2) == 2);
    assert(get_item(list, 3) == 3);
    assert(len_list(list) == 4);
    set_item(list, 3, 0);
    set_item(list, 2, 1);
    set_item(list, 1, 2);
    set_item(list, 0, 3);
    assert(get_item(list, 0) == 3);
    assert(get_item(list, 1) == 2);
    assert(get_item(list, 2) == 1);
    assert(get_item(list, 3) == 0);
    insert_item(list, 3, 3);
    insert_item(list, 2, 2);
    insert_item(list, 1, 1);
    insert_item(list, 0, 0);
    assert(get_item(list, 0) == 0);
    assert(get_item(list, 1) == 3);
    assert(get_item(list, 2) == 1);
    assert(get_item(list, 3) == 2);
    assert(get_item(list, 4) == 2);
    assert(get_item(list, 5) == 1);
    assert(get_item(list, 6) == 3);
    assert(get_item(list, 7) == 0);

}
