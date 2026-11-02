import { createServer } from "node:http";
import { createReadStream } from "node:fs";
import { mkdir, readFile, readdir, stat, writeFile } from "node:fs/promises";
import path, { extname, relative, resolve, sep } from "node:path";
import AxeBuilder from "@axe-core/playwright";
import { chromium } from "playwright";

const siteDirectory = path.resolve(process.argv[2] ?? "site");
const reportPath = path.resolve(
  process.argv[3] ?? "engineering/qa/accessibility-report.json",
);
const mkdocsConfig = await readFile("mkdocs.yml", "utf8");
const siteUrl = mkdocsConfig.match(/^site_url:\s*["']?([^"'\s]+)["']?\s*$/m)?.[1];
if (!siteUrl) throw new Error("site_url is required to audit the deployed Pages path");
const siteBasePath = new URL(siteUrl).pathname.endsWith("/")
  ? new URL(siteUrl).pathname
  : `${new URL(siteUrl).pathname}/`;
const contentTypes = {
  ".css": "text/css; charset=utf-8",
  ".gif": "image/gif",
  ".html": "text/html; charset=utf-8",
  ".jpeg": "image/jpeg",
  ".jpg": "image/jpeg",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".ttf": "font/ttf",
  ".txt": "text/plain; charset=utf-8",
  ".webp": "image/webp",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".xml": "application/xml; charset=utf-8",
  ".zip": "application/zip",
};

function createSiteServer() {
  const root = resolve(siteDirectory);
  return createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
      if (!pathname.startsWith(siteBasePath)) {
        response.writeHead(404).end("Not found");
        return;
      }
      const relativePath = pathname.slice(siteBasePath.length);
      let file = resolve(root, `./${relativePath}`);
      if (file !== root && !file.startsWith(`${root}${sep}`)) {
        response.writeHead(403).end("Forbidden");
        return;
      }
      let info = await stat(file).catch(() => null);
      if (info?.isDirectory()) {
        file = resolve(file, "index.html");
        info = await stat(file).catch(() => null);
      }
      if (!info?.isFile()) {
        response.writeHead(404).end("Not found");
        return;
      }
      response.writeHead(200, {
        "content-length": info.size,
        "content-type": contentTypes[extname(file).toLowerCase()] ?? "application/octet-stream",
      });
      createReadStream(file).pipe(response);
    } catch {
      response.writeHead(400).end("Bad request");
    }
  });
}

async function main() {
  const htmlFiles = [];
  async function collect(directory) {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const entryPath = path.join(directory, entry.name);
      if (entry.isDirectory()) await collect(entryPath);
      else if (entry.isFile() && entry.name.endsWith(".html")) htmlFiles.push(entryPath);
    }
  }

  await collect(siteDirectory);
  if (htmlFiles.length === 0) throw new Error(`No rendered HTML pages found in ${siteDirectory}`);

  const browser = await chromium.launch({ headless: true });
  const server = createSiteServer();
  const pages = [];
  try {
    await new Promise((resolveListen, reject) => {
      server.once("error", reject);
      server.listen(0, "127.0.0.1", resolveListen);
    });
    const address = server.address();
    const origin = `http://127.0.0.1:${address.port}`;
    for (const htmlFile of htmlFiles.sort()) {
      const context = await browser.newContext({
        colorScheme: "dark",
        viewport: { width: 1440, height: 1000 },
      });
      const page = await context.newPage();
      await page.route("**/*", async (route) => {
        if (new URL(route.request().url()).origin !== origin) await route.abort();
        else await route.continue();
      });
      await page.emulateMedia({ reducedMotion: "reduce" });
      const pagePath = relative(siteDirectory, htmlFile).split(path.sep).join("/");
      const routePath = pagePath === "index.html"
        ? ""
        : pagePath.endsWith("/index.html")
          ? pagePath.slice(0, -"index.html".length)
          : pagePath;
      await page.goto(`${origin}${siteBasePath}${routePath}`, { waitUntil: "load" });
      const results = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"])
        .analyze();
      pages.push({
        path: path.relative(siteDirectory, htmlFile).split(path.sep).join("/"),
        title: await page.title(),
        violations: results.violations.map((violation) => ({
          id: violation.id,
          impact: violation.impact,
          description: violation.description,
          help: violation.help,
          helpUrl: violation.helpUrl,
          nodes: violation.nodes.map((node) => ({
            target: node.target,
            html: node.html,
            failureSummary: node.failureSummary,
          })),
        })),
      });
      await context.close();
    }
  } finally {
    await browser.close();
    await new Promise((resolveClose, reject) => server.close((error) => error ? reject(error) : resolveClose()));
  }

  const violations = pages.flatMap((page) => page.violations.map((violation) => ({
    page: page.path,
    ...violation,
  })));
  const counts = {
    critical: violations.filter((violation) => violation.impact === "critical").length,
    serious: violations.filter((violation) => violation.impact === "serious").length,
    moderate: violations.filter((violation) => violation.impact === "moderate").length,
    minor: violations.filter((violation) => violation.impact === "minor").length,
  };
  const report = {
    generatedAt: new Date().toISOString(),
    site: siteDirectory,
    pageCount: pages.length,
    counts,
    pages,
  };

  await mkdir(path.dirname(reportPath), { recursive: true });
  await writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);
  console.log(
    `Accessibility audit: ${pages.length} pages; ` +
      `${counts.critical} critical, ${counts.serious} serious, ` +
      `${counts.moderate} moderate, ${counts.minor} minor. Report: ${reportPath}`,
  );
  if (counts.critical + counts.serious > 0) process.exitCode = 1;
}

main().catch((error) => {
  console.error(`Accessibility audit failed: ${error.message}`);
  process.exitCode = 1;
});
