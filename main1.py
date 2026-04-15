from rag.ingest_credit_data import ingest_credit_data
from rag.agent_new import ask_agent


def main():

    print("Ingesting credit fraud dataset...")
    ingest_credit_data()

    print("\nDataOps AI Fraud Agent Ready\n")

    while True:

        question = input("Ask Fraud Agent: ")

        if question.lower() in ["exit", "quit"]:
            break

        answer = ask_agent(question)

        print("\nAI Agent Response:\n")
        print(answer)
        print("\n")


if __name__ == "__main__":
    main()