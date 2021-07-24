from bs4 import BeautifulSoup
import requests
import lxml
import re

class Rating:
    name_selector = '.NameTitle__Name-dowf0z-0'
    school_selector = '.NameTitle__Title-dowf0z-1'
    date_selector = '.TimeStamp__StyledTimeStamp-sc-9q2r30-0'
    heading_selector = '.CourseMeta__StyledCourseMeta-x344ms-0'
    uid_selector = '.NameTitle__Title-dowf0z-1'
    pid_selector = '.NameLink__StyledNameLink-sc-4u2ek-0'
    rating_selector = '.CardNumRating__CardNumRatingNumber-sc-17t4b9u-2'
    blank_selector = '.GAMAdInfeed__InfeedAdWrapper-rvdgxi-0'

    def __init__(self, professor, school, quality, difficulty, date, grade="None", pid="None",uid="None"):
        self.professor = professor
        self.school = school
        self.quality = quality
        self.difficulty = difficulty
        self.date = Rating.date_parse(date)
        self.grade = grade
        self.pid = pid
        self.uid=uid

    @staticmethod
    def date_parse(date):
        return date

    def __str__(self):
        x = "Professor: " + self.professor + "\n"
        x= x+"School: " + self.school + "\n"
        x=x+"Quality: " + self.quality + "\n"
        x=x+"Difficulty: " + self.difficulty + "\n"
        x=x+"Date: " + self.date + "\n"
        if self.grade is not None:
            x=x+"Grade: " + self.grade + "\n"
        x=x+"PID: " + self.pid + "\n"
        x=x+"UID: " + self.uid + "\n"
        return x
    
    def csv_rep(self):
        return ",".join(list(vars(self).values()))+"\n"

    def __repr__(self):
        return str(self)

    def data_point(self):
        return self.difficulty,self.quality
    
    @staticmethod
    def get_id(url):
        return re.findall(r'\d+', url)[0]
        
    @staticmethod
    def load_info(data,in_format,ret_format="objs"):
        if in_format == "json":
            json_part = data

        else:
            html_part = data

        try:
            li = html_part.find(id="ratingsList").contents
        except:
            return []
        teacher_id = 80895
        p_name = html_part.select_one(Rating.name_selector).get_text()[:-1]
        u_name = html_part.select_one(Rating.school_selector).a.get_text()
        u_id = Rating.get_id(html_part.select_one(Rating.uid_selector).a['href'])
        p_id = Rating.get_id(html_part.select_one(Rating.pid_selector).a['href'])
        # Can remove the u and p name selectors. Use the dict to lookup the values for names.
        #print("Beginning of program")
        ratings = []
        for review in li:
            if review.select(Rating.blank_selector):
                continue
            nums = review.select(Rating.rating_selector)
            date = re.sub("(st|nd|rd|th){1},{1}","",review.select_one(Rating.date_selector).get_text())
            quality=nums[0].string
            difficulty=nums[1].string
            headers =review.select_one(Rating.heading_selector).contents
            #print(len(headers))
            grade= "None"
            for h in headers:
                if "Grade" in h.get_text():
                    grade = h.span.string
                    break
            obj = Rating(p_name,u_name,quality,difficulty,date,grade,p_id,u_id)
            #print(ret_format)
            if(ret_format=="objs"):
                ratings.append(obj)
            elif(ret_format=="csv"):
                ratings.append(obj.csv_rep())
            else:
                print("Format not specified correctly")
        
        return ratings
"""
def main():
    total_ratings = []
    professors = dict()
    schools = dict()
    
    starting_teacher_id = 80895
    i = 0
    while i < 10:
        url = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid="+str(starting_teacher_id+i)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        total_ratings += Rating.load_info(soup)
        i = i + 1
    print(total_ratings)
if __name__ == "__main__":
    main()
"""
