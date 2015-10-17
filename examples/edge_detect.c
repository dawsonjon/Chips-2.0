/*Edge Detection*/
/*Jonathan P Dawson 2014-07-06*/

void set_xy(int image[], int x, int y, int pixel){
    if(x<0) return;
    if(x>=WIDTH) return;
    image[x+y*WIDTH] = pixel;
}

int get_xy(int image[], int x, int y){
    if(x<0) return 0;
    if(x>=WIDTH) return 0;
    return image[x+y*WIDTH];
}

void main()
{

    unsigned image_in = input("image_in");
    unsigned image_out = output("image_out");

    unsigned image[SIZE];
    unsigned new_image[SIZE];

    int x, y, pixel;

    while(1){

        /* read in image */
        for(y=0; y<HEIGHT; y++){
            for(x=0; x<WIDTH; x++){
                set_xy(image, x, y, fgetc(image_in));
            }
            report(y);
        }

        /* apply edge detect */
        for(y=0; y<HEIGHT; y++){
            for(x=0; x<WIDTH; x++){

                pixel =  get_xy(image, x,   y  ) << 2;
                pixel -= get_xy(image, x-1, y+1);
                pixel -= get_xy(image, x+1, y-1);
                pixel -= get_xy(image, x-1, y-1);
                pixel -= get_xy(image, x+1, y+1);
                set_xy(new_image, x, y, pixel);
            }
            report(y);
        }

        /* write out image */
        for(y=0; y<HEIGHT; y++){
            for(x=0; x<WIDTH; x++){
                fputc(get_xy(new_image, x, y), image_out);
            }
            report(y);
        }

    }
}
