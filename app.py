from graph import get_agent

agent = get_agent()

config = {
    "configurable": {
        "thread_id": "user-1"
    }
}

print("=" * 60)
print("🤖 AI Research Assistant (LangGraph ReAct Agent)")
print("Type 'exit' to quit.")
print("=" * 60)

while True:
    query = input("\nYou: ")

    if query.lower() == "exit":
        print("\nGoodbye! 👋")
        break

    try:
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            },
            config=config
        )

        print("\nAgent:", response["messages"][-1].content)

    except Exception as e:
        print(f"\nError: {e}")