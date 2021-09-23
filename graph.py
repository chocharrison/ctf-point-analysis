from urllib.request import Request, urlopen
import matplotlib.pyplot as plt
import json
import math
import numpy as np
import sys, getopt

def steps(start,end,n):
    n = min(end, max(n, 2))
    step = (end-start)/float(n-1)
    return (int(round(start+x*step)) for x in range(n))

#########parameters####################################33
def main(argv):
	year = argv[0]
	ctf = argv[1]
	if(len(argv) == 3):
		team_id = argv[2]
		c = "not"
	if(len(argv) > 3):
		num = int(argv[3])
		c = argv[2]
#######get and display info###############################
	try:
		req = Request('https://ctftime.org/api/v1/results/'+year+'/', headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		j = json.loads(webpage.decode('utf-8'))
	except:
		print("invalid year")
		exit()

	try:
		if(ctf.isnumeric() == False):
			for idc,ct in j.items():
				if(ct['title'] == ctf):
					ctf = idc
	except:
		print("invalid ctf name")
		exit()
	try:
		req = Request('https://ctftime.org/api/v1/events/'+ctf+'/', headers={'User-Agent': 'Mozilla/5.0'})
		scores = j[ctf]['scores']
		webpage = urlopen(req).read()
		jctf = json.loads(webpage.decode('utf-8'))
		print("*************************************************************")
		print("Event name: "+jctf['title'])
		print("Event id: "+str(jctf['id']))
		print("Event organisers: ")
		for category in jctf['organizers']:
    			print ("\t" + category['name'])
		print("Start time: "+jctf['start'].replace("T"," "))
		print("Finish time: "+jctf['finish'].replace("T"," "))
		print("Duration: "+ "\n  days: "+ str(jctf['duration']['days'])+ "\n  hours: "+ str(jctf['duration']['hours']))
		print("Restrictions: "+jctf['restrictions'])
		print("link: "+jctf['url'])
		print("*************************************************************")
	except:
		print("invalid id")
		exit()


#graphing#####################################
	point = []
	pos = []
	team = []
	for i in range(len(scores)):
		point.append(float(scores[i]['points']))
		pos.append(scores[i]['place'])
		team.append(scores[i]['team_id'])
	f1 = plt.figure()
	plt.plot(pos,point)
	plt.xlabel('ranking')
	plt.ylabel('points')
	plt.title(jctf['title'])
##########team info##############################
	check = 0
	try:
		if(c == "pos"):
			num = num - 1
			team_id = str(team[num])
		else:
			num = team.index(int(team_id))
		req = Request('https://ctftime.org/api/v1/teams/'+team_id+'/', headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		jteam = json.loads(webpage.decode('utf-8'))
		print("team name: "+jteam['name'])
		print("team id: "+str(jteam['id']))
		print("ctftime link: "+ 'https://ctftime.org/team/'+team_id+'/')
		print("team points: "+str(point[num]))
		print("team position: "+str(pos[num]) + "/" + str(pos[len(pos)-1]))
		print("point ratio: "+str(point[num]/point[0]*100)+"%")
		print("*************************************************************")
		plt.scatter(pos[num],point[num], c='red')
		check = 1
	except:
		print("invalid team id")
	
	
#############statistics##########################

	meen = sum(point) / len(point) 
	sigma = 0
	for i in range(len(point)):
		sigma = sigma + (point[i] - meen)**2
	sigma = np.sqrt(sigma/len(point))
	print("mean: "+str(meen))
	print("standard deviation: "+ str(sigma))
	#bins = list(steps(meen - 4*sigma,meen + 4 * sigma, 100))
	bins = list(steps(point[len(point)-1],point[0], len(pos)))
	f3 = plt.figure()
	fx = []
	for i in range(len(bins)):
		fx.append(1/(sigma * np.sqrt(2 * np.pi)) * np.exp( -1* (bins[i] - meen)**2 / (2 * sigma**2)))
	plt.plot(bins, fx ,linewidth=3, color='y')
	plt.xlabel('density')
	plt.ylabel('distribution')
	plt.title(jctf['title'] + "distribution")
	if(check == 1):
		plt.axvline(x=point[num])
	plt.tight_layout()
	plt.show()
	plt.close('all')
	
if __name__ == "__main__":
   main(sys.argv[1:])
