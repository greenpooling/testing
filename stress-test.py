#!/usr/bin/env python3

import json
import requests
import time

from random import randint

NUM_USERS = 4

def Stress():
	capacity = 4
	tdepart = "09:00"
	tarrive = "17:00"
	state = 0
	roundtrip = 1

	while 1:
		date = str(randint(1, 2)) + "/09/2015"
		origin = randint(1,3)

		pool = []

		for index in range(0,4):
			if not index == origin:
				pool.append(index)

		destination = pool[randint(1,2)]		

		organiser = randint(1, NUM_USERS)
		payload = {'capacity': capacity, 'origin': origin, 'destination': destination, 'date': date, 'tdepart': tdepart, 'tarrive': tarrive, 'organiser': organiser, 'state': state, 'roundtrip': roundtrip}

		r = requests.post("http://localhost:5000/carpools", data=payload);
		print(r.url)
		print(r.text)

		Accept()
		time.sleep(1)
		Accept()

def Accept():
	for index in range(0, NUM_USERS+1):
		r = requests.get("http://localhost:5000/proposals/" + str(index))
		
		json_data = json.loads(r.text)
		if any(json_data['proposals']):
			print(json_data['proposals'][0])

			proposal = json_data['proposals'][0]
			print(proposal['accepted'] != 1)

			for proposal in json_data['proposals']:
				if proposal['accepted'] != 1:
					payload = {'uid': proposal['uid'], 'cid': proposal['cid'], 'accepted': '1'}
					r = requests.post("http://localhost:5000/proposals", data=payload)

def main():
	Stress()
	while 1:
		Accept()

main()
