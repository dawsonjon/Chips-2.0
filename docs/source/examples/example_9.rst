

LZSS Compression
================

LZSS is a simple form of of run length compression that exploits repeated
sequences in a block of data. The encoder scans a block of data, and sends
literal characters. However if the encoder encounters a sequence of characters
that have already been sent, it will substitute the sequence with a
reference to the earlier data. The encoder will always select the longest
matching sequence that it has already sent. To achieve this the encoder
needs to store a number of previously sent characters in a buffer. This buffer
is referred to as the window.

.. code-block:: c

    /*LZSS Compression Component*/
    /*Jonathan P Dawson 2014-07.10*/
    
    unsigned raw_in = input("raw_in");
    unsigned compressed_out = output("compressed_out");
    
    /*Send data of an arbitrary bit length*/
    unsigned packed, stored = 0;
    void send_bits(unsigned data, unsigned bits){
        unsigned i;
        for(i=0; i<bits; i++){
            packed >>= 1;
            packed |= (data & 1) << 31;
            data >>= 1;
            stored++;
            if(stored == 32){
                fputc(packed, compressed_out);
                stored = 0;
            }
        }
    }
    
    /*A function that reads a stream of uncompressed data, 
    and creates a stream of compressed data*/
    
    void compress(){
    
        unsigned pointer, match, match_length, longest_match, longest_match_length;
        unsigned buffer[N];
    
        unsigned new_size;
    
        while(1){
            for(pointer=0; pointer<N; pointer++){
                buffer[pointer] = fgetc(raw_in);
            }
    
            pointer=0;
            new_size = 0;
            while(pointer<N){
    
                /*Find the longest matching string already sent*/
                longest_match = 0;
                longest_match_length = 0;
                for(match=0; match<pointer; match++){
    
                    /*match length of 0 indicates no match*/
                    match_length = 0;
    
                    /*search through buffer to find a match*/
                    while(buffer[match+match_length] == buffer[pointer+match_length]){
                        match_length++;
                    }
    
                    /*If this is the longest match, remember it*/
                    if(match_length > longest_match_length){
                        longest_match = match;
                        longest_match_length = match_length;
                    }
    
                }
    
                /*send data*/
                if(longest_match_length >= 3){
                    send_bits(0, 1);
                    send_bits(longest_match_length, LOG2N);
                    send_bits(pointer - longest_match, LOG2N);
                    pointer += longest_match_length;
                    new_size += LOG2N + LOG2N + 1;
                }
                else{
                    send_bits(1, 1);
                    send_bits(buffer[pointer], 8);
                    pointer++;
                    new_size += 9;
                }
    
                report(pointer);
            }
            /*report the compression ratio of this block in simulation*/
            report(new_size / (8.0*N));
        }
    }

The encoding is simple. A bit is sent to indicate whether a raw character or a
reference continues. A reference consists of a distance length pair. The
distance tells the decoder how many characters ago the matching sequence was
sent, and the distance indicates the length of the matching sequence. The
size of the distance and length pointers will depend on the size of the
window, for example a window size of 1024 requires the pointers to be 10 bits each.

.. code-block:: c

    /*LZSS Decmpression Component*/
    /*Jonathan P Dawson 2014-07-10*/
    
    unsigned raw_out = output("raw_out");
    unsigned compressed_in = input("compressed_in");
    
    /*A function to get data of an arbitrary bit length*/
    
    unsigned stored = 0;
    unsigned packed;
    unsigned get_bits(unsigned bits){
        unsigned i, value = 0;
        for(i=0; i<bits; i++){
            if(!stored){
                stored = 32;
                packed = fgetc(compressed_in);
            }
            value >>= 1;
            value |= (packed & 1) << 31;
            packed >>= 1;
            stored--;
        }
        return value >> (32 - bits);
    }
    
    
    /*Decompress a stream of lzss compressed data, 
    and generate a stream of raw data*/
    
    void decompress(){
        unsigned i, pointer, distance, length, data;
        unsigned buffer[N];
    
        while(1){
    
            /*get distance length*/
            if(get_bits(1)){
                data = get_bits(8);
                buffer[pointer] = data;
                pointer++;
                fputc(data, raw_out);
            }
            else{
                length = get_bits(LOG2N);
                distance = get_bits(LOG2N);
                for(i=0; i<length; i++){
                    data = buffer[pointer-distance];
                    buffer[pointer] = data;
                    pointer++;
                    fputc(data, raw_out);
                }
            }
        }
    }
    
                

In the simulation, a short passage of text is compressed by the encoder
component, sent to the decoder component, decompressed and recovered. A fuller
explanation may be found on `wikipedia <http://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Storer%E2%80%93Szymanski>`_.

