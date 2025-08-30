from playwright.sync_api import sync_playwright
import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key="api")  

# Playwright Test
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=800)
    page = browser.new_page()
    page.goto("https://playwright.dev/")
    page.get_by_text("Search").click()
    search_box = page.get_by_placeholder("Search docs")
    search_box.fill("auto waiting")
    page.keyboard.press("Enter")
    page.wait_for_selector("main")
    
    # Capture relevant test results
    search_results = page.query_selector("main").inner_text()  # Get text from the main content
    page.wait_for_timeout(3000)
    browser.close()

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Create a prompt that includes Playwright test results
prompt = f"Analyze the following Playwright test results and suggest improvements or summarize the outcome:\n\n"


# Generate response
response = model.generate_content(prompt)

# Print the AI-generated response
print(response.text)

