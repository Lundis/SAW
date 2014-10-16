#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script takes a text file as input.
The file should contain the template cards from the technical req document.
It outputs a .dot file for graphviz

"""
import re
import sys

#Read data from file
#TODO input & output filenames from arguments
with open ("example_data_input.txt", "r") as myfile:
	data=myfile.read()

#Sanity checking input
#Each requiements card should have the same amount of delimiters
#TODO fix useful error messages. don't judge me I need coffee
tmpcnt = data.count("Requirement ID")
if tmpcnt != data.count("Requirement Description"):
	print "error! Requirement Description"
	sys.exit()
if tmpcnt != data.count("Requirement Priority"):
	print "error! Requirement Priority"
	sys.exit()
if tmpcnt != data.count("depends on"):
	print "error! depends on"
	sys.exit()
if tmpcnt != data.count("specializes"):
	print "error! specializes"
	sys.exit()
if tmpcnt != data.count("specialized by"):
	print "error! specialized by"
	sys.exit()
if tmpcnt != data.count("Input"):
	print "error! Input"
	sys.exit()
if tmpcnt != data.count("Output"):
	print "error! Output"
	sys.exit()
if tmpcnt != data.count("Actors using the requirement"):
	print "error! Actors using the requirement"
	sys.exit()
	
#Input seems sane

#Set up header
output = ""
nodes = ""
edges = ""

output = "digraph techdef {\n"
#Splitting input into different cards
cards = data.split("Requirement ID")

#TODO fix the ugly regular expressions
#TODO check with multiple lines in the result we want, e.g. multiple depends_on
for card in cards:
	if card.split("Requirement Description")[0].strip() != "":
		#print card.split("Requirement Description")[0].strip() 
		card_id = card.split("Requirement Description")[0].strip()
		
		matchObj = re.search( r'Requirement Priority(\s*)\n([0-9]*)(\s*)\nRequirement Dependencies', card)
		if matchObj:
			card_priority = matchObj.group(2)
		else:
			print "Error close to card " + card_id + " (card_priority)"
			sys.exit()
		
		
		matchObj = re.search( r'depends on(\s)*(.*)\nspecializes', card)
		if matchObj:
			card_depends_on = matchObj.group(2).strip()
		else:
			print "Error close to card " + card_id + " (card_depends_on)"
			sys.exit()
			
		matchObj = re.search( r'specializes(\s)*(.*)\nspecialized by', card)
		if matchObj:
			card_specializes = matchObj.group(2).strip()
		else:
			print "Error close to card " + card_id + " (card_specializes)"
			sys.exit()
			
		matchObj = re.search( r'specialized by(\s)*(.*)\nInput', card)
		if matchObj:
			card_specialized_by = matchObj.group(2).strip()
		else:
			print "Error close to card " + card_id + " (card_specialized_by)"
			sys.exit()
			
		matchObj = re.search( r'Input\s*\n(.*)\nOutput', card)
		if matchObj:
			card_input = matchObj.group(1).strip()
		else:
			print "Error close to card " + card_id + " (card_input)"
			sys.exit()

		matchObj = re.search( r'Output\s*\n(.*)\nActors using the requirement', card)
		if matchObj:
			card_output = matchObj.group(1).strip()
		else:
			print "Error close to card " + card_id + " (card_output)"
			sys.exit()
			
		matchObj = re.search( r'Actors using the requirement\s*\n(.*)', card)
		if matchObj:
			card_actors = matchObj.group(1).strip()
		else:
			print "Error close to card " + card_id + " (card_actors)"
			sys.exit()
		
		
		#debugging purposes
		print "card_id: " + card_id
		print "card_priority: " + card_priority
		print "card_depends_on: " + card_depends_on
		print "card_specializes: " + card_specializes
		print "card_specialized_by: " + card_specialized_by
		print "card_input: " + card_input
		print "card_output: " + card_output
		print "card_actors: " + card_actors
		print "\n" 
	
		
		
		#TODO Start adding to "nodes" variable 
		
		#nodes += "\"" + card_id + "\""
		
		#TODO Start adding to "edges" variable
		

#TODO Add "nodes" and "edges" to "output"

output += "}\n"
#TODO Write output to file