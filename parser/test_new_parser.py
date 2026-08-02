from parser.data_cleaner import parse_cell

print("Paste the complete cell.")
print("Press ENTER twice when finished.\n")

while True:

    lines = []

    while True:

        line = input()

        if line == "":
            break

        lines.append(line)

    text = "\n".join(lines)

    result = parse_cell(text)

    print()

    if result:

        for k, v in result.items():
            print(f"{k:8} : {v}")

    else:
        print("None")

    print("-" * 50)