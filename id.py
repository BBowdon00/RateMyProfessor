import requests
import json
import base64

url = "https://www.ratemyprofessors.com/graphql"

results_num = 10
total_wanted = 50
headers = {
  'Connection': 'keep-alive',
  'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
  'Authorization': 'Basic dGVzdDp0ZXN0',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
  'Content-Type': 'application/json',
  'Accept': '*/*',
  'Origin': 'https://www.ratemyprofessors.com',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.ratemyprofessors.com/search/teachers?query=*',
  'Accept-Language': 'en-US,en;q=0.9'
}

array_name = "arrayconnection:"
names = dict()
curr =0 
while(curr < total_wanted):
    argu = array_name + str(curr)
    curr =curr+ results_num
    message_bytes = argu.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    payload = json.dumps({
	  "query": "query TeacherSearchPaginationQuery(\n  $count: Int\n  $cursor: String\n  $query: TeacherSearchQuery!\n) {\n  search: newSearch {\n    ...TeacherSearchPagination_search_1jWD3d\n  }\n}\n\nfragment TeacherSearchPagination_search_1jWD3d on newSearch {\n  teachers(query: $query, first: $count, after: $cursor) {\n    edges {\n      cursor\n      node {\n        ...TeacherCard_teacher\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n    resultCount\n  }\n}\n\nfragment TeacherCard_teacher on Teacher {\n  id\n  legacyId\n  avgRating\n  numRatings\n  ...CardFeedback_teacher\n  ...CardSchool_teacher\n  ...CardName_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment CardFeedback_teacher on Teacher {\n  wouldTakeAgainPercent\n  avgDifficulty\n}\n\nfragment CardSchool_teacher on Teacher {\n  department\n  school {\n    name\n    id\n  }\n}\n\nfragment CardName_teacher on Teacher {\n  firstName\n  lastName\n}\n\nfragment TeacherBookmark_teacher on Teacher {\n  id\n  isSaved\n}\n",
	  "variables": {
	    "count": results_num,
	    "cursor": base64_message,
	    "query": {
	      "text": "",
	      "schoolID": ""
	    }
	  }
	})
    response = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(response.text)
    responses=response["data"]["search"]["teachers"]["edges"]
    for entry in responses:
	    #print(entry["node"]["firstName"])
        names[entry["node"]["legacyId"]] = entry["node"]["firstName"]+" "+entry["node"]["lastName"]
    print("Currently %.2f%% of the way through (iteration %d of %d)" % (100*curr/total_wanted, curr/results_num, total_wanted/results_num)) 
print(names)
#with open('names.txt', 'w') as file:
#     file.write(json.dumps(names))
print(len(names))

