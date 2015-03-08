unsigned isalnum(char c){
	return (c >= 'A' && c <= 'Z') || (c >='a' && c <= 'z') || (c >= '0' && c <= '9');
}

unsigned isalpha(char c){
	return (c >= 'A' && c <= 'Z') || (c >='a' && c <= 'z');
}

unsigned islower(char c){
	return (c >='a' && c <= 'z');
}

unsigned isupper(char c){
	return (c >='A' && c <= 'Z');
}

unsigned isdigit(char c){
	return (c >='0' && c <= '9');
}

unsigned isxdigit(char c){
	return (c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f') || (c >= '0' && c <= '9');
}

unsigned isgraph(char c){
	return (c >= 0x21  && c <= 0x7e);
}

unsigned isspace(char c){
	return (c == ' ' || c == '\\t' || c == '\\v' || c == '\\n' || c == '\\r' || c == '\\f');
}

unsigned isprint(char c){
	return (c >= 0x20  && c <= 0x7e);
}

unsigned ispunct(char c){
	return isgraph(c) && !isalnum(c);
}

unsigned toupper(char c){
	if(islower(c)){
	      return c - 'a' + 'A';	
	} else {
	      return c;
	}
}

unsigned tolower(char c){
	if(isupper(c)){
	      return c - 'A' + 'a';	
	} else {
	      return c;
	}
}
