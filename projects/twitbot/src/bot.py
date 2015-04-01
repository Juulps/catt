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
	twts = api.search(q="play a game")
	pprint(twts[0])
	print "*"*80
	print twts[0].text
	#for t in twts:
	 	#pprint( t.text )
	 	#print "---------------------------------"

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
		#api.update_with_media(filename="images/mypic.jpg", status=line)
		print line
		#time.sleep(3600) # Sleep for 1 hour

def load_my_answers():
	global ANSWERS
	f=open('conversation.txt','r')
	ANSWERS=f.readlines()
	f.close()
	#print ANSWERS

def get_answer():
	return random.choice(ANSWERS)

def main():
	connect()
	#while 1:
	#	search()
	#mentions()
	# this is a comment
	#tweetforever()
	#api.update.status("I will start doing something now")
	load_my_answers()

	while 1:
		try:
			twts = api.search(q="play a game")
			if twts:
				#print "We have been mentioned! "
				for t in twts:
					# print "*"*80
					# print m.text
					# print "^"*80
					# print m.author.name
					# print "%"*80
					# print m.author.screen_name
					# print "@"*80
					# print "answer: ", get_answer()
					# print "@"*80

					answer = "@{0} {1}".format(t.author.screen_name, get_answer())
					answer.replace("<name>", t.author.name)
					api.update_status(status=(answer)) #, m.id)
					# TODO:
					# use tweepy to reply to a mention using get_answer()
			else:
				print "we haven't been mentioned  :("
		except Exception, e:
			continue

		time.sleep(1)

if __name__ == "__main__":
	print "Press Ctrl-C to stop bot from messing on twitter..."
	try:
		main()
	except KeyboardInterrupt, e:
		pass
