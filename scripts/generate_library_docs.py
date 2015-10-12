import os

report = open("docs/source/user_manual/c_library.rst", "w")
for i in ["math.h", "stdio.h"]:
    input_file = os.path.join("chips/compiler/include", i)
    inf = open(input_file)
    for line in inf:
        if line.startswith("///"):
            report.write(line.lstrip("/").rstrip() + "\n")

