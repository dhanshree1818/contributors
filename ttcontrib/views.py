from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import Search
import requests
from django.core import validators
from django.core.exceptions import ValidationError


# Create your views here.
def index(request):
    context = {'form':Search}
    form=Search()
    context['form']=form
    return render(request,'base.html',context)

def directlink(request):
    base_url='https://api.github.com/repos/'

    context = {

        'text': "",

    }
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            text=form.cleaned_data.get('Repository_Link')
            text=text.replace('https://github.com/','')
            # url = base_url + text + 'contributors'
            url_commits = base_url + text + 'stats/contributors'
            # return redirect(url)
            # response = requests.get(url)
            response_commit = requests.get(url_commits)

            if response_commit.status_code < 400:

                # contributions = response.json()
                commits = response_commit.json()
                commits = reversed(commits)
                comm_list=[]
                for commit in commits:
                    if len(comm_list)<=10:
                        comm_list.append(commit)
                    else:
                        break

                context['commits']= comm_list



                return render(request,'contributions.html',context)
            else:
                return render(request,'errorpage.html')


        else:
            form = Search()
            context['form'] = form
    return render(request,'contributions.html')
