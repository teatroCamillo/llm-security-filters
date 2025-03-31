import sys
import requests
import json

from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator

def main():
    BASE_URL = "http://localhost:11434/api/chat"
    conversation_history = []

    # Create an instance of the orchestrator.
    # Switch 'mode' to "serial", "parallel", or "hybrid" as desired.
    orchestrator = FilterOrchestrator(mode="serial")  

    print("Simple console chat with llama3.2 (example). Type Ctrl+C or an empty line to exit.\n")

    while True:
        try:
            user_input = input("User: ")
            if not user_input.strip():
                print("Exiting chat.")
                break

            # ---- 1) Apply Inbound Filters via Orchestrator ----
            inbound_result = orchestrator.apply_inbound(user_input)
            if inbound_result["verdict"] == "block":
                print(f"[SYSTEM] Request blocked by filters: {inbound_result['reason']}")
                continue
            elif inbound_result["verdict"] == "sanitize":
                user_input_filtered = inbound_result["final_text"]
                print(f"[SYSTEM] User input sanitized: {user_input_filtered}")
            else:
                user_input_filtered = inbound_result["final_text"]

            # ---- Add user message to conversation ----
            conversation_history.append({"role": "user", "content": user_input_filtered})

            # ---- 2) Call the LLM API ----
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
                # Remove last user message from history if needed
                conversation_history.pop()
                continue

            result = response.json()
            llm_output = result.get("message", {}).get("content", "")

            # ---- 3) Apply Outbound Filters via Orchestrator ----
            outbound_result = orchestrator.apply_outbound(llm_output)
            if outbound_result["verdict"] == "block":
                print(f"[SYSTEM] LLM response blocked by filters: {outbound_result['reason']}")
                # Optionally remove from conversation history if blocked
                continue
            elif outbound_result["verdict"] == "sanitize":
                llm_output_filtered = outbound_result["final_text"]
                print(f"[SYSTEM] LLM output sanitized: {llm_output_filtered}")
            else:
                llm_output_filtered = outbound_result["final_text"]

            # ---- 4) Display to user & add to conversation ----
            print(f"Assistant: {llm_output_filtered}")
            conversation_history.append({"role": "assistant", "content": llm_output_filtered})

        except KeyboardInterrupt:
            print("\nExiting chat.")
            break


if __name__ == "__main__":
    main()
