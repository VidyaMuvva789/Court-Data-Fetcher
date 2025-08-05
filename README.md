# Delhi High Court Case Search

This is a Django-based web application allows users to search for Delhi High Court cases by **Case Type**, **Case Number**, and **Filing Year**.  
It fetches live case details from the Delhi High Court's official website(https://delhihighcourt.nic.in/) using a web scraper.

---

## Features
- Search cases by **Case Type, Case Number, and Filing Year**
- Retrieve **case details, petitioner/respondent info, and listing dates**
- View **orders/PDF links** for the case
- Saves search history in the database for reference

---

## Tech Stack
- **Backend:** Django (Python Framework)
- **Frontend:** Django Templates (HTML, CSS)
- **Scraping:** `requests`, `BeautifulSoup4`
- **Database:** SQLite (default Django DB)
- **Language:** Python 

---

## Required Search Details
To perform a search, the user must provide:
- **Case Type** → Select from a predefined list (e.g., `W.P.(C)`, `CS(OS)`, `CRL.A.`)
- **Case Number** → Numeric case number
- **Filing Year** → Year when the case was filed

- ---

## How It Works

### 1. Cookie Handling
- Uses **`requests.Session()`** to maintain cookies between requests.
- Cookies are set by the Delhi High Court website when the initial search page is loaded.
- These cookies are reused for all search requests to maintain a valid session.

### 2. Captcha Handling
- The site uses a **text-based captcha** (not an image).
- The scraper:
  1. Loads the search page.
  2. Reads captcha value from `<span id="captcha-code">`.
  3. Reads a hidden **random ID** from `<input name="randomid">`.

### 3. Fetching Data from Delhi High Court
- After obtaining the captcha and random ID, the scraper sends a request to:
/app/get-case-type-status
- Parameters sent:
- `case_type`
- `case_number`
- `case_year`
- `captcha`
- `randomid`
- The site responds with JSON containing:
- Case number and status
- Petitioner and respondent names
- Listing dates
- Embedded HTML for case/order links

### 4. Extracting Order Links
- The application parses the HTML in the response to:
- Extract PDF order links
- Valid PDF links are then displayed in the UI.

### 5. Display in Web Application
- Results are shown in a clean HTML table.
- Clicking the **Orders** link opens a page listing all related PDF order files.
- Clicking a PDF link opens it directly in a new browser tab.
