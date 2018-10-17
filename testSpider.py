#This script is using Python library imdbpy to fetch urls of required series names in the IMDB website server
#For scraping data and fetching urls from the IMDB website, Scrapy, a free open source web crawling framework written in Python is used
#For creating mysql database table of the input variables i.e. Email address and TV series names corresponding to that email, pymylib library is used
#Email containing required output of status information of the desired series is sent using smtplib library
#In scrapy.Request method which is used to crawl to next url, dont_filter = True is passed everywhere to execute script indefinitely without stopping due to duplicacy condition

#To run this script run command  'scrapy runspider testSpider.py'    on your terminal after installing all the required libraries and dependencies as required and mentioned

import scrapy                                       #Libraries required
import imdb
import send_email
import datetime
import pymysql
#import imdb_database
#from imdb_database import mysqldb
from send_email import send_email
from datetime import datetime
from imdb import IMDb

tvid = IMDb()
subject = "TV Series Query Status"                  #subject for email to be sent
temp_url = "https://www.imdb.com"                   #fetched and visited imdb homepage as a starting point

class testSpider(scrapy.Spider):                    #scrapy spider with subclass scrapy.Spider inherited
    name="testSpider"                               #name of spider
    start_urls= ["https://www.imdb.com"]

    star_rating = ""
    series_list = []                                            #it will store the series names for current email id used in form of list
    email_id = ""                                               #it will store the current user email id    
    msg =""

    def parse(self, response):
        dataset = response.css('.subtext a::text').extract()                            #checking class for tv series main page
        last_season = response.css('.season-year-separator::text').extract_first()      #checking class for tv series last season page
        if dataset!=[] or last_season!=None :
            if dataset :
                y_text=dataset[len(dataset)-1]
                series_year = y_text[11:len(y_text)-2]
                y=series_year.split("–").pop()
                
                if(len(y)==4):                                                          #checking coondition if series has ended already
                    testSpider.msg = testSpider.msg + "The show has finished streaming all its episodes.\n\n"
                    if len(testSpider.series_list) > 0 :                                   #checking condition if series_list is not empty yet
                        next_series_name = tvid.search_movie(testSpider.series_list.pop())[0]
                        next_series_url=str(tvid.get_imdbURL(next_series_name))
                        testSpider.msg = testSpider.msg + "Tv series name : " + str(next_series_name)
                        testSpider.msg = testSpider.msg + "\nStatus : "
                        yield scrapy.Request(                                           #callback to next series url
                            response.urljoin(next_series_url),
                            callback=self.parse,
                            dont_filter = True
                        )
                    else :
                        print("\nMessage : \n" + testSpider.msg)                        #displaying status message to be sent through email
                        yield scrapy.Request(
                            response.urljoin("https://www.imdb.com"),
                            callback=self.parse,                                        #callback to imdb homepage
                            dont_filter = True
                        )
                else:                                                                   #executed when series not finished according to main page info. of series
                    last_season_url = response.css('.seasons-and-year-nav div a::attr(href)').extract_first()   
                    last_season_url = "https://www.imdb.com" + last_season_url          #complete url to last season page of the given series
                    yield scrapy.Request(
                        response.urljoin(last_season_url),
                        callback=self.parse,                                            #callback to last season page for given series
                        dont_filter = True
                    )

            else:
                flag=0                                  #flag=0 indicates series has finished airing
                airdate = response.css('.airdate::text').extract()
                if airdate==[]:                            #condition to check if airing date value not given
                    testSpider.msg = testSpider.msg + "The show has finished streaming all its episodes.\n\n"
                else :
                    for i in range(len(airdate)):
                        airdate[i] = airdate[i].strip()
                        if len(airdate[i]) == 0:            #if airdate value not given
                            testSpider.msg = testSpider.msg + "Series has already finished airing.\n\n"
                            flag =1
                            break
                        else :    
                            airdate[i] = airdate[i].split(" ")
                            
                            ep_year = airdate[i].pop()                      #episode airing year value
                            c_year = datetime.now().year                    #current date year value
                            if int(ep_year) < c_year :                      #condition to check year 
                                continue
                            elif int(ep_year) == c_year :
                                months = {'Jan':1 , 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}           #dicttionary to maonth number from episode airing month name
                                c_month = datetime.now().month              #current time month value
                                if airdate[i]==[]:                          #condition to check if month value not given
                                    flag=1
                                    testSpider.msg = testSpider.msg + "The next season will begin in " + str(ep_year) + ".\n\n"
                                    break
                                temp = airdate[i].pop()
                                temp1 = temp[0:3]
                                ep_month = months[temp1]                    #episode airing month name
                                if int(ep_month) < c_month :
                                    continue
                                elif int(ep_month) == c_month :
                                    c_date = int(datetime.now().strftime("%d"))             #current date number
                                    if airdate[i]==[]:                                      #condition when episode airing date value not given
                                        flag=1
                                        testSpider.msg = testSpider.msg + "The next season will begin in " + str(ep_year) + "-" + str(ep_month) +".\n\n"
                                        break
                                    ep_date = airdate[i].pop()                              #episode airing date number value
                                    if int(ep_date) > c_date :
                                        flag=1
                                        testSpider.msg = testSpider.msg + "The next episode will air on " + str(ep_year) + "-" + str(ep_month) + "-" +str(ep_date) +".\n\n"    
                                        break
                                    else :
                                        continue
                                        
                                else :
                                    ep_date = airdate[i].pop()
                                    flag=1
                                    testSpider.msg = testSpider.msg + "The next episode will air on " + str(ep_year) + "-" + str(ep_month) + "-" +str(ep_date) +".\n\n"
                                    break
                            else :                                                          #condition when episode airing year value is greater than current date year value
                                flag=1
                                testSpider.msg = testSpider.msg + "The next season will begin in " + str(ep_year) + ".\n\n"
                                break
                    
                    if flag == 0:                                                           #condition when no episode airing date value is greater than current time date value
                        testSpider.msg = testSpider.msg + "Series has already finished airing"
                
                if len(testSpider.series_list) > 0 :                                        #condition to check if series_list is empty or not
                    next_series_name = tvid.search_movie(testSpider.series_list.pop())[0]
                    next_series_url=str(tvid.get_imdbURL(next_series_name))
                    testSpider.msg = testSpider.msg + "Tv series name : " + str(next_series_name)
                    testSpider.msg = testSpider.msg + "\nStatus : "
                    yield scrapy.Request(
                        response.urljoin(next_series_url),
                        callback=self.parse,                                                 #callback to next series main page url
                        dont_filter = True
                    )
                else :                                                                       #condition when series_list is empty
                    print("\nMessage : \n" + testSpider.msg)                                 #printing status message result to be sent through email to user
                    yield scrapy.Request(
                        response.urljoin("https://www.imdb.com"),
                        callback=self.parse,                                                 #callback to imdb home page
                        dont_filter = True
                    )
        else :                                                                              #condition when reaching imdb home page
            
            send_email(subject,testSpider.msg,testSpider.email_id)                          #email sending method

            testSpider.msg = ""                                                             
            testSpider.email_id = input("Email address:")                                       #input for user email address value
            b = input ("TV Series:")                                                        #input for TV series list input seperated by commas

            #mysqldb(testSpider.email_id,b)                                                  #method to create mysql database table of inputs
        
            testSpider.series_list = b.split(",")                                           #creating list of tv series names
            testSpider.series_list.reverse()
            first_series_name = tvid.search_movie(testSpider.series_list.pop())[0]          #getting first series name from series_list
            first_series_url = str(tvid.get_imdbURL(first_series_name))                     #first series main page url

            testSpider.msg = testSpider.msg + "Tv series name : " + str(first_series_name)
            testSpider.msg = testSpider.msg + "\nStatus : "
            yield   scrapy.Request(
                response.urljoin(first_series_url),
                callback=self.parse,                                                        #callback to first series main page url
                dont_filter = True
            )


       