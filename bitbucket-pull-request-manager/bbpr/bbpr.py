#!/usr/bin/env python3
import os
import requests
import datetime
import git
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\u001b[36m'
    OKGREEN = '\033[92m'
    WARNING = '\u001b[31;1m'
    YELLOW = '\u001b[33;1m'
    ENDC = '\033[0m'

def print_remote(remote):
    print(bcolors.HEADER + '\tREMOTE' + bcolors.ENDC)
    print('\t\t'+remote+'\n')

def print_branch(branch):
    print(bcolors.HEADER + '\tBRANCH' + bcolors.ENDC)
    print('\t\t'+branch+'\n')

def print_approvals(activities):
    approvals = [act for act in activities if act['action']=='APPROVED']
    print(bcolors.OKGREEN + '\tAPPROVALS' + bcolors.ENDC)
    for approval in approvals:
        print('\t\tUser: ' + approval['user']['displayName'])
        print('\t\tTime: ' + str(datetime.datetime.fromtimestamp(approval['createdDate']/1000.0))+'\n')
    print('\n')   

def print_reviews(activities):
    reviews = [act for act in activities if act['action']=='REVIEWED']
    print(bcolors.WARNING + '\tNEEDS WORK' + bcolors.ENDC)
    for review in reviews:
        print('\t\tUser: ' + review['user']['displayName'])
        print('\t\tTime: ' + str(datetime.datetime.fromtimestamp(review['createdDate']/1000.0))+'\n')
    print('\n')        

def pull_request_for_branch(auth, base_url, branch):
    pullReqsUrl = base_url + '?state=open'
    pull_requests = requests.get(pullReqsUrl, auth=auth).json()['values']
    filt = [pr for pr in pull_requests if(pr['fromRef']['displayId'] == branch)]
    if len(filt) == 0:
        print('No open pull requests for branch '+ branch)
        sys.exit()
    return filt[0]    

def get_all_activities(auth, base_url, id):
    activitiesUrl = base_url + id + '/activities'
    return requests.get(activitiesUrl, auth=auth).json()['values']


def print_comments(activities):
    comments = [act for act in activities if act['action']=='COMMENTED' and act['comment']['state']=='OPEN' ]
    print(bcolors.YELLOW + '\tCOMMENTS'+bcolors.ENDC)
    for comment in comments:
        print('\t\tUser: ' + comment['user']['displayName'])
        print('\t\tTime: ' + str(datetime.datetime.fromtimestamp(comment['createdDate']/1000.0)))
        try:
            file = comment['commentAnchor']['path'] + ':' + str(comment['commentAnchor']['line'])
        except KeyError:    
            file = 'N/A'
        finally:    
            print('\t\tFile: ' + file)
            print('\t\tComment: ' + comment['comment']['text'])
            print('\n')


def print_go_to(url_base, slug, repo, pr_id):
    print(bcolors.OKBLUE + '\tPULL REQUEST' + bcolors.ENDC)
    print('\t\thttps://'+url_base+'/projects/'+slug+'/repos/'+repo+'/pull-requests/'+pr_id+'/overview')
    print('\n')


def print_branch_details(remote, branch):
    print_remote(remote)
    print_branch(branch)

def print_activities(auth, rest_api_base_url, slug, repo, pr_id):
    activities = get_all_activities(auth, rest_api_base_url, pr_id)
    print_reviews(activities)
    print_approvals(activities)
    print_comments(activities)

def check_status(auth):
    repo = git.Repo(search_parent_directories=True)
    branch = repo.active_branch.name
    remote = repo.remotes[0].config_reader.get("url")
    deconstructed_url = repo.remotes[0].config_reader.get("url").replace("ssh://git@", "").replace(".git","").split("/")
    url_base = deconstructed_url[0]
    slug = deconstructed_url[1]
    repo = deconstructed_url[2]

    print_branch_details(remote, branch)

    rest_api_base_url = 'https://'+url_base+'/rest/api/1.0/projects/'+slug+'/repos/'+repo+'/pull-requests/'

    pr_id = str(pull_request_for_branch(auth, rest_api_base_url, branch)['id'])
    print_go_to(url_base, slug, repo, pr_id)
    print_activities(auth, rest_api_base_url, slug, repo, pr_id)
