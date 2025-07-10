import os
import yaml

def evalEnv(envName: any, defaultValue: any):
    envValue = os.getenv(envName)
    if envValue != None and isinstance(envValue, str):
        return eval(envValue)
    else:
        return defaultValue

DEBUG = evalEnv("DEBUG", True)

# Playwright browser settings.
HEADLESS = evalEnv("HEADLESS", True) # Typically set to True but helps to set to False if running natively instead of in Container.
SLO_MO = evalEnv("SLO_MO", 250)  # ms of slowdown, 0 to disable.
IGNORE_HTTPS_ERRORS = evalEnv("IGNORE_HTTPS_ERRORS", True)
USER_AGENTS = evalEnv(
    "USER_AGENTS",
    [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Vivaldi/5.4.2753.51",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Vivaldi/5.4.2753.51",
    ],
)

# URL selection options.
SEARCH_TERMS = evalEnv("SEARCH_TERMS", ['top news', 'top scores'])
CRAWL_URLS = evalEnv("CRAWL_URLS", ['https://www.zscaler.com'])
EXCLUDED_DOMAINS = evalEnv("EXCLUDED_DOMAINS", [])
HREF_QUERY_STRING = "a[href]"

# Surfing options
SEARCH_DEPTH = evalEnv("SEARCH_DEPTH", 3)
LINKS_MAX_PER_PAGE = evalEnv("LINKS_MAX_PER_PAGE", 5)
SLEEP_MAX = evalEnv("SLEEP_MAX", 5.5)
SLEEP_MIN = evalEnv("SLEEP_MIN", 0.5)

# User Settings.
DEFAULT_PASSWORD = evalEnv("DEFAULT_PASSWORD", "Zscaler123!")
USERS = evalEnv("USERS", [{'username': 'test@example.com'}])

# IDP Stuff
OKTA_LOGIN_URL = "dev-83162149.okta.com"
OKTA_SIGNIN_SUBMIT = "#okta-signin-submit"
OKTA_USERNAME = "#okta-signin-username"
OKTA_PASSWORD = "#okta-signin-password"
MICROSOFT_LOGIN_URL = "login.microsoftonline.com"
MICROSOFT_SIGNIN_SUBMIT = "#idSIButton9"
MICROSOFT_USERNAME = "#i0116"
MICROSOFT_PASSWORD = "#i0118"
MICROSOFT_STAY_SIGNED_IN = "#idBtn_Back"
ZIA_LOCAL_URLS = [
    "zscloud",
]
ZIA_LOCAL_USERNAME = 'input[name="lognsfc"]'
ZIA_LOCAL_PASSWORD = '[placeholder="Enter your Password\\.\\.\\."]'
ZIA_LOCAL_SIGNIN_SUBMIT = 'input:has-text("Sign In")'

# Acceptable Usage Policy (AUP) Stuff
AUP_BUTTON = "button"

# DuckduckGo Stuff
DDG_SEARCH_URL_LINKS = 'a[data-testid="result-title-a"]'