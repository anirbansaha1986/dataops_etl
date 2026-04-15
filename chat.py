from rag.agent import ask_agent

while True:

    question = input("\nAsk question (or type exit): ")

    if question.lower() == "exit":
        break

    answer = ask_agent(question)

    print("\nAnswer:\n", answer)