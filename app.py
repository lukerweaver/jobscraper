from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
from urllib.parse import urlparse

app = FastAPI(title="Job Scraper Service")

@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/jobs/hiringcafe")
async def jobs(search_url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Wait for Hiring Cafe's job search API call.
            async with page.expect_response(
                lambda response: urlparse(response.url).path == "/api/search-jobs",
                timeout=30000,
            ) as response_info:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)

            api_response = await response_info.value
            return await api_response.json()
        except Exception as exc:
            raise HTTPException(
                status_code=504,
                detail=f"Failed to capture Hiring Cafe jobs response: {exc}",
            ) from exc
        finally:
            await context.close()
            await browser.close()
