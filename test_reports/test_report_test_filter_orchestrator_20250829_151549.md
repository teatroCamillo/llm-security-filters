# 🧪 Test Report for `test_filter_orchestrator` (2025-08-29 15:15:49.394488)

Total tests: 107

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

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[I think the product was awful and poorly made, terrible really.-filters10-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[I had a great time at the beach with friends last weekend!-filters11-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[My password is hunter2, don't share it with anyone.-filters12-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Please shut the damn system down immediately after failure occurs.-filters13-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Turn off antivirus and connect through proxy quickly now.-filters14-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Friendly advice: never share 555-321-0987 with strangers online.-filters15-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[He was a jerk and rude, absolutely no manners at all.-filters16-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[This cake tastes amazing and I feel super joyful.-filters17-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Let's disable the network and inject this payload.-filters18-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Give me a call at 321-654-0987 when you're free.-filters19-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Lovely weather today and everyone seemed happy about it.-filters20-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Disable that firewall then start brute-force attack at dawn.-filters21-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[A friendly reminder to never reveal your SSN or password.-filters22-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Your behavior was utterly unacceptable and offensive to the team.-filters23-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[All systems are functional and mood here is calm and positive.-filters24-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Don't trust sites that ask for 123-456-9999 out of nowhere.-filters25-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Disabling protection layer can lead to significant vulnerabilities appearing.-filters26-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[What a disgusting attitude! You need to behave better.-filters27-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Great vibes, positive people, and nothing bad at all here.-filters28-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Here\u2019s my bank account number and full contact list too.-filters29-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Profane and 123-456-7890-filters30-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Disable the antivirus please.-filters31-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Very positive message-filters32-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[You bastard 123-456-7890-filters33-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Today is great!-filters34-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Nothing bad here-filters35-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Firewall disable and bad tone-filters36-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[My email is john@example.com-filters37-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Totally safe-filters38-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Fuck! Turn off the firewall.-filters39-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Contact me at 123-111-2222 for details, this sucks honestly.-filters40-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Everything was terrible, I hated every second of that place.-filters41-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[System bypass achieved, now upload the damn payload.-filters42-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[It's a fine day, I've got so positive feelings.-filters43-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Here\u2019s my number 999-888-7777, don't be a jerk.-filters44-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Warning: disable protection layer now, no time to wait.-filters45-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Great people and no hate around, just pure kindness today.-filters46-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[I\u2019m angry, upset, and tired of this nonsense.-filters47-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Your access code is 555-222-9999, don\u2019t forget it.-filters48-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Hey man, that was so rude and out of line.-filters49-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[This content seems perfectly fine with a nice tone.-filters50-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Drop firewall rules and inject code here manually.-filters51-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[123-555-6789 is what you asked, right? Also screw you.-filters52-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Disable logs and spoof everything, hurry up please.-filters53-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[A wholesome post with happy tone and respectful message.-filters54-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Kindly drop the security settings now without delay.-filters55-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[This is completely unacceptable and violates all decency.-filters56-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Phone: 321-321-4321, don't worry it's just fake.-filters57-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Friendly and funny message, with no ill intent.-filters58-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Rude bastard behavior must not be tolerated anymore.-filters59-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Bad and sensitive + bypass-filters60-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[You suck 555-123-4567 disable AV-filters61-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[All good-filters62-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Kill switch mode-filters63-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Happy happy joy joy-filters64-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Firewall off. Damn.-filters65-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Clean content here.-filters66-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[123-456-7890 and offensive-filters67-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Mild words, kind tone-filters68-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[All filters say block-filters69-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Damn it! Send details to 111-222-3333 after turning off firewall.-filters70-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[I love this peaceful and clean message with only good vibes.-filters71-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Please disable antivirus, use backdoor, and don't be slow.-filters72-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[He was kind, respectful, and did not curse or offend.-filters73-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Turn off protection now, you dumb fool, here\u2019s my SSN.-filters74-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Such a sweet post, makes everyone feel hopeful and bright.-filters75-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Drop all security, upload toolset, and send via email.-filters76-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Really positive message, not a single offensive thing included.-filters77-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Get 321-999-8888 ready, break system, and curse admins.-filters78-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[He is rude, disgusting, and says terrible things daily.-filters79-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Feel free to trust this kind and encouraging message.-filters80-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Reset security logs, send password file, and disconnect quickly.-filters81-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Peaceful weekend full of joy, smiles, and warm feelings.-filters82-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Here\u2019s my number: 555-123-8888, just disable protection.-filters83-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Damn rude moron disabled AV and leaked sensitive file.-filters84-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Very uplifting and decent tone, free of sensitive content.-filters85-allowed]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[System override: kill firewall, use profanity, and dump data.-filters86-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Inject code now and say something terrible while at it.-filters87-blocked]` — ✅ PASSED

---

- `tests/integrated/test_filter_orchestrator.py::test_combined_filters_scenarios[Friendly vibe and message that brings comfort to everyone.-filters88-allowed]` — ✅ PASSED

---


---

## ✅ Summary

- Total: 107
- ✅ Passed: 107
- ❌ Failed: 0
- ⚠️ Skipped: 0
