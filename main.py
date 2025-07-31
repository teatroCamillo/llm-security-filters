# main.py
import requests

from llm_sf.filter_manager.filter_orchestrator import FilterOrchestrator
from llm_sf.filter_manager.decision_maker import DecisionMaker
from llm_sf.filter_manager.filter_results_aggregator import FilterResultsAggregator
from llm_sf.filters.profanity_filter import ProfanityFilter
from llm_sf.filters.sentiment_filter import SentimentFilter
from llm_sf.filters.bypass_detection_filter import BypassDetectionFilter
from llm_sf.filters.sensitive_data_filter import SensitiveDataFilter
from llm_sf.utils.constants import Constants

def main():
    BASE_URL = Constants.OLLAMA_CHAT_URL
    conversation_history = []

    # Create a single Orchestrator instance.
    # You may add or configure filters separately if needed.
    dm = DecisionMaker("threshold")
    orchestrator = FilterOrchestrator(dm)
    orchestrator.add_filter(ProfanityFilter())
    # orchestrator.add_filter(SentimentFilter())
    # orchestrator.add_filter(BypassDetectionFilter())
    # orchestrator.add_filter(SensitiveDataFilter())

    print("Simple console chat with llama3.2 (example). Type Ctrl+C or an empty line to exit.\n")

    while True:
        try:
            user_input = input("User: ")
            if not user_input.strip():
                print("Exiting chat.")
                break

            # ---- 1) Inbound Filtering on User Input ----
            inbound_agg = orchestrator.run(user_input)

            if inbound_agg.dm_result.verdict == Constants.BLOCKED:
                print(f"[SYSTEM] Request blocked by filters: {inbound_agg.dm_result.reason}")
                continue
            else:
                user_input_filtered = user_input # inbound_agg.dm_result.metadata.get("final_text", "")

            # ---- Add user message to the conversation history ----
            conversation_history.append({"role": "user", "content": user_input_filtered})
            
            # ---- 2) Send the request to the LLM API ----
            payload = {
                "model": "llama3.2",
                "messages": conversation_history,
                "stream": False
            }

            try:
                response = requests.post(Constants.OLLAMA_CHAT_URL, json=payload)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Communication with LLM failed: {e}")
                conversation_history.pop()
                continue

            result = response.json()
            llm_output = result.get("message", {}).get("content", "")
            
            # ---- 3) Outbound Filtering on LLM Response ----
            outbound_agg = orchestrator.run(llm_output)
            
            if outbound_agg.dm_result.verdict == Constants.BLOCKED:
                print(f"[SYSTEM] LLM response blocked by filters: {outbound_agg.dm_result.reason}")
                continue
            else:
                llm_output_filtered = outbound_agg.dm_result.metadata.get("original_text", "")

            # ---- 4) Display LLM response & add to conversation ----
            print(f"Model: {llm_output_filtered}")
            conversation_history.append({"role": "assistant", "content": llm_output_filtered})

        except KeyboardInterrupt:
            print("\nExiting chat.")
            break


if __name__ == "__main__":
    main()
