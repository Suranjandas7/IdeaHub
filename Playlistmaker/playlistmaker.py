# randomize youtube picking no.

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import os.path
import glob


def operations(list_of_songs):
    chromedriver = 'chromedriver.exe'
    os.environ["webdriver.chrome.driver"] = chromedriver

    while len(list_of_songs) > 0:

        for song in list_of_songs:
            search_query = song
            driver = webdriver.Chrome(chromedriver)

            try:
                add = 0
                query = urllib.quote(search_query)
                url = "https://www.youtube.com/results?search_query=" + query
                response = urllib2.urlopen(url)
                html = response.read()
                soup = BeautifulSoup(html, 'lxml')
                k = []
                for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
                    k.append('https://www.youtube.com' + vid['href'])

                final_url = k[3]

                driver.get('http://www.youtube-mp3.org/')
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="youtube-url"]').clear()
                driver.find_element_by_xpath(
                    '//*[@id="youtube-url"]').send_keys(final_url)
                driver.find_element_by_xpath('//*[@id="submit"]').click()
                time.sleep(4)
                driver.set_window_size(1920, 1080)
                time.sleep(4)
                driver.find_element_by_xpath('//*[@id="dl_link"]/a[4]').click()
                while True:
                    time.sleep(5)
                    list_of_files = glob.glob("c:\users\sd\downloads\*")
                    latest_file = max(list_of_files, key=os.path.getctime)

                    if latest_file.endswith('.mp3') is True:
                        driver.quit()
                        list_of_songs.remove(song)
                        k = str(latest_file)
                        i = k.split('\\')
                        name = 'E:\\music\\' + str(i[len(i) - 1])
                        os.rename(
                            latest_file, name)
                        print '[Song Added : ' + str(name) + ']'
                        break
                        # SONG DOWNLOADED
            except ElementNotVisibleException:
                print '[NETWORK ERROR]'
                driver.quit()
                break
            except NoSuchElementException:
            	print '[NETWORK ERROR]'
            	driver.quit()
            	break
    driver.quit()


def query_list():
    query = ['nothing else matters metallica',
             'Le tasche piene di sassi Violetta']
    operations(query)

if __name__ == '__main__':
    query_list()
