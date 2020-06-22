Instructions for running the Project Officium python script are incredibly simple and there only a few of them.

Mostly you will only have to install some external libraries. These libraries can be installed via the Python Installer Package (i.e. pip) through the system command prompt or via your IDE - either through the terminal or through a particular setting that allows the installation of external libraries.

These external libraries are as follows:
1. ttkthemes - this is for themed appearance of the GUI
2. gTTS - This is the google text to speech library, this is to enable the Speak function
3. selenium  - this to allow the working of the google search function
4. urllib3 - this module allows this module allows us to perform the YouTube search as this module allows us to access websites, parse data and send GET & POST requests.
5. wikipedia - library that makes it easy to access and parse data from Wikipedia.
6. pyowm - Python Open weather module is a wrapper library for OWM web APIs

The other libraries used come included with Python 3.8

Another important thing to do before running the program is the installation of the browser specific driver that works in conjunction with the Selenium library to allow the google search. The browser specific driver is essentially a standalone server or a separate executable that is used by Selenium to control the respective browser.

Which driver for which browser?
GeckoDriver (the one used in the current project script) - Firefox
ChromeDriver - Chrome

The steps to perform:
1. Download the driver based on your current browser. If you have Firefox, then you can simply download from project repository on GitHub. If you have chrome then use this link: https://chromedriver.chromium.org/downloads
2. There is no installation whatsoever, just place the driver wherever in your computer and then simply follow the subsequent steps.
3. Once driver has been placed, copy the PATH - that is, the address, for example: "C:\Users\fahad\Documents\Pycharm Projects\geckodriver"
4. Once path is noted paste/write/change the PATH given in the source code on line #149, this the following line of code: driver = webdriver.Firefox(executable_path=r'C:\Users\fahad\Documents\Pycharm Projects\geckodriver')

Once these steps and installations have been done, you are free to run the python script for Project Officium!