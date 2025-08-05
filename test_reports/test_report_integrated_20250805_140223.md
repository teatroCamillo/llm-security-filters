# 🧪 Test Report for `integrated` (2025-08-05 14:02:23.264795)

Total tests: 49

- `tests/integrated/test_filter_orchestrator.py::test_should_allow_sentence_without_profanity` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_sentence_with_profanity` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_allow_low_weight_profanity_in_threshold_mode` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_high_weight_profanity_in_threshold_mode` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_phone_number_by_sensitive_filter` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_allow_low_weight_sensitive_data_in_threshold_mode` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_high_weight_sensitive_data_in_threshold_mode` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_bypass_instruction` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_bypass_instruction_in_threshold_mode` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_allow_low_weight_bypass_in_threshold_mode` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_allow_positive_sentiment` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_allow_sentiment_below_threshold_weight` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_sentiment_above_threshold_weight` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_if_any_filter_blocks` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_allow_if_all_filters_allow` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_allow_empty_string` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_allow_neutral_sentence` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_all_caps_profanity` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_should_block_mixed_sensitive_and_profanity` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[This is clean text.-filters0-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[This is damn bad.-filters1-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Call me at 123-456-7890!-filters2-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Disable firewall.-filters3-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[I love this!-filters4-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Here is my SSN: 123-45-6789.-filters5-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[You damn fool-filters6-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Happy mood today!-filters7-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Bad stuff, also 123-456-7890-filters8-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Just a comment-filters9-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Profane and 123-456-7890-filters10-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Disable the antivirus please.-filters11-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Very positive message-filters12-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[You bastard 123-456-7890-filters13-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Today is great!-filters14-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Nothing bad here-filters15-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Firewall disable and bad tone-filters16-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[My email is john@example.com-filters17-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Totally safe-filters18-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Fuck! Turn off the firewall.-filters19-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Bad and sensitive + bypass-filters20-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[You suck 555-123-4567 disable AV-filters21-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[All good-filters22-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Kill switch mode-filters23-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Happy happy joy joy-filters24-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Firewall off. Damn.-filters25-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Clean content here.-filters26-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[123-456-7890 and offensive-filters27-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Mild words, kind tone-filters28-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[All filters say block-filters29-blocked]` — ✅ PASSED

---


---

## ✅ Summary

- Total: 49
- ✅ Passed: 49
- ❌ Failed: 0
- ⚠️ Skipped: 0
