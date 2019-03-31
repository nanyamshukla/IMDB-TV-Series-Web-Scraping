---- PROJECT DETAILS ----

This project is used to write a Python script to take an Email address and a list of TV series names seperated by commas as inputs and creating a mysql database table of those inputs.
After taking inputs, the running status of the required series is needed to be sent to the mentioned email address.


---- INPUT/OUTPUT FORMATS ----

Input Format :

Email address: abc.123@xyz.com
TV Series: Game of thrones, suits, friends, black mirror, gotham

Email address: abcdef.1234@xyz.com
TV Series: Game of thrones, black mirror, da vinci demons, breaking bad

...


Output Format :

The mail send to abc.123@xyz.com should look like:

Tv series name: Game of thrones
Status: The next season begins in 2019.

Tv series name: Suits
Status: The next episode airs on 2018-09-19.

Tv series name: Friends
Status: The show has finished streaming all its episodes.

Tv series name: Gotham
Status: The next season begins in 2019.



---- WORKING EXPLANATION ----

Web Scraping done using : Scrapy
Email sent through : smtplib library functionality
Database created using : mysql connect and pymysql 

Working : 
The script uses scrapy spider to crawl through links.The spider initially starts by reaching imdb home page url (https://www.imdb.com).Then from there based on the inputs, one by one series names are fetched and there corresponding urls in the imdb website server are fetched using IMDbPY and crawled by using callback to the given url.
Status data is fetched based on the information provided in the various html classes on the corresponding series main page or their last season url page.
The airing date is compared through date values obtained through datetime.datetime.now() function so it will work for any date value i.e. no need to change code for later year values.
Rest of the comparisions done in the code to obtain status data are mentioned in the testSpider.py file in the form of comments.


---- SCRIPT EXECUTION ----

After saving the required files and dependecies, run anaconda prompt and change present working directory to the saved files directory and run this command :

scrapy runspider testSpider.py



