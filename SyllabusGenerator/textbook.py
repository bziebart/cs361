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
import os
import urllib
import jinja2
import time
from jinja2 import Environment, FileSystemLoader
from google.appengine.ext import ndb

JINJA_ENV = Environment(loader=FileSystemLoader('./'))

courseKey = 5
bookKey = 5
noCourse = True
displayCourse = []


class MainHandler(webapp2.RequestHandler):
    def get(self):
        storedBooks = Book.query()
        courseList = Course.query()
        template = JINJA_ENV.get_template('textbook.html')
        render_parameter = {}
        render_parameter['courseList'] = courseList
        render_parameter['storedBooks'] = storedBooks
        render_parameter['noCourse'] = noCourse
        render_parameter['displayCourse'] = displayCourse
        output = template.render(render_parameter)
        self.response.write(output)
        
class LandingHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('landing.html')
        render_parameter = {}
        output = template.render(render_parameter)
        self.response.write(output)
        
class LectureHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('lecture.html')
        render_parameter = {}
        output = template.render(render_parameter)
        self.response.write(output)

class GradescaleHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('gradescale.html')
        render_parameter = {}
        output = template.render(render_parameter)
        self.response.write(output)

class PolicyHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('policy.html')
        render_parameter = {}
        output = template.render(render_parameter)
        self.response.write(output)

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('calendar.html')
        render_parameter = {}
        output = template.render(render_parameter)
        self.response.write(output)

class previewHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('preview.html')
        render_parameter = {}
        output = template.render(render_parameter)
        self.response.write(output)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/landing', LandingHandler),
    ('/lecture', LectureHandler),
    ('/gradescale', GradescaleHandler),
    ('/policy', PolicyHandler),
    ('/calendar', CalendarHandler),
    ('/preview', previewHandler),
], debug=True)
