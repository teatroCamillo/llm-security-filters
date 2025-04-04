# llm-security-filters
## How to run
- run ollama
- python main.py
- (optional) if necessary, adjust the configuration

## Tests
pytest tests

## Cache
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
