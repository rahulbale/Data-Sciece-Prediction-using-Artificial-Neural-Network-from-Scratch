from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,ElementNotInteractableException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword,num_jobs,path,slp_time):

    

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.co.in/Job/india-"+keyword+"-jobs-SRCH_IL.0,5_IN115_KO6,20.htm?srs=RECENT_SEARCHES"

    driver.get(url)

    jobs = []

    while len(jobs) < num_jobs:

        time.sleep(slp_time)

        # Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("react-job-listing")  # jl for Job Listing. These are the buttons we're going to click.

        for job_button in job_buttons:


            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))

            if len(jobs) >= num_jobs:
                break
            try:
                job_button.click()  # You might
                time.sleep(.8)
            except:
                pass


            try:
                driver.find_element_by_css_selector('[alt="Close"]').click()
                print('x out worked')
            except NoSuchElementException:  # spelling error making this code not work as expected
                print(' x out failed')
                pass

            result_html = job_button.get_attribute('innerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')


            try:
                title = soup.find("a", class_="jobLink css-1rd3saf eigr9kq2").text
            except:
                title = 'None'

            try:
                location = driver.find_element_by_xpath('.//div[@class="css-56kyx5 e1tk4kwz5"]').text
            except:
                location = 'None'

            try:
                company = soup.find("div", class_="d-flex justify-content-between align-items-start").text
            except:
                company = 'None'

            try:
                rating = soup.find("span", class_="css-19pjha7 e1cjmv6j1").text.replace("\n", "").strip()
            except:
                rating = 'None'

            try:
                salary = soup.find("div", class_="css-nq3w9f pr-xxsm").text.replace("\n", "").strip()
            except:
                salary = 'None'

            try:
                jd = driver.find_element_by_id('JobDescriptionContainer').text
            except:
                jd = 'None'



            try:
                try:
                    driver.find_element_by_xpath('.//div[@data-item="tab" and @data-tab-type="overview"]').click()
                    print("CLICKED")
                except:
                    pass

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = 'None'

                try:
                    industry = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Industry"]//following-sibling::*').text

                except NoSuchElementException:
                    industry = 'None'

                try:
                    sector = driver.find_element_by_xpath('.//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = 'None'

            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                type_of_ownership = 'None'
                industry = 'None'




            jobs.append({'Title': title,
                         'Location': location,
                         "Company": company,
                         "Rating": rating,
                        "Ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector" : sector,
                         "Salary": salary,
                         "Description": jd})
        time.sleep(1)
        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="css-1yshuyv e1gri00l3"]//a').click()

        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         len(jobs)))
            break
    time.sleep(1)
    return pd.DataFrame(jobs)

path="C:/Users/Users/PycharmProjects/Data_Science_Salary/chromedriver.exe"
dataframe = get_jobs("data-scientist",850,path,4)
dataframe.to_csv("Data-Science-Salary.csv", index=False)
