# Goodreads Giveaway Auto-Entry Bot

A Python automation script built with Playwright that automatically enters eligible Goodreads giveaways.

The script logs into a Goodreads account, navigates through featured giveaways, detects whether a giveaway is for a Kindle or physical copy, and completes the appropriate entry workflow.

> **Disclaimer:** This project is intended for educational purposes only. Automating interactions with websites may violate their Terms of Service. Use responsibly and at your own risk.

---

## Features

- Secure login using environment variables
- Browser automation with Playwright
- Automatically scans featured giveaways
- Detects Kindle vs. physical giveaways
- Handles address confirmation for physical book giveaways
- Accepts giveaway terms automatically
- Tracks the number of successful giveaway entries
- Includes basic error handling for unexpected page closures and navigation failures

---

## Technologies Used

- Python 3
- Playwright
- python-dotenv

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/goodreads-giveaway-bot.git
cd goodreads-giveaway-bot
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Install the Playwright browser:

```bash
playwright install
```

---

## Environment Variables

Create a `.env` file in the project root with the following values:

```env
GOODREADS_EMAIL=your_email@example.com
GOODREADS_PASSWORD=your_password
```

Do not commit your `.env` file to version control.

---

## Usage

Run the script with:

```bash
python main.py
```

The script will:

1. Launch a Chromium browser.
2. Log into Goodreads.
3. Navigate to the Featured Giveaways page.
4. Collect giveaway entry links.
5. Visit each giveaway page.
6. Determine whether the giveaway is for a Kindle or physical copy.
7. Complete the appropriate giveaway entry process.
8. Display the total number of successful entries before exiting.

---

## Project Structure

```text
.
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## How It Works

```
Launch Browser
      │
      ▼
Login to Goodreads
      │
      ▼
Navigate to Featured Giveaways
      │
      ▼
Collect Giveaway Links
      │
      ▼
Visit Giveaway
      │
      ├───────────────┐
      ▼               ▼
Kindle Giveaway   Physical Giveaway
      │               │
Accept Terms   Confirm Address
      │               │
      └──────► Submit Entry
                    │
                    ▼
          Increment Entry Counter
```

---

## Limitations

- Goodreads may display CAPTCHA or other anti-automation measures.
- Changes to Goodreads' website structure may require updating element selectors.
- The script currently processes approximately 30 featured giveaways (15 giveaways per page across two iterations).
- Random delays are included to mimic normal browsing behavior but do not guarantee avoidance of bot detection.

---

## Future Improvements

- Configurable number of giveaway pages
- Headless mode support
- Logging to a file
- Retry failed giveaway entries
- Command-line arguments
- Docker support
- Improved statistics and reporting

---

## License

This project is provided for educational purposes. Users are responsible for ensuring their use complies with Goodreads' Terms of Service.

This project is not affiliated with Goodreads or Amazon.
