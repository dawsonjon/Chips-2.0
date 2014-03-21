/* servo_controller.c */
/* Jonathan P Dawson */
/* 2013-12-24 */


/*   
 
Control Word 0
--------------

Selcect Servo 0 to 7.

Control Word 1
--------------

Select Position -500 to 500.

position -500 = 90 degrees CCW
position 0    = central
position 500  = 90 degrees CW

*/

void wait_us(unsigned long us){
    unsigned i;
    const unsigned long CLK_FREQ_MHZ = 100;
    for(i=0; i<us; i++) wait_clocks(CLK_FREQ_MHZ); 
}

void servo_controller(){

    int positions[8];
    unsigned servo;
    unsigned position;
    unsigned pulses;


    /* Centralise the servos */
    for(servo=0; servo<8; servo++){
        positions[servo] = 0;
    }

    while (1){

        /* Check for new commanded position */
        if(ready_control()){
            servo = input_control();
            position = input_control();
            positions[servo] = position;
        }

        /* output pulses */

        /*
         *     90 degrees CCW   <-o
         *      _______                           ______
         *  ___|       |_________________________|      |____
         *
         *     |<-1ms->|
         *     |<-----------12 ms--------------->|
         *                         
         *                        ^
         *     Central            o
         *      __________                        ______
         *  ___|          |______________________|      |____
         *
         *     |<--1.5ms->|
         *     |<-----------12 ms--------------->|
         *
         *
         *     90 degrees CW      o->
         *      ____________                      ______
         *  ___|            |____________________|      |____
         *
         *     |<----2ms--->|
         *     |<-----------12 ms--------------->|
         *
         */

        pulses = 0xff;
        wait_us(1000);
        for(position=-500; position<500; position++){
            for(servo=0; servo<8; servo++){
                if(position >= positions[servo]){
                    pulses &= ~(1 << servo);
                    output_servos(pulses);
                }
            }
            wait_us(1);
        }
        wait_us(10000);
    }
}
