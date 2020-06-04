import csv
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .functions import time_divide
from .objects import Experience, Education, Scraper, Skills
import os



class Person(Scraper):
    __TOP_CARD = "pv-top-card"

    def __init__(self, linkedin_url=None, name=None, experiences=[], educations=[], skills=[],
                 driver=None, get=True, scrape=True, close_on_complete=True):
        self.linkedin_url = linkedin_url
        self.name = name
        self.experiences = experiences
        self.educations = educations
        self.skills=skills
        self.also_viewed_urls = []

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(os.path.dirname(__file__), 'drivers/chromedriver')
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_skill(self,skill):
        self.skills.append(skill)

    def add_location(self, location):
        self.location = location

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            self.scrape_not_logged_in(close_on_complete=close_on_complete)

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver
        duration = None

        root = driver.find_element_by_class_name(self.__TOP_CARD)
        self.name = root.find_elements_by_xpath("//section/div/div/div/*/li")[0].text.strip()

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

        # get experience
        try:
            _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "experience-section")))
            exp = driver.find_element_by_id("experience-section")
        except:
            exp = None

        if (exp is not None):
            for position in exp.find_elements_by_class_name("pv-position-entity"):
                position_title = position.find_element_by_tag_name("h3").text.encode('utf-8').strip()
                try:
                    company = position.find_element_by_class_name("pv-entity__secondary-title").text.encode(
                        'utf-8').strip()

                except:
                    pass
                    #company = None
                    #from_date, to_date = (None, None)
                experience = Experience(position_title=position_title)
                experience.institution_name = company
                self.add_experience(experience)

        # get location
        location = driver.find_element_by_class_name(f'{self.__TOP_CARD}--list-bullet')
        location = location.find_element_by_tag_name('li').text
        self.add_location(location)

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

        # get education
        try:
            _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "education-section")))
            edu = driver.find_element_by_id("education-section")
        except:
            edu = None


        if (edu is not None):
            for school in edu.find_elements_by_class_name("pv-profile-section__sortable-item"):
                university = school.find_element_by_class_name("pv-entity__school-name").text.encode('utf-8').strip()
                try:
                    degree = school.find_element_by_class_name("pv-entity__degree-name").text.encode('utf-8').strip()
                except:
                    pass
                    #degree = None
                    #from_date, to_date = (None, None)
                education = Education( degree=degree)
                education.institution_name = university
                self.add_education(education)


        #get skill
        try:
            self.driver.execute_script("document.getElementsByClassName('pv-skills-section__additional-skills')[0].click()")
            time.sleep(loading_pause_time)
        except:
            pass

        try:
            skills= self.driver.execute_script("return (function(){els = document.getElementsByClassName('pv-skill-category-entity');results = [];for (var i=0; i < els.length; i++){results.push(els[i].getElementsByClassName('pv-skill-category-entity__name-text')[0].innerText);}return results;})()")
        except:
            skills= []
        for x in skills:
            skill=Skills(x)
            self.add_skill(skill)

        if close_on_complete:
            driver.quit()

    def scrape_not_logged_in(self, close_on_complete=True, retry_limit=10):
        driver = self.driver
        retry_times = 0
        while self.is_signed_in() and retry_times <= retry_limit:
            page = driver.get(self.linkedin_url)
            retry_times = retry_times + 1

        # get name
        self.name = driver.find_element_by_id("name").text.strip()

        # get experience
        exp = driver.find_element_by_id("experience")
        for position in exp.find_elements_by_class_name("position"):
            position_title = position.find_element_by_class_name("item-title").text.strip()
            company = position.find_element_by_class_name("item-subtitle").text.strip()
            experience = Experience(position_title=position_title)
            experience.institution_name = company
            self.add_experience(experience)

        # get education
        edu = driver.find_element_by_id("education")
        for school in edu.find_elements_by_class_name("school"):
            university = school.find_element_by_class_name("item-title").text.strip()
            degree = school.find_element_by_class_name("original").text.strip()
            education = Education(degree=degree)
            education.institution_name = university
            self.add_education(education)

        if close_on_complete:
            driver.close()

    def __repr__(self):
        with open('education.csv', 'w', newline='') as file2:
            writer2 = csv.writer(file2)
            writer2.writerow(self.educations)
        with open('experience.csv', 'w', newline='') as file3:
            writer3 = csv.writer(file3)
            writer3.writerow(self.experiences)
        with open('skills.csv', 'w', newline='') as file1:
            writer1 = csv.writer(file1)
            writer1.writerow(self.skills)

        return "{name}\n\nExperience\n{exp}\n\nEducation\n{edu}\n\nSkill\n{skill}".format(name=self.name, exp=self.experiences, edu=self.educations,skill=self.skills)

