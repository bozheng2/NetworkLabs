#Copyright (c) 2015 Crowd Dynamics Labs
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


import sys
import os
import pyorient

# List of stop words
stop_words = ['beef','pork','lamb','ham','shrimp','creamy','fried','fry','bacon','sausage','seafood','ribs','salami','crab','b.b.q.','bbq','rib','ribs','steak','pepperoni','b.b.q','sausage','wings','pig','turtle','octapus','meatball','chorizo','brisket','squid','calamari','turkey']

# converting to set for faster checking
stop_words = set(stop_words)

def connect():
        '''Function to connect to the database'''
        client = pyorient.OrientDB("localhost", 2424)
        session_id = client.connect( "root", "rootlabs" )
        client.db_open( "NetworkLabs", "admin", "admin")
        return client

def getScore(filename):
	# Constuct the path name
	filename = "backup/" + filename

	# check if the menu exists
	if os.path.isfile(filename):
		#open the menu for reading
        	infile = open(filename,"r")

		# initialize the counts
	        count = 0.0
        	total = 0.0

		# for each menu item check if it is healthy or not
	        for line in infile:
        		total += 1.0

			# flag to set on detecting unhealthy menu item
	            	flag = 0

			# split the menu item using the delimiter '###'
			items = line.rstrip().split('###')
			items = ' '.join(items).split()

		        #print items

			# loop over the menu items and increment count
		        for word in items:
                		if word.lower() in stop_words:
					# not healthy so skip incrementing count by setting flag
			                flag = 1
		                        break
				
				# else update count if flag is not set
		                if flag == 0:
			                count += 1.0
		
		# close the file
        	infile.close()

		# if file empty then score is 0.0
		if total == 0.0:
			score = 0.0
        		print "\nScore for: " + filename + " --> " + str(score) 
			return score
        	score = count
	        print "\nScore for: " + filename + " --> " + str(score) 

		# return the score
		return score

def compute_health_option():
        '''Function to read each menu in the directory, call getScore and update db'''

        # obtain a client
        cl = connect()

        # obtain all the menus
        files = os.listdir("menus/")

        for filename in files:
                # compute the score
                score = getScore(filename)

                # construct the query base
                sql_query = "UPDATE Restaurant SET health_option=%s WHERE res_id LIKE " % (score)+ "\'%" + filename + "%\'"

                # run query and update the db
                cl.command(sql_query)
	

if __name__ == "__main__":
	print "Processing each file"

        compute_health_option()

        print "Finished updating the db"
