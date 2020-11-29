import json
import pickle
import time
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Setup Selenium Webdriver
CHROMEDRIVER_PATH = r"./driver/chromedriver.exe"
options = Options()
options.headless = True
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)


def main():
    # Leetcode API URL to get json of problems on algorithms categories
    ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

    # Problem URL is of the following format format ALGORITHMS_BASE_URL + question__title_slug
    ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

    # Load JSON from API
    algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
    algorithms_problems_json = json.loads(algorithms_problems_json)

    # List to store question_title_slug
    count = 0
    for child in algorithms_problems_json["stat_status_pairs"]:

        # Currently we are only processing free problems
        if not child["paid_only"]:
            question__title_slug = child["stat"]["question__title_slug"]
            question__title = child["stat"]["question__title"]
            frontend_question_id = child["stat"]["frontend_question_id"]
            difficulty = child["difficulty"]["level"]
            total_accepted_solutions = child["stat"]["total_acs"]

            # map difficulty integer values to its corresponding string values
            difficulty_level = "hard"
            if difficulty == 1:
                difficulty_level = "easy"
            elif difficulty == 2:
                difficulty_level = "medium"

            url = ALGORITHMS_BASE_URL + question__title_slug

            try:
                driver.get(url)
                # Wait 20 secs or until div with id initial-loading disappears
                element = WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located(
                        (By.ID, "initial-loading"))
                )

                # Get current tab page source.
                html = driver.page_source
                soup = bs4.BeautifulSoup(html, "html.parser")

                # problem description in HTML format so that styling and expressions
                # can be retained.
                problem_html = str(soup.find(
                    "div", {"class": "content__u3I1 question-content__JfgR"}))

                # coma separated list of topics related to the problem like
                # Dynamic programming, Greedy, String etc.
                topics = ""
                for topic in soup.find_all("span", {"class": "tag__2PqS"}):
                    if topics == "":
                        topics = ''.join(topic.findAll(text=True))
                    else:
                        topics += ", " + ''.join(topic.findAll(text=True))

                print(frontend_question_id+", "+question__title+", " +
                      difficulty_level+", "+total_accepted_solutions+", "+tags)

            except Exception as e:
                print(f" Failed Writing!!  {e} ")
                driver.quit()


if __name__ == "__main__":
    main()
