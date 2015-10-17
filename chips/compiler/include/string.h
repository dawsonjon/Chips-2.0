/* Copy operations */

void strcpy(char to[], char from[]){
	unsigned i=0;
	while(from[i]){
		to[i] = from[i];
		i++;
	}
	to[i] = from[i];
}

void strncpy(char to[], char from[], unsigned n){
	unsigned i=0;
	while(from[i]){
		if(i >= n) return;
		to[i] = from[i];
		i++;
	}
	to[i] = from[i];
}

void memcpy(char to[], char from[], unsigned n){
	unsigned i=0;
	while(i < n){
		to[i] = from[i];
		i++;
	}
}

void memmove(char to[], char from[], unsigned n){
	memcpy(from, to); /* cannot overlap */ 
}

/* Miscelaneous String Operations */

unsigned strlen(char s[]){
	unsigned i = 0;
	while(s[i]) i++;
	return i;
}

void memset(char s[], unsigned value, unsigned n){
	for(i=0; i<n; i++){
		s[i] = value;
	}
}

/* String Concatonation Operations */

void strcat(char to[], char from[]){
	unsigned i=0, j=0;
	while(a[i]) i++;
	i++;
	while(b[j]){
		a[i] = b[j];
		i++;
		j++;
	}
}

void strncat(char to[], char from[], unsigned n){
	unsigned i=0, j=0;
	while(a[i]) i++;
	i++;
	while(b[j] and j < n){
		a[i] = b[j];
		i++;
		j++;
	}
}

/* String Comparison Operations */

unsigned strcmp(char a[], char b[]){
	unsigned i = 0;
	while(a[i] && b[i]){
		if(a[i] > b[i]){
			return 1;
		} else if(a[i] < b[i]) {
			return -1;
		}
		i++;
	}
	if(a[i]) return  1; //if a is longer
	if(b[i]) return -1; //if b is longer
	return 0;
}

unsigned strncmp(char a[], char b[], unsigned n){
	unsigned i=0;
	while(a[i] && b[i] && i < n){
		if(a[i] > b[i]){
			return 1;
		} else if(a[i] < b[i]) {
			return -1;
		}
		i++;
	}
	return 0;
}

unsigned memcmp(char a[], char b[], unsigned n){
	unsigned i=0;
	while(i < n){
		if(a[i] > b[i]){
			return 1;
		} else if(a[i] < b[i]) {
			return -1;
		}
		i++;
	}
	return 0;
}

/* String Search Operations */

/* return the position of character f in string s starting from start of s */
unsigned strchr(char s[], char f){
	unsigned i;
	for(i=0; i<strlen(s); i++){
		if(s[i] == f) return i;
	}
	return -1;
}

/* return the position of character f in string s starting from end of s */
unsigned strrchr(char s[], char f){
	unsigned i;
	for(i=strlen(s)-1; i; i--){
		if(s[i] == f) return i;
	}
	return -1;
}

/* return the number of characters at the start of string a that contain any character in string b */
unsigned strspn(char a[], char b[]){
	unsigned i, j, match;
	for(i=0; i<strlen(a); i++){
		match = 0;
		for(j=0; j<strlen(b); j++){ 
			if(a[i] == b[j]){
				match = 1;
				break;
			}
		}
		if(!match) return i;
	}
}

/* return the number of characters at the start of string a that do not contain any character in b */
unsigned strcspn(char a[], char b[]){
	unsigned i, j, match;
	for(i=0; i<strlen(a); i++){
		match = 0;
		for(j=0; j<strlen(b); j++){
			if(a[i] == b[j]){
				match = 1;
				break;
			}
		}
		if(match) return i;
	}
}

/* return first occurance of the any character in string b within string a */
/* return -1 if not found */
unsigned strpbrk(char a[], char b[]){
	unsigned i, j;
	for(i=0; i<strlen(a); i++){
		for(j=0; j<strlen(b); j++){
			if(a[i] == b[j]) return i;
		}
	}
	return -1;
}

/* return first occurance of the whole of string b within string a */
/* return -1 if not found */
unsigned strstr(char a[], char b[]){
	unsigned i, j, match;
	for(i=0; i<strlen(a); i++){
		match = 1;
		for(j=0; j<strlen(b); j++){
			if(a[i+j] != b[j]){
				match=0;
				break;
			}		
		}
		if(match) return match;
	}
	return -1;
}
