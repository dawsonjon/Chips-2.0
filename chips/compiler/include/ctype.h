///
///ctype.h
///-------
///
///
///The isalnum function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int isalnum(int c);
///
///Description:
///
///   The isalnum function tests for any character for which isalpha or
///   isdigit is true.
///

unsigned isalnum(char c){
	return (c >= 'A' && c <= 'Z') || (c >='a' && c <= 'z') || (c >= '0' && c <= '9');
}

///
///The isalpha function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int isalpha(int c);
///
///Description:
///
///   The isalpha function tests for any character for which isupper or
///   islower is true, or any of an implementation-defined set of characters
///   for which none of iscntrl, isdigit, ispunct, or isspace is true.
///   In the C locale, isalpha returns true only for the characters for
///   which isupper or islower is true.
///

unsigned isalpha(char c){
	return (c >= 'A' && c <= 'Z') || (c >='a' && c <= 'z');
}

///
///The iscntrl function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int iscntrl(int c);
///
///Description:
///
///   The iscntrl function tests for any control character.  
///

unsigned iscntrl(char c){
	return (c >=0 && c <= 0x1f) || c == 0x7f;
}

///
///The isdigit function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int isdigit(int c);
///
///Description:
///
///   The isdigit function tests for any decimal-digit character.
///

unsigned isdigit(char c){
	return (c >='0' && c <= '9');
}

///
///The isgraph function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int isgraph(int c);
///
///Description:
///
///   The isgraph function tests for any printing character except space (' ').  
///

unsigned isgraph(char c){
	return (c >= 0x21  && c <= 0x7e);
}

///
///The islower function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int islower(int c);
///
///Description:
///
///   The islower function tests for any lower-case letter or any of an
///   implementation-defined set of characters for which none of iscntrl,
///   isdigit, ispunct, or isspace is true.  In the C locale, islower
///   returns true only for the characters defined as lower-case letters.
///

unsigned islower(char c){
	return (c >='a' && c <= 'z');
}

///
///The isprint function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int isprint(int c);
///
///Description:
///
///   The isprint function tests for any printing character including
///   space (' ').
///

unsigned isprint(char c){
	return (c >= 0x20  && c <= 0x7e);
}

///
///The ispunct function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int ispunct(int c);
///
///Description:
///
///   The ispunct function tests for any printing character except space
///   (' ') or a character for which isalnum is true.
///

unsigned ispunct(char c){
	return isgraph(c) && !isalnum(c);
}

///
///The isspace function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int isspace(int c);
///
///Description:
///
///   The isspace function tests for the standard white-space characters
///   or for any of an implementation-defined set of characters for which
///   isalnum is false.  The standard white-space characters are the
///   following: space (' '), form feed ('\f'), new-line ('\n'), carriage
///   return ('\r'), horizontal tab ('\t'), and vertical tab ('\v').  In the
///   C locale, isspace returns true only for the standard white-space
///   characters.
///

unsigned isspace(char c){
	return (c == ' ' || c == '\t' || c == '\v' || c == '\n' || c == '\r' || c == '\f');
}

///
///The isupper function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int isupper(int c);
///
///Description:
///
///   The isupper function tests for any upper-case letter or any of an
///   implementation-defined set of characters for which none of iscntrl,
///   isdigit, ispunct, or isspace is true.  In the C locale, isupper
///   returns true only for the characters defined as upper-case letters.
///

unsigned isupper(char c){
	return (c >='A' && c <= 'Z');
}

///
///The isxdigit function
///*********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int isxdigit(int c);
///
///Description:
///
///   The isxdigit function tests for any hexadecimal-digit character.
///

unsigned isxdigit(char c){
	return (c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f') || (c >= '0' && c <= '9');
}

///
///The tolower function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int tolower(int c);
///
///Description:
///
///   The tolower function converts an upper-case letter to the
///   corresponding lower-case letter.
///
///Returns:
///
///   If the argument is an upper-case letter, the tolower function
///   returns the corresponding lower-case letter if there is one; otherwise
///   the argument is returned unchanged.  In the C locale, tolower maps
///   only the characters for which isupper is true to the corresponding
///   characters for which islower is true.
///

unsigned tolower(char c){
	if(isupper(c)){
	      return c - 'A' + 'a';	
	} else {
	      return c;
	}
}

///
///The toupper function
///********************
///
///Synopsis:
///
///    .. code-block:: c
///
///         #include <ctype.h>
///         int toupper(int c);
///
///Description:
///
///   The toupper function converts a lower-case letter to the corresponding upper-case letter.  
///
///Returns:
///
///   If the argument is a lower-case letter, the toupper function
///   returns the corresponding upper-case letter if there is one; otherwise
///   the argument is returned unchanged.  In the C locale, toupper maps
///   only the characters for which islower is true to the corresponding
///   characters for which isupper is true.
///

unsigned toupper(char c){
	if(islower(c)){
	      return c - 'a' + 'A';	
	} else {
	      return c;
	}
}

