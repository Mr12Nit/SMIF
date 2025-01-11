#!/usr/bin/python3

from services import sharedMethods
from Person import *
from models import *

import json
from services import web_driver_handler

import time
from datetime import datetime 
from services import logSetup



webdriverPath = "/home/mr124/Documents/Projects/SMIF/geckodriver"
profilePath =  "/home/mr124/Documents/Projects/SMIF/WhatsAppProfile"

logger = SharedMethods.logSetup.log("whatsApp","log.txt")

class XPath():
    def __init__(self):
        # Xpath Part
        self.newChatXpath = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div'
        self.searchXpath = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'
        self.smallImageXpath = '/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[1]/div/img'
        self.aboutXpath = '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[2]/span/span'
        self.BigImageXpath='/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[1]/div[1]/div/img' 
        self.onlineDivXpath='/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]'

        self.bussinessProfileXpath = '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[2]/div/div/div[1]'
        self.bussinessBigImage = '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[1]/div[2]/div/div/img'
        self.bussinessCoverDiv = '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[1]/div[1]/div'
        self.bussinessAboutDiv = '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[3]'
        self.bussinessAbout = '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[7]/div[2]/div/div/span/span'          
        self.bussinessName = '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[1]/div[3]/div[1]/div[2]/span'
                                


        self.contactDivXpath = '/html/body/div[1]/div/div/div[2]/div[4]/div/header'
        self.myImageXpath = '/html/body/div[1]/div/div/div[2]/div[3]/header/div[1]/div/img'
        self.whatsAppUrl = "https://web.whatsapp.com"


class WhatsApp(Person,XPath):
    def __init__(self, phoneNumber=None, name=None, username=None):
        self.logger = logger or logSetup.setup_logger("WhatsApp", "WhatsAppLog.txt")
        self.webdriverPath = webdriverPath
        self.profilePath = profilePath
        self.Xpath = XPath()
        self.person = Person(name=name,phoneNumber=phoneNumber, username=username)
        self.bussinessAcc = False # defualt value for normal ppl
        self.data = {'about':'','bussnissAbout':'', 'newAbout':'','bigImageUrl':'','smallImageUrl':'','bussnissCover':'', }
        self.session = self.createClassSession()
        self.persondb = self.loadDatabaseData()


    def saveCookie(self, cookieFileName ,cookies):
        if cookies:
            with open(cookieFileName,"w") as cookieFile:
                json.dump(cookies, cookieFile, indent=4)
            self.logger.info("done writeing what's app cookie")
            return True
        else:
            self.logger.error("erro in saving the cookie")

    def LoadCookeFile(self, cookieFileName):
        if SharedMethods.BaseClass.checkIfFileExist(cookieFileName):
            with open(cookieFileName, 'r') as cookiesFile:
                cookies = json.load(cookiesFile)
                self.logger.info(f"done loading cookefile {cookieFileName}")
                return cookies
        else:
            self.logger.error("can't load cooke file")
            return False

        
    def setupWhatsAppProfile(self):
        try:
            driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath)
            driver.get(self.Xpath.whatsAppUrl)
            self.logger.info("Link Your Device")
            SaveCookie = input("Done Linking Save the cookie?: Y/n ")
            if SaveCookie.lower() == "y" or SaveCookie.lower == 'yes':
                driver.quit()
        except:
            self.logger.error('Error in setuping the whats profile')
        
    def LoadCookies(self):
        # not ready yet
        driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath)
        WhatsAppCookies = self.LoadCookeFile("WhatsAppCookies.json")
        if WhatsAppCookies:
            for cookie in WhatsAppCookies:
                driver.add_cookie(cookie)
            else:
                self.logger.info("done adding the cookies")
        return driver
            
    def creatWhatssAppDriver(self, HeadLess=None):
        try:
            driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath, HeadLess=HeadLess)
            driver.get(self.Xpath.whatsAppUrl)
            self.logger.info("now opened whatsApp")
            self.driver = driver
            return True
        except:
            self.logger.error("Couldn't create Driver")
            return False
        
    def creatWebDriver(self, HeadLess=None):
        try:
            driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath, HeadLess=HeadLess)
            self.logger.info("now opened Web driver")
            self.driver = driver
            return True
        except:
            self.logger.error("Couldn't create Driver")
            return False

    
    def checkIfElementIsLoaded(self, elementClass):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,elementClass )))
            if element:
                self.logger.info("element is loaded in the page")
                time.sleep(3)
                return True
        except TimeoutException as e:
            self.logger.error("Time out on loading whatsApp")
        except Exception as e:
            self.logger.error(f'error {e}')

    def checkIfElementIsLoadedByXpath(self, elementXpath):
        try:
            element = WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, elementXpath)))
            if element:
                self.logger.info("element is loaded in the page")
                time.sleep(3)
                return True
        except TimeoutException as e:
            self.logger.error("Time out on loading whatsApp")
        except Exception as e:
            self.logger.error(f'error {e}')





    def findElementByXpath(self, xpath):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            if element:
                return element
            else:
                return False
        except:
            self.logger.error("can't find element")

    def findElementByClass(self, ClassName):
        try:
            element = self.driver.find_element(By.CLASS_NAME, ClassName)
            if element:
                return element
            else:
                return False
        except:
            self.logger.error("can't find element")

    def findElementByCssSelector(self, cssSelector):
        try:
            element = self.driver.find_element_by_css_selector(cssSelector)
            if element:
                return element
            else:
                return False
        except:
            self.logger.error(f"couldn't find this element {cssSelector}")

    def findElementByText(self, ElementText):
        # Find element by partial text content using XPath
        try:
            element = self.driver.find_element(By.XPATH, f"//*[text()='{ElementText}']")
            if element:
                return element
            else:
                return False
        except:
            self.logger.info(f"Text {ElementText} not found in the site")
            return False
    
    def sendKeys(self, word=None):
        actions = ActionChains(self.driver)
        actions.send_keys(word)
        actions.perform()




    def openContactViaUrl(self):
        try:
            self.logger.info(f'{self.Xpath.whatsAppUrl}/send?phone={self.person.phoneNumber}')
            self.driver.get(f'{self.Xpath.whatsAppUrl}/send?phone={self.person.phoneNumber}')
            WebDriverWait(self.driver, 240).until(EC.presence_of_element_located((By.XPATH, self.Xpath.contactDivXpath)))
            time.sleep(3)
            return True
        except:
            self.logger.error("can't find contact")
            return False
    
    def searchContact(self):
        try:
            newChatElement = self.findElementByXpath(self.Xpath.newChatXpath)
            newChatElement.click()
            searchElement = self.findElementByXpath(self.Xpath.searchXpath)
            searchElement.click()
            self.sendKeys(word=self.person.phoneNumber)
            self.logger.info("done searching for contact ")
            time.sleep(3)
            return True
        except:
            self.logger.error("can't find contact")
            return False

    def openContact(self):
        try:
            smallImageElement = self.findElementByXpath(self.Xpath.smallImageXpath)
            smallImageElement.click()
            time.sleep(2)
            self.logger.info("Done opening the contact chat")
            return True
        except:
            self.logger.error("error in opening the contact chat")


    def openContactInfo(self):
        try:
            contactDiv = self.findElementByXpath(self.Xpath.contactDivXpath)
            contactDiv.click()
            self.logger.info("done opeing the about")
            return True
        except:
            self.logger.error("can't open the contact Info")
    
    def getUrlFromImg(self, element):
        try:
            if element.tag_name == 'img':
                return element.get_attribute('src')
        except:
            self.logger.error("can't find url from the element")
            return False
        
    def checkIfBussinessProfile(self):
        try:
            element = self.findElementByXpath(self.Xpath.bussinessProfileXpath)
            if element.text == 'This is a business account.':
                self.bussinessAcc = True
                return True
            else:
                return False
        except:
            self.logger.error("Error in trying to know if what's app bussiness profile")

    def checkIfBussinessProfileUsingSearch(self):
        try:
            element = self.findElementByText('This is a business account.')
            if element.text == 'This is a business account.':
                self.bussinessAcc = True
                return True
            else:
                return False
        except:
            self.logger.info("Not a bussniss Profile")
            return False
        

    def findSmallImageUrl(self):
        # set the value of the small image url MUSTH RUN AFTER OPEN CONTACT
        try:
            smallImageElement = self.findElementByXpath(self.Xpath.smallImageXpath)
            smallImageUrl = self.getUrlFromImg(element=smallImageElement)
            self.data['smallImageUrl'] = smallImageUrl
            self.logger.info("Done finding small image url")
            return True
        except:
            self.logger.error("can't find the small image")
            return False
    
    def findAbout(self):
        try:
            aboutElemnet = self.findElementByXpath(self.Xpath.aboutXpath)
            if aboutElemnet:
                self.data['about'] = aboutElemnet.text
                self.logger.info("done finding about")
                return True
            else:
                self.logger.error("can't find about element")
        except:
            self.logger.error("can't get about ")
        

    def findImageLink(self):
        try:
            imageElement = self.findElementByXpath(self.Xpath.BigImageXpath)
            BigImageUrl =  self.getUrlFromImg(imageElement)
            self.data['bigImageUrl'] = BigImageUrl
        except:
            self.logger.error("can't find the big image url")
            return False
        
    def findBussinessBigImageLink(self):
        if self.bussinessAcc:
            try:
                imageElement = self.findElementByXpath(self.Xpath.bussinessBigImage)
                BigImageUrl =  self.getUrlFromImg(imageElement)
                self.data['bigImageUrl'] = BigImageUrl
            except:
                self.logger.error('error in getting the Image link')
                return False
            

    def findBussinessCoverUrl(self):
        if self.bussinessAcc:
            try:
                coverElement = self.findElementByXpath(self.Xpath.bussinessCoverDiv)
                if coverElement:
                    style = coverElement.get_attribute('style')
                    url_start_index = style.find('url("') + len('url("')
                    url_end_index = style.find('")', url_start_index)
                    url = style[url_start_index:url_end_index]
                    self.data['bussnissCover'] =  url
                    self.logger.info('Done finding the bussiness cover ')
            except:
                self.logger.error('error in getting the cover link')
                return False

    
    def findBussinessAbout(self):
        if self.bussinessAcc:
            try:
                aboutDivElement = self.findElementByXpath(self.Xpath.bussinessAbout)
                bussinessAboutElement = self.findElementByXpath(self.Xpath.bussinessAboutDiv)
                if aboutDivElement:
                    aboutText = aboutDivElement.text
                    bussinessAboutText = bussinessAboutElement.text
                    self.data['bussnissAbout'] = bussinessAboutText
                    self.data['about'] = aboutText
                    self.logger.info("done finding about info")
            except:
                self.logger.error("error in geting about")


    def findBussinessName(self):
        if self.bussinessAcc:
            try:
                NameElement = self.findElementByXpath(self.Xpath.bussinessName)
                if NameElement:
                    bussinessName = NameElement.text
                    self.data['bussinessName'] = bussinessName
                    self.logger.info("done finding bussinessName info")
            except:
                self.logger.error("error in geting bussinessName")


    def collectUserInfo(self):
        try:
            if self.bussinessAcc:
                self.findSmallImageUrl()
                self.findBussinessAbout()
                self.findBussinessBigImageLink()
                self.findBussinessCoverUrl()
                self.findBussinessName()
                self.logger.info("Done Collecting all the bussniss user data")
                return True
            else:
                self.findAbout()
                self.findImageLink()
                self.findSmallImageUrl()
                self.logger.info("Done collecting all the user data")
                return True
        except:
            self.logger.error("error while collecting all user data ")
            return False

    def getAlluserInfo(self):
        if self.person.name and self.person.phoneNumber:
            contactDiv = self.checkIfElementIsLoadedByXpath(self.Xpath.contactDivXpath)
            if contactDiv:
                self.openContact()
                self.checkIfBussinessProfile()
                result = self.collectUserInfo()
                return True if result else False
            else:
                self.logger.error('cant find contact div element')
                return False
        else:
            self.logger.error("can't find user name or phoneNumber")
            return False
        
    def downloaImage(self, imgUrl, tempImage=False):
        try:
            if imgUrl and self.person.name and SharedMethods.BaseClass.checkIfDir(f"Files/{self.person.name}"): # ensure that the person has dir profile
                ImgName = f"Files/{self.person.name}/whatsApp/TempSmallImage" if tempImage else f'Files/{self.person.name}/whatsApp/{self.person.name}-{f"{datetime.now()}".replace(" ","-")}'
                Img = SharedMethods.Image(imageUrl=imgUrl, imageName=ImgName)
                if Img.DownloadImage():
                    Img.GenerateImageHash()
                    return Img
                else:
                    self.logger.error("Error while downloading the Image")
                    return False
            else:
                self.logger.error("couldn't downlaod the img probably the user foldar not found")
                return False
        except Exception as e:
            self.logger.error('Error While downloading Image ')
            return False

    def compareImages(self):
        try:
            # fun to cmp the old with new
            if self.newSmallImage and self.oldCurrentImage:
                if SharedMethods.Image.isTheSameImage(self.oldCurrentImage, self.newSmallImage):
                    return False
                else:
                    return True
            else:
                return "Faild"
        except:
            return "Faild"
        
   
    def sameProfilePic(self):
        '''
            Check if the new profile picture differs from the last one.
            
            Returns:
                bool: True if the profile picture has changed, False otherwise.
                None: If an error occurs during the process.        
        '''
        try:
            if not self.persondb:
                self.logger.error("No database entry found for this person.")
                return None
            
            whatsData = self.getWhatsAppEntry(self.persondb.whatsappEntries)

            if not whatsData:
                self.logger.error("No WhatsApp entry found for this person.")
                return None
            
            if not whatsData.currentProfilePic:
                self.logger.info("no curretn profile image")
                self.logger.info("storing the current as the current")
                self.newBigImage = self.downloaImage(self.data.get('bigImageUrl'))
                self.storeNewSmallImage()
                self.storeNewBigImage()
                return True
            else:
                self.oldCurrentImage = SharedMethods.Image(imageName=whatsData.currentProfilePic, imageHash=whatsData.currentHash, )
        
            if self.newSmallImage and self.oldCurrentImage:
                self.logger.info("starting compairing the two images")
                return self.compareImages()
            elif self.data['smallImageUrl'] == False:
                # compare it with the last state to see if this is the defalut state
                self.logger.info("The user has some Depression stuff")
                if whatsData.currentProfilePic == False:
                    return True
                else:
                    return False
        except Exception as e:
            self.logger.error(f"Error in checking is the same Pic {e}")
            return None 


    def createUserFoldar(self):
        try:
            SharedMethods.BaseClass.makeDir(f"Files/{self.person.name}/whatsApp")
            self.logger.info("Done making user whats foldar")
            return True
        except:
            self.logger.error("couldn't make user foldar")
            return False

    def isActiveNow(self):
        try:
            body = self.driver.find_element("css selector", "body")
            onlineElement = self.findElementByXpath(self.Xpath.onlineDivXpath)
            ActionChains(self.driver).move_to_element(body).perform()
            ActionChains(self.driver).move_to_element(onlineElement).perform()
            if 'online' in onlineElement.text.lower():
                return True
            else:
                return False
        except:
            self.logger.error("error in monitor active now")
            return "False"

    def monitorOnline(self, durationToRun, frequency):
        try:
            if isinstance(durationToRun, int) and isinstance(frequency, int):
                startTime = time.time()
                self.whatsData = self.getWhatsAppEntry(self.persondb.whatsappEntries)
                while time.time() - startTime < durationToRun:
                    self.logger.info("checking now")
                    activeResult = self.isActiveNow()
                    self.storeActiveStatus(activeResult)
                    time.sleep(frequency)
            else:
                self.logger.error("wtf the duration and freq is not int")
        except:
            self.logger.error("error in monitoring online status")

    def sameAboutBio(self):
        '''
            this method to check if the new about deffers from the last one
            
            Returns:
                 bool: True if the about status bio has changed, False otherwise.
    
        '''
        try:
            if not self.persondb:
                self.logger.error("No database entry found for this person.")
                return None
            
            whatsData = self.getWhatsAppEntry(self.persondb.whatsappEntries)

            if not whatsData:
                self.logger.error("No WhatsApp entry found for this person.")
                return None
            
            oldAboutBio = whatsData.currentAbout
            newAboutBio = self.data.get("about")
            if newAboutBio:
                return newAboutBio == oldAboutBio # True if the same bio from the one in db false if it has been changed
            else:
                self.logger.error("no new about data")
                return None
        except Exception as e:
            self.logger.error(f"Error in checking is the same about {e}")
            return None    


    
    # database section
    def createClassSession(self):
        # Check if the database file exists
        if not SharedMethods.BaseClass.checkIfFileExist("SMIF.db"):
            self.logger.error("Database file not found")
            return False    
        # Create a session to interact with the database
        return createSession()
    
    def loadDatabaseData(self):
        try:
            if self.session:
                # Query the database for user data based on phone number
                userdata = self.session.query(Persondb).filter_by(username=self.person.username).first()
                self.logger.info("User data loaded from the database")
                return userdata
            else:
                self.logger.error("Failed to find session")
                return False
        except Exception as e:
            self.logger.error(f"Error loading user data from database: {str(e)}")
            return False

    def getWhatsAppEntry(self, whatsappEntries):
        if whatsappEntries:
            entries = {entry.phoneNumber: entry for entry in whatsappEntries}
        else:
            return False
        
        if self.person.phoneNumber in entries:
                return entries[self.person.phoneNumber]
        else:
            # Handle case where WhatsApp entry is not found
            self.logger.info("No DataBase is found, adding one")
            #self.addNewWhatsEntry()
            return None


    def changeUserAbout(self):
        try:
            # only if their is a new about data, which is made by changedAbout method  
            currentAbout = self.data.get("newAbout")
            if currentAbout and self.persondb:
                whatsData = self.getWhatsAppEntry(self.persondb.whatsappEntries)
                whatsData.currentAbout = currentAbout
                return True
            else:
                # this means that about data is empty
                self.logger.info("you need to get the about first and check if the user has changed it befor running the store to db")
                return False
        except:
            self.logger.error("got an error while storing the about into db")
            return False

    def monitorAbout(self):
        sameAbout = self.sameAboutBio()
        if sameAbout == False:
            if not self.data.get('about'):
                self.getAlluserInfo() # if no about data fetch new ones from the servers
                
            self.data['newAbout'] = self.data.get('about')
            result = self.changeUserAbout()
            if result:
                return True # about has been changed just need to commit to db
            else:
                return False
        else:
            self.logger.info('user has the same about bio')
    
    def changeUserPic(self):
        pass

    def monitorProfilePic(self):
        bigImageUrl, smallImageUrl = self.data.get('bigImageUrl'), self.data.get('smallImageUrl')
        self.newSmallImage = self.downloaImage(smallImageUrl, tempImage=True)
        samePic = self.sameProfilePic()
        if samePic == False:
            if not (bigImageUrl and smallImageUrl):
                self.getAlluserInfo() # if no about data fetch new ones from the servers

            self.newBigImage =  self.downloaImage(bigImageUrl)
            dbSmallResult = self.storeNewSmallImage()
            dbBigResult = self.storeNewBigImage()
            return dbSmallResult and dbBigResult
        else:
            self.logger.info('user has the same about Pic')
    
    def storeNewSmallImage(self):
        """
            Iterate over the arguments passed to the function.
            
            Args:
                *args: Variable number of Images.
                
            Returns:
                True if all is okay then u need to commit the db changes
        """
        if self.persondb:
            whatsData = self.getWhatsAppEntry(self.persondb.whatsappEntries)
        if self.newSmallImage.Hash and self.newSmallImage.FileName and whatsData:
            whatsData.currentProfilePic = self.newSmallImage.FileName
            whatsData.currentHash = self.newSmallImage.Hash
            return True
        elif self.newSmallImage == False:
            whatsData.currentProfilePic = str(False)
            whatsData.currentHash = str(False)
        else:
            return False
        
    def storeNewBigImage(self):
        """
            Iterate over the arguments passed to the function.
            
            Args:
                *args: Variable number of Images.
                
            Returns:
                True if all is okay then u need to commit the db changes
        """
        if self.persondb:
            whatsData = self.getWhatsAppEntry(self.persondb.whatsappEntries)
        if self.newBigImage.Hash and self.newBigImage.FileName and whatsData:
            bigImage = profilePicsLog(picPath=self.newBigImage.FileName, picHash=self.newBigImage.Hash)
            whatsData.profilePicLog.append(bigImage)
            return True
        elif self.newBigImage == False:
            whatsData.currentProfilePic = str(False)
            whatsData.currentHash = str(False)
        else:
            return False
    
    def addNewWhatsEntry(self):
        try:
            if not self.persondb:
                self.logger.info("No Person Found so adding new one")
                self.person.persondb.addPerson(self.session)
            
            whatsData = self.getWhatsAppEntry(self.persondb.whatsappEntries)
            if not whatsData:
                newWhats = whatsAppdb(phoneNumber=self.person.phoneNumber)
                self.persondb.whatsappEntries.append(newWhats)
                return True
            else:
                self.logger.info("user is already has what's entry")
        except Exception as e :
            self.logger.error(f"error during add the whats entry: {e}")
    
    def storeActiveStatus(self, activeResult): 
        ''' store active log to db'''
        if activeResult != 'False' and self.whatsData:
            self.whatsData.onlineLog.append(onlineLog(status=activeResult))


if __name__ == "__main__":
    print("hello")
    # storing about databse need to change
    x = web_driver_handler.WebDriverHandler()