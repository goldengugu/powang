from selenium import webdriver

browser = webdriver.Chrome()

browser.get('https://twitter.com/search?q=vpn')
print(browser.page_source)
browser.close()