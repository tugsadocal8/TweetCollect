from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import csv

pencere = Tk()
pencere.title("Bilgi Toplama")
pencere.geometry("300x200")
pencere.minsize(300,200)
pencere.resizable(FALSE,FALSE)

kelime = Label(text="Aranacak Kelime : ")
kelime.pack(anchor = "nw",padx = 15)
kelimeGirisi = Entry()
kelimeGirisi.pack(anchor = "nw",padx = 15)

def tweetBilgileri():
    aranacakTweet = kelimeGirisi.get()
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(100)

    url = 'https://twitter.com/search?q=%23' + aranacakTweet + '&src=typed_query&f=live'
    driver.get(url)
    sleep(10)

    #scrolling down to find posts
    driver.find_element_by_css_selector(".u-size2of3")
    i = 0
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while(match == False):
        lastCount = lenOfPage
        sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    tweetCount=1
    usernameCount=1

    #scraping usernames
    boy = driver.find_elements_by_css_selector("span[class*='username u-dir u-textTruncate']")
    usernames = []
    for i in range(0,len(boy),1):

        b = driver.find_elements_by_css_selector("span[class*='username u-dir u-textTruncate']")[i].text
        usernames.append(b)
    with open("usernames.txt","w",encoding = "UTF-8") as file:
        for username in usernames:
            file.write(str(usernameCount)+ ".\n" + username + "\n")
            file.write("**************************" + "\n")
            usernameCount += 1
                
    #scraping tweets
    links = []
    main1 = driver.find_element_by_css_selector("#timeline>div>div.stream")
    articles = main1.find_elements_by_tag_name("li")
    for alphas in articles:
        try:
            a = alphas.find_element_by_tag_name("p").text
            links.append(a)
        except:
            pass
    file = open("tweets.txt","w",encoding = "UTF-8")
    for tweet in links:
        file.write(str(tweetCount)+ ".\n" + tweet + "\n")
        file.write("**************************" + "\n")
        tweetCount += 1

buton2 = Button(text="Tweet ve Yazarlarını Listele",command = tweetBilgileri)
buton2.pack(anchor = "nw",padx = 15)


############################################################################################

usernameAra = Label(text="Aranacak Profil : ")
usernameAra.pack(anchor = "nw",padx = 15, pady= 5)
usernameGirisi = Entry()
usernameGirisi.pack(anchor = "nw",padx = 15)

def profilBilgileri():
    username = usernameGirisi.get()
    browser = webdriver.Firefox()
    browser.set_page_load_timeout(100)

    url = 'https://twitter.com/' + username
    browser.get(url)
    sleep(5)
    
    browser.find_element_by_css_selector(".u-size2of3")
    i = 0
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while(match == False):
        lastCount = lenOfPage
        sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    isim = browser.find_elements_by_css_selector("a[class*='ProfileHeaderCard-nameLink u-textInheritColor js-nav']")[0].text
    profilBio = browser.find_elements_by_css_selector("p[class*='ProfileHeaderCard-bio u-dir']")[0].text
    konum = browser.find_elements_by_css_selector("span[class*='ProfileHeaderCard-locationText u-dir']")[0].text
    katilmaTarihi = browser.find_elements_by_css_selector("span[class*='ProfileHeaderCard-joinDateText js-tooltip u-dir']")[0].text
    dogumTarihi = browser.find_elements_by_css_selector("span[class*='ProfileHeaderCard-birthdateText u-dir']")[0].text
    say = browser.find_elements_by_css_selector("span[class*='ProfileNav-value']")[0].text
    boy2 = browser.find_elements_by_css_selector("p[class*='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text']")

    protweetCount=1
    
    #scraping tweets
    prolinks =[]
    for i in range(0,len(boy2),1):
        tweet = browser.find_elements_by_css_selector("p[class*='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text']")[i].text
        prolinks.append(tweet)

    with open("profileTweetsAndInfo.txt","w",encoding = "UTF-8") as file:
        
        file.write("Ad: " + isim + "\n")
        file.write("Bio:  " + profilBio + "\n")
        file.write("Konum:  " + konum + "\n")
        file.write("Hesap Açılış Tarihi:  " + katilmaTarihi + "\n")
        file.write("Doğum Tarihi:  " + dogumTarihi + "\n")
        file.write("Tweetler:  " + " \n")
        if len(boy2)==0:
            file.write("Tweetler koruma altında erişilemiyor.")
        for protweet in prolinks:
            file.write(str(protweetCount) + " " + protweet + "\n")
            file.write("**************************" + "\n")
            protweetCount +=1
            
buton = Button(text="Profil Verileri Al",command = profilBilgileri)
buton.pack(anchor = "nw",padx = 15)

mainloop()
