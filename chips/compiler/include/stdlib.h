const unsigned long RAND_MAX = 0xfffffffful;

unsigned long int seed;

void srand(unsigned long int s){
	seed = s;
}

unsigned long rand(){
	const unsigned long a = 1103515245ul;
	const unsigned long c = 12345ul;
	seed = (a*seed+c);
	return seed;
}

    /* return absolute value of an int */

    int abs(int x){
        if (x < 0) {
            return - x;
        } else {
            return x;
        }
    }

    /* return absolute value of a long*/

    long labs(long x){
        if (x < 0) {
            return - x;
        } else {
            return x;
        }
    }
