from bs4 import BeautifulSoup 
import lxml
import rate
import concurrent.futures
import numpy as np
import json
import requests
from tqdm import tqdm

MAX_THREADS = 10
csv_list = []
def download_prof(url):
    # Access class and load info and print to csv
    base_url = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + url
    print(base_url)
    try:
        page = requests.get(base_url)
    except:
        print("Network error")
    try:
        soup = BeautifulSoup(requests.get(base_url).text,'lxml')
    except:
        print("XML Parsing Error")
    #print(soup)
    #print("hello")
    rating_list = rate.Rating.load_info(soup,"csv")
    if(rating_list is None):
        print("Rating parsing error")
    return rating_list
    #with open("ff.csv", "a"):
    #csv_list = csv_list + rating_list

def get_data(profs): 
    # will pass in list of teacher ids to grab
    threads = min(MAX_THREADS,len(profs))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            #print(f"Thread starting for PROF: {id_num}")
            futures = {executor.submit(download_prof,id_num): id_num for id_num in tqdm(profs)}
            f = open("test1.csv", "a")
            
            for fut in concurrent.futures.as_completed(futures):
                f.write("".join(fut.result()))
            f.close()

def main():
    # First grab IDs from dictionary in text document
    teacher_num = 5
    names = open("names.txt", "r")
    prof_dict = json.load(names)
    #prof_list = np.array(prof_dict.values()[:teacher_num)
    prof_list = list(prof_dict.keys())[:teacher_num]
    get_data(prof_list)

if __name__ == '__main__':
    main()

