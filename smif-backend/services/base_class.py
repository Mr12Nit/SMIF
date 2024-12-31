import logSetup
import os
import subprocess
import requests
import hashlib
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

import json

logger = logSetup.log("BaseClass","log.txt")

class BaseClass:

    @staticmethod
    def WriteImage(FileName, Data):
        with open(FileName, "wb") as file:
            file.write(Data)

    @staticmethod
    def sendRequest(url):
        return requests.get(url)

    @staticmethod
    def chekcTool(tool):
        command = f"which {tool}"
        result = BaseClass.ExcuteCommand(command)
        if BaseClass.checkCommandResult(result):
            return True
        else:
            logger.error(f"This {tool} is not installed")
            return False

    @staticmethod
    def checkResponseResult(response):
        try:
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            logger.error("response doesn't have status_code")

    @staticmethod
    def DownloadImage(FileName, URL):
        logger.info(f"starting downloading {FileName}")
        response = BaseClass.sendRequest(URL)
        if BaseClass.checkResponseResult(response) and FileName:
            ImageData = response.content
            BaseClass.WriteImage(FileName, ImageData)
            logger.info(f"Done saving the image {FileName}")
        else:
            logger.error(f"can't download the image {URL} ")


    @staticmethod
    def CreatWebDriver(DriverPath, profilePath, HeadLess=None):
        if BaseClass.checkIfFileExist(DriverPath) and BaseClass.checkIfDir(profilePath) :
            options = Options()
            if HeadLess:
                options.add_argument("-headless") 
            options.add_argument('--profile')
            options.add_argument(profilePath)
            return WebDriver(service=Service(DriverPath), options=options)
        else:
            logger.error("Can't find Driver Path or profile directory")

