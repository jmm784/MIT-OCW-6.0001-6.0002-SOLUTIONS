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
from datetime import datetime , timezone
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
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    def is_phrase_in(self, text):
        text = text.lower()
        ss = " "
        for i in string.punctuation:
            text = text.replace(i, ss)
        text_list = text.split()
        for i in range(len(text_list)):
            text_list[i] = text_list[i].strip(string.punctuation)
        no_punc_text = ss.join(text_list)
        new_text = ss + no_punc_text + ss
        new_phrase = ss + self.phrase + ss
        if new_phrase in new_text:
            return True
        return False
        
    

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    def evaluate(self, story):
        title = story.get_title()
        return self.is_phrase_in(title)

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    def evaluate(self, story):
        title = story.get_description()
        return self.is_phrase_in(title)

# TIME TRIGGERS



# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

#'''
class TimeTrigger(Trigger):
    def __init__(self, time_str):
        est = pytz.timezone('EST')
        time_format = "%d %b %Y %H:%M:%S"
        parsed_time = datetime.strptime(time_str.strip(), time_format)
        self.time = est.localize(parsed_time)

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        if pubdate.tzinfo is None:
            pubdate = pytz.timezone("EST").localize(pubdate)
        return pubdate < self.time

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        if pubdate.tzinfo is None:
            pubdate = pytz.timezone("EST").localize(pubdate)
        return pubdate > self.time


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trig):
        self.trig = trig
    def evaluate(self, story):
        return not self.trig.evaluate(story)
        

# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2
    def evaluate(self, story):
        return self.trig1.evaluate(story) and self.trig2.evaluate(story)

# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2
    def evaluate(self, story):
        return self.trig1.evaluate(story) or self.trig2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    story_list = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) == True:
                story_list.append(story)
    stories = story_list
    return stories



#======================
# User-Specified Triggers
#======================
# Problem 11

'''
Note: below function taking from another online solution
'''

def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    trigger_file = open(filename, 'r')
    triggers = {}
    response = []
    for line in trigger_file:
        line = line.rstrip()
        # ignore comments and whitespace
        if len(line) == 0 or line.startswith('//'):
            continue
        args = line.split(',')
        [trigger_name, trigger_type] = args[:2]
        # make trigger objects and populate dict accordingly
        if trigger_name == 'ADD':  # finish making triggers
            response = [triggers.get(n) for n in args[1:] if triggers.get(n)]
            break
        if trigger_type == 'TITLE':
            triggers[trigger_name] = TitleTrigger(args[2])
        if trigger_type == 'DESCRIPTION':
            triggers[trigger_name] = DescriptionTrigger(args[2])
        if trigger_type == 'AFTER':
            triggers[trigger_name] = AfterTrigger(args[2])
        if trigger_type == 'BEFORE':
            triggers[trigger_name] = BeforeTrigger(args[2])
        if trigger_type == 'NOT':
            obj = triggers.get(args[2], None)
            if obj is None:  # ignore invalid triggers
                continue
            triggers[trigger_name] = NotTrigger(obj)
        if trigger_type == 'AND':
            obj1 = triggers.get(args[2], None)
            obj2 = triggers.get(args[3], None)
            if obj1 is None or obj2 is None:  # ignore invalid triggers
                continue
            triggers[trigger_name] = AndTrigger(obj1, obj2)
        if trigger_type == 'OR':
            obj1 = triggers.get(args[2], None)
            obj2 = triggers.get(args[3], None)
            if obj1 is None or obj2 is None:  # ignore invalid triggers
                continue
            triggers[trigger_name] = OrTrigger(obj1, obj2)
    return response


SLEEPTIME = 120 #seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        '''
        t1 = TitleTrigger("israel")
        t2 = DescriptionTrigger("palestine")
        t3 = DescriptionTrigger("gaza")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]
        '''

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        #print(triggerlist)
        
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
            #print("working check 1")
            stories = process("http://news.google.com/news?output=rss")
            #print("working check 2")

            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)
            #print("working check 3")

            list(map(get_cont, stories))
            #print("working check 4")
            scrollbar.config(command=cont.yview)
            #print("working check 5")


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

