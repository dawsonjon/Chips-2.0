examples = {
"empty template":"""
void main()
{

}
""",

"knight rider":"""
int leds = output("leds");
void main()
{
    int shifter = 1;
    while(1){
        while(shifter < 0x80){
            shifter <<= 1;
            fputc(leds, shifter);
        }
        while(shifter > 1){
            shifter >>= 1;
            fputc(leds, shifter);
        }
    }
}
""",

"seven segment":"""

/* Seven Segment Display Driver */

int nibble = input("nibble");
int leds = output("leds");

void main()
{
    int digits[] = {0x7E, 0x30, 0x6D, 0x79, 0x33, 0x5B, 0x5F, 0x70, 
                    0x7F, 0x7B, 0x77, 0x1F, 0x4E, 0x3D, 0x4F, 0x47};
    while(1) fputc(leds, digits[fgetc(nibble)]);
}
"""

}
