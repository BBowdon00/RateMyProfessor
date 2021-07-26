from bs4 import BeautifulSoup 
import lxml
import rate
import concurrent.futures
import numpy as np
import json
import requests
import base64
from tqdm import tqdm

MAX_THREADS = 17
csv_list = []
import requests
import json

headers = {
  'Connection': 'keep-alive',
  'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
  'Authorization': 'Basic dGVzdDp0ZXN0',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
  'Content-Type': 'application/json',
  'Accept': '*/*',
  'Origin': 'https://www.ratemyprofessors.com',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=48',
  'Accept-Language': 'en-US,en;q=0.9'
}

def make_payload(pid, num_reviews=500):
    base_pid = "Teacher-"+str(pid)
    pid_bytes = base_pid.encode('ascii')
    base_pid = base64.b64encode(pid_bytes).decode('ascii')
    payload = json.dumps({"query": "query RatingsListQuery(\n  $count: Int\n  $id: ID\n  $courseFilter: String\n  $cursor: String\n) {\n  node(id: $id) {\n    __typename\n    ... on Teacher {\n      ...RatingsList_teacher_4pguUW\n    }\n    id\n  }\n}\n\nfragment RatingsList_teacher_4pguUW on Teacher {\n  id\n  legacyId\n  lastName\n  numRatings\n  school {\n    id\n    legacyId\n    name\n    city\n    state\n    avgRating\n    numRatings\n  }\n  ...Rating_teacher\n  ...NoRatingsArea_teacher\n  ratings(first: $count, after: $cursor, courseFilter: $courseFilter) {\n    edges {\n      cursor\n      node {\n        ...Rating_rating\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n  }\n}\n\nfragment Rating_teacher on Teacher {\n  ...RatingFooter_teacher\n  ...RatingSuperHeader_teacher\n  ...ProfessorNoteSection_teacher\n}\n\nfragment NoRatingsArea_teacher on Teacher {\n  lastName\n  ...RateTeacherLink_teacher\n}\n\nfragment Rating_rating on Rating {\n  comment\n  flagStatus\n  teacherNote {\n    id\n  }\n  ...RatingHeader_rating\n  ...RatingSuperHeader_rating\n  ...RatingValues_rating\n  ...CourseMeta_rating\n  ...RatingTags_rating\n  ...RatingFooter_rating\n  ...ProfessorNoteSection_rating\n}\n\nfragment RatingHeader_rating on Rating {\n  date\n  class\n  helpfulRating\n  clarityRating\n  isForOnlineClass\n}\n\nfragment RatingSuperHeader_rating on Rating {\n  legacyId\n}\n\nfragment RatingValues_rating on Rating {\n  helpfulRating\n  clarityRating\n  difficultyRating\n}\n\nfragment CourseMeta_rating on Rating {\n  attendanceMandatory\n  wouldTakeAgain\n  grade\n  textbookUse\n  isForOnlineClass\n  isForCredit\n}\n\nfragment RatingTags_rating on Rating {\n  ratingTags\n}\n\nfragment RatingFooter_rating on Rating {\n  id\n  comment\n  adminReviewedAt\n  flagStatus\n  legacyId\n  thumbsUpTotal\n  thumbsDownTotal\n  thumbs {\n    userId\n    thumbsUp\n    thumbsDown\n    id\n  }\n  teacherNote {\n    id\n  }\n}\n\nfragment ProfessorNoteSection_rating on Rating {\n  teacherNote {\n    ...ProfessorNote_note\n    id\n  }\n  ...ProfessorNoteEditor_rating\n}\n\nfragment ProfessorNote_note on TeacherNotes {\n  comment\n  ...ProfessorNoteHeader_note\n  ...ProfessorNoteFooter_note\n}\n\nfragment ProfessorNoteEditor_rating on Rating {\n  id\n  legacyId\n  class\n  teacherNote {\n    id\n    teacherId\n    comment\n  }\n}\n\nfragment ProfessorNoteHeader_note on TeacherNotes {\n  createdAt\n  updatedAt\n}\n\nfragment ProfessorNoteFooter_note on TeacherNotes {\n  legacyId\n  flagStatus\n}\n\nfragment RateTeacherLink_teacher on Teacher {\n  legacyId\n  numRatings\n  lockStatus\n}\n\nfragment RatingFooter_teacher on Teacher {\n  id\n  legacyId\n  lockStatus\n  isProfCurrentUser\n}\n\nfragment RatingSuperHeader_teacher on Teacher {\n  firstName\n  lastName\n  legacyId\n  school {\n    name\n    id\n  }\n}\n\nfragment ProfessorNoteSection_teacher on Teacher {\n  ...ProfessorNote_teacher\n  ...ProfessorNoteEditor_teacher\n}\n\nfragment ProfessorNote_teacher on Teacher {\n  ...ProfessorNoteHeader_teacher\n  ...ProfessorNoteFooter_teacher\n}\n\nfragment ProfessorNoteEditor_teacher on Teacher {\n  id\n}\n\nfragment ProfessorNoteHeader_teacher on Teacher {\n  lastName\n}\n\nfragment ProfessorNoteFooter_teacher on Teacher {\n  legacyId\n  isProfCurrentUser\n}\n","variables": {"count": num_reviews,"id": base_pid,"courseFilter": None,"cursor": "YXJyYXljb25uZWN0aW9uOjA"}})
    return payload

def download_prof(pid,in_mode,out_mode):
    # Access class and load info and print to csv
    if(in_mode=="json"):
        base_url = "https://www.ratemyprofessors.com/graphql"
        payload = make_payload(pid)
        try:
            response = requests.request("POST", base_url, headers=headers, data=payload)
        except:
            print("Network Error")
        in_data = response.json()["data"]["node"] #array of dict, info is in node key    
    elif in_mode =="html":
        base_url = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + pid
        #print(base_url)
        try:
            page = requests.get(base_url)
        except:
            print("Network error")
        try:
            in_data = BeautifulSoup(requests.get(base_url).text,'lxml')
        except:
            print("XML Parsing Error")

    rating_list = rate.Rating.load_info(in_data,in_mode,out_mode)
    if(rating_list is None):
        print("Rating parsing error")
    return rating_list
    #with open("ff.csv", "a"):
    #csv_list = csv_list + rating_list

def get_data(profs,in_mode, out_mode): 
    # will pass in list of teacher ids to grab
    threads = min(MAX_THREADS,len(profs))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            #print(f"Thread starting for PROF: {id_num}")
            futures = {executor.submit(download_prof,id_num,in_mode,out_mode): id_num for id_num in profs}
            f = open("test1.csv", "w")
            f.write("Professor,University,Quality,Difficulty,Date,Grade,PID,UID")
            for fut in tqdm(concurrent.futures.as_completed(futures)):
                f.write("".join(fut.result()))
            f.close()
def main():
    # First grab IDs from dictionary in text document
    teacher_num = 100
    names = open("names.txt", "r")
    prof_dict = json.load(names)
    names.close()
    in_mode = "json"
    out_mode = "csv"
    #prof_list = np.array(prof_dict.values()[:teacher_num)
    prof_list = list(prof_dict.keys())[:teacher_num]
    get_data(prof_list,in_mode,out_mode)

if __name__ == '__main__':
    main()

