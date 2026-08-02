from parser.components.class_parser import ClassParser

while True:

    text = input("Input : ")

    class_name, remaining = ClassParser.extract(text)

    print()

    print("Class     :", class_name)
    print("Remaining :", remaining)

    print("-" * 40)