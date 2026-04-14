from playwright.sync_api import sync_playwright #necessary library to implement the script


with sync_playwright() as p: #start the playwright
    giveaway_counter = 0 #initialize the giveaway counter
    browser = p.chromium.launch(headless=False) #launch the browser in non-headless mode
    page = browser.new_page() #create a new page in the browser


    #go to the GoodReads login
    page.goto("https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=eyJyZXR1cm5fdXJsIjoiaHR0cHM6Ly93d3cuZ29vZHJlYWRzLmNvbS8ifQ%3D%3D") #navigate to the login page

 
    
    #Simulate user input to avoid captcha detection (not gauranteed to work and generally frowned upon by websites owners lol)
    page.wait_for_timeout(10000)

    #Fill in the login form
    #user = d.velazquez521@gmail.com
    #password = MelLesBab12!
    page.fill("#ap_email", "d.velazquez521@gmail.com")
    page.fill("#ap_password", "MelLesBab12!")
    page.click("#signInSubmit") #click the login button


    page.wait_for_timeout(5000) #wait for 5 seconds to allow the page to load
    # Check if the login was successful by looking for a specific element on the page   

    print("Logged in. Current page:", page.url)

    #navigate to the giveaway page
    page.goto("https://www.goodreads.com/giveaway?sort=featured") 
    page.wait_for_timeout(5000) #wait for 5 seconds to allow the page to load

    # Wait for giveaways to load
    page.wait_for_selector("article.BookListItem")

    # Get all giveaway entry URLs on the page
    entry_links = page.eval_on_selector_all(
        "article.BookListItem a.Button--primary",  # "Enter Giveaway" buttons
        "elements => elements.map(el => el.href)"
    )

    print(f" Found {len(entry_links)} giveaways to enter.")
    
    for link in entry_links:
        print(f"👉 Visiting: {link}")
        page.goto(link)  # Visit the giveaway page
        
        
        
        #giveway flow: click enter give away -> confirm address -> enter giveaway -> wait to simuluate humnan behavior
        try:
            if page.query_selector("a.addressLink"):
                page.wait_for_timeout(5000)
                page.wait_for_selector("a.addressLink")
                page.click("a.addressLink")
                page.wait_for_timeout(2000)
                page.check('input#termsCheckBox')
                page.click('input[type="submit"]')
                giveaway_counter += 1
                
        
        except Exception as e:
            print("No address link found, skipping to next giveaway.")
            pass


        print(f"Giveaways entered: {giveaway_counter}")
        page.wait_for_timeout(5000)

            

        