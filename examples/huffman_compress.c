frequencies[];
values[];
lefts[];
rights[];

void reset(queue self){
    self.in=0;
    self.out=0;
}

unsigned peek(queue self){
    return self.buffer[self.out];
}

unsigned pop(queue self){
    return self.buffer[self.out++];
}

void push(queue self, unsigned pointer){
    self.buffer[self.in++] = pointer;
}

unsigned length(queue self){
    return self.in - self.out;
}

unsigned pop_lowest_frequency(){
    if(length(first) && length(second)){
        if(frequencies[peek(first)] < frequencies[peek(second)]){
            return pop(first);
        } else {
            return pop(second);
        }
    } else if(length_first){
        return pop(first);
    } else {
        return pop(second);
    }
}

/*if value has allready been encountered, increase the frequency*/
unsigned increment_frequency(unsigned value){
    for(i=0; i<new; i++){
        if(values[i] = value){
            frequencies[i] += 1;
            return 1;
        }
    }
    return 0;
}

void walk(unsigned tree; unsigned code;  unsigned length){
    if( tree < new ){
        code[tree] = code;
        lengths[tree] = code;
        return;
    }
    walk(lefts[tree], code << 1, length + 1);
    walk(rights[tree], code << 1 | 1, length + 1);
}

unsigned create_huffman_tree(){

    /*create leaf nodes by counting frequency of occurence in buffer*/
    for(i=0; i<buffer_length; i++){
        value = buffer[i];
        if(!increment_frequency())
            lefts[new] = 0;
            rights[new] = 0;
            frequency[new] = 1;
            value[new] = value;
            new++;
        }
    } 

    /*sort leaves in increasing order of probabiulity*/
    for(i=1; i<new; i++){
        for(j=i; j; j--){
            if(frequencies[j-1] <= frequencies[i]) break;
            frequencies[j] = frequencies[j-1];
            values[j] = values[j-1];
        }
        frequencies[j] = frequencies[i];
        values[j] = values[i];
    }

    /*push leaves in first queue*/
    for(i=1; i<new; i++){
        push(first, i);
    }

    /*create tree nodes*/
    while(length(first) + length(second) > 1){
        lowest = pop_lowest_frequency();
        next_lowest = pop_lowest_frequency();
        frequencies[new] = frequencies[lowest] + frequencies[next_lowest];
        lefts[new] = lowest;
        rights[new] = next_lowest;
        new++;
    }

    if(length(first)){
        walk(first, 0, 0);
        return pop(first);
    } else {
        walk(first, 0, 0);
        return pop(second);
    }

}



