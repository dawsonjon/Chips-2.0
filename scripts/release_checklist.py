import os

while 1:
    ifn = open("version")
    major, minor, revision = ifn.read().split(".")
    major = int(major)
    minor = int(minor)
    revision = int(revision)
    ifn.close()
    print "version", major, minor, revision

    print "Increment Major version ?"
    if raw_input().upper() == "Y":
        major += 1
        minor = 0
        revision = 0
        ofn = open("version", "w")
        ofn.write("%u.%u.%u" % (major, minor, revision))
        ofn.close()


    print "Increment Minor version ?"
    if raw_input().upper() == "Y":
        minor += 1
        revision = 0
        ofn = open("version", "w")
        ofn.write("%u.%u.%u" % (major, minor, revision))
        ofn.close()

    print "Increment Revision ?"
    if raw_input().upper() == "Y":
        revision += 1
        ofn = open("version", "w")
        ofn.write("%u.%u.%u" % (major, minor, revision))
        ofn.close()

    ifn = open("version")
    major, minor, revision = ifn.read().split(".")
    ifn.close()
    print "version", major, minor, revision

    print "Version OK ?"
    if raw_input().upper() == "Y":
        break

while 1:

    print "Lint Code ?"
    if raw_input().upper() == "Y":
        os.system("flake8 chips/*/*.py")

    print "Auto Tidy Code ?"
    if raw_input().upper() == "Y":
        os.system("autopep8 -v --in-place -a -a chips/*/*.py")

    print "Code Correct ?"
    if raw_input().upper() == "Y":
        break

while 1:
    print "Run Automatic Tests?"
    if raw_input().upper() == "Y":
        os.chdir("test_suite")
        os.system("./test_all")
        os.chdir("..")

    print "Run Manual Tests?"
    if raw_input().upper() == "Y":
        os.chdir("examples")
        os.system("./example_1.py")
        os.system("./example_2.py")
        os.system("./example_3.py")
        os.system("./example_4.py")
        os.system("./example_5.py")
        os.system("./example_6.py")
        os.system("./example_7.py")
        os.system("./example_8.py")
        os.system("./example_9.py")
        os.chdir("..")
        os.system("python -m chips.utils.debugger")
        os.system("python -m chips.utils.block_diagram")

    print "Tests OK ?"
    if raw_input().upper() == "Y":
        break

while 1:

    print "Build the documentation ?"
    if raw_input().upper() == "Y":
        os.chdir("docs")
        os.system("make html")
        os.system("make pdf")
        os.system("make linkcheck")
        os.system("make doctest")
        os.chdir("..")

    print "Review the documentation ?"
    if raw_input().upper() == "Y":
        os.system("google-chrome docs/build/html/index.html")

    print "Publish documentation ?"
    if raw_input().upper() == "Y":
        os.system("scripts/publish_docs")

    print "Documentation OK ?"
    if raw_input().upper() == "Y":
        break

while 1:

    os.system("git status")

    print "commit all?"
    if raw_input().upper() == "Y":
        os.system("git add .")
        os.system("git commit")

    print "tag version ?"
    if raw_input().upper() == "Y":
        os.system("git tag %u.%u.%u"%(major, minor, revision))

    print "push ?"
    if raw_input().upper() == "Y":
        os.system("git push origin master")

    print "Version Control OK ?"
    if raw_input().upper() == "Y":
        break


print "Ready to Release?"
if raw_input().upper() == "Y":
    os.system("python setup.py register")
