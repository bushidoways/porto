import functools
import http.server
import json
import pathlib
import threading
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'test-results'
OUT.mkdir(exist_ok=True)
PAGES = [ROOT / 'index.html', *sorted((ROOT / 'journal').rglob('*.html'))]
if len(PAGES) < 2:
    raise SystemExit('No journal HTML pages discovered')
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{server.server_port}'
results = []

def check(condition, message):
    if not condition:
        raise AssertionError(message)

def background(page):
    return page.evaluate('getComputedStyle(document.body).backgroundColor')

try:
    with sync_playwright() as p:
        for engine in ('chromium', 'firefox', 'webkit'):
            browser = getattr(p, engine).launch()
            for width in (390, 1440):
                for reduced in ('no-preference', 'reduce'):
                    for file in PAGES:
                        relative = file.relative_to(ROOT).as_posix()
                        row = dict(browser=engine, width=width, motion=reduced, page=relative)
                        context = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion=reduced)
                        page = context.new_page()
                        errors, missing = [], []
                        page.on('pageerror', lambda error: errors.append(str(error)))
                        page.on('response', lambda response: missing.append(f'{response.status} {response.url}') if response.url.startswith(BASE) and response.status >= 400 else None)
                        try:
                            response = page.goto(BASE + '/' + relative, wait_until='load')
                            check(response and response.ok, 'HTML did not load')
                            check(page.locator('h1').count() == 1, 'Expected one main heading')
                            page.wait_for_timeout(1200)
                            check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2'), 'Horizontal overflow')
                            for theme in ('sore', 'malem'):
                                button = page.locator(f'button[data-tset="{theme}"]')
                                check(button.count() == 1, f'Missing shared theme control: {theme}')
                                if not button.is_visible():
                                    menu = page.locator('button[aria-expanded][aria-label="Menu"]')
                                    check(menu.count() == 1, 'Cannot expose theme controls on mobile')
                                    menu.click()
                                button.click()
                                page.wait_for_timeout(1400)
                                check(page.locator('html').get_attribute('data-theme') == theme, f'Theme not applied: {theme}')
                                check(page.evaluate('localStorage.getItem("nang-theme")') == theme, 'Theme preference not persisted')
                                if theme == 'sore':
                                    light = background(page)
                                else:
                                    check(background(page) != light, 'Body background unchanged across themes')
                            page.screenshot(path=str(OUT / f'{engine}-{width}-{reduced}-{file.stem}.png'), full_page=True)
                            for target in PAGES:
                                page.goto(BASE + '/' + target.relative_to(ROOT).as_posix(), wait_until='load')
                                page.wait_for_timeout(300)
                                check(page.locator('html').get_attribute('data-theme') == 'malem', f'Theme lost navigating to {target.name}')
                            check(not errors, 'JavaScript errors: ' + '; '.join(errors))
                            check(not missing, 'Failed local requests: ' + '; '.join(missing))
                            row['status'] = 'passed'
                        except Exception as error:
                            row.update(status='failed', error=str(error))
                            try:
                                page.screenshot(path=str(OUT / f'FAIL-{engine}-{width}-{reduced}-{file.stem}.png'), full_page=True)
                            except Exception:
                                pass
                        finally:
                            results.append(row)
                            context.close()
            browser.close()
finally:
    server.shutdown()
    (OUT / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')

failed = [row for row in results if row['status'] != 'passed']
print(json.dumps({'total': len(results), 'failed': len(failed)}, indent=2))
raise SystemExit(1 if failed else 0)
