import unittest

from claude_client import ClaudeClient, DEFAULT_MAX_TOKENS, DEFAULT_MODEL, resolve_prompt


class ClaudeClientTests(unittest.TestCase):
    def test_build_payload_uses_defaults(self) -> None:
        client = ClaudeClient(api_key="test-key")

        payload = client.build_payload("Draw a coupe")

        self.assertEqual(payload["model"], DEFAULT_MODEL)
        self.assertEqual(payload["max_tokens"], DEFAULT_MAX_TOKENS)
        self.assertEqual(
            payload["messages"],
            [{"role": "user", "content": "Draw a coupe"}],
        )
        self.assertNotIn("system", payload)

    def test_build_payload_includes_system_prompt(self) -> None:
        client = ClaudeClient(api_key="test-key", model="custom-model", max_tokens=512)

        payload = client.build_payload("Draw an SUV", system="Use CAD terminology.")

        self.assertEqual(payload["model"], "custom-model")
        self.assertEqual(payload["max_tokens"], 512)
        self.assertEqual(payload["system"], "Use CAD terminology.")

    def test_extract_text_combines_text_blocks(self) -> None:
        response = {
            "content": [
                {"type": "text", "text": "First line"},
                {"type": "tool_use", "id": "ignored"},
                {"type": "text", "text": "Second line"},
            ]
        }

        self.assertEqual(
            ClaudeClient.extract_text(response),
            "First line\nSecond line",
        )

    def test_extract_text_requires_text_content(self) -> None:
        with self.assertRaises(ValueError):
            ClaudeClient.extract_text({"content": [{"type": "tool_use"}]})

    def test_resolve_prompt_uses_cli_value(self) -> None:
        self.assertEqual(resolve_prompt("hello"), "hello")


if __name__ == "__main__":
    unittest.main()
