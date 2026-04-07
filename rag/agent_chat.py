from rag.rag_query import ask_pipeline

def start_chat():

    print("\n===============================")
    print(" DataOps AI Monitoring Agent ")
    print("===============================")
    print("Ask questions about the ETL pipeline.")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() in ["exit", "quit"]:
            print("Agent: Goodbye!")
            break

        try:
            answer = ask_pipeline(question)

            print("\nAgent:")
            print(answer)
            print()

        except Exception as e:
            print("Agent Error:", str(e))