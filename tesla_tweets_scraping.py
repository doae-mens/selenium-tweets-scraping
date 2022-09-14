import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver

def get_tweet_data(card):
    """Extract data from tweet data"""
    username = card.find_element_by_xpath('.//span').text
    handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    comment = card.find_element_by_xpath('./div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('./div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    
    tweet = (username, handle, postdate, text, reply_cnt, retweet_cnt, like_cnt)
    return tweet


# create instant of the driver
driver = webdriver.Edge(executable_path=r'C:\PATH\msedgedriver.exe')
# navigate to Login screen
driver.get('https://www.twitter.com/login')
print("Page title is: %s" %(driver.title))
sleep(4)
email = driver.find_element_by_xpath('//input[@name="text"]')
sleep(4)
email.send_keys('YourEmail')
sleep(4)
email.send_keys(Keys.RETURN)


my_password = getpass()
sleep(6)
password = driver.find_element_by_xpath('//input[@name="password"]')
sleep(6)
password.send_keys(my_password)
sleep(6)
password.send_keys(Keys.RETURN)

# find search input and search for term
sleep(6)
search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
sleep(10)

search_input.send_keys('#Tesla')


sleep(10)
search_input.send_keys(Keys.RETURN)

#navigate to historical Latest tab
driver.find_element_by_link_text('Latest').click()

# get all tweets on the page
data =[]
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True


while scrolling:
    page_cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
    for card in page_cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
    
    scroll_attempt = 0
    while True:
        # chack scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(1)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position: 
            scroll_attemp +=1
            
            #end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2) # attempt to scroll again
        else:
            last_position = curr_position
            break
