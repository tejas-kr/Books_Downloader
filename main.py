import requests
from bs4 import BeautifulSoup as bs

import re

main_uri = "https://www.pdfdrive.com"


def download_book(book_link, book_name):

	book_link = book_link.split("-")
	book_id = book_link[-1] # will be used later on...
	book_link[-1] = book_link[-1].replace("e", "d")
	s = "-"
	book_link = s.join(book_link)

	req = requests.get(book_link)
	soup = bs(req.content, "html5lib")

	scripts = soup.findAll("script")

	matching = [s for s in scripts if "session:" in str(s)]

	src1 = str(matching)
	src1 = src1.split(":")

	session_val = re.compile("^'.*,r$")
	session_val_str_list = list(filter(session_val.match, src1))

	session_val_str = session_val_str_list[0].split(',')[0].replace("'", "")


	# Preparing the book_id

	book_id = book_id.split('.')[0].replace('e', '')
	to_download = requests.get(main_uri+"/ebook/broken?id="+book_id+"&session="+session_val_str) 
	to_download_soup = bs(to_download.content, "html5lib")
	download_link = to_download_soup.find_all("a", href=re.compile('ext=pdf'))[0]['href']

	print(book_name+" DOWNLOAD STARTED !")

	final_download = requests.get(main_uri+download_link, stream = True)
	with open(book_name+".pdf", 'wb') as f:
		for chunk in final_download.iter_content(chunk_size = 1024*1024):
			if chunk:
				f.write(chunk)

	print(book_name+" DOWNLOADED SUCCESSFULLY !")




def main():

	book_name = str(input("Please enter the exact book name to get the accurate results\nEnter book name: "))

	r = requests.get(main_uri+"/search?q="+book_name.replace(" ", "+")+"&em=1")

	soup = bs(r.content, "html5lib")

	link = soup.findAll("a", "ai-search")

	if len(link) != 0:

		book_link = str(link[0]['href'])

		book_link = main_uri+book_link

		download_book(book_link, book_name)


	else:
		print("The book you are searching does not exists in the database !")





if __name__ == "__main__":
	main()
