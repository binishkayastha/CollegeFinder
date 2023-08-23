from django.shortcuts import render, redirect
import os
from os import listdir
from os.path import isfile, join
import pickle
from sign_in.models import Profile
from django.http import HttpResponse,JsonResponse
from .models import *
from .forms import CollegeForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def colleges(request):
	if request.user.is_authenticated and request.user.is_superuser:
		colleges = College.objects.all()
		context = {'colleges_copy': colleges}
		return render(request, "colleges/admin/college_list.html",context)
	return redirect('login/')

def predictor(student):
	to_test = student
	settings_dir = os.path.dirname(__file__)
	PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
	mypath = PROJECT_ROOT + '/colleges/ml/'
	all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	colleges = []

	for file in all_files:
		loaded_model = pickle.load(open(mypath + file, 'rb'))
		result = loaded_model.predict(to_test)

		if (int)(0.5 * result[0] + 0.5) >= 1:
			name = ''
			i = 0
			while file[i] != '.':
				name += file[i]
				i += 1
			colleges.append(name)
	return colleges

def checker(user):	
	profile = Profile.objects.get(user = user)
	possible_colleges = predictor([[profile.gpa,profile.percentage]])

	college_list = []
	print(college_list)

	for college in possible_colleges:
		college_details = College.objects.get(name = college)
		college_list.append(college_details)

	return college_list

@login_required(login_url='login')
def add_college(request):
	if request.user.is_authenticated and request.user.is_superuser:
		if request.method == "POST":
			college_form = CollegeForm(request.POST)

			if college_form.is_valid():
				college_form.save()
				return redirect('colleges:colleges')
		else:
			college_form = CollegeForm()
		return render(request, 'colleges/admin/add.html', {'college_form': college_form})

@login_required(login_url='login')
def edit_college(request, pk):
    college = College.objects.get(id=pk)
    form = CollegeForm(instance=college)
    
    if request.method == "POST":
        form = CollegeForm(request.POST, instance=college)
        if form.is_valid():
            college = form.save()  
            messages.success(request, 'College information updated successfully')
            return redirect('colleges:colleges')  
    context = {'form': form}
    return render(request, 'colleges/admin/edit_college.html', context)

@login_required(login_url='login')
def delete_college(request, pk):
    college = College.objects.get(id=pk)
    if request.method == "POST":
        college.delete()
        messages.danger(request, 'College deleted successfully')
        return redirect('colleges:colleges')
    return render(request, 'colleges/admin/delete_college.html', {"obj": college})



def search(request):
	print('in search')

	if request.user.is_authenticated:
		user = request.user
		colleges = checker(user)
		colleges_copy = []
		colleges_copy1 = []

		maxCost = location = None
		
		maxCost = request.POST.get('maxRange')
		location = request.POST.get('location')
		print(maxCost, location)
		if maxCost is None and location is None:
			colleges_copy = colleges

		elif maxCost is not None and location is None:
			maxCost = (int)(maxCost)
			for college in colleges:
				if college.average_cost <= maxCost:
					colleges_copy.append(college)

		elif maxCost is None or maxCost is '' and location is not None:
			for college in colleges:
				if location.lower() in college.location.lower():
					colleges_copy.append(college)

		else:
			maxCost = (int)(maxCost)
			for college in colleges:
				if college.average_cost <= maxCost:
					colleges_copy1.append(college)

			for college in colleges_copy1:
				if location.lower() in college.location.lower():
					colleges_copy.append(college)

		return render(request, 'colleges/college_list.html', {'colleges_copy': colleges_copy})
	return redirect('login')
	return 


def apply_to_college(request, pk):
    if request.method == 'POST':
        college_id = pk
        try:
            college = College.objects.get(id=college_id)
        except College.DoesNotExist:
            return JsonResponse({'message': 'College not found'}, status=400)
        
        application = Apply.objects.create(college=college, student=request.user)
        application.save()
        
        messages.success(request, 'Application successful')
        return redirect(reverse('colleges:search'))
    else:
        return redirect(reverse('colleges:search'))