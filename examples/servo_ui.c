char stdin_get_char(){
    return input_rs232();
}

void stdout_put_char(char character){
    output_rs232(character);
}

#include <print.h>

unsigned is_num(char character){
    if(character >= '0' && character <= '9'){
        return 1;
    }
    return 0;
}

int scan(){
    unsigned character;
    int sign;
    int value;
    character = stdin_get_char();
    if(character == '-'){
        sign = -1;
        value = 0;
    } else if(character == '+'){
        sign = 1;
        value = 0;
    } else {
        sign = 1;
        value = character - '0';
    }
    while(1){
        character = stdin_get_char();
        value *= 10;
        value += (character - '0');
        if(!is_num(character)){
            break;
        }
    }
    return value;
}

void servo_ui(){

    unsigned servo;
    unsigned position;

    print_string("Servo Controller\n");
    print_string("Jonathan P Dawson\n");
    print_string("2013-12-24\n");

    while(1){
        while(1){
            print_string("Enter Servo 0 to 7:\n");
            print_string("~$\n");
            servo = scan();
            if(servo >= 0 && servo <= 7){
                break;
            } else {
                print_string("servo should be between 0 and 7");
            }
        }

        while(1){
            print_string("Enter Position -500 to 500:\n");
            print_string("~$\n");
            if(position >= 0 && position <= 7){
                break;
            } else {
                print_string("position should be between -500 and 500");
            }
        }

        output_control(servo);
        output_control(position);
    }

}

