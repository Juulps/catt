#!/usr/bin/env python
import tweepy
#from our keys module (keys.py), import the keys dictionary
from keys import keys
from pprint import pprint
import time
import random

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

REPLIES = [
"Hello <name>. I want to play a game. The rules are simple. All you have to do is sit here and talk to me. Listen to me. My name is John",
"Hello <name>. I want to play a game. The rules are simple. Do what I say and you will find your <information> safe and secure.",
"Hello <name>. I want to play a game.. Be aware.. We haven't properly introduced. My name is John.",
"Hello <name>. Do you want to play a game? I want to play a game. The rules are simple. Sit here and talk to me. Listen to me. ",
"Hello <name>. I want to play a game. Listen to me. If you do that long enough you will find your <information> in a safe and secure state.",
"Hello <name>. I want to play a game. Listen to me. If you do that long enough you will find yourself in a safe and secure state."
]

api = None
ANSWERS = None

def connect():
	global api
	print "Connecting to the twitter API"
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

def search():
	global api

	allresults = []
	
	resplayagame = api.search(q="play a game")
	resplayinggames = api.search(q="playing games")
	resgame = api.search(q="game")
	
	allresults.append(resplayagame)
	allresults.append(resplayinggames)
	allresults.append(resgame)

	return allresults


def mentions():
	mentions = api.mentions_timeline(count=1)
	if mentions:
		for m in mentions:
			print(m)
	else:
		print "No mentions yet"

def tweetforever():
	filename=open('conversation.txt','r')
	f=filename.readlines()
	filename.close()

	for line in f:
		api.update_status(status=line)
		print line

def load_my_answers():
	global ANSWERS
	f=open('conversation.txt','r')
	ANSWERS=f.readlines()
	f.close()

def get_answer():
	return random.choice(ANSWERS)

def get_additional_info_from(who):
	global api

	last4tweets = api.user_timeline(screen_name=who, count=4)

	import nltk

	allnouns = []
	for t in last4tweets:
		tokens = nltk.word_tokenize(t.text)
		pprint(tokens)
		tagged = nltk.pos_tag(tokens)
		pprint(tagged)
		for word, tag in tagged:
			if tag == 'NN':
				allnouns.append(word)
	
	return allnouns

	# find nouns in all these tweets

def main():
	connect()

	tweets = api.search(q="play a game") #search()
	if tweets:
		for t in tweets:
			# choose a reply
			ourreply = random.choice(REPLIES)
			if -1 != ourreply.find("<name>"):
				ourreply.replace("<name>", t.user.screen_name)

			if -1 != ourreply.find("<information>"):
				# WE NEED MORE INFO
				nouns = get_additional_info_from(t.user.screen_name)
				pprint(nouns)
				ournoun = random.choice(nouns)
				ourreply.replace("<information>", ournoun)
				print "My reply: ", ourreply

if __name__ == "__main__":
	print "Press Ctrl-C to stop bot from messing on twitter..."
	try:
		main()
	except KeyboardInterrupt, e:
		pass
