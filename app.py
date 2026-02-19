from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
import os
from urllib.parse import urlparse

app = FastAPI(title="Hiring Cafe Scraper Service")

@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/jobs/hiringcafe")
async def jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            search_url = os.getenv(
                "HIRINGCAFE_SEARCH_URL",
                "https://hiring.cafe/?searchState=%7B%22restrictJobsToTransparentSalaries%22%3Atrue%2C%22maxCompensationLowEnd%22%3A%22140000%22%2C%22workplaceTypes%22%3A%5B%22Remote%22%5D%2C%22dateFetchedPastNDays%22%3A2%2C%22sortBy%22%3A%22date%22%2C%22searchQuery%22%3A%22product+manager%22%7D",
            )

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
