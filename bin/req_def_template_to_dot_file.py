#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes a text file as input.
The file should contain the template cards from the technical req document.
It outputs a .dot file for graphviz

"""
import re
import sys

if len(sys.argv) < 3:
    print(("Usage: " + sys.argv[0] + " <input_file.txt> <output_file.dot>"))
    sys.exit()

print("Opening input file")
with open(sys.argv[1], "r") as myfile:
    data = myfile.read()

#Sanity checking input
#Each requiements card should have the same amount of delimiters
print("Beginning sanity checking of input file")
#TODO fix useful error messages. don't judge me I need coffee
tmpcnt = data.count("Requirement ID")
print("Found " + str(tmpcnt) + " requirement cards")
if tmpcnt != data.count("Requirement Description"):
    print("error! Requirement Description")
    sys.exit()
if tmpcnt != data.count("Requirement Priority"):
    print("error! Requirement Priority")
    sys.exit()
if tmpcnt != data.count("depends on"):
    print("error! depends on")
    sys.exit()
if tmpcnt != data.count("specializes"):
    print("error! specializes")
    sys.exit()
if tmpcnt != data.count("specialized by"):
    print("error! specialized by")
    sys.exit()
if tmpcnt != data.count("Input"):
    print("error! Input")
    sys.exit()
if tmpcnt != data.count("Output"):
    print("error! Output")
    sys.exit()
if tmpcnt != data.count("Actors using the requirement"):
    print("error! Actors using the requirement")
    sys.exit()
    
print("Input seems sane")

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
cards = data.split("Requirement ID")
specializes_checklist = {}
specialized_by_checklist = {}

print("Beginning to process the cards")
for card in cards:
    if card.split("Requirement Description")[0].strip() != "":
        card_id = card.split("Requirement Description")[0].strip()
        
        matchObj = re.search(r'Requirement Description\s*((.|\n)*)\nRequirement Priority', card)
        if matchObj:
            card_description = matchObj.group(1).strip()
        else:
            print("Error close to card " + card_id + " (card_depends_on)")
            sys.exit()
            
        matchObj = re.search(r'Requirement Priority\s*\n([0-9]*)\s*\nRequirement Dependencies', card)
        if matchObj:
            card_priority = int(matchObj.group(1).strip())
        else:
            print("Error close to card " + card_id + " (card_priority)")
            sys.exit()
        
        matchObj = re.search(r'depends on\s*((.|\n)*)\nspecializes', card)
        if matchObj:
            card_depends_on = re.split('\s*|\n*', matchObj.group(1).strip())
            card_depends_on = filter(None, card_depends_on)  # removes empty strings
        else:
            print("Error close to card " + card_id + " (card_depends_on)")
            sys.exit()
            
        matchObj = re.search(r'specializes\s*((.|\n)*)\nspecialized by', card)
        if matchObj:
            card_specializes = re.split('\s*|\n*', matchObj.group(1).strip())
            card_specializes = filter(None, card_specializes)
        else:
            print("Error close to card " + card_id + " (card_specializes)")
            sys.exit()
            
        matchObj = re.search(r'specialized by\s*((.|\n)*)\nInput', card)
        if matchObj:
            card_specialized_by = re.split('\s*|\n*', matchObj.group(1).strip())
            card_specialized_by = filter(None, card_specialized_by)
        else:
            print("Error close to card " + card_id + " (card_specialized_by)")
            sys.exit()
            
        matchObj = re.search(r'Input\s*((.|\n)*)\nOutput', card)
        if matchObj:
            card_input = matchObj.group(1).strip()
        else:
            print("Error close to card " + card_id + " (card_input)")
            sys.exit()

        matchObj = re.search(r'Output\s*((.|\n)*)\nActors using the requirement', card)
        if matchObj:
            card_output = matchObj.group(1).strip()
        else:
            print("Error close to card " + card_id + " (card_output)")
            sys.exit()
            
        matchObj = re.search(r'Actors using the requirement\s*\n(.*)', card)
        if matchObj:
            card_actors = matchObj.group(1).strip()
        else:
            print("Error close to card " + card_id + " (card_actors)")
            sys.exit()

        # debugging purposes
        """
        print("card_id: " + card_id
        print("card_priority: " + str(card_priority)
        print("card_depends_on: " + str(card_depends_on)
        print("card_specializes: " + str(card_specializes)
        print("card_specialized_by: " + str(card_specialized_by)
        print("card_input: " + card_input
        print("card_output: " + card_output
        print("card_actors: " + card_actors
        #print("\n" 
        """
        
        if card_id in card_depends_on:
            print("INCONSISTENCY: " + card_id + " is dependent on itself!\n")
        if card_id in card_specializes:
            print("INCONSISTENCY: " + card_id + " specializes itself!\n")
        if card_id in card_specialized_by:
            print("INCONSISTENCY: " + card_id + " is specialized by itself!\n")
            
        #Checking if "specialized" requirements are "specialized by" back, and vice versa
        specializes_checklist[card_id] = card_specializes
        specialized_by_checklist[card_id] = card_specialized_by
        
        for special_kid in card_specializes:
            if special_kid in specialized_by_checklist.keys():
                if card_id not in specialized_by_checklist[special_kid]:
                    print("INCONSISTENCY: Add specialized by " + card_id + " to " + special_kid + " !")
        
        for special_kid in card_specialized_by:
            if special_kid in specializes_checklist.keys():
                if card_id not in specializes_checklist[special_kid]:
                    print("INCONSISTENCY: Add specializes " + card_id + " to " + special_kid + " !")
            
        #TODO put into constants
        #Pick out module from card_id and specify color
        if card_priority == 1:
            node_color = "color = crimson,"
        elif card_priority == 2:
            node_color = "color = darkmagenta,"
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

        node_tooltip = "tooltip=\""+card_description.replace('\n', '').replace('\r', '').replace('"', '')+"\","
        
        #Start adding to "nodes" variable 
        nodes += "\"" + card_id + "\"" + "[style=filled, " + node_color + node_tooltip + "];\n"
        
        #Start adding to "edges" variable
        for perjantai in card_depends_on:
            edges += "\"" + card_id + "\" -> \"" + perjantai + \
                     "\" [color=blue,tooltip=\"" + card_id + " depends on " + perjantai + "\"];\n"
            
        for perjantai in card_specializes:
            edges += "\"" + card_id + "\" -> \"" + perjantai + \
                     "\" [color=green,tooltip=\"" + card_id + " specializes " + perjantai + "\"];\n"
        
        #Actually, we don't want an arrow back.        
        #for perjantai in card_specialized_by:
        #    edges += "\"" + card_id + "\" -> \"" + perjantai + "\" [color=green];\n"

print("Done processing cards")
output += nodes + edges
output += "}\n"

print("Writing output to file")
f_out = open(sys.argv[2], 'w')
f_out.write(output)