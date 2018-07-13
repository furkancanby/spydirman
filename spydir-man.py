import requests
import colorama
import wget
from 	bs4 		import BeautifulSoup
from    colorama   	import init, Fore, Back, Style

SUCCESS_COLOR 	= Fore.GREEN

#FIND LINES WORDS IN KEYWORDS LIST, RETURN LINE NUMBERS
def find_lines(htmltext_beautified_splitted,keywords):
	line_number=0
	total_line = len(htmltext_beautified_splitted)
	
	foundded_lines_numbers = []

	for line in htmltext_beautified_splitted:
		flag = 0
		for kw in keywords:
			
			if kw in line:
				foundded_lines_numbers.append(line_number)
				flag=1			

		if flag==0:
			pass

		line_number += 1
	return foundded_lines_numbers

# GET LINK AFTER A PARAMETER LIKE ...src="LINK"... 
def find_withPreword_link_fromLine(line,needed_Preword):
	inside = ""

	if line.find(needed_Preword) > 0:
		if needed_Preword != "":
			pos = int(line.find(needed_Preword)) + 3
		else:
			pos = 0

		line= line[pos:]
		num_q = 0
		
		for char in line:
			if num_q==2:
				#num_q=0
				break
			
			if num_q==1:
				if char != "\"":
					inside += char
				else:
					num_q=2
					continue

			if char == "\"":
				num_q+=1

		return inside
	else:
		return None

# IF THE WEBSITE IS REACHABLE RETURN TRUE
def check_website(link):

	request = requests.get(str(link))
	if request.status_code == 200:
		return True
	else:
		return False

# CHECK END OF THE WEBSITE IF UNNECESSERILY "/" IS EXIST 
# DELETE THEM AND RETURN NICE FORMAT WEBSITE :D
def complete_links_withBaseSite(website):
	
	dotta	= website.split(".")
	_com 	= dotta[len(dotta)-1]
	last_word = _com[len(_com)-1]

	if last_word == "/":
		
		return complete_links_withBaseSite(website[0:len(website)-1])
	else:
		return website

def image_downloader(WEBSITE):
	images 			= [".jpeg",".jpg",".png"]
	images_pre 		= ["src","href"]
	page = requests.get(str(WEBSITE),verify=True)
	soup = BeautifulSoup(page.content,"html.parser" ,from_encoding="utf-8")
	print(soup.prettify())
	
	beautified = soup.prettify()
	linebyline = beautified.split("\n")

	print(  str(len(str(page.text).split("\n")) )+  " lines are read from" + SUCCESS_COLOR + " ORIGINAL " + Fore.WHITE +"source code of " + str(WEBSITE))
	print(  str(len(linebyline) )+ " lines are reduced codes to" + SUCCESS_COLOR + " BEAUTIFIED " + Fore.WHITE +"source code of " + str(WEBSITE))
	
	founded_lines = find_lines(linebyline,images)
	print(Fore.YELLOW+str(images)+"\n"+Fore.CYAN+str(founded_lines))

	for i in range(len(founded_lines)):
	
		line =linebyline[ founded_lines[i] ]
	
		for pre in images_pre:
			urL = find_withPreword_link_fromLine(line,pre)
			#print(urL)
			if urL != None:
				print(urL)
				if urL.find("http://"):

					final_link = WEBSITE +'/' + str(urL)
					destination = urL
				else:
					final_link = urL
					destination = 'files/' 
				print(str(final_link))
				wget.download(final_link, destination)
				print()

if __name__ == "__main__":
	init(autoreset=True)    # AUTORESET COLORING	
	WEBSITE 		= "http://www.github.com"
	image_downloader(WEBSITE)
