from chatbot.intent_detector import IntentDetector

while True:

    q = input("Ask : ")

    print()

    print("Intent :", IntentDetector.detect(q))

    print("-" * 50)