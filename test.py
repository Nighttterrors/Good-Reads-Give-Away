import asyncio
from playwright.async_api import async_playwright

async def test_bot_blocking():
    bot_user_agents = [
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
        "Mozilla/5.0 (compatible; DuckDuckBot/1.0; +http://duckduckgo.com/duckduckbot.html)",
        "Mozilla/5.0 (compatible; Sogou web spider/4.0; +http://www.sogou.com/docs/help/webmasters.htm#07)",
        "Mozilla/5.0 (compatible; Exabot/3.0; +http://www.exabot.com/go/robot)",
        "Mozilla/5.0 (compatible; facebot/1.0; +http://www.facebook.com/externalhit_uatext.php)",
        "Mozilla/5.0 (compatible; ia_archiver; +http://www.alexa.com/site/help/webmasters;"
        ]


    async with async_playwright() as p:
        browser = await p.chromium.launch()


        for i, ua in enumerate(bot_user_agents,1):
            page = await browser.new_page(user_agent=ua)

            try:
                response = await page.goto('https://cloudninjas.com/', timeout=10000)
                status = response.status if response else 'No Response'
                print(f"{i}. {ua[:50]}...-> Status: {status}" )
            except Exception as e:
                print(f"{i}. {ua[:50]}...-> Blocked: {str(e)[:50]}")
            finally:
                await page.close()
asyncio.run(test_bot_blocking())

        
