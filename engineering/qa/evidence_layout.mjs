import assert from "node:assert/strict";
import { createServer } from "node:http";
import { readFile, readdir, mkdir, writeFile } from "node:fs/promises";
import { resolve, sep, extname } from "node:path";
import { chromium } from "playwright";

// Exercise rendered evidence, not CSS source text. No external network is needed.
const site = resolve(process.argv[2] ?? "site");
const report = resolve(process.argv[3] ?? "/tmp/opencode/evidence-layout.json");
const server = createServer(async (request, response) => {
  try {
    let file = resolve(site, `.${decodeURIComponent(new URL(request.url, "http://localhost").pathname)}`);
    assert.ok(file.startsWith(`${site}${sep}`));
    if (request.url.endsWith("/")) file += "/index.html";
    const body = await readFile(file);
    const mime = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".png": "image/png" };
    response.writeHead(200, { "Content-Type": mime[extname(file)] ?? "application/octet-stream" }).end(body);
  } catch {
    response.writeHead(404).end();
  }
});
const browser = await chromium.launch();
const results = [];
try {
  await mkdir(resolve(report, ".."), { recursive: true });
  await new Promise((done) => server.listen(0, "127.0.0.1", done));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const labs = (await readdir(site)).filter((name) => /^(09|10|14|24|25|26|27|28|29|30)-/.test(name));
  assert.equal(labs.length, 10);
  for (const width of [1440, 360]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    await page.route("**/*", (route) => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
    for (const lab of [...labs].sort((a, b) => Number(b.startsWith("30-")) - Number(a.startsWith("30-")))) {
      await page.goto(`${origin}/${lab}/`, { waitUntil: "load" });
      const images = await page.locator('article img[src*="/images/lab-"]').evaluateAll((nodes) => nodes.map((img) => {
        const box = img.getBoundingClientRect();
        const link = img.closest("a");
        return { src: img.src, naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight,
          width: box.width, height: box.height, href: link?.href, alt: img.alt,
          linkName: link?.getAttribute("aria-label") || img.alt };
      }));
      assert.ok(images.length > 0, `${lab}: evidence missing`);
      for (const image of images) {
        assert.ok(image.naturalWidth > 0, `${lab}: image failed to load`);
        assert.ok(image.linkName.length > 10, `${lab}: link needs a useful accessible name`);
        assert.ok(Math.abs(image.width / image.height - image.naturalWidth / image.naturalHeight) < 0.01, `${lab}: distorted image`);
        if (image.naturalHeight > image.naturalWidth) {
          assert.ok(image.width <= 301 && image.width > 200, `${lab}: portrait width ${image.width}`);
        } else if (width === 1440) {
          assert.ok(image.width > 600, `${lab}: terminal/source evidence was shrunk`);
        }
        assert.equal(image.href, image.src, `${lab}: full-resolution original must be linked`);
      }
      const overflow = await page.evaluate(() => ({
        width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
        elements: [...document.querySelectorAll("body *")].filter((el) => {
          const box = el.getBoundingClientRect();
          return box.right > innerWidth && box.width > 0 && getComputedStyle(el).visibility !== "hidden";
        }).slice(0, 10).map((el) => ({ tag: el.tagName, class: el.className, text: el.textContent.slice(0, 80),
          left: el.getBoundingClientRect().left, right: el.getBoundingClientRect().right,
          overflow: getComputedStyle(el).overflow, position: getComputedStyle(el).position,
          parent: el.parentElement.className, parentOverflow: getComputedStyle(el.parentElement).overflow })),
      }));
      assert.ok(overflow.scrollWidth <= width, `${lab}: horizontal overflow ${JSON.stringify(overflow)}`);
      results.push({ lab, viewport: width, images });
    }
    await page.goto(`${origin}/30-runtime-bypass/`);
    const original = page.locator('article a:has(img[src*="passcode-rejected.png"])');
    await original.focus();
    await page.keyboard.press("Enter");
    await page.waitForURL("**/images/lab-30/passcode-rejected.png");
    assert.ok((await page.locator("img").getAttribute("src")).endsWith("passcode-rejected.png"));
    await page.goto(`${origin}/30-runtime-bypass/`);
    await page.locator('article img[src*="passcode-rejected.png"]').scrollIntoViewIfNeeded();
    await page.screenshot({ path: resolve(report, `../evidence-${width}.png`) });
    await page.close();
  }
  assert.equal(results.filter((r) => r.viewport === 1440).flatMap((r) => r.images).length, 16);
  await mkdir(resolve(report, ".."), { recursive: true });
  await writeFile(report, JSON.stringify(results, null, 2));
  console.log(`Evidence layout passed: 10 labs, 16 originals, desktop/mobile. Report: ${report}`);
} finally {
  await browser.close();
  await new Promise((done) => server.close(done));
}
