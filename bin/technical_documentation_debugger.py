#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script takes a text file as input.
The file should contain the functional requirements template cards from the technical documentation.

This script also takes an optional input file with the visual requirements from the technical documentation.
It checks which functional requirements aren't fulfilled by the visual definitions 

If a output file is specified, it will also output a .dot file for graphviz.
"""

import re
import sys
import argparse

def dprint(message,level):
	if args.verbose>=level:
		print message
		
parser = argparse.ArgumentParser(description='Debugger and visualizer for the StudAssWeb Technical document')
parser.add_argument('--verbose', '-v', action='count', default=0)
parser.add_argument('--inputfunc','-if', metavar="functional_requirements.txt",type=argparse.FileType('r'),required=True, help="Text file with functional requirement cards")
parser.add_argument('--inputvisual','-iv', metavar="visual_requirements.txt",type=argparse.FileType('r'), help="Text file with visual requirements")
parser.add_argument('--output','-o', metavar="output_file.dot",type=argparse.FileType('w'), help="Output file for the graphviz .dot layout")
args = parser.parse_args()


dprint("Opening functional requirements input file",1)	
funcdata=args.inputfunc.read()	

#Each requiements card should have the same amount of delimiters
dprint("Beginning sanity checking of functional requirements input file",1)
tmpcnt = funcdata.count("Requirement ID")
dprint("Found " + str(tmpcnt) + " requirement cards",1)
tmpstr = "Requirement Description"
if tmpcnt != funcdata.count(tmpstr):
	print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
	sys.exit(1)
tmpstr = "Requirement Priority"
if tmpcnt != funcdata.count(tmpstr):
	print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
	sys.exit(1)
tmpstr = "depends on"
if tmpcnt != funcdata.count(tmpstr):
	print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
	sys.exit(1)
tmpstr = "specializes"
if tmpcnt != funcdata.count(tmpstr):
	print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
	sys.exit(1)
tmpstr = "specialized by"
if tmpcnt != funcdata.count(tmpstr):
	print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
	sys.exit(1)
tmpstr = "Input"
if tmpcnt != funcdata.count(tmpstr):
	print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
	sys.exit(1)
tmpstr = "Output"
if tmpcnt != funcdata.count(tmpstr):
	print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
	sys.exit(1)
tmpstr = "Actors using the requirement"
if tmpcnt != funcdata.count(tmpstr):
	print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
	sys.exit(1)
dprint("Functional requirements input seems sane",1)

if args.inputvisual!=None:
	dprint("Opening visual requirements input file",1)	
	visdata=args.inputvisual.read()
		
	dprint("Beginning sanity checking of visual requirements input file",1)
	tmpcnt = visdata.count("Id")
	dprint("Found " + str(tmpcnt) + " visual definitions/pages",1)
	tmpstr = "Description"
	if tmpcnt != visdata.count(tmpstr):
		print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
		sys.exit(1)
	tmpstr = "Fulfills requirements"
	if tmpcnt != visdata.count(tmpstr):
		print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
		sys.exit(1)	
	tmpstr = "URL"
	if tmpcnt != visdata.count(tmpstr):
		print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
		sys.exit(1)	
	tmpstr = "Views"
	if tmpcnt != visdata.count(tmpstr):
		print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
		sys.exit(1)	
	tmpstr = "Parameters"
	if tmpcnt != visdata.count(tmpstr):
		print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
		sys.exit(1)	
	tmpstr = "Forms"
	if tmpcnt != visdata.count(tmpstr):
		print "Error! Found "+str(funcdata.count(tmpstr))+" of string \""+tmpstr+"\""
		sys.exit(1)		
	dprint("Visual requirements input seems sane",1)

	
#Set up header
output = ""
nodes = ""
edges = ""

output = "digraph techdef {\n"
#Preserves the overall geometric relationships in the layout, can require high scale factors
#output += "overlap=scale\n"
#Magic bounded Voronoi diagram voodoo
output += "overlap=false\n"
#no overlapping edges (EXPENSIVE!)
output += "splines=true\n"
#"weight" makes more distance between nodes, penwidth creates wider edges 
output += "edge[weight=0.5,penwidth=1.5]" 

#Splitting input into different cards
cards = funcdata.split("Requirement ID")
functional_requirements = []
specializes_checklist = {}
specialized_by_checklist = {}

dprint("Beginning to process the functional requirement cards",1)
for card in cards:
	if card.split("Requirement Description")[0].strip() != "":
		card_id = card.split("Requirement Description")[0].strip()
		functional_requirements.append(card_id);
		
		matchObj = re.search( r'Requirement Description\s*((.|\n)*)\nRequirement Priority', card)
		if matchObj:
			card_description = matchObj.group(1).strip()
		else:
			print "Error close to card " + card_id + " (card_depends_on)"
			sys.exit(1)
			
		matchObj = re.search( r'Requirement Priority\s*\n([0-9]*)\s*\nRequirement Dependencies', card)
		if matchObj:
			card_priority = int(matchObj.group(1).strip())
		else:
			print "Error close to card " + card_id + " (card_priority)"
			sys.exit(1)
		
		matchObj = re.search( r'depends on\s*((.|\n)*)\nspecializes', card)
		if matchObj:
			card_depends_on = re.split('\s*|\n*',matchObj.group(1).strip())
			card_depends_on = map(str.strip, card_depends_on)
			card_depends_on = filter(None, card_depends_on)#removes empty strings
		else:
			print "Error close to card " + card_id + " (card_depends_on)"
			sys.exit(1)
			
		matchObj = re.search( r'specializes\s*((.|\n)*)\nspecialized by', card)
		if matchObj:
			card_specializes = re.split('\s*|\n*',matchObj.group(1).strip())
			card_specializes = map(str.strip, card_specializes)
			card_specializes = filter(None, card_specializes)
		else:
			print "Error close to card " + card_id + " (card_specializes)"
			sys.exit(1)
			
		matchObj = re.search( r'specialized by\s*((.|\n)*)\nInput', card)
		if matchObj:
			card_specialized_by = re.split('\s*|\n*',matchObj.group(1).strip())
			card_specialized_by = map(str.strip, card_specialized_by)
			card_specialized_by = filter(None, card_specialized_by)
		else:
			print "Error close to card " + card_id + " (card_specialized_by)"
			sys.exit(1)
			
		matchObj = re.search( r'Input\s*((.|\n)*)\nOutput', card)
		if matchObj:
			card_input = matchObj.group(1).strip()
		else:
			print "Error close to card " + card_id + " (card_input)"
			sys.exit(1)

		matchObj = re.search( r'Output\s*((.|\n)*)\nActors using the requirement', card)
		if matchObj:
			card_output = matchObj.group(1).strip()
		else:
			print "Error close to card " + card_id + " (card_output)"
			sys.exit(1)
			
		matchObj = re.search( r'Actors using the requirement\s*\n(.*)', card)
		if matchObj:
			card_actors = matchObj.group(1).strip()
		else:
			print "Error close to card " + card_id + " (card_actors)"
			sys.exit(1)
		
		
		#debugging purposes
		dprint("card_id: " + card_id,2)
		dprint("card_priority: " + str(card_priority),2)
		dprint("card_depends_on: " + str(card_depends_on),2)
		dprint("card_specializes: " + str(card_specializes),2)
		dprint("card_specialized_by: " + str(card_specialized_by),2)
		dprint("card_input: " + card_input,2)
		dprint("card_output: " + card_output,2)
		dprint("card_actors: " + card_actors,2)
		dprint("\n",2)

		
		if card_id in card_depends_on:
			print "INCONSISTENCY: " + card_id + " is dependent on itself!\n"
		if card_id in card_specializes:
			print "INCONSISTENCY: " + card_id + " specializes itself!\n"
		if card_id in card_specialized_by:
			print "INCONSISTENCY: " + card_id + " is specialized by itself!\n"
			
		#Checking if "specialized" requirements are "specialized by" back, and vice versa
		specializes_checklist[card_id] = card_specializes
		specialized_by_checklist[card_id] = card_specialized_by
		
		for special_kid in card_specializes:
			if special_kid in specialized_by_checklist.keys():
				if card_id not in specialized_by_checklist[special_kid]:
					print "INCONSISTENCY: Add specialized by " + card_id + " to " + special_kid + " !"
		
		for special_kid in card_specialized_by:
			if special_kid in specializes_checklist.keys():
				if card_id not in specializes_checklist[special_kid]:
					print "INCONSISTENCY: Add specializes " + card_id + " to " + special_kid + " !"
			
		#TODO put into constants
		#Pick out module from card_id and specify color
		if card_priority == 1:
			node_color = "color = crimson,"
		elif card_priority == 2:
			node_color = "color = purple,"
		elif card_priority == 3:
			node_color = "color = dodgerblue,"
		elif card_priority == 4:
			node_color = "color = gold,"
		elif card_priority == 5:
			node_color = "color = khaki,"
		elif card_priority > 5:
			node_color = "color = white,"
		else:
			node_color = "color = black,"

		node_tooltip = "tooltip=\""+card_description.replace('\n', '').replace('\r', '').replace('"','')+"\","
		
		#Start adding to "nodes" variable 
		nodes += "\"" + card_id + "\"" + "[style=filled, " + node_color + node_tooltip +"];\n"
		
		#Start adding to "edges" variable
		for perjantai in card_depends_on:
			edges += "\"" + card_id + "\" -> \"" + perjantai + "\" [color=blue,tooltip=\"" + card_id + " depends on " + perjantai + "\"];\n"
			
		for perjantai in card_specializes:
			edges += "\"" + card_id + "\" -> \"" + perjantai + "\" [color=green,tooltip=\"" + card_id + " specializes " + perjantai + "\"];\n"
		
		#Actually, we don't want an arrow back.		
		#for perjantai in card_specialized_by:
		#	edges += "\"" + card_id + "\" -> \"" + perjantai + "\" [color=green];\n"

dprint("Done processing cards",1)

if args.inputvisual!=None:
	fulfilled_functional_requirements = []
	dprint("Beginning to process the visual requirements",1)
	cards = visdata.split("Id")
	for card in cards:
		#matchObj = re.search( r'([A-Z]+-[A-Z0-9]+-[A-Z0-9]+)', card)
		#if matchObj:
		#	card_id = matchObj.group(1).strip()
			
		if "Fulfills requirements" in card and card.split("Description")[0].strip() != "":
			card_id = card.split("Description")[0].strip()	
			
			matchObj = re.search( r'Fulfills requirements\s*((.|\n)*)\nURL', card)
			if matchObj:
				card_fulfills = matchObj.group(1).strip().split(',')
				card_fulfills = map(str.strip, card_fulfills)
				card_fulfills = filter(None, card_fulfills)#removes empty strings
			else:
				print "Error close to card " + card_id + " (card_fulfills)"
				sys.exit(1)
		
			#debugging purposes
			dprint("card_id: " + card_id,2)
			dprint("card_fulfills: " + str(card_fulfills),2)
			dprint("\n",2)
			
			#remove all the card_fulfills from functional_requirements
			#put them into another list
			for requirement in card_fulfills:
				if requirement not in fulfilled_functional_requirements:
					if requirement in functional_requirements:
						functional_requirements.remove(requirement)
						fulfilled_functional_requirements.append(requirement)
					else:
						print "Visual requirement " + card_id + " refers to functional requirement " + requirement + " which does not exist!" 
			
			
		else:
			dprint("-------------------------------",2)
			dprint("skipped card!",2)
			dprint(card,2)
			dprint("-------------------------------",2)
			
		

	print "The following functional requirements are not fulfilled by a visual requirement: " + str(functional_requirements)

output += nodes + edges
output += "}\n"

if args.output!=None:
	dprint("Writing output to file",1)
	args.output.write(output)
else:
	dprint("No output file specified, skipping writing",1)