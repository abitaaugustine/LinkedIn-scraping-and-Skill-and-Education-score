import os
from linkedin_scraper import person, actions
from selenium import webdriver
from samples import score_calculator
driver = webdriver.Chrome(r"C:\Users\Admin\PycharmProjects\LinkedInScrapingWithQualification\Windows\chromedriver.exe")

email = "abitaaugustine@gmail.com"
password = ""  #enter password
f = open("LinkedIn_URL.txt","r")
text = f.read()
#print(text)
actions.login(driver, email, password)  # if email and password isnt given, it'll prompt in terminal
data = person.Person(text, driver=driver)
print("")
score_calculator.calc_score()
