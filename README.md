# autocadd-claude-integration

Use Claude to generate executable AutoCAD `.scr` files from natural-language prompts.

## Prerequisites

- Node.js 18+
- An Anthropic API key
- AutoCAD (to run the generated `.scr` file)

## Setup

```bash
npm install
```

Set your API key:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

Optional model override:

```bash
export CLAUDE_MODEL="claude-sonnet-4-5"
```

## Generate an AutoCAD script

```bash
npm run generate -- "Draw a simple 2D car side view with wheels and body outline"
```

This creates:

- `/home/runner/work/autocadd-claude-integration/autocadd-claude-integration/output/drawing.scr`

## Run in AutoCAD

1. Open AutoCAD.
2. Start a new or existing drawing.
3. Run the `SCRIPT` command.
4. Select `output/drawing.scr`.

Claude output is constrained to plain AutoCAD command lines suitable for `.scr` execution.
