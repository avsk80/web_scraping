from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from selenium import webdriver
import time
import os
#import requests

## scraping images using selenium (JS tags)

def find_images(g_image_url: str, no_of_images: int, wd, sleep_between_interactions=0.5):
    #function to enable scrolling
    def scroll_page(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # sleep for 0.5 s
        time.sleep(sleep_between_interactions)

    #load the search image page
    wd.get(g_image_url)

    # fetching the mentioned no of image links and storing in the set
    image_links = set()
    image_count = 0
    results_start = 0
    while image_count < no_of_images:
        scroll_page(wd)

        # get all the thumbnail results
        # locate elements by class attribute name
        thumbnails = wd.find_elements_by_css_selector("img.Q4LuWd")
        thumbnail_count = len(thumbnails)
        #print("no of results found are:" + str(thumbnail_count))
        #print(thumbnails) ## this has unique thumbnails of the image elements present
        for img in thumbnails[results_start:thumbnail_count]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception as e:
                continue
            # extract image urls
            images = wd.find_elements_by_css_selector("img.n3VNCb")
            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_links.add(image.get_attribute('src'))
            image_count = len(image_links)

            if image_count >= no_of_images:
                print("images found count is:" + str(image_count))
                break
        else: ## this happens when the links count is less than required so we opt for loading more images by clicking the button in google
            print("images found count is:" + str(image_count) + "so, looking for more images!!")
            time.sleep(30)
            load_more = wd.find_elements_by_css_selector(".mye4qd")
            if load_more:
                wd.execute_script("document.querySelector('.mye4qd').click();")
        results_start = len(thumbnails)
    return image_links

def download_image(target_loc:str, link:str, counter:int):
    try:
        print(link)
        image_content = urlopen(link).read()
    except Exception as e:
        print("could not load image")

    with open(os.path.join(target_loc,'jpg'+"_"+str(counter)+".jpg"),'wb') as f:
        f.write(image_content)
        print("image url:"+ str(link) + "has been saved in" + str(target_loc))

def find_and_save(g_image_url, target_loc, driver_loc, no_of_images):
    # target loction of images
    if not os.path.exists(target_loc):
        print("creating new target location")
        os.makedirs(target_loc)
        print("created!!")
    else:
        print("target location already present")

    # run google webdriver from executable path of your choice
    with webdriver.Chrome(executable_path=driver_loc) as wd:
        # res has the image links to download the images
        res = find_images(g_image_url, no_of_images, wd=wd, sleep_between_interactions=0.5)
        print("length of res is:", len(res))
        counter = 0
        for ele in res:
            download_image(target_loc, ele, counter)
            counter = counter + 1
    # driver.quit()

if __name__ == "__main__":
    google = "https://www.google.com/search?tbm=isch&q="
    search = "apple"
    target_loc = 'D:\ineuron\projects\images'
    driver_loc = 'D:\ineuron\projects\image_scrapper\chromedriver_win32\chromedriver.exe'
    no_of_images = 10
    try:
        g_image_url = google + search
        print(g_image_url)
    except HTTPError as e:
        print("HTTP error")
    except URLError as e:
        print("URL error")
    except Exception as e:
        print("unknown exception handled" + str(e))
    g_image_url = google + search
    find_and_save(g_image_url, target_loc,driver_loc,no_of_images)

'''
JSON DATA

# import json library
import json
# request url
urlreq = 'https://groceries.asda.com/api/items/search?keyword=yogurt'
# get response
response = urllib.request.urlopen(urlreq)
# load as json
jresponse = json.load(response)
# write to file as pretty print
with open('asdaresp.json', 'w') as outfile:
    json.dump(jresponse, outfile, sort_keys=True, indent=4)
'''