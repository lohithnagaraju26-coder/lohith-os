from agents import Agent, Runner, RunConfig

from config import OPENAI_MODEL, validate_config


def main():
    print("LOHITH OS — LIVE AI TEST")
    print("=" * 40)
    print()

    valid, message = validate_config()

    if not valid:
        print("LIVE AI TEST STOPPED")
        print(message)
        print()
        print("Add your OpenAI API key to .env before running the live test.")
        return

    print(f"Model: {OPENAI_MODEL}")
    print("API key detected.")
    print()
    print("Sending test request...")
    print()

    agent = Agent(
        name="LOHITH OS Test Agent",
        instructions=(
            "You are a simple test agent for LOHITH OS. "
            "Respond briefly and confirm that you are connected."
        ),
        model=OPENAI_MODEL,
    )

    result = Runner.run_sync(
        agent,
        "Say hello to Lohith and confirm that LOHITH OS is connected.",
        run_config=RunConfig(
            workflow_name="LOHITH OS — Live API Test",
            trace_include_sensitive_data=False,
        ),
    )

    print("AI RESPONSE")
    print("-" * 40)
    print(result.final_output)
    print()
    print("LIVE AI TEST PASSED")


if __name__ == "__main__":
    main()