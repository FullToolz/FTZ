import strSniffer
import Jpat
import DSWL
import HexoRat
import rich

print(
    """\n
 88888888b          dP dP d888888P                   dP
 88                 88 88    88                      88
a88aaaa    dP    dP 88 88    88    .d8888b. .d8888b. 88 d888888b
 88        88    88 88 88    88    88'  `88 88'  `88 88    .d8P'
 88        88.  .88 88 88    88    88.  .88 88.  .88 88  .Y8P
 dP        `88888P' dP dP    dP    `88888P' `88888P' dP d888888P

                                                                 """
)

print("\n")

path = input("Enter executable/library file path: ")


print("\n")

while True:
    print("#1. strSniff ")
    print("#2. JPat ")
    print("#3. DSWL (incomplete)")  # ? -> Decode String Within LEA
    print("#4. HexoRat")

    user_input = input(">> ")

    match user_input:
        case "1":
            strSniffer.main(path)
        case "2":
            Jpat.main(path)
        case "3":
            DSWL.main(path)
        case "4":
            HexoRat.main(path)
