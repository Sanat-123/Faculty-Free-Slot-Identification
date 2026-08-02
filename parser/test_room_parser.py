from parser.components.room_parser import RoomParser

while True:

    text = input("Input : ")

    room, remaining = RoomParser.extract(text)

    print()

    print("Room      :", room)
    print("Remaining :", remaining)

    print("-" * 40)