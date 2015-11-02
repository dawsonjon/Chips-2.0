import os

report = open("docs/source/user_manual/c_library.rst", "w")
report.write("\n")
report.write("C Libraries\n")
report.write("===========\n")
report.write("\n")
for i in sorted(["math.h", "stdio.h", "ctype.h", "stdlib.h"]):
    input_file = os.path.join("chips/compiler/include", i)
    inf = open(input_file)
    for line in inf:
        if line.startswith("///"):
            report.write(line.lstrip("/").rstrip() + "\n")

