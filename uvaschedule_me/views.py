from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template

import forms
from getcourses import get_section_list

@csrf_protect
def index(request):
    form = forms.CourseForm(auto_id=False)
    return render(request, 'index.html', {'form': form})
    
def about(request):
    return render(request, 'about.html')
    
def schedule(request):
    if request.method == 'POST':
        form = forms.CourseForm(request.POST)
        
        if form.is_valid():
            list_of_courses = get_section_list(form.cleaned_data['courses'])
            
            if list_of_courses == 'ConnectionError':
                return render(request, 'error.html', {error: "Lou's List seems to be down at the moment."});
                
            # Colors found at http://colors.findthedata.com/saved_search/Pastel-Colors
            # Pastel colors are best for showing text on top of them, and aren't too bright for the page
            #colors = ['#9400D3', '#00CED1','#FFA812', '#8B008B', '#666699', '#BDB76B', '#556B2F', '#8B0000', '#E75480', '#9B870C']
            #colors = ['#C23B22', '#FF6961', '#FDFD96', '#AEC6CF', '#FFB347', '#77DD77', '#B19CD9', '#779ECB', '#836953', '#DEA5A4']
            colors = ['#836953', '#DEA5A4', '#FF6961', '#966FD6', '#AEC6CF', '#FFB347', '#77DD77', '#F49AC2']
            #PASTEL BROWN, PASTEL PINK, PASTEL RED, PASTEL PURPLE, PASTEL BLUE, PASTEL ORANGE, PASTEL GREEN
            
            has_lecture = {}
            has_lab = {}
            
            i = 0
            
            import random
            r = lambda: random.randint(0,255)
            
            #color = colors[0]
            
            
            lecture_name = {}
            lecture_vowel = {}
            course_titles = {}
            
            for course in list_of_courses: # Each course
                if i >= len(colors):
                    color = colors[i % len(colors)]
                else:
                    color = colors[i]
                
                for section in list_of_courses[course]: # Each section for each course
                    course_titles[course] = section['course_title']
                    
                    section['color'] = color
                
                    if section['type'] == 'Lecture':
                        has_lecture[course] = True
                        lecture_name[course] = 'Lecture'
                        lecture_vowel[course] = False
                    elif course not in has_lecture:
                        has_lecture[course] = False
                        
                    section['instructortimes'] = zip(section['instructors'], section['times'])
                    
                for section in list_of_courses[course]: # Each section for each course
                    if has_lecture[course]:
                        if section['type'] != lecture_name[course]:
                            has_lab[course] = True
                    else:
                        if section['type'] == 'Laboratory' or section['type'] == 'Discussion':
                            has_lab[course] = True
                        else:
                            lecture_name[course] = section['type']
                            has_lecture[course] = True
                    
                    if course in lecture_name and lecture_name[course][0] in ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U']:
                        lecture_vowel[course] = True
                
                i += 1
                
                
            import json
            json_data = json.dumps(list_of_courses)
            #print(json_data);
            
            json_lecture_names = json.dumps(lecture_name)
            #courses = zip(list_of_courses, colors)
            
            update_form = forms.UpdateForm()
            
            return render(request, 'schedule.html', {'courses': list_of_courses, 'lecture_vowel': lecture_vowel, 
                'json_lecture_names': json_lecture_names, 'lecture_names': lecture_name,'colors': colors, 
                'json_data': json_data, 'has_lecture': has_lecture, 'has_lab': has_lab, 'update_form': update_form, 'course_titles':course_titles}, context_instance=RequestContext(request))
        else:
            print form.errors
            print("Error found")
    else:
        return HttpResponseRedirect('/')
            
@csrf_protect
def update(request):
    if request.method == 'POST':
        form = forms.UpdateForm(request.POST)
        if form.is_valid():
            list_of_courses = get_section_list(form.cleaned_data['courses'])
            
             # Colors found at http://colors.findthedata.com/saved_search/Pastel-Colors
            # Pastel colors are best for showing text on top of them, and aren't too bright for the page
            #colors = ['#9400D3', '#00CED1','#FFA812', '#8B008B', '#666699', '#BDB76B', '#556B2F', '#8B0000', '#E75480', '#9B870C']
            #colors = colors.reverse()
            #colors = ['#C23B22', '#FF6961', '#FDFD96', '#AEC6CF', '#FFB347', '#77DD77', '#B19CD9', '#779ECB', '#836953', '#DEA5A4']
            
            
            has_lecture = {}
            has_lab = {}
            
            i = 0
            
            import random
            r = lambda: random.randint(50,200)
            
            #color = colors[0]
            
            
            lecture_name = {}
            lecture_vowel = {}
            course_titles = {}
            
            for course in list_of_courses: # Each course
                color = '#%02X%02X%02X' % (r(),r(),r())
                
                for section in list_of_courses[course]: # Each section for each course
                    course_titles[course] = section['course_title']
                    
                    section['color'] = color
                
                    if section['type'] == 'Lecture':
                        has_lecture[course] = True
                        lecture_name[course] = 'Lecture'
                        lecture_vowel[course] = False
                    elif course not in has_lecture:
                        has_lecture[course] = False
                        
                    section['instructortimes'] = zip(section['instructors'], section['times'])
                    
                for section in list_of_courses[course]: # Each section for each course
                    if has_lecture[course]:
                        if section['type'] != lecture_name[course]:
                            has_lab[course] = True
                    else:
                        if section['type'] == 'Laboratory' or section['type'] == 'Discussion':
                            has_lab[course] = True
                        else:
                            lecture_name[course] = section['type']
                            has_lecture[course] = True
                    
                    if course in lecture_name and lecture_name[course][0] in ['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U']:
                        lecture_vowel[course] = True
                
                i += 1
                
                
            import json
            json_data = json.dumps(list_of_courses)
            #print(json_data);
            
            json_lecture_names = json.dumps(lecture_name)
            
            return HttpResponse(json.dumps({'courses': list_of_courses, 'lecture_vowel': lecture_vowel, 'json_lecture_names': json_lecture_names, 'lecture_names': lecture_name, 
                'json_data': json_data, 'has_lecture': has_lecture, 'has_lab': has_lab, 'course_titles': course_titles}))
        else:
            return HttpResponse("Invalid Form")
    else:
        return HttpResponse("Failure")
    
def error(request):
    return render(request, 'error.html')
    
def feedbackbug(request):
    return render(request, 'feedbackbug.html')
    
def contact(request):
    return render(request, 'contact.html')