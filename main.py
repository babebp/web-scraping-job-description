from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# setup chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")

# set path to chromedriver as per your configuration
chromedriver_autoinstaller.install()

# initial driver
driver = webdriver.Chrome(options=chrome_options)

# set the target URL
url = "https://www.linkedin.com/jobs/search?position=1&pageNum=0"
driver.get(url)

# search for Data Engineer
job_search_box_XPATH = '//input[@id="job-search-bar-keywords"]'
location_search_box_XPATH = '//input[@id="job-search-bar-location"]'

job_search_box = driver.find_element(By.XPATH, job_search_box_XPATH)
job_search_box.clear()
job_search_box.send_keys('Data Engineer')

location_search_box = driver.find_element(By.XPATH, location_search_box_XPATH)
location_search_box.clear()
location_search_box.send_keys('Thailand')

location_search_box.submit()

# get job cards
job_description_list = []

job_card_XPATH = f'//a[@data-tracking-control-name="public_jobs_jserp-result_search-card"]'
job_card_list = driver.find_elements(By.XPATH, job_card_XPATH)

number_of_cards = len(job_card_list)
epoch = 1

target_length = 100
while epoch <= number_of_cards:
    print(epoch)
    print('max', number_of_cards)
    if epoch == 100:
        break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    job_card_XPATH = f'//a[@data-tracking-control-name="public_jobs_jserp-result_search-card"]'
    job_card_list = driver.find_elements(By.XPATH, job_card_XPATH)
    number_of_cards = len(job_card_list)
    
    job_card_XPATH = f'(//a[@data-tracking-control-name="public_jobs_jserp-result_search-card"])[{epoch}]'
    job_card = driver.find_element(By.XPATH, job_card_XPATH)
    job_card.click()

    job_description_XPATH = '//div[@class="description__text description__text--rich"]'
    show_more_button_XPATH = '//div[@class="description__text description__text--rich"]/section/button[1]'

    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, show_more_button_XPATH)))
        show_more_button = driver.find_element(By.XPATH, show_more_button_XPATH)
        show_more_button.click()

        job_description = driver.find_element(By.XPATH, job_description_XPATH)
        job_description_list.append(job_description.text)
    except:
        epoch += 1
        continue

    epoch += 1

# extract distinct word in JD
all_jd = ''

for jd in job_description_list:
    if jd != ' ':
        all_jd += jd

all_jd = all_jd.replace('\n', ' ')

# save word cloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import time

stopwords = STOPWORDS
wc = WordCloud(background_color='white',
     stopwords = stopwords, width = 800, height = 500).generate(all_jd)
plt.axis("off")
plt.imshow(wc)
plt.savefig(f'results/{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}.png')
