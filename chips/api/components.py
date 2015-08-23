sn=0
def constant(type_, value):

    c_model_name = "constant_%s.c"%sn
    sn+=1
    c_file = open(c_model_name, "w")

    if type_ == "double":
        c_file.write("""
void main(){
  const int output("out"); 
  while(1){ fput_double(%f); }
}"""%value)

    elif type_ == "float":

        c_file.write("""
void main(){
  const int output("out"); 
  while(1){ fput_float(%ff); }
}"""%value)

    elif type_ == "int":

        c_file.write("""
void main(){
  const int output("out"); 
  while(1){ fput_float(%d); }
}"""%value)

    elif type_ == "long":

        c_file.write("""
void main(){
  const int output("out"); 
  while(1){ fput_long(%dl); }
}"""%value)
    
    return Component(c_model_name)

tee = Component(os.path.join(os.path.dirname(__file__), "tee.c"))
discard = Component(os.path.join(os.path.dirname(__file__), "discard.c"))
