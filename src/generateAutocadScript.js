const fs = require("node:fs/promises");
const path = require("node:path");
const Anthropic = require("@anthropic-ai/sdk");

function parseArgs(argv) {
  const joined = argv.join(" ").trim();
  if (!joined) {
    throw new Error(
      "Missing prompt. Usage: npm run generate -- \"draw a 2D sedan top view\""
    );
  }
  return joined;
}

function buildSystemPrompt() {
  return [
    "You generate AutoCAD .scr script content only.",
    "Return plain text commands without markdown fences.",
    "Use simple AutoCAD command syntax, one command per line.",
    "Do not include explanations.",
    "Prefer 2D geometry using LINE, PLINE, ARC, CIRCLE, RECTANG, OFFSET, TRIM, FILLET.",
    "Ensure commands are executable when saved as a .scr file."
  ].join(" ");
}

async function generateScript(prompt) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new Error("Missing ANTHROPIC_API_KEY environment variable.");
  }

  const client = new Anthropic({ apiKey });
  const response = await client.messages.create({
    model: process.env.CLAUDE_MODEL || "claude-sonnet-4-5",
    max_tokens: 2000,
    system: buildSystemPrompt(),
    messages: [{ role: "user", content: prompt }]
  });

  const textBlocks = response.content
    .filter((item) => item.type === "text")
    .map((item) => item.text.trim())
    .filter(Boolean);

  if (!textBlocks.length) {
    throw new Error("Claude returned no script text.");
  }

  return `${textBlocks.join("\n\n")}\n`;
}

async function main() {
  const prompt = parseArgs(process.argv.slice(2));
  const script = await generateScript(prompt);

  const outputPath = path.resolve(process.cwd(), "output", "drawing.scr");
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, script, "utf8");

  console.log(`Generated AutoCAD script: ${outputPath}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
