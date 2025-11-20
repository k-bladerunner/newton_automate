from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from typing import Dict, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Service for automating Google OAuth login to Newton School"""

    def __init__(self, headless: bool = False):
        self.headless = headless

    async def authenticate_google(
        self,
        email: str,
        password: str,
        timeout: int = 60000
    ) -> Dict[str, str]:
        """
        Automate Google OAuth login and return session cookies

        Args:
            email: Google email address
            password: Google password
            timeout: Maximum time to wait for authentication (ms)

        Returns:
            Dictionary of cookies from the authenticated session

        Raises:
            Exception: If authentication fails
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            page = await context.new_page()

            try:
                logger.info("Navigating to Newton School login page...")
                await page.goto("https://my.newtonschool.co/login", timeout=timeout)
                await page.wait_for_timeout(2000)

                logger.info("Clicking 'Sign in with Google' button...")
                # Wait for and click Google sign-in button
                google_button_selectors = [
                    'button:has-text("Sign in with Google")',
                    'button:has-text("Continue with Google")',
                    'a:has-text("Sign in with Google")',
                    '[aria-label*="Google"]'
                ]

                clicked = False
                for selector in google_button_selectors:
                    try:
                        await page.click(selector, timeout=5000)
                        clicked = True
                        break
                    except:
                        continue

                if not clicked:
                    raise Exception("Could not find Google sign-in button")

                await page.wait_for_timeout(3000)

                # Handle Google OAuth flow
                logger.info("Entering email...")
                await page.fill('input[type="email"]', email)
                await page.click('button:has-text("Next")')
                await page.wait_for_timeout(3000)

                logger.info("Entering password...")
                # Wait for password field to be visible
                await page.wait_for_selector('input[type="password"]', state="visible", timeout=10000)
                await page.fill('input[type="password"]', password)

                # Click Next button
                await page.click('button:has-text("Next")')
                await page.wait_for_timeout(3000)

                # Wait for redirect to Newton dashboard
                logger.info("Waiting for authentication to complete...")
                try:
                    await page.wait_for_url("**/dashboard**", timeout=timeout)
                    logger.info("Authentication successful!")
                except:
                    # Try alternative success indicators
                    await page.wait_for_url("**/my.newtonschool.co/**", timeout=timeout)

                # Extract cookies
                cookies = await context.cookies()
                cookie_dict = {c['name']: c['value'] for c in cookies}

                logger.info(f"Retrieved {len(cookie_dict)} cookies")

                await browser.close()
                return cookie_dict

            except Exception as e:
                logger.error(f"Authentication failed: {str(e)}")
                await browser.close()
                raise Exception(f"Authentication failed: {str(e)}")

    async def validate_session(self, cookies: Dict[str, str]) -> bool:
        """
        Validate if session cookies are still valid

        Args:
            cookies: Dictionary of cookies to validate

        Returns:
            True if session is valid, False otherwise
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()

            # Set cookies
            cookie_list = [
                {
                    "name": name,
                    "value": value,
                    "domain": ".newtonschool.co",
                    "path": "/"
                }
                for name, value in cookies.items()
            ]
            await context.add_cookies(cookie_list)

            page = await context.new_page()

            try:
                # Try to access a protected endpoint
                await page.goto("https://my.newtonschool.co/api/v1/user/me/")
                await page.wait_for_timeout(2000)

                # Check if we got redirected to login
                current_url = page.url
                is_valid = "login" not in current_url.lower()

                await browser.close()
                return is_valid

            except Exception as e:
                logger.error(f"Session validation failed: {str(e)}")
                await browser.close()
                return False

    async def refresh_session(
        self,
        email: str,
        password: str,
        old_cookies: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Refresh an expired session

        Args:
            email: Google email
            password: Google password
            old_cookies: Old expired cookies

        Returns:
            New session cookies
        """
        logger.info("Refreshing expired session...")
        return await self.authenticate_google(email, password)
