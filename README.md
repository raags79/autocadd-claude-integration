# autocadd-claude-integration

Integration of AutoCADD API with Claude for generating car drawings.

## Connect to Claude

This repository now includes a small Python client for the Anthropic Messages API at `/home/runner/work/autocadd-claude-integration/autocadd-claude-integration/claude_client.py`.

### 1. Export your API key

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

### 2. Send a prompt

```bash
python /home/runner/work/autocadd-claude-integration/autocadd-claude-integration/claude_client.py "Describe a modern electric sedan profile"
```

You can also pipe prompt text in on stdin:

```bash
echo "Generate a car drawing brief for a compact SUV" | python /home/runner/work/autocadd-claude-integration/autocadd-claude-integration/claude_client.py
```

### 3. Optional settings

- `CLAUDE_MODEL`: override the default model (`claude-3-5-sonnet-latest`)
- `CLAUDE_MAX_TOKENS`: override the response limit
- `ANTHROPIC_BASE_URL`: point to a different compatible endpoint if needed
- `--system`: provide a system prompt for domain-specific guidance

### Run tests

```bash
cd /home/runner/work/autocadd-claude-integration/autocadd-claude-integration
python -m unittest discover -s tests
```
