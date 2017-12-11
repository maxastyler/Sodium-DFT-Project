#!/bin/python3
#Sorts out a list of phonons and a list of computers and pairs them, then outputs to stdin 
#! compname
# min_ph1 max_ph1 min_ph2 max_ph2 min_ph3 max_ph3...
#Pipe in a list of computers to run on, put phonons as arguments
import sys
phonons=[int(i) for i in sys.argv[1:]]
stdinput=sys.stdin.readlines()
comps=[int(i) for i in stdinput]
phonons.sort()
target_chunk_size=len(phonons)//len(comps)

def group_into_ascending(l):
    l.sort() 
    if len(l)==0:
        return []
    if len(l)==1:
        return [[l[0]]]
    grouped=[[]]
    for i in range(len(l)):
        if i==0:
            grouped[-1].append(l[i])
        else:
            if l[i]-l[i-1]!=1:
                grouped.append([])
            grouped[-1].append(l[i])
    return grouped

def split_up_larger(l, chunk_size):
    if len(l)<=chunk_size:
        return [l]
    grouped=[]
    splits=[i*chunk_size for i in range(len(l)//chunk_size)]
    remainder=len(l)%chunk_size
    if remainder!=0:
        splits.append(splits[-1]+chunk_size)
    for i in splits:
        grouped.append(l[i:i+chunk_size])
    return grouped

def find_min_comp(computers):
    min_comp=(None, float('inf'))
    for key in computers:
        phon_size=sum([len(l) for l in computers[key]])
        if phon_size<min_comp[1]:
            min_comp=(key, phon_size)
    return min_comp[0]

def pretty_print_comp_phonon_pairings(comp_phon):
    for key in comp_phon:   
        print("! {key:03g}".format(key=key))
        for phonons in comp_phon[key]:
            print("{p1} {p2}".format(p1=phonons[0], p2=phonons[-1]), end=" ")

grouped_phonons=group_into_ascending(phonons)
sized_phonons=[]
for group in grouped_phonons:
    sized_phonons+=split_up_larger(group, target_chunk_size)
sized_phonons.sort(key=lambda x: len(x))
sized_phonons.reverse()
computer_phonon_pairings={}
for comp in comps:
    computer_phonon_pairings[comp]=[]
for item in sized_phonons:
    comp_to_add=find_min_comp(computer_phonon_pairings)
    computer_phonon_pairings[comp_to_add].append(item)
pretty_print_comp_phonon_pairings(computer_phonon_pairings)
