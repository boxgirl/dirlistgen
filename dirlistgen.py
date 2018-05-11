#!/usr/bin/env python3
import datrie
import re
import os
import click

pattern=re.compile(r'/')
roots=set()

@click.command()
@click.option('--add', '-a', help='Folder to add', multiple=True)
@click.option('--delete', '-d', help='Folder to delete', multiple=True)
@click.option('--root', '-r', help='Start folder')
@click.option('--file', '-f', help='File with folders and operations')
def processing(add, delete,root,file):
    global rootpath
    a = list()
    d = list()
    if file:
        with open(file, 'r',encoding='utf-8') as data:
            for line in data:
                line=line.replace('\n','')
                if line[0] == 'r':
                    rootpath = line[2:]
                if line[0] == '+':
                    a.append(line[2:])
                if line[0] == '-':
                    d.append(line[2:])
    else:
        rootpath=root
        a=list(add)
        d=list(delete)
    dive_into_folder(rootpath, pattern, None)
    pre_processing(a,d)
    print_res(rootpath)

def pre_processing(a,d):
    for folder in a:
        roots.add(folder)
        addition(folder)
    for folder in d:
        if trie[folder].state_of_add != False:
            prep_for_deleting(folder)
            key_for_node = re.split(pattern, folder)[-1].__len__()
            deleting(rootpath, folder[:-1 - key_for_node])
        else:
            raise NotInListOfFoldersToProcessing('no such folder{}'.format(folder))

state_of_addition = [None]

class Pain:
    def __init__(self, st=False):
        self.list_child = list()
        self.child_del = st

    def __getattr__(self, attr):
        if attr == 'state_of_add':
            return state_of_addition[0]
        raise AttributeError

def dive_into_folder(foldpath, pattern, isnew):
    pain = Pain()
    if os.path.isdir(foldpath) and 0 != os.listdir(foldpath).__len__():
        for nextfold in filter(lambda x: os.path.isdir(os.path.join(foldpath, x)), os.listdir(foldpath)):
            dive_into_folder(os.path.join(foldpath, nextfold), pattern, isnew)
            trie[foldpath] = pain
            pain.list_child.append(os.path.join(foldpath, nextfold))
            if isnew:
                    pain.state_of_add = True
    elif isnew:
        trie[foldpath].state_of_add = True
    else:
        trie[foldpath] = pain

class NotInListOfFoldersToProcessing(ValueError): pass

def prep_for_deleting(foldpath):
    '''For children state_of_add to false'''
    temp = trie[foldpath]
    temp.state_of_add = False
    for child in temp.list_child:
        trie[child].state_of_add = False
        if trie[child].list_child.__len__() != 0:
            prep_for_deleting(child)
    temp.child_del = True


def deleting(root, foldpath):
    '''Change state of parents of '-' node'''
    if(len(foldpath)>=len(root)):
        if trie[foldpath].state_of_add !=False:
            trie[foldpath].child_del = True
            key_for_node = re.split(pattern, foldpath)[-1].__len__()
            foldpath = foldpath[:-1 - key_for_node]
            if foldpath != root:
                deleting(root, foldpath)
            if foldpath == root and trie[foldpath].state_of_add != False:
                trie[foldpath].child_del = True


def addition(fpath):
    '''Add node and change children's state_of_add to False and parent's state_child to True'''
    #add child of '+' root to True
    change_child_of_folder_to_true(fpath)
    trie[fpath].state_of_add=True
    # add other child of parent to False
    key_for_node = re.split(pattern, fpath)[-1].__len__()
    foldpath = fpath[:-1 - key_for_node]
    #for other child in the same lvl which are None
    for child in filter(lambda x: trie[x].state_of_add is None,trie[foldpath].list_child):
        prep_for_deleting(child)
        key_for_node = re.split(pattern, child)[-1].__len__()
        if child[:-1 - key_for_node]!=rootpath:
            deleting(rootpath, child[:-1 - key_for_node])
    trie[fpath].state_of_add=True

def change_child_of_folder_to_true(fpath):
    for child in trie[fpath].list_child:
        trie[child].state_of_add=None
        if len(trie[child].list_child)!=0:
            change_child_of_folder_to_true(child)

res_nodes = set()
def detection_of_nodes_in_add_list(r):
    for child in trie[r].list_child:
        if trie[child].state_of_add==True:
            trie[child].state_of_add=None
        if len(trie[child].list_child)!=0:
            detection_of_nodes_in_add_list(child)

def detection_of_nodes_in_lowest_lvl(fpath):
    '''Search nodes in the lowest lvl without child_del'''
    temp=list(filter(lambda x: trie[x].state_of_add is None, trie[fpath].list_child))
    #if  all child-nodes are None and don't have del_child and len!=0
    if len(temp)==len(trie[fpath].list_child) and len(trie[fpath].list_child)!=0:
        if len(list(filter(lambda x: trie[x].child_del is False, trie[fpath].list_child)))==len(trie[fpath].list_child):
             res_nodes.add(fpath)
        else:
            ##which  have del_child
            for child in trie[fpath].list_child:
                if  trie[child].child_del==False:
                    res_nodes.add(child)
                else:
                    detection_of_nodes_in_lowest_lvl(child)
    else:
        for child in trie[fpath].list_child:
            if trie[child].state_of_add==None and trie[child].child_del==False:
                res_nodes.add(child)
            if trie[child].child_del==True:
                detection_of_nodes_in_lowest_lvl(child)

def print_res(fpath):
    res_nodes.clear()
    detection_of_nodes_in_add_list(fpath)
    detection_of_nodes_in_lowest_lvl(fpath)
    for r in roots:
        trie[r].state_of_add=True
    for r_n in res_nodes:
        print(r_n)

if __name__ == '__main__':
    trie = datrie.Trie(ranges=[(u'\x00', u'\xff')])
    processing()
