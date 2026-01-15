import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def capturar_horarios():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        
        await page.goto("https://sii.celaya.tecnm.mx/login") 
        print("Por favor, inicia sesión...")
        
        await page.wait_for_selector("table", timeout=120000) 
        
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        with open("horarios_sii.html", "w") as f:
            f.write(html)
            
        print("HTML guardado. Ya puedes cerrar el navegador.")
        await browser.close()

asyncio.run(capturar_horarios())