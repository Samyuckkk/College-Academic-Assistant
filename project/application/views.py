from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError, models
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from application.models import Appointment, AcceptedAppointment, Subject

# Create your views here.

def home(request):
    if request.method == "POST":
        
        if 'login_btn' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('role_redirect')
            else:
                messages.error(request, "Invalid username or password")

        elif 'register_btn' in request.POST:
            username = request.POST.get('loginID')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('regEmail')
            password = request.POST.get('regPassword')

            if User.objects.filter(username=username).exists():
                messages.error(request, "User already exists")
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                messages.success(request, "Registration successful! Please login.")

    return render(request, 'index.html')


@login_required(login_url='home')
def role_based_redirect(request):
    user = request.user

    if user.groups.filter(name='admin').exists():
        return redirect('adminDash')
    elif user.groups.filter(name='teacher').exists():
        return redirect('profDash')
    elif user.groups.filter(name='student').exists():
        return redirect('studDash')
    
    return render(request, 'index.html')

@login_required(login_url='home')
def studDash(request):

    # user = request.user

    # return render(request, 'stud_board.html', {'user': user}) => no need to do this for fetching logge in user details
    return render(request, 'stud_board.html')


@login_required(login_url='home')
def cabinLoc(request):

    return render(request, 'cabin_loc.html')

@login_required(login_url='home')
def studApp(request):

    teacher_group = Group.objects.get(name='teacher')
    
    teachers = teacher_group.user_set.all()
    
    return render(request, 'stud_appoin.html', {'teachers': teachers})

@login_required(login_url='home')
def create_appointment(request):
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        student_username = request.POST.get('student_username')
        message = request.POST.get('message')
        teacher_name = request.POST.get('professor_name')
        teacher_username = request.POST.get('teacher_username')

        appointment = Appointment(student_name=student_name, student_username=student_username, message=message, teacher_name=teacher_name, teacher_username=teacher_username)

        appointment.save()

        return redirect('studApp') 
    else:
        return redirect('home')
    

@login_required(login_url='home')
def profDash(request):

    return render(request, 'prof_board.html')


@login_required(login_url='home')
def profApp(request):

    teacher = request.user

    appointments = Appointment.objects.filter(teacher_username=teacher.username)

    return render(request, 'prof_appoin.html', {'appointments': appointments})

@login_required(login_url='home')
def adminDash(request):

    return render(request, 'dashboard/index.html')

@login_required(login_url='home')
def loginRoles(request):

    return render(request, 'dashboard/loginRoles.html')


@login_required(login_url='home')
def accept_appointment(request):

    if request.method == "POST":
        student_name = request.POST.get("student_name")
        student_username = request.POST.get("student_username")
        teacher_name = request.POST.get("teacher_name")
        teacher_username = request.POST.get("teacher_username")
        message = request.POST.get("message")
        appointment_date = request.POST.get("appointment_date")
        appointment_time = request.POST.get("appointment_time")

        # print("Received data:", student_name, student_username, message, teacher_name, teacher_username ,appointment_date, appointment_time)

        accepted = AcceptedAppointment.objects.create(student_name=student_name, student_username=student_username, teacher_name=teacher_name, teacher_username=teacher_username, message=message, appointment_date=appointment_date, appointment_time=appointment_time)

        # print("Saved Accepted Appointment:", accepted)

        Appointment.objects.filter(student_username=student_username, teacher_username=teacher_username, message=message).delete()

        return redirect('profDash')
    

@login_required(login_url='home')
def accepted_appointments(request):

    accepted_appointments = AcceptedAppointment.objects.filter(teacher_username=request.user.username)

    return render(request, 'credit/accepted_appoin.html', {'accepted_appointments': accepted_appointments})


@login_required(login_url='home')
def stud_accepted(request):

    accepted_appointment = AcceptedAppointment.objects.filter(student_username = request.user.username)

    return render(request, 'stud_accepted_appoin.html', {'accepted_appointment': accepted_appointment})


def semesters(request):

    return render(request, 'credit/semesters.html')


def sem_subjects(request, sem_number):

    if request.method == "POST":
        course_code = request.POST.get('course_code')
        course_name = request.POST.get('course_name')
        course_type = request.POST.get('course_type')
        category = request.POST.get('category')
        credits = int(request.POST.get('credits'))
        lecture_hours = int(request.POST.get('lecture_hours'))
        pr_hours = int(request.POST.get('pr_hours'))

        if course_type.lower() == 'elective' and credits > 3:
            messages.error(request, "❌ Elective cour ses cannot have more than 3 credits.")
        else:
            current_credits = Subject.objects.filter(semester=sem_number).aggregate(total=models.Sum('credits'))['total'] or 0

            max_credits_per_sem = {1: 22, 2: 22, 3: 23, 4: 20, 5: 25, 6: 24, 7: 21, 8: 15}
            max_credits = max_credits_per_sem.get(sem_number)

            # if current_credits + credits > 22:
            #     messages.error(request, f"❌ Total credits for Semester {sem_number} cannot exceed 22. Current total: {current_credits}")

            if current_credits + credits > max_credits:
                messages.error(request, f"❌ Total credits for Semester {sem_number} cannot exceed {max_credits}. Current total without this subject: {current_credits}")
            else:
                try:
                    Subject.objects.create(
                        course_code=course_code,
                        course_name=course_name,
                        course_type=course_type,
                        category=category,
                        credits=credits,
                        lecture_hours=lecture_hours,
                        pr_hours=pr_hours,
                        semester=sem_number
                    )
                    messages.success(request, "✅ Subject added successfully.")
                except IntegrityError:
                    messages.error(request, "❌ Course Code or Course Name already exists.")

    
    subjects = Subject.objects.filter(semester=sem_number)

    return render(request, 'credit/sem_subjects.html', {'subjects': subjects, 'semester': sem_number})


@login_required(login_url='home')
def edit_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    
    if request.method == 'POST':

        if 'delete' in request.POST:
            subject.delete()
            messages.success(request, "✅ Subject deleted successfully.")
            return redirect('sem_subjects', sem_number=subject.semester)

        course_code = request.POST.get('course_code')
        course_name = request.POST.get('course_name')
        course_type = request.POST.get('course_type')
        category = request.POST.get('category')
        credits = int(request.POST.get('credits'))
        lecture_hours = int(request.POST.get('lecture_hours'))
        pr_hours = int(request.POST.get('pr_hours'))

        if course_type.lower() == 'elective' and credits > 3:
            messages.error(request, "❌ Elective courses cannot have more than 3 credits.")
        else:
            current_credits = Subject.objects.filter(semester=subject.semester).exclude(id=subject.id).aggregate(total=models.Sum('credits'))['total'] or 0

            max_credits_per_sem = {1: 22, 2: 22, 3: 23, 4: 20, 5: 25, 6: 24, 7: 21, 8: 15}
            max_credits = max_credits_per_sem.get(subject.semester)

            # if current_credits + credits > 22:
            #     messages.error(request, f"❌ Total credits for Semester {subject.semester} cannot exceed 22. Current total without this subject: {current_credits}")

            if current_credits + credits > max_credits:
                messages.error(request, f"❌ Total credits for Semester {subject.semester} cannot exceed {max_credits}. Current total without this subject: {current_credits}")
            else:
                subject.course_code = course_code
                subject.course_name = course_name
                subject.course_type = course_type
                subject.category = category
                subject.credits = credits
                subject.lecture_hours = lecture_hours
                subject.pr_hours = pr_hours
                subject.save()
                messages.success(request, "✅ Subject updated successfully.")
                return redirect('sem_subjects', sem_number=subject.semester)


    return render(request, 'credit/edit_subject.html', {'subject': subject})



def specializations(request):

    return render(request, 'credit/specializations.html')
