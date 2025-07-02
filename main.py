# main.py
import requests

from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filters.profanity_filter import ProfanityFilter

def main():
    BASE_URL = "http://localhost:11434/api/chat"
    conversation_history = []

    # Create a single Orchestrator instance.
    # You may add or configure filters separately if needed.
    orchestrator = FilterOrchestrator(mode="serial")
    orchestrator.add_filter(ProfanityFilter())

    print("Simple console chat with llama3.2 (example). Type Ctrl+C or an empty line to exit.\n")

    while True:
        try:
            user_input = input("User: ")
            if not user_input.strip():
                print("Exiting chat.")
                break

            # ---- 1) Inbound Filtering on User Input ----
            inbound_result = orchestrator.run(user_input)

            if inbound_result.verdict == "block":
                print(f"[SYSTEM] Request blocked by filters: {inbound_result.reason}")
                continue
            elif inbound_result.verdict == "sanitize":
                # 'sanitized_text' is the typically used field if the filter replaced something
                user_input_filtered = inbound_result.metadata.get("sanitized_text", "")
                print(f"[SYSTEM] User input sanitized: {user_input_filtered}")
            else:
                # 'allow' verdict => text is in 'final_text'
                user_input_filtered = inbound_result.metadata.get("final_text", "")

            # ---- Add user message to the conversation history ----
            conversation_history.append({"role": "user", "content": user_input_filtered})

            # ---- 2) Send the request to the LLM API ----
            payload = {
                "model": "llama3.2",
                "messages": conversation_history,
                "stream": False
            }

            try:
                response = requests.post(BASE_URL, json=payload)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Communication with LLM failed: {e}")
                # Optionally remove last user message if the request fails
                conversation_history.pop()
                continue

            result = response.json()
            llm_output = result.get("message", {}).get("content", "")

            # ---- 3) Outbound Filtering on LLM Response ----
            outbound_result = orchestrator.run(llm_output)

            if outbound_result.verdict == "block":
                print(f"[SYSTEM] LLM response blocked by filters: {outbound_result.reason}")
                # You may choose to remove the last user input from the conversation if blocked
                continue
            elif outbound_result.verdict == "sanitize":
                llm_output_filtered = outbound_result.metadata.get("sanitized_text", "")
                print(f"[SYSTEM] LLM output sanitized: {llm_output_filtered}")
            else:
                llm_output_filtered = outbound_result.metadata.get("final_text", "")

            # ---- 4) Display LLM response & add to conversation ----
            print(f"Assistant: {llm_output_filtered}")
            conversation_history.append({"role": "assistant", "content": llm_output_filtered})

        except KeyboardInterrupt:
            print("\nExiting chat.")
            break


if __name__ == "__main__":
    main()
