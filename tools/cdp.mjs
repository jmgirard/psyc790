// Minimal headless-Chrome driver over the DevTools Protocol.
//
// No npm dependencies: Node's global WebSocket is enough, so `tools/` stays a
// couple of files you can read rather than a node_modules tree. It drives the
// Chrome that Puppeteer already cached on this machine; point CHROME_PATH at
// another binary if that ever moves.
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { setTimeout as sleep } from "node:timers/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import { readdirSync } from "node:fs";

function findChrome() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const cache = join(homedir(), ".cache/puppeteer/chrome-headless-shell");
  if (existsSync(cache)) {
    for (const build of readdirSync(cache).sort().reverse()) {
      for (const dir of ["chrome-headless-shell-mac-arm64", "chrome-headless-shell-mac-x64",
                         "chrome-headless-shell-linux64"]) {
        const bin = join(cache, build, dir, "chrome-headless-shell");
        if (existsSync(bin)) return bin;
      }
    }
  }
  const fallback = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  if (existsSync(fallback)) return fallback;
  throw new Error(
    "No Chrome found. Set CHROME_PATH, or install one with:\n" +
    "  npx @puppeteer/browsers install chrome-headless-shell@stable"
  );
}

export async function withBrowser(fn, { width = 1920, height = 1080 } = {}) {
  // Unique port and profile per run. A leftover instance otherwise holds the
  // profile lock and the new one silently attaches to the old browser, which
  // looks like a hang.
  const port = 9300 + (process.pid % 400);
  const proc = spawn(findChrome(), [
    `--remote-debugging-port=${port}`,
    `--window-size=${width},${height}`,
    "--disable-gpu",
    "--no-sandbox",
    "--hide-scrollbars",
    `--user-data-dir=/tmp/cdp-profile-${process.pid}`,
    "--allow-file-access-from-files",
  ]);
  proc.stderr.on("data", () => {});

  let version;
  for (let i = 0; i < 60; i++) {
    try {
      version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
      break;
    } catch { await sleep(200); }
  }
  if (!version) { proc.kill(); throw new Error("chrome did not start"); }

  const ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r, { once: true }));
  let id = 0;
  const pending = new Map();
  ws.addEventListener("message", (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      msg.error ? reject(new Error(JSON.stringify(msg.error))) : resolve(msg.result);
    }
  });
  const send = (method, params = {}, sessionId) =>
    new Promise((resolve, reject) => {
      const mid = ++id;
      pending.set(mid, { resolve, reject });
      ws.send(JSON.stringify({ id: mid, method, params, sessionId }));
    });

  const { targetId } = await send("Target.createTarget", { url: "about:blank" });
  const { sessionId } = await send("Target.attachToTarget", { targetId, flatten: true });
  const S = (m, p) => send(m, p, sessionId);
  await S("Page.enable");
  await S("Runtime.enable");
  await S("Emulation.setDeviceMetricsOverride",
          { width, height, deviceScaleFactor: 1, mobile: false });

  const page = {
    async goto(url) {
      // Adding only a #hash to the current URL is a same-document navigation and
      // fires no load event, so callers must go via about:blank for that case.
      const done = new Promise((resolve) => {
        const h = (ev) => {
          const m = JSON.parse(ev.data);
          if (m.method === "Page.loadEventFired" && m.sessionId === sessionId) {
            ws.removeEventListener("message", h);
            resolve();
          }
        };
        ws.addEventListener("message", h);
      });
      await S("Page.navigate", { url });
      await done;
    },
    async screenshot() {
      return (await S("Page.captureScreenshot", { format: "png" })).data;
    },
    async eval(expression) {
      const r = await S("Runtime.evaluate",
                        { expression, awaitPromise: true, returnByValue: true });
      if (r.exceptionDetails)
        throw new Error(r.exceptionDetails.exception?.description || "eval failed");
      return r.result.value;
    },
  };

  try {
    return await fn(page);
  } finally {
    ws.close();
    proc.kill();
  }
}
