import { expect, test } from "@playwright/test";
import { fileURLToPath } from "node:url";
import path from "node:path";

test("upload, edit, and calculate an invoice total", async ({ page }, testInfo) => {
  await page.goto("/");

  const fixturePath = path.join(
    path.dirname(fileURLToPath(import.meta.url)),
    "fixtures",
    "invoice.json",
  );
  await page.getByTestId("invoice-upload").setInputFiles(fixturePath);
  await page.getByLabel("Line 1 unit price").fill("20.005");
  await page.getByTestId("calculate-invoice").click();

  await expect(page.getByTestId("invoice-total")).toContainText("$207.38");
  await expect(page.locator(".money-symbol")).toHaveCSS(
    "color",
    "rgb(17, 132, 91)",
  );
  await page.screenshot({
    path: testInfo.outputPath("invoice-review.png"),
    fullPage: true,
  });
});
