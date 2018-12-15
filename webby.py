#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from multiprocessing import Process, Queue, current_process


domain_list = []
choice = ''
done_queue = Queue()
process_queue = Queue()
NUM_WORKERS = 4 
def adddomain():
    global domain_list
    url1 = input("\n Enter the domain you would like to crawl: ")
    domain_list.append(url1)
    print("\n ***Domains to be Crawled*** \n")
    print(domain_list)
    print("\n" + "\n")

def deletedomain():
    global domain_list
    url1 = input("\n Enter the domain you would like to delete: ")
    domain_list.remove(url1)
    print("\n ***New List of Domains** \n")
    print(domain_list)
    print("\n" + "\n")

def loaddomains():
    global domain_list
    for domain in domain_list:
        process_queue.put(domain)
    print("\n The following domain(s) were loaded into the queue \n")
    print(domain_list)
    print("\n" + "\n")

def startproqueue(process_queue, done_queue):
    done_queue.put("{} starting".format(current_process().name))
    for domain in iter(process_queue.get, 'STOP'):
        result = requests.get(domain)
        done_queue.put("{}: Domain {} retrieved with {} bytes".format(current_process().name, domain, len(result.text)))


def main():
    global choice
    
    for i in range(NUM_WORKERS):
                    Process(target=startproqueue, args=(process_queue, done_queue)).start()

    while choice != "7":

        print("********************MAIN MENU********************")
        #time.sleep(1)
        print()

        choice = input("""
            1: Add a Domain Name
            2: Delete Domain Name
            3: Load Domains to Queue
            4: Start Processing Queue
            5: Stop Processing Queue
            6: Display Logs
            7: Exit

                
            Please enter your choice: """)

        if choice == "1":
            adddomain()
        elif choice == "2":
            deletedomain()
        elif choice == "3":
            loaddomains()
        elif choice == "4":
            startproqueue(process_queue, done_queue)
            for message in iter(done_queue.get, 'STOP'):
                print(message)
        elif choice == "5":
            stopproqueue()
        elif choice == "6":
            displaylog()
        elif choice == "7":
            sys.exit
        else:
            print("You must only select either 1, 2, 3, 4 or 5.")
            print("Please try again")
            menu()

if __name__== '__main__':
    main()   
