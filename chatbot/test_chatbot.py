from intents import process_query

print("=" * 60)
print("UNIVERSITY ANALYTICS CHATBOT")
print("=" * 60)

while True:

    user = input("\nYou : ")

    if user.lower() in ["exit", "quit"]:
        print("Good Bye!")
        break

    print("\nBot :")
    print(process_query(user))