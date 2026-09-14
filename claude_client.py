#!/usr/bin/env python3

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


DEFAULT_MODEL = "claude-3-5-sonnet-latest"
DEFAULT_MAX_TOKENS = 1024
DEFAULT_API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_API_VERSION = "2023-06-01"


class ClaudeClient:
    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        api_url: str = DEFAULT_API_URL,
        api_version: str = DEFAULT_API_VERSION,
    ) -> None:
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is required.")

        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.api_url = api_url
        self.api_version = api_version

    def build_payload(self, prompt: str, system: str | None = None) -> dict:
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system
        return payload

    def send_message(self, prompt: str, system: str | None = None) -> str:
        payload = self.build_payload(prompt=prompt, system=system)
        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "content-type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": self.api_version,
            },
        )

        try:
            with urllib.request.urlopen(request) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"Claude API request failed with status {exc.code}: {error_body}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Claude API connection failed: {exc.reason}") from exc

        return self.extract_text(json.loads(body))

    @staticmethod
    def extract_text(response_json: dict) -> str:
        text_blocks = [
            block.get("text", "")
            for block in response_json.get("content", [])
            if block.get("type") == "text"
        ]
        response_text = "\n".join(block for block in text_blocks if block).strip()
        if not response_text:
            raise ValueError("Claude response did not include any text content.")
        return response_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send a prompt to Claude using the Anthropic Messages API."
    )
    parser.add_argument("prompt", nargs="?", help="Prompt text to send to Claude.")
    parser.add_argument(
        "--system",
        help="Optional system prompt to guide the assistant response.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("CLAUDE_MODEL", DEFAULT_MODEL),
        help="Claude model name. Defaults to CLAUDE_MODEL or claude-3-5-sonnet-latest.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=int(os.getenv("CLAUDE_MAX_TOKENS", DEFAULT_MAX_TOKENS)),
        help="Maximum tokens to generate. Defaults to CLAUDE_MAX_TOKENS or 1024.",
    )
    parser.add_argument(
        "--api-url",
        default=os.getenv("ANTHROPIC_BASE_URL", DEFAULT_API_URL),
        help="Anthropic Messages API endpoint.",
    )
    return parser.parse_args()


def resolve_prompt(cli_prompt: str | None) -> str:
    if cli_prompt:
        return cli_prompt
    if not sys.stdin.isatty():
        piped_input = sys.stdin.read().strip()
        if piped_input:
            return piped_input
    raise ValueError("Provide a prompt argument or pipe prompt text on stdin.")


def main() -> int:
    args = parse_args()
    prompt = resolve_prompt(args.prompt)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = ClaudeClient(
        api_key=api_key or "",
        model=args.model,
        max_tokens=args.max_tokens,
        api_url=args.api_url,
    )
    print(client.send_message(prompt=prompt, system=args.system))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1) from exc
