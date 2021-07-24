from bs4 import BeautifulSoup
import requests
import lxml
import re


# TODO: Write the web scraping in python
# TODO: Implement the threading
# Basically have threads sending the requests and passing them to other threads searching html and populating objects


class Rating:
    def __init__(self, professor, school, quality, difficulty, date, grade=None, pid=None,uid=None):
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
    def __repr__(self):
        return str(self)

    def data_point(self):
        return self.difficulty,self.quality
    
    @staticmethod
    def get_id(url):
        return re.findall(r'\d+', url)[0]
        
    @staticmethod
    def load_info(html_part):
        try:
            li = html_part.find(id="ratingsList").contents
        except:
            return []
        teacher_id = 80895
        p_name = html_part.select_one('.NameTitle__Name-dowf0z-0').get_text()
        u_name = html_part.select_one('.NameTitle__Title-dowf0z-1').a.get_text()
        u_id = Rating.get_id(html_part.select_one('.NameTitle__Title-dowf0z-1').a['href'])
        p_id = Rating.get_id(html_part.select_one('.NameLink__StyledNameLink-sc-4u2ek-0').a['href'])
        # Can remove the u and p name selectors. Use the dict to lookup the values for names.

        ratings = []
        for x in li:
            if x.select('.GAMAdInfeed__InfeedAdWrapper-rvdgxi-0'):
                continue
            nums = x.select('.CardNumRating__CardNumRatingNumber-sc-17t4b9u-2')
            date = x.select_one('.TimeStamp__StyledTimeStamp-sc-9q2r30-0').get_text()
            quality=nums[0].string
            difficulty=nums[1].string
            headers =x.select_one('.CourseMeta__StyledCourseMeta-x344ms-0').contents
            #print(len(headers))
            grade= None
            for h in headers:
                if "Grade" in h.get_text():
                    #print("Found grade!")
                    #print("GRADE: " + h.span.string)
                    grade = h.span.string
                    break
            ratings.append(Rating(p_name,u_name,quality,difficulty,date,grade,p_id,u_id))
        return ratings

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
