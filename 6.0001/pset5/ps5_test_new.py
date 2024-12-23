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
    def evaluate(self, story):
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
        self.string_phrase = string_phrase
    
    def is_phrase_in(self, text):
        # New code
        text_lower = text.lower()
        
        for char in text_lower:
            if char in string.punctuation:
                text_lower = text_lower.replace(char, " ")
        
        text_split = text_lower.split()
        phrase_split = self.string_phrase.split()
        
        for e in phrase_split:
            if e not in text_split:
                return False
        
        text_join = " ".join(text_split)
        phrase_join = " ".join(phrase_split)
        
        return phrase_join in text_join

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, str_time):
        """
        Constructor:
        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
        Convert time from string to a datetime before saving it as an attribute.
        """
        time = datetime.strptime(str_time, "%d %b %Y %H:%M:%S")
        self.time = time

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        try:
            result = story.get_pubdate() < self.time
        except TypeError:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
            result = story.get_pubdate() < self.time
            
        return result

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        try:
            result = story.get_pubdate() > self.time
        except TypeError:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
            result = story.get_pubdate() > self.time
            
        return result

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger


class NotTrigger(Trigger):
    def __init__(self, some_trigger):
        self.some_trigger = some_trigger
    
    def evaluate(self, story):
        return not self.some_trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, some_trigger1, some_trigger2):
        self.some_trigger1 = some_trigger1
        self.some_trigger2 = some_trigger2
    
    def evaluate(self, story):
        return self.some_trigger1.evaluate(story) and self.some_trigger2.evaluate(story)

# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, some_trigger1, some_trigger2):
        self.some_trigger1 = some_trigger1
        self.some_trigger2 = some_trigger2
    
    def evaluate(self, story):
        return self.some_trigger1.evaluate(story) or self.some_trigger2.evaluate(story)



#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    story_fired = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                story_fired.append(story)
    
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
    t_dict = {'TITLE':TitleTrigger, 'DESCRIPTION':DescriptionTrigger, 'BEFORE':BeforeTrigger, 'AFTER':AfterTrigger, 'NOT':NotTrigger, 'AND':AndTrigger, 'OR':OrTrigger}
    
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


print(read_trigger_config('triggers.txt'))
