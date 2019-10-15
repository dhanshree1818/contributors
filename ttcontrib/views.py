from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Contributor
from .forms import Search
import requests
from django.core import validators
from django.core.exceptions import ValidationError


# Create your views here.


class MyIndex(View):
    template_name = 'base.html'

    def get(self, request):
        context = {'form': Search}
        form = Search()
        context['form'] = form
        return render(request, self.template_name, context)


class MyView(View):
    template_name = 'contributions.html'
    error_temp = 'errorpage.html'

    def post(self, request):
        base_url = 'https://api.github.com/repos/'
        avatar_base1 = 'https://avatars2.githubusercontent.com/u/'
        avatar_base2 = '?s=460&v=4'
        context = {

            'text': "",

        }
        if request.method == "POST":
            form = Search(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('Repository_Link')
                text = text.replace('https://github.com/', '')

                url_commits = base_url + text + 'stats/contributors'

                response_commit = requests.get(url_commits)

                if response_commit.status_code < 400:

                    commits = response_commit.json()
                    commits = reversed(commits)

                    comm_list = []
                    for commit in commits:
                        if len(comm_list) <= 10:
                            comm_list.append(commit)
                        else:
                            break
                    context['commits'] = comm_list
                    # context['avatar1'] = avatar_base1
                    # context['avatar2'] = avatar_base2
                    for data in commits:
                        new_contribution= Contributor.objects.create(
                            c_name= data['author']['login'],
                            c_commits = data['total'],
                            c_url = data['author']['html_url']
                        )
                        new_contribution.save()
                        id = str(data['author']['id'])
                        avatar = avatar_base1+id+avatar_base2

                        context['avatar']=avatar

                    return render(request, self.template_name, context)
                else:
                    return render(request, self.error_temp)


            else:
                form = Search()
                context['form'] = form
        return render(request, self.template_name)
