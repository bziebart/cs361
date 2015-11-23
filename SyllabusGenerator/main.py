#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import random
import os
import urllib
import jinja2
import datetime
import textbook
from textbook import *
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

DEFAULT_DOMAIN_NAME = 'basicName'
termKey = ''

class Calendar(ndb.Model):
	startDate = ndb.DateProperty(required = True)
	endDate = ndb.DateProperty(required = True)
	weekdayString = ndb.StringProperty(required = True)
	numOfWeeks = ndb.IntegerProperty(required = True)
	numOfDays = ndb.IntegerProperty(required = True)
	items = ndb.StringProperty(repeated = True)
	name = ndb.StringProperty(required = True)
	def create(cls):
		return Calendar().create(datetime.date(2015,7,3), datetime.date(2015, 9, 12),"MWF",[], '')
	
	def create(cls, classStartDate = datetime.date(2015,7,3),
	classEndDate = datetime.date(2015, 9, 12), classWeekdayString = "MWF", classItems = [], calendarName = ''):
		temp = Calendar()
		temp.startDate = classStartDate 
		temp.endDate = classEndDate
		temp.weekdayString = classWeekdayString
		dateHolder = classStartDate
		temp.numOfWeeks = 0
		while (dateHolder < classEndDate):
			temp.numOfWeeks = temp.numOfWeeks + 1
			dateHolder = dateHolder + datetime.timedelta(weeks=1)
		temp.numOfDays = 0
		if ("M" in classWeekdayString):
			temp.numOfDays = temp.numOfDays + 1
		if ("Tu" in classWeekdayString):
			temp.numOfDays = temp.numOfDays + 1
		if ("W" in classWeekdayString):
			temp.numOfDays = temp.numOfDays + 1
		if ("Th" in classWeekdayString):
			temp.numOfDays = temp.numOfDays + 1
		if ("F" in classWeekdayString):
			temp.numOfDays = temp.numOfDays + 1
		if ("Sa" in classWeekdayString):
			temp.numOfDays = temp.numOfDays + 1
		if ("Su" in classWeekdayString):
			temp.numOfDays = temp.numOfDays + 1
		temp.items = classItems
		temp.name = calendarName
		return temp
	def clone(self, cloneCalendar):
		self.startDate = cloneCalendar.startDate
		self.endDate = cloneCalendar.endDate
		self.weekdayString = cloneCalendar.weekdayString
		self.numOfWeeks = cloneCalendar.numOfWeeks
		self.numOfDays = cloneCalendar.numOfDays
		self.items = cloneCalendar.items
		self.name = cloneCalendar.name
		
class Lecture(ndb.Model):
	subject = ndb.StringProperty(required = True)
	courseNumber = ndb.IntegerProperty(required = True)
	sectionNumber = ndb.IntegerProperty(required = True)
	startDate = ndb.DateProperty(required = True)
	endDate = ndb.DateProperty(required = True)
	daysOfWeek = ndb.StringProperty(required = True)
	
	classTitle = ndb.StringProperty()
	TAName = ndb.StringProperty()
	TAOfficeHours = ndb.StringProperty()
	TAOfficeLocation = ndb.StringProperty()
	professorName = ndb.StringProperty()
	professorOfficeLocation = ndb.StringProperty()
	professorOfficeHours = ndb.StringProperty()
	classLocation = ndb.StringProperty()
	
	def create(cls):
		return Lecture.create('', 000, 000, datetime.date(2015,1,1), datetime.date(2015, 12, 31),"MTuWThFSaSu", '', '', '', '', '', '')
		
	def create(cls, classSubject = '', classCourseNumber = 0, classSectionNumber = 0, classStartDate = datetime.date(2015,1,1), classEndDate = datetime.date(2015, 12, 31), classDaysOfWeek = "MTuWThFSaSu", classTAName = '', classTAOfficeHours = '', classTAOfficeLocation = '', classProfessorName = '', classProfessorOfficeLocation = '', classProfessorOfficeHours = '', location = ''):
		temp = Lecture()
		temp.subject = classSubject
		temp.courseNumber = classCourseNumber
		temp.sectionNumber = classSectionNumber
		temp.startDate = classStartDate
		temp.endDate = classEndDate
		temp.daysOfWeek = classDaysOfWeek
		temp.TAName = classTAName
		temp.TAOfficeHours = classTAOfficeHours
		temp.TAOfficeLocation = classTAOfficeLocation
		temp.professorName = classProfessorName
		temp.professorOfficeLocation = classProfessorOfficeLocation
		temp.professorOfficeHours = classProfessorOfficeHours
		temp.classLocation = location
		return temp

class Grade(ndb.Model):
	letter = ndb.StringProperty(required = True)
	grade = ndb.IntegerProperty(required = True)

class Gradescale(ndb.Model):
	size = ndb.IntegerProperty(required = True)
	name = ndb.StringProperty(required = True)
	scale = ndb.StructuredProperty(Grade, repeated=True)
	def create(cls):
		return Gradescale.create(0,[],'')
	def create(cls, scaleSize = 0, scaleList = [], scaleName = ''):
		temp = Gradescale()
		temp.size = scaleSize
		temp.scale = scaleList
		temp.name = scaleName
		return temp
class Policy(ndb.Model):
    name = ndb.StringProperty(required = True)
    policy = ndb.StringProperty(required = True)
    def create(cls):
        return Policy('','')
    def create(cls, policyName = '', policyPolicy = ''):
        temp = Policy()
        temp.name = policyName
        temp.policy = policyPolicy
        return temp

class Policies(ndb.Model):
    policy = ndb.StructuredProperty(Policy, repeated=True)
    def create(cls): 
        return Policies([])
    def create(cls, newPolicy = []):
        temp = Policies()
        temp.policy = newPolicy
        return temp
        
class Book(ndb.Model):
    name = ndb.StringProperty()
    edition = ndb.StringProperty()
    author = ndb.StringProperty()
    isbn = ndb.StringProperty()
    cKey = ndb.StringProperty()
    bKey = ndb.StringProperty()


class Course(ndb.Model):
    cKey = ndb.StringProperty()
    department = ndb.StringProperty()
    courseNumber = ndb.StringProperty()
    bookList = ndb.StructuredProperty(Book, repeated=True)


class Syllabus(ndb.Model):
	name = ndb.StringProperty(required = True)
	gradeScale = ndb.StructuredProperty(Gradescale)
	calendar = ndb.StructuredProperty(Calendar)
	lecture = ndb.StructuredProperty(Lecture)
	book = ndb.StructuredProperty(Book, repeated=True)

	def create(cls):
		return Syllabus.create('blank', Calendar.create(), Lecture.create(), Gradescale.create())
	def create(cls, passedName = 'blank', passedCalendar = Calendar().create(), passedLecture = Lecture().create(), passedGradescale = Gradescale().create()):
		temp = Syllabus()
		temp.name = passedName
		temp.gradeScale = passedGradescale
		temp.calendar = passedCalendar
		temp.lecture = passedLecture
		temp.book.append(Book(name='Cat'))
		return temp
		
def main_key(domain_name = DEFAULT_DOMAIN_NAME):
	return ndb.Key('Domain', domain_name)
	
currentName = 'Default'
gradeScales = []
policies = []
uPolicies = []
sPolicies = []
newPolicy = Policy()

class MainHandler(webapp2.RequestHandler):
	def get(self):
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name)).order(-Syllabus.name)
		syllabi = syllabus_query.fetch(10)
		template_values = {
			
		}
		mySyllabus = Syllabus(parent=main_key(domain_name), name='Test1')
		#mySyllabus.name = 'Default'
		mySyllabus.gradeScale = Gradescale().create()
		mySyllabus.calendar = Calendar().create()
		mySyllabus.lecture = Lecture().create()
		#mySyllabus.put()
		global currentName
		currentName = 'Default'
		template = JINJA_ENVIRONMENT.get_template('landing.html')
		self.response.write(template.render(template_values)) 

class SyllabusHandler(webapp2.RequestHandler):
    def get(self):
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name)).order(-Syllabus.name)
		syllabi = syllabus_query.fetch()
		template = JINJA_ENVIRONMENT.get_template('select.html')
		render_parameter = {}
		render_parameter['tempSyllabus'] = syllabi
		output = template.render(render_parameter)
		self.response.write(output)

class NewSyllabusHandler(webapp2.RequestHandler):
    def post(self):
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name)).order(Syllabus.name)
		syllabi = syllabus_query.fetch(10)
		template_values = {
			
		}
		syllabusTerm = self.request.get('newSyllabus')
		global termKey
		termKey = str(syllabusTerm)
		newSyllabus = Syllabus(parent=main_key(domain_name), name=termKey)
		newSyllabus.gradeScale = Gradescale().create()
		newSyllabus.calendar = Calendar().create()
		newSyllabus.lecture = Lecture().create()
		newSyllabus.put()
		time.sleep(0.25)
		self.redirect('/select')

class DisplayHandler(webapp2.RequestHandler):
	def get(self):
		tempSyllabus = list(Syllabus.query(Syllabus.name==termKey))
		template = JINJA_ENVIRONMENT.get_template('displayBooks.html')
		render_parameter = {}
		render_parameter['termBooks'] = tempSyllabus[0].book
		output = template.render(render_parameter)
		self.response.write(output)

	def post(self):
		t = self.request.get('syllabus')
		tempSyllabus = list(Syllabus.query(Syllabus.name==t))
		if tempSyllabus:
			global termKey
			termKey = tempSyllabus[0].name
			template = JINJA_ENVIRONMENT.get_template('displayBooks.html')
			render_parameter = {}
			render_parameter['termBooks'] = tempSyllabus[0].book
			output = template.render(render_parameter)
			self.response.write(output)


class LectureHandler(webapp2.RequestHandler):
	def get(self):
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name))
		syllabus_query.filter(ndb.GenericProperty('name') == currentName)
		syllabi = syllabus_query.get()
		template_values = {
			'subject':syllabi.lecture.subject,
			'courseNumber':syllabi.lecture.courseNumber,
			'sectionNumber':syllabi.lecture.sectionNumber,
			'startDate':syllabi.lecture.startDate,
			'endDate':syllabi.lecture.endDate,
			'daysOfWeek':syllabi.lecture.daysOfWeek,
			'title':syllabi.lecture.classTitle,
			'taname':syllabi.lecture.TAName,
			'taOfficeHours':syllabi.lecture.TAOfficeHours,
			'taOfficeLocation':syllabi.lecture.TAOfficeLocation,
			'professorName':syllabi.lecture.professorName,
			'professorOfficeLocation':syllabi.lecture.professorOfficeLocation,
			'professorOfficeHours':syllabi.lecture.professorOfficeHours,
			'classLocation':syllabi.lecture.classLocation,
			}

		template = JINJA_ENVIRONMENT.get_template('lecture.html')
		self.response.write(template.render(template_values))  
		
	def post(self):	
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name)).order(Syllabus.name)
		syllabus_query.filter(ndb.GenericProperty('name') == currentName)
		
		syllabi = syllabus_query.get()
		myCalendar = syllabi.calendar
		myLecture = syllabi.lecture
		startDate = datetime.datetime.strptime(self.request.get('startDate'),"%Y-%m-%d")
		classEndDate = datetime.datetime.strptime(self.request.get('endDate'),"%Y-%m-%d")
		weekdayString = self.request.get('daysOfWeek')
		myLecture.subject = self.request.get('subject')
		myLecture.courseNumber = int(self.request.get('coursenumber'))
		myLecture.sectionNumber = int(self.request.get('sectionnumber'))
		myLecture.startDate = startDate
		myLecture.endDate = classEndDate
		myLecture.daysOfWeek = weekdayString
		myLecture.classTitle = self.request.get('title')
		myLecture.TAName = self.request.get('TAName')
		myLecture.TAOfficeHours = self.request.get('taOfficeHours')
		myLecture.TAOfficeLocation = self.request.get('taOfficeLocation')
		myLecture.professorName = self.request.get('professorName')
		myLecture.professorOfficeLocation = self.request.get('professorOfficeLocation')
		myLecture.professorOfficeHours = self.request.get('professorOfficeHours')
		myLecture.classLocation = self.request.get('classLocation')
	
		myCalendar = Calendar().create(startDate, classEndDate, weekdayString, myCalendar.items, myLecture.classTitle)
		syllabi.calendar = myCalendar
		syllabi.lecture = myLecture
		syllabi.put()
		self.redirect('/calendar')
		
class CalendarHandler(webapp2.RequestHandler):
	def get(self):
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name)).order(Syllabus.name)
		syllabus_query.filter(ndb.GenericProperty('name') == currentName)
		syllabi = syllabus_query.get()
		
		calendar_query = Calendar.query(
		ancestor=main_key(domain_name)).order(Calendar.name)
		
		calendars = calendar_query.fetch(10)
		template_values = {
			'startDate': syllabi.calendar.startDate,
			'endDate': syllabi.calendar.endDate,
			'weekdayString': syllabi.calendar.weekdayString,
			'oneDay': datetime.timedelta(days=1),
			'oneWeek': datetime.timedelta(weeks=1),
			'weeksInTerm':syllabi.calendar.numOfWeeks,
			'daysInWeek':syllabi.calendar.numOfDays,
			'ItemList':syllabi.calendar.items,
			'calendarName':syllabi.calendar.name,
			'calendars':calendars,
		}

		template = JINJA_ENVIRONMENT.get_template('calendar.html')
		self.response.write(template.render(template_values)) 
		
	def post(self):
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name)).order(Syllabus.name)
		syllabus_query.filter(ndb.GenericProperty('name') == currentName)
		
		syllabi = syllabus_query.get()
		test = self.request.get('generate')
		if 'Submit Calendar Information' in test or 'Save Calendar Information' in test:
			myCalendar = syllabi.calendar
			myCalendar.items=[]
			for index in range(0, myCalendar.numOfDays * myCalendar.numOfWeeks):
				myCalendar.items.append(self.request.get('Item'+str(index)))
			syllabi.calendar = myCalendar
			syllabi.put()
			self.response.write(myCalendar)
			if 'Save Calendar Information' in test:
				myCalendar.name = self.request.get('calendarName')
				calendar = Calendar(parent = main_key(domain_name))
				calendar.clone(myCalendar)
				calendar.put()
				self.response.write(calendar)
		else:
			calendar_query = Calendar.query(
		ancestor=main_key(domain_name)).order(Calendar.name)
			calendarName = self.request.get('previousCalendars')
			
			calendar = calendar_query.filter(Calendar.name == calendarName).get()
			syllabi.calendar = calendar
			syllabi.lecture.startDate = calendar.startDate
			syllabi.lecture.endDate = calendar.endDate
			syllabi.lecture.daysOfWeek = calendar.weekdayString
			syllabi.put()
			# self.response.write(calendarName)
			# self.response.write(calendar)
		self.redirect('/calendar')
		
class GradescaleHandler(webapp2.RequestHandler):
	def get(self):
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name)).order(Syllabus.name)
		syllabus_query.filter(ndb.GenericProperty('name') == currentName)
		
		syllabi = syllabus_query.get()
		template_values = {
			'size':syllabi.gradeScale.size,
			'scale':syllabi.gradeScale.scale,
			'name':syllabi.gradeScale.name,
			'gradeScales':gradeScales,
			}
		template = JINJA_ENVIRONMENT.get_template('gradescale.html')
		self.response.write(template.render(template_values))
		
		
	def post(self):
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name)).order(Syllabus.name)
		syllabus_query.filter(ndb.GenericProperty('name') == currentName)
		
		syllabi = syllabus_query.get()
		myGradescale = syllabi.gradeScale
		test = self.request.get('generate')
		# global myGradescale
		if 'Generate Scale' in test:
			size = int(self.request.get('size'))
			name = self.request.get('name')
			newScale = []
			for x in range(size):
				newScale.append(Grade(letter=''))
			myGradescale = myGradescale.create(size, newScale, name)
			syllabi.gradeScale = myGradescale
			syllabi.put()
			self.redirect('/gradescale')
		elif 'Save' in test:
			for i in range(myGradescale.size):
				myGradescale.scale[i].letter = self.request.get('letter'+str(i))
				myGradescale.scale[i].grade = int(self.request.get('grade'+str(i)))
			gradeScales.append(myGradescale)
			syllabi.gradeScale = myGradescale
			syllabi.put()
			self.redirect('/gradescale')
		elif 'Load' in test:
			i = int(self.request.get('previousScale'))
			myGradescale = gradeScales[i]
			syllabi.gradeScale = myGradescale
			syllabi.put()
			self.redirect('/gradescale')
		
	
class PolicyHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'policies':policies,
            'uPolicies':uPolicies,
            'sPolicies':sPolicies,
            'name':newPolicy.name,
            'policy':newPolicy.policy
            }
        template = JINJA_ENVIRONMENT.get_template('policy.html')
        self.response.write(template.render(template_values))
		
    def post(self):
        test = self.request.get('generate')
        if 'Save' in test:
            newPolicyText = str(self.request.get('policy'))
            newName = str(self.request.get('name'))
            global newPolicy
            newPolicy = Policy()
            newPolicy = newPolicy.create(newName,newPolicyText)
            policies.append(newPolicy)
            uPolicies.append(newPolicy)
            self.redirect('/policy')
			
        elif 'Load' in test:
            i = int(self.request.get('previousPolicy'))
            newPolicy = policies[i]
            self.redirect('/policy')
			
        elif 'Remove' in test:
            i = int(self.request.get('selectedPolicies'))
            uPolicies.append(sPolicies.pop(i))
		    #append sPolicies[i] to uPolicies
			#remove sPolicies[i]
            self.redirect('/policy')
			
        elif '<<' in test: 
			#append all items in sPolicies to uPolicies
			#remove all items from sPolicies
			
            self.redirect('/policy')

        elif 'Add' in test:
            i = int(self.request.get('unselectedPolicies'))
            sPolicies.append(uPolicies.pop(i))
            #append uPolicies[i] to sPolicies
			#remove uPolicies[i]
            self.redirect('/policy')
			
        elif '>>' in test:
			#append all items in uPolicies to sPolicies
			#remove all items from uPolicies
            self.redirect('/policy')

class TextbookHandler(webapp2.RequestHandler):
    def get(self):
        storedBooks = Book.query()
        courseList = Course.query()
        template = JINJA_ENVIRONMENT.get_template('textbook.html')
        render_parameter = {}
        render_parameter['courseList'] = courseList
        render_parameter['storedBooks'] = storedBooks
        render_parameter['noCourse'] = noCourse
        render_parameter['displayCourse'] = displayCourse
        output = template.render(render_parameter)
        self.response.write(output)

class TextbookPageHandler(webapp2.RequestHandler):
    def post(self):
        dep = self.request.get('dep')
        num = self.request.get('num')
        selectedCourse = self.request.get('Course')
        selectBook = self.request.get('Textbook')
        n = self.request.get('name')
        e = self.request.get('edition')
        a = self.request.get('author')
        i = self.request.get('isbn')

        if 'addCourse' in self.request.POST:
            global courseKey
            courseKey = courseKey + 1
            newCourse = Course(department=dep, courseNumber=num, cKey=str(courseKey))
            newCourse.put()
        elif 'removeCourse' in self.request.POST:
            newCourse = list(Course.query(Course.cKey==selectedCourse))
            if newCourse:
                newCourse[0].key.delete()
        elif 'addBook' in self.request.POST:
            global bookKey
            bookKey = bookKey + 1
            tempCourse = list(Course.query(Course.cKey==selectedCourse))
            if tempCourse:
                newKey = tempCourse[0].cKey + str(bookKey)
                newBook = Book(name=n, edition=e, author=a, isbn=i, cKey=tempCourse[0].cKey, bKey=str(newKey))
                newBook.put()
                tempCourse[0].bookList.append(newBook)
                tempCourse[0].put()
                global displayCourse
                displayCourse = tempCourse[0].bookList
        elif 'removeBook' in self.request.POST:
            tempBook = list(Book.query(Book.bKey==selectBook))
            tempCourse = list(Course.query(Course.cKey==tempBook[0].cKey))

            if tempBook and tempCourse:
                c = tempCourse[0]
                x = tempBook[0]
                time.sleep(0.25)
                for b in c.bookList:
                    if b.cKey == x.cKey and b.bKey == selectBook:
                        tempCourse[0].bookList.remove(b)
                        tempCourse[0].put()
                        break
                tempBook[0].key.delete()
                global displayCourse
                displayCourse = tempCourse[0].bookList
        elif 'chooseCourse' in self.request.POST:
            tempCourse = list(Course.query(Course.cKey==selectedCourse))
            if selectedCourse == 'showAll':
                noCourse = True
            elif tempCourse:
                global displayCourse
                displayCourse = tempCourse[0].bookList
                global noCourse
                noCourse = False
        elif 'chooseBook' in self.request.POST:
            tempBook = list(Book.query(Book.bKey==selectBook))
            if tempBook:
                global termKey
                tempSyllabus = list(Syllabus.query(Syllabus.name==termKey))
                if tempSyllabus:
                    tempSyllabus[0].book.append(tempBook[0])
                    tempSyllabus[0].put()
        time.sleep(0.25)
        if 'chooseBook' in self.request.POST:
            self.redirect('/display')
        else:
            self.redirect('/textbook')

class RemoveBookHandler(webapp2.RequestHandler):
    def post(self):
        tempSyllabus = list(Syllabus.query(Syllabus.name==termKey))
        book = self.request.get('syllabusBooks')
        if 'removeFromSyllabus' in self.request.POST:
            for b in tempSyllabus[0].book:
                if b.bKey == book:
                    tempSyllabus[0].book.remove(b)
                    tempSyllabus[0].put()
                    break
        time.sleep(0.25)
        self.redirect('/display')

class RemoveSyllabusHandler(webapp2.RequestHandler):
	def get(self):
		domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
		syllabus_query = Syllabus.query(
		ancestor=main_key(domain_name)).order(-Syllabus.name)
		syllabi = syllabus_query.fetch()
		for s in syllabi:
			s.key.delete()
		self.redirect('/select')

class PreviewHandler(webapp2.RequestHandler):
              def get(self):
                             domain_name = self.request.get('domain_name', DEFAULT_DOMAIN_NAME)
                             syllabus_query = Syllabus.query(
                             ancestor=main_key(domain_name)).order(Syllabus.name)
                             syllabus_query.filter(ndb.GenericProperty('name') == currentName)
                            
                             cSyllabus = syllabus_query.get()
                             template_values = {
                                           'title':cSyllabus.lecture.classTitle,
                                           'courseNumber':cSyllabus.lecture.courseNumber,
                                           'sectionNumber':cSyllabus.lecture.sectionNumber,
                                           'startDate':cSyllabus.lecture.startDate,
                                           'endDate':cSyllabus.lecture.endDate,
                                           'daysOfWeek':cSyllabus.lecture.daysOfWeek,
                                           'startDate': cSyllabus.calendar.startDate,
                                           'endDate': cSyllabus.calendar.endDate,
                                           'weekdayString': cSyllabus.calendar.weekdayString,
                                           'oneDay': datetime.timedelta(days=1),
                                           'oneWeek': datetime.timedelta(weeks=1),
                                           'weeksInTerm':cSyllabus.calendar.numOfWeeks,
                                           'daysInWeek':cSyllabus.calendar.numOfDays,
                                           'ItemList':cSyllabus.calendar.items,
                                           'dept_code':cSyllabus.lecture.subject,
                                           'courseLocation':cSyllabus.lecture.classLocation,
                                           'instrname':cSyllabus.lecture.professorName,
                                           'instrRoom':cSyllabus.lecture.professorOfficeLocation,
                                           'officeHours':cSyllabus.lecture.professorOfficeHours,
                                           'TAname':cSyllabus.lecture.TAName,
                                           'TAroom':cSyllabus.lecture.TAOfficeLocation,
                                           'TAhours':cSyllabus.lecture.TAOfficeHours,
                                           'syllabiLink':"http://uwm.edu/",
                                           'books':cSyllabus.book,
                                           'scale':cSyllabus.gradeScale.scale,
                                           'assessItem':"Project",
                                           'assessPercent':"40",
                                           'assessDesc':"The course project is implemented in phases by small groups of students. There are several phases of creating and refining deliverables such as requirements specifications, design documents, etc.",
                                          
                             }
 
                             template = JINJA_ENVIRONMENT.get_template('preview.html')
                             self.response.write(template.render(template_values))
                            
              def post(self):
                             self.redirect('/preview')
		
app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/select', SyllabusHandler),
	('/newSyllabus', NewSyllabusHandler),
	('/display', DisplayHandler),
	('/lecture', LectureHandler),
	('/calendar', CalendarHandler),
	('/gradescale', GradescaleHandler),
	('/policy', PolicyHandler),
	('/textbook', TextbookHandler),
	('/command', TextbookPageHandler),
	('/remove', RemoveBookHandler),
	('/clear', RemoveSyllabusHandler),
	('/preview', PreviewHandler)
], debug=True)
