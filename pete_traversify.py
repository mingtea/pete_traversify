
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re

#there are currently 264 pages of Pete Travers reviews on Rolling Stone, start at page 1.
page_count = 1

#the base url of pete travers' reviews
url_root = "https://www.rollingstone.com/contributor/peter-travers?page="

#counting how many instances of triumph we find
triumph_counter = 0
#the regex that matches triumph, don't care if it's upper or lower case
triumph_regex = re.compile(r'triumph(ant)?', re.I)

#each page has like 15 reviews on it. this is the base page
page_urls = []
#...and this is the page we will scrape for instances of the word 'triumph'
review_urls = []

print("Let's see how often that hack Pete Travers uses the word 'triumph'!")
#first get all the base pages
for counter in range(1,265):
	cur_url = url_root+str(page_count)
	page_urls.append(cur_url)
	page_count = page_count + 1
print("Gathered "+str(len(page_urls))+" base pages...")
#then get all the review urls from the base pages and put them in a list

for review_url in page_urls:
	r = get(review_url)
	soup = BeautifulSoup(r.content, 'html.parser')
	for a in soup.find_all('article', class_="content-card card-container"):
		l = a.find('a')
		review_urls.append(l.attrs['href'])
print("For a total of "+str(len(review_urls))+" reviews by Peter Travers.")

#here's where the magic happens... i guess.
#why am i doing this
for review in review_urls:
	r = get(review)
	soup = BeautifulSoup(r.content, 'html.parser')
	para = soup.find_all('p')
	for p in para:
		text = p.text
		for t in re.finditer(triumph_regex, text):
			triumph_counter += 1
print("I combed "+ str(len(review_urls))+ " reviews and found "+str(triumph_counter)+ " instances of the word triumph.")


