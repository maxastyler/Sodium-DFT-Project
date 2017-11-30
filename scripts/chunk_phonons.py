#!/bin/python3
import sys
args=sys.argv
phonons=[30, 10, 11, 12, 14, 15, 17, 20, 21, 22, 23, 24]
phonons.sort()
target_chunk_size=3

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

grouped_phonons=group_into_ascending(phonons)
sized_phonons=[]
for group in grouped_phonons:
    sized_phonons+=split_up_larger(group, target_chunk_size)
sized_phonons.sort(key=lambda x: len(x))
print(sized_phonons)
