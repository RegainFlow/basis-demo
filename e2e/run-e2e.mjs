import { spawn, spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const e2eRoot = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(e2eRoot, "..");
const children = [];

function commandName(name) {
  return process.platform === "win32" && name === "npm" ? "npm.cmd" : name;
}

function start(command, args) {
  const child = spawn(command, args, {
    cwd: repoRoot,
    detached: process.platform !== "win32",
    shell: false,
    stdio: ["ignore", "pipe", "pipe"],
  });

  child.stdout.on("data", (chunk) => process.stdout.write(chunk));
  child.stderr.on("data", (chunk) => process.stderr.write(chunk));
  child.on("error", (error) => {
    console.error(error);
    process.exitCode = 1;
  });
  children.push(child);
  return child;
}

async function waitFor(url) {
  const deadline = Date.now() + 120_000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(url);
      if (response.ok) {
        return;
      }
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 500));
    }
  }
  throw new Error(`Timed out waiting for ${url}`);
}

function stopAll() {
  for (const child of children.reverse()) {
    child.stdout?.destroy();
    child.stderr?.destroy();
    if (!child.pid || child.exitCode !== null) {
      continue;
    }
    if (process.platform === "win32") {
      spawnSync("taskkill", ["/pid", String(child.pid), "/T", "/F"], {
        stdio: "ignore",
      });
    } else {
      try {
        process.kill(-child.pid, "SIGTERM");
      } catch {
        child.kill("SIGTERM");
      }
    }
  }
}

async function main() {
  start(commandName("uv"), [
    "--cache-dir",
    ".uv-cache",
    "run",
    "uvicorn",
    "api.main:app",
    "--app-dir",
    "packages/api/src",
    "--host",
    "127.0.0.1",
    "--port",
    "8000",
  ]);
  start(commandName("npm"), [
    "--workspace",
    "packages/web",
    "run",
    "dev",
    "--",
    "--host",
    "127.0.0.1",
    "--port",
    "5173",
  ]);

  await waitFor("http://127.0.0.1:8000/healthz");
  await waitFor("http://127.0.0.1:5173");

  const result = spawnSync(
    commandName("npm"),
    [
      "--workspace",
      "e2e",
      "exec",
      "--",
      "playwright",
      "test",
      "--config",
      path.join(e2eRoot, "playwright.config.ts"),
    ],
    {
      cwd: repoRoot,
      stdio: "inherit",
    },
  );
  process.exitCode = result.status ?? 1;
}

process.on("exit", stopAll);
process.on("SIGINT", () => {
  stopAll();
  process.exit(130);
});
process.on("SIGTERM", () => {
  stopAll();
  process.exit(143);
});

try {
  await main();
} finally {
  stopAll();
}

process.exit(process.exitCode ?? 0);
