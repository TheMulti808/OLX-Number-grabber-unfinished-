from tkinter import W
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, time

PATH = "C:\Program Files (x86)\chromedriver.exe" #selenium chrome driver path
driver = webdriver.Chrome(PATH)
user_information = {"email": "multi_808@tlen.pl", "password": "Marysienka2016"}
olxCategories = {}
elementsToAnalyze = []
pagesToAnalyze = 0
receivedData = []


def wfe(driver, byWhat, arg): #wait for element, function because im lazy
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((byWhat, arg)))
    return element

def analyzeOtomotoLink(driver, link):
    #print("otomoto Link")
    pass
def analyzeOlxLink(driver, link):
    driver.get(link)
    try:
        callButton = wfe(driver, By.XPATH,'//button[@data-cy="ad-contact-phone"]')
    except:
        pass
    finally:
        callButton.click()
        time.sleep(5)
        driver.quit()
        sys.exit("I give up here, olx is blocking getting many phone numbers")


def analyzeLinks(driver):
    for link in elementsToAnalyze:
        if 'otomoto' in link:
            analyzeOtomotoLink(driver, link)
        else:
            analyzeOlxLink(driver, link)

def analyzePages(driver, pagesToAnalyze, userCategory):
    for i in range(int(pagesToAnalyze)):
        #if i == 0: continue
        driver.get(olxCategories[userCategory]["link"]+"?search%5Border%5D=created_at:desc&page="+str(i))
        print(f'Changing site to {i}')
        mainElement = wfe(driver, By.CLASS_NAME, "listing-grid-container")
        elements = mainElement.find_elements_by_class_name("css-19ucd76")
        for element in elements:
            try:
                elementLink = element.find_element(by=By.TAG_NAME, value='a').get_attribute("href")
            except:
                #print('No "a" element, probably ad or smth')
                pass
            finally:
                elementsToAnalyze.append(elementLink)
        
    print(f'Iteration finished, collected {len(elementsToAnalyze)} elements')
    analyzeLinks(driver)

def main():
    try: #login
        driver.get("https://www.olx.pl/")
        wfe(driver, By.ID, "onetrust-accept-btn-handler").click() #Not saving as variable because i dont need to, just one action
        wfe(driver, By.ID, "topLoginLink").click() #Not saving as variable because i dont need to, just one action
        wfe(driver,By.CLASS_NAME, "login-tabs") #Just to be sure
        wfe(driver, By.ID, "userEmail").send_keys(user_information["email"]) #Not saving as variable because i dont need to, just one action
        passwordField = wfe(driver, By.ID, "userPass") #Saving as variable becase i need to use it twice
        passwordField.send_keys(user_information["password"])
        passwordField.send_keys(Keys.RETURN)

        wfe(driver, By.CLASS_NAME, "css-1o36jun-BaseStyles").click() #close safety window
        driver.get("https://www.olx.pl/") #Go back to main site
        mainElement = wfe(driver, By.CLASS_NAME, "maincategories")
        categories = mainElement.find_elements_by_class_name("fleft")
        tempId = 0
        print("Printing categories")
        for category in categories:
            categoryName = category.find_element(by=By.TAG_NAME, value='span').text
            if len(categoryName) > 1:
                tempId += 1
                categoryLink = category.find_element(by=By.TAG_NAME, value='a').get_attribute("href") 
                olxCategories[str(tempId)] =  {
                    "name": categoryName,
                    "link": categoryLink
                }
                print(f"{tempId}. {categoryName}")
        print(f"\nGet one of {len(olxCategories)} categories by id or enter 'q' to quit")
        while True:
            userCategory = input("Category id: ")
            if userCategory == 'q':
                driver.quit()
                sys.exit("User closed app")
            if not userCategory.isnumeric(): 
                print('You have to enter category id!') 
            else:
                if str(userCategory) in olxCategories:
                    break
                else:
                    print('Wrong category id!') 
        userCategoryName = olxCategories[str(userCategory)]["name"]
        print(f"You picked {userCategoryName} category!\nHow many pages to analyze? (max 25)")
        while True:
            pagesToAnalyze = input("How many pages: ")
            if not pagesToAnalyze.isnumeric(): 
                print('You have to enter number!') 
            else:
                if pagesToAnalyze == 0:
                    print("Okay, closing app")
                    driver.quit()
                    sys.exit("Nothing to analyze")
                if int(pagesToAnalyze) > 25:
                    print("Pick a number between 1 and 25!")
                else:
                    break
        analyzePages(driver, pagesToAnalyze, str(userCategory))

    except Exception as e:
        print('Error, quiting application\n', e)
        driver.quit()


if __name__ == "__main__":
    main()