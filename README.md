# Delhi High Court Case Search

This is a Django-based web application allows users to search for Delhi High Court cases by using **Case Type**, **Case Number**, and **Filing Year**.  
It fetches live case details from the Delhi High Court's official website(https://delhihighcourt.nic.in/) using web scraper.

---

## Features
- Search cases by **Case Type, Case Number, and Filing Year**.
- Retrieve **case details, petitioner/respondent info, and listing dates**.
- View **orders/PDF links** for the case.
- Saves search history in the database for reference.

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
- **Case Type** → Select from a predefined list (e.g., `CS(COMM)`, `CS(OS)`, `CRL.A.`)
- **Case Number** → Numeric case number
- **Filing Year** → Year when the case was filed
  <img width="842" height="267" alt="Image" src="https://github.com/user-attachments/assets/2284cd2d-656a-4c92-879c-a79191ccc5be" />

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
  2. Reads captcha value and random ID from HTML.

### 3. Fetching Data from Delhi High Court
- After obtaining the captcha and random ID, the scraper sends a request to:
/app/get-case-type-status
- Parameters sent:
 `case_type` `case_number` `filing_year` `captcha` `randomid`
- The site responds with JSON containing:
  Case number and status, Petitioner and respondent names, Listing dates / courtno embedded HTML for case/order links.
  <img width="962" height="373" alt="Image" src="https://github.com/user-attachments/assets/38606a5d-6277-42e9-904b-a91a1cd58ca9" />
- If given data is incorrect then UI returns No results found.
  <img width="954" height="314" alt="Image" src="https://github.com/user-attachments/assets/f04d4c97-2698-4b4f-bae2-bdbc2d88cc8d" />

### 4. Extracting Order Links
- The application parses the HTML in the response to:
   1. Extract PDF order links.
   2. Valid PDF links are then displayed in the UI.

### 5. Display in Web Application
- Results are shown in a clean HTML table.
- Clicking the **Orders** link opens a page listing all related PDF order files.
- Clicking on View Order Details opens pdf directly in the browser tab.
  <img width="697" height="370" alt="Image" src="https://github.com/user-attachments/assets/fb903629-fc2a-42fa-9e65-233c6d8b9a61" />
