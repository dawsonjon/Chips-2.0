/*globals*/
unsigned long int seed;

void srand(unsigned int s){
    seed = s;
}

unsigned long rand(){
    const unsigned a = 1103515245u;
    const unsigned c = 12345u;
    seed = (a*seed+c);
    return seed;
}

void main(){
    unsigned i;
    for (i=0; i<4096; i++){
        file_write(rand(), "x");
        file_write(rand(), "y");
        file_write(rand(), "z");
    }
}
