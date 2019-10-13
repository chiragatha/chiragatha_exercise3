#!/usr/bin/env python
# coding: utf-8

# In[34]:


import numpy as np
import pandas as pd
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = "C:\Program Files\Git\cmd\git.exe"
import git
from git import RemoteProgress

from git import Repo
import re
from datetime import datetime


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[35]:


class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)


# In[36]:


# NO: 1

import pprint as pprint
remote_link = "https://github.com/apache/activemq"
local_link = "activemq"
fixing_commit = "fed39c3619825bd92990cf1aa7a4e85119e00a6e"
repo = Repo(local_link)


# In[37]:


# TASK 3 #




show_data = repo.git.show("--shortstat", fixing_commit).splitlines()
commit = repo.commit(fixing_commit)
stats = commit.stats

files = stats.files
directoryList = []
for file in files:   
    print("Name of file: "+file)
    print("Insertions: "+str(files[file]['insertions']))
    print("Deletions: "+str(files[file]['deletions']))
    print("Total: "+str(files[file]['lines']))

diff_data = repo.git.diff("-U0",fixing_commit + "^", fixing_commit).splitlines()

fileName = ""
for line in diff_data:
    
    if(line[0:10] == 'diff --git'):
        fileName = line[13:line.find(' b')]

    if(line[0:3] == '@@ '):

        start = ' +'
        parentScopeStart = ' @@ '
        end = ' @@'
        s = line
       
        plen = 0 if(len(parentScopeStart)==-1) else len(parentScopeStart)
        parentScope = (s[s.find(parentScopeStart)+plen:])
      
        affectedLines = (s[s.find(start)+len(start):s.rfind(end)]).split(',')
        
        print("File Name: "+fileName)
        if("Project" == str(parentScope[:parentScope.find(': ')])):
            print("No enclosing scope for this line.")
        else:
            print("The smallest enclosing Scope: "+str(parentScope[:parentScope.find(': ')]))
        if(len(affectedLines)>1):
            print("Affected Lines: "+"Line number " + affectedLines[0] + " to "+ str((int(affectedLines[0])+int(affectedLines[1]))))
        else:
            print("Affected Lines: "+"Line number " + affectedLines[0])
        alines='1'
        lines =''
        if(len(affectedLines)>1):
            alines=affectedLines[1]
            if(affectedLines[1]=='0'):
                alines='1'
            lines = "-L "+affectedLines[0]+",+"+alines
        else:
            lines = "-L "+affectedLines[0]
        
        blameResult = repo.git.blame(lines, fixing_commit, "--", fileName).splitlines()
        commits = []
        for l in blameResult:
            commits.append(l[0:8])
      
        latestCommit = commits[len(commits)-1];
     
        unique, counts = np.unique(commits, return_counts=True)
        d = dict(zip(unique, counts))
        mostFrequent = max(d, key=d.get)
        print("Latest identified commit : "+latestCommit)
        print("Most frequently identified commit : "+mostFrequent)
  


# In[38]:


# a) message and title of the fixing commit




import pprint as pprint
remote_link = "https://github.com/apache/activemq"
local_link = "activemq"
fixing_commit = "fed39c3619825bd92990cf1aa7a4e85119e00a6e"


show_data = repo.git.show("--shortstat", fixing_commit).splitlines()
commit = repo.commit(fixing_commit)
print("Commit Title:"+'\x1b[0m'+show_data[4])
print("Commit Message:")
for index in range(len(show_data)):
    if index>5 and index<19:
        print(show_data[index])


# In[39]:


# b)affected files


stats = commit.stats

print("Affected Files:"+ str(stats.total["files"]))


# In[40]:


# c)How many total directories were affected in the fixing commit?

totalDirAffected = repo.git.show("--dirstat", fixing_commit).splitlines()
affectedDir = []
for info in totalDirAffected:
    if "% " in info:
        affectedDir.append(info[info.find("% ")+2:])
print(len(affectedDir),"Directories affected: ")
for pline in affectedDir:
    print(pline)


# In[41]:


# d)How many total lines of code(including comments and blank lines) were deleted?

total_line_deleted = repo.git.show("--shortstat",fixing_commit).splitlines()
total_line_deleted.reverse()
total_line_deleted = total_line_deleted[0].split(',')
print("total number of lines of codes detected(including blank spaces)"+total_line_deleted[2])


# In[42]:


#e) How many total lines of code(including comments and blank lines) were added?

total_line_added = repo.git.show("--shortstat",fixing_commit).splitlines()
total_line_added.reverse()
total_line_added = total_line_added[0].split(',')
print("total number of lines of codes deleted(including blank spaces):"+total_line_added[1])


# In[43]:


# f) How many total lines of code(excluding comments and blank lines) were deleted?

show_del_line = repo.git.show("-U0","--pretty=""",fixing_commit).splitlines()
tot_del = 0;
for line in show_del_line:
    if re.search("^\-",line):
        l=line.split(" ")
        if(len(l) > 1):
            if(len(l[0]) == 1):
                if(l[1][:1] != '*' or l[1][:1] != '/'):
                    tot_del += 1
                    
                    print ("total lines deleted(excluding comments and blank lines)="+str(tot_del))


# In[44]:


# g) How many total lines of code(excluding comments and blank lines) were added?

show_del_line = repo.git.show("-U0","--pretty=""",fixing_commit).splitlines()
tot_del = 0;
for line in show_del_line:
    if re.search("^\-",line):
        l=line.split(" ")
        if(len(l) > 1):
            if(len(l[0]) == 1):
                if(l[1][:1] != '*' or l[1][:1] != '/'):
                    tot_del += 1
                    
                    print ("total lines added(excluding comments and blank lines)="+str(tot_del))


# In[45]:


# h) How many days were between the current fixing commit and the previous commit of each affected file?

from datetime import datetime
from datetime import date

for file in stats.files:   
    print("File: "+file)
    log_data = repo.git.log(fixing_commit,file).splitlines()
    commitID = 0
    date1 = datetime.now()
    date2 = datetime.now()
    for line in log_data:
        if(line[0:8] == "Date:   "):
            commitID=commitID+1
            if(commitID ==1):
                date1 = datetime.strptime(line[8:31], '%a %b %d %H:%M:%S %Y')
                print("Current Commit Time: "+str(date1))
                continue
            if(commitID ==2):
                date2 = datetime.strptime(line[8:31], '%a %b %d %H:%M:%S %Y')
                print("Previous Commit Time: "+str(date2))
                break
    if(commitID == 1):
        print("This file only has one commit.")
        print("----------------------")
    else:
        print("Time Difference: "+str(date1-date2))
        print("----------------------")


# In[46]:


# i) How many time has each affected file of the current fixing commit been modified in the past since their creation?

for file in stats.files:   
    print("File: "+file)
    log_data = repo.git.log(fixing_commit,"--pretty=\"format:%H%M%S\"", "--",file).splitlines()
    print("Times of modification(including renaming): "+str(len(log_data)))
    


# In[47]:


# j) Which developers have modified each affected file since its creation?

for file in stats.files:   
    print("File: "+file) 
    log_data = repo.git.log(fixing_commit,"--pretty=format:%an", "--follow", "--",file).splitlines()
    x = np.array(log_data) 
    uniqueNames = np.unique(x)
    print("Contributors: ")
    for name in uniqueNames:
        print(name) 
    print()


# In[48]:


# k) For each developer identified, how many commits have each of them submitted? From your observation, are the involving developers experienced or new ones or both?

all_developers = repo.git.shortlog("-sne", "--all").splitlines()

author_commits = []
identifiedDev = []
for file in stats.files:   
    #print("File: "+file) 
    log_data = repo.git.log(fixing_commit,"--pretty=format:%an", "--follow", "--",file).splitlines()
    x = np.array(log_data) 
    uniqueNames = np.unique(x)
    #print("Contributors: ")
    for name in uniqueNames:
        identifiedDev.append(name) 
dev = list(set(identifiedDev))
print("commitTimes"+"\t\t"+"author")
for developer in all_developers:
    #print(developer)
    commitTimes, author = developer.split("\t")
    for tem in dev:
        if tem in author:
            print(commitTimes+"\t\t"+author)


# In[49]:


lines = "-L"+affectedLines[0]+",+"+affectedLines[1]

blameResult = repo.git.blame(lines, fixing_commit, "--", fileName).splitlines()
commits = []
for l in blameResult:
    commits.append(l[0:8])
unique, counts = np.unique(commits, return_counts=True)
d = dict(zip(unique, counts))
mostFrequent = max(d, key=d.get)
print("Most frequent commit no parameter : "+'\t'+mostFrequent)
#-w

blameResult = repo.git.blame(lines, fixing_commit, "-w", "--", fileName).splitlines()
commits = []
for l in blameResult:
    commits.append(l[0:8])
unique, counts = np.unique(commits, return_counts=True)
d = dict(zip(unique, counts))
mostFrequent = max(d, key=d.get)
print("Most frequent commit with -w : "+'\t'+mostFrequent)
#-wM
blameResult = repo.git.blame(lines, fixing_commit, "-wM", "--", fileName).splitlines()
commits = []
for l in blameResult:
    commits.append(l[0:8])
unique, counts = np.unique(commits, return_counts=True)
d = dict(zip(unique, counts))
mostFrequent = max(d, key=d.get)
print("Most frequent commit with -wM : "+'\t'+mostFrequent)
#-wC
blameResult = repo.git.blame(lines, fixing_commit, "-wC", "--", fileName).splitlines()
commits = []
for l in blameResult:
    commits.append(l[0:8])
unique, counts = np.unique(commits, return_counts=True)
d = dict(zip(unique, counts))
mostFrequent = max(d, key=d.get)
print("Most frequent commit with -wC : "+'\t'+mostFrequent)
#-wCC
blameResult = repo.git.blame(lines, fixing_commit, "-wCC", "--", fileName).splitlines()
commits = []
for l in blameResult:
    commits.append(l[0:8])
unique, counts = np.unique(commits, return_counts=True)
d = dict(zip(unique, counts))
mostFrequent = max(d, key=d.get)
print("Most frequent commit with -wCC : "+'\t'+mostFrequent)
#-wCCC
blameResult = repo.git.blame(lines, fixing_commit, "-wCCC", "--", fileName).splitlines()
commits = []
for l in blameResult:
    commits.append(l[0:8])
unique, counts = np.unique(commits, return_counts=True)
d = dict(zip(unique, counts))
mostFrequent = max(d, key=d.get)
print("Most frequent commit with -wCCC : "+'\t'+mostFrequent)


# In[ ]:




