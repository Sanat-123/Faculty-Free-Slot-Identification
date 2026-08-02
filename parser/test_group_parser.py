from parser.components.group_parser import GroupParser

while True:

    text = input("Input : ")

    group, remaining = GroupParser.extract(text)

    print()

    print("Group     :", group)
    print("Remaining :", remaining)

    print("-" * 40)