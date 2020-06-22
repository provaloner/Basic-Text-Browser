import sys
import os
import requests
import bs4
from colorama import Fore, Style, init, deinit
init()

# for initializing a new directory from the command line
args = sys.argv
folder = args[1]
saved_pages = []
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, folder)
if not os.path.exists(final_directory):
    os.makedirs(final_directory)

scrape = ["p", "a", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6", ]
scrape_list = []
back_stack = []
while True:
    command = input()
    if command == "back":  # functions as a back button
        if len(back_stack) == 0:
            continue
        else:
            back_stack.pop()
            back_read = open(f"{final_directory}\\{back_stack[-1]}.txt")
            print(back_read.read())
            back_read.close()
    elif ".com" in command or ".org" in command:  # checks if command is a searchable url
        file_base = command[:command.rfind('.')]
        file_name = f"{final_directory}\\{file_base}.txt"  # creates file to be saved in directory
        back_stack.append(file_base)
        file_handle = open(file_name, "w")
        if command.startswith("https://"):
            r = requests.get(command)
            soup = bs4.BeautifulSoup(r.content, "html.parser")
            site_main = soup.children
            html = None
            body = None
            for element in site_main:
                if type(element) == bs4.element.Tag:
                    html = element
                    break
            for element in list(html.children):
                if type(element) == bs4.element.Tag:
                    body = element
                    break
            all_text = []
            for tag in body.find_all(scrape):  # writes page text to file, highlights links
                if tag.name == "a":
                    scrape_list.append((Fore.BlUE + tag.get_text()).strip().replace("\n", " "))
                else:
                    print(Style.RESET_ALL)
                    scrape_list.append(tag.get_text().strip().replace("\n", " "))
            for line in scrape_list:
                print(line)
                file_handle.write(line)
        else:
            r = requests.get(f"https://{command}")
            soup = bs4.BeautifulSoup(r.content, "html.parser")
            site_main = soup.children
            html = None
            body = None
            for element in site_main:
                if element.name == 'html':
                    html = element
                    break
            for element in list(html.children):
                if element.name == 'body':
                    body = element
                    break
            all_text = []
            for tag in body.find_all(scrape):
                if tag.name == "a":
                    scrape_list.append((Fore.BLUE + tag.get_text()).strip().replace("\n", " "))
                else:
                    print(Style.RESET_ALL)
                    scrape_list.append(tag.get_text().strip().replace("\n", " "))
            for line in scrape_list:
                print(line)
                file_handle.write(line)
        file_handle.close()
        saved_pages.append(file_base)
    elif command in saved_pages:  # allows for reading of previously saved pages 
        file_read = open(f"{final_directory}\\{command}.txt")
        print(file_read.read())
        file_read.close()
    elif command == "exit":
        break
    else:
        print("Error: Incorrect URL")
deinit()
