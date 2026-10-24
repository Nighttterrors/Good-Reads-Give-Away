from playwright.sync_api import sync_playwright  # necessary library to implement the script
import os
from dotenv import load_dotenv  # library to load environment variables from .env file
from playwright._impl._errors import TargetClosedError
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)

load_dotenv()  # load environment variables from .env file

console = Console()


with sync_playwright() as p:  # start the playwright

    giveaway_counter = 0  # initialize the giveaway counter

    browser = p.chromium.launch(headless=False)  # launch the browser in non-headless mode
    page = browser.new_page()  # create a new page in the browser

    # ---------------------------------------------------------
    # LOGIN
    # ---------------------------------------------------------

    console.print()
    console.print(
        "[bold cyan]╔══════════════════════════════════════════════╗[/bold cyan]"
    )
    console.print(
        "[bold cyan]║       Goodreads Giveaway Bot Spinning Up     ║[/bold cyan]"
    )
    console.print(
        "[bold cyan]╚══════════════════════════════════════════════`╝[/bold cyan]"
    )
    console.print()

    # go to the GoodReads login
    page.goto(
        "https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=eyJyZXR1cm5fdXJsIjoiaHR0cHM6Ly93d3cuZ29vZHJlYWRzLmNvbS8ifQ%3D%3D"
    )

    # Simulate user input to avoid captcha detection
    # (not guaranteed to work and generally frowned upon by websites owners lol)
    page.wait_for_timeout(10000)

    # Fill in the login form
    page.fill("#ap_email", os.getenv("GOODREADS_EMAIL"))
    page.fill("#ap_password", os.getenv("GOODREADS_PASSWORD"))
    page.click("#signInSubmit")  # click the login button

    page.wait_for_timeout(10000)
    page.wait_for_timeout(5000)  # wait for 5 seconds to allow the page to load

    console.print("[green]✓[/green] Logged in successfully")
    console.print(f"[dim]Current page: {page.url}[/dim]")
    console.print()

    if page.is_closed():
        console.print(
            "[bold red]✗ Page closed after login. Exiting.[/bold red]"
        )
        browser.close()
        exit()

    # ---------------------------------------------------------
    # GIVEAWAY LOOP
    # ---------------------------------------------------------

    # loop twice for 30 entries (15 per page)
    for i in range(2):

        if page.is_closed():
            console.print(
                "[bold red]✗ Page closed before navigating to giveaway page. Exiting.[/bold red]"
            )
            browser.close()
            exit()

        console.print(
            f"\n[bold yellow]━━━ Giveaway Page {i + 1}/2 ━━━[/bold yellow]"
        )

        # navigate to the giveaway page
        try:
            page.goto(
                "https://www.goodreads.com/giveaway?sort=featured"
            )

        except TargetClosedError:
            console.print(
                "[bold red]✗ Page closed while navigating to giveaway page. Exiting.[/bold red]"
            )
            browser.close()
            exit()

        page.wait_for_timeout(5000)  # wait for 5 seconds to allow the page to load

        # Wait for giveaways to load
        page.wait_for_selector("article.BookListItem")

        # Get all giveaway entry URLs on the page
        entry_links = page.eval_on_selector_all(
            "article.BookListItem a.Button--primary",
            "elements => elements.map(el => el.href)"
        )

        console.print(
            f"[cyan]Found [bold]{len(entry_links)}[/bold] giveaways on this page.[/cyan]"
        )
        console.print()

        # ---------------------------------------------------------
        # RICH PROGRESS BAR
        # ---------------------------------------------------------

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:

            task = progress.add_task(
                "[cyan]Entering giveaways...",
                total=len(entry_links),
            )

            for link in entry_links:

                if page.is_closed():
                    progress.console.print(
                        "[bold red]✗ Page closed. Exiting.[/bold red]"
                    )
                    browser.close()
                    exit()

                progress.update(
                    task,
                    description="[cyan]Visiting giveaway...[/cyan]",
                )

                try:
                    page.goto(link)

                except TargetClosedError:
                    progress.console.print(
                        "[bold red]✗ Page closed while visiting giveaway link. Exiting.[/bold red]"
                    )
                    browser.close()
                    exit()

                except Exception as e:
                    progress.console.print(
                        f"[red]✗ Navigation error:[/red] {e}"
                    )
                    progress.advance(task)
                    continue

                kindleCount = page.locator(
                    '[alt*="Kindle"]'
                ).count()

                progress.update(
                    task,
                    description=(
                        "[cyan]Processing giveaway "
                        f"({'Kindle' if kindleCount > 0 else 'Physical'})...[/cyan]"
                    ),
                )

                # ---------------------------------------------------------
                # GIVEAWAY FLOW
                # ---------------------------------------------------------

                try:

                    if kindleCount > 0:

                        page.wait_for_timeout(2000)
                        page.check('input#termsCheckBox')
                        page.click('input#giveawaySubmitButton')
                        page.check('input#ageAttestationCheckBox')

                        giveaway_counter += 1

                        progress.console.print(
                            "[green]✓ Kindle giveaway entered[/green]"
                        )

                    else:

                        page.wait_for_timeout(2000)
                        page.wait_for_selector("a.addressLink")
                        page.click("a.addressLink")

                        page.wait_for_timeout(2000)
                        page.check('input#termsCheckBox')
                        page.check('input#ageAttestationCheckBox')
                        page.click('input[type="submit"]')

                        giveaway_counter += 1

                        progress.console.print(
                            "[green]✓ Physical giveaway entered[/green]"
                        )

                except Exception as e:

                    progress.console.print(
                        "[bold red]✗ Error occurred during giveaway entry.[/bold red]"
                    )

                    progress.console.print(
                        f"[dim red]Error details: {e}[/dim red]"
                    )

                progress.advance(task)

                try:
                    page.wait_for_timeout(5000)

                except TargetClosedError:

                    progress.console.print(
                        "[bold red]✗ Page closed during final wait. Exiting.[/bold red]"
                    )

                    browser.close()
                    exit()

    # ---------------------------------------------------------
    # FINISHED
    # ---------------------------------------------------------

    console.print()

    console.print(
        "[bold green]╔══════════════════════════════════════════════╗[/bold green]"
    )
    console.print(
        "[bold green]║              RUN COMPLETE ✓                  ║[/bold green]"
    )
    console.print(

        "[bold green]╚══════════════════════════════════════════════╝[/bold green]"
    )

    console.print(
        f"[bold cyan]Giveaways entered:[/bold cyan] "
        f"[bold green]{giveaway_counter}[/bold green]"
    )

    console.print()

    browser.close()