# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:08:19 2022

@author: Joseph Mason
"""

# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate
    
    


#======================
# Triggers
#======================

class Trigger(object):
    def eval(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    def __init__(self, string_phrase):
        self.lower_string_phrase = string_phrase.lower()
    
    def get_low_string_phrase(self):
        return self.lower_string_phrase
    
    def is_phrase_in(self, text):
        # New code
        text_lower = text.lower()
        
        for char in text_lower:
            if char in string.punctuation:
                text_lower = text_lower.replace(char, " ")
        
        text_split = text_lower.split()
        phrase_split = self.lower_string_phrase.split()
        
        for e in phrase_split:
            if e not in text_split:
                return False
        
        text_join = " ".join(text_split)
        phrase_join = " ".join(phrase_split)
        
        return phrase_join in text_join

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def eval(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def eval(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, dt_string):
        self.month_dict     = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        self.dt_list        = dt_string.split()
        self.day            = int(self.dt_list[0])
        self.month          = self.dt_list[1]
        self.year           = int(self.dt_list[2])
        self.time_list      = self.dt_list[3].split(':')
        self.hours          = int(self.time_list[0])
        self.minutes        = int(self.time_list[1])
        self.seconds        = int(self.time_list[2])
        self.dt_object      = datetime(self.year, self.month_dict[self.month], self.day, self.hours, self.minutes, self.seconds)
    
    def get_dt_object(self):
        return self.dt_object.replace(tzinfo = pytz.timezone("EST"))
    
# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def __init__(self, dt_string):
        TimeTrigger.__init__(self, dt_string)
    
    def eval(self, story):
        return story.get_pubdate().replace(tzinfo = pytz.timezone("EST")) < self.get_dt_object()
    
class AfterTrigger(TimeTrigger):
    def __init__(self, dt_string):
        TimeTrigger.__init__(self, dt_string)
    
    def eval(self, story):
        return story.get_pubdate().replace(tzinfo = pytz.timezone("EST")) > self.get_dt_object()

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, some_trigger):
        self.some_trigger = some_trigger
    
    def eval(self, story):
        inverse_result = not self.some_trigger.eval(story)
        return inverse_result
        
# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, some_trigger1, some_trigger2):
        self.some_trigger1 = some_trigger1
        self.some_trigger2 = some_trigger2
    
    def eval(self, story):
        and_result = self.some_trigger1.eval(story) and self.some_trigger2.eval(story)
        return and_result
    
# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, some_trigger1, some_trigger2):
        self.some_trigger1 = some_trigger1
        self.some_trigger2 = some_trigger2
    
    def eval(self, story):
        or_result = self.some_trigger1.eval(story) or self.some_trigger2.eval(story)
        return or_result

#======================
# Filtering
#======================

# Problem 10

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    story_fired = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.eval(story):
                story_fired.append(story)
    
    print(story_fired)
    
    return story_fired

#======================
# User-Specified Triggers
#======================
# Problem 11

def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    
    triggerlist = []
    t_dict = {'TITLE':TitleTrigger,
              'DESCRIPTION':DescriptionTrigger,
              'BEFORE':BeforeTrigger,
              'AFTER':AfterTrigger,
              'NOT':NotTrigger,
              'AND':AndTrigger,
              'OR':OrTrigger
              }
    
    for item in lines:
        
        item_split = item.split(',')
        
        if item_split[0] == 'ADD':
            for i in range(len(item_split)):
                if i != 0:
                    triggerlist.append(item_split[i])
        
        elif item_split[1] == 'AND' or item_split[1] == 'OR':
            ts1 = item_split[2]
            ts2 = item_split[3]
            item_split[0] = t_dict[item_split[1]](ts1, ts2)
            
        else:
            ts = item_split[2]
            item_split[0] = t_dict[item_split[1]](ts)
    
    return triggerlist


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("war")
        t2 = DescriptionTrigger("Palestine")
        t3 = DescriptionTrigger("Hamas")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]


        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()