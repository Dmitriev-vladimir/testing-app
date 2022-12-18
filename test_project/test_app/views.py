from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .models import TestCase, Test, Answer


def index(request):
    return render(request, 'test_app/index.html')


def registration(request):
    if request.method == 'POST':
        print('POST')
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('catalog')
            except IntegrityError:
                return render(
                    request,
                    'test_app/registration.html',
                    {
                        'form': UserCreationForm(),
                        'error_name': f'''Пользователь с именем {request.POST["username"]} уже зарегистрирован. 
                                            Введите другое имя '''
                    }
                )
        else:
            return render(
                request,
                'test_app/registration.html',
                {'form': UserCreationForm(), 'error_pass': 'Пароли не совпадают. Введите данные заново'}
            )

    return render(request, 'test_app/registration.html', {'form': UserCreationForm()})


@login_required
def catalog(request):
    test_list = TestCase.objects.all()
    return render(request, 'test_app/catalog.html', {'catalog': test_list})


@login_required
def test_view(request, test_case_pk):
    test_case = TestCase.objects.get(pk=test_case_pk)

    test_case.temp_correct = 0
    test_case.temp_wrong = 0
    test_case.save()

    return render(request, 'test_app/test.html', {'test_case': test_case})


@login_required
def test_page(request, test_case_pk, test_index):
    test_case = TestCase.objects.get(pk=test_case_pk)
    test_questions = Test.objects.all().filter(case=test_case)
    test_current = test_questions[test_index]

    if request.method == 'POST':
        test_pass = True
        if (len(request.POST.keys()) - 1) == len(Answer.objects.all().filter(test=test_current, is_right=True)):
            for elem in request.POST.keys():
                if elem.isdigit():
                    if not Answer.objects.get(pk=elem).is_right:
                        test_pass = False
        else:
            test_pass = False
        test_index += 1
        if test_pass:
            test_case.temp_correct += 1
        else:
            test_case.temp_wrong += 1

        test_case.save()

        if test_index == len(Test.objects.all().filter(case=test_case)):
            return redirect(f'/test/result/{test_case_pk}')
        return redirect(f'/test/{test_case_pk}/{test_index}/')

    test_dict = {
        'question': test_current,
        'answers': Answer.objects.all().filter(test=test_current)
    }
    return render(request, 'test_app/test-page.html', {'test_case': test_case, 'test': test_dict, 'pk': test_index})


@login_required
def test_result(request, test_case_pk):
    test_case = TestCase.objects.get(pk=test_case_pk)
    correct = test_case.temp_correct
    wrong = test_case.temp_wrong
    result = {
        'test_case': test_case,
        'correct': correct,
        'wrong': wrong,
        'percent': round(correct * 100 / (correct + wrong), 1)
    }
    return render(request, 'test_app/test-result.html', {'result': result})


def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(
                request,
                'test_app/login.html',
                {'form': AuthenticationForm(), 'error': 'Неверная пара имя - пароль'}
            )
        else:
            login(request, user)
            return redirect('catalog')

    return render(request, 'test_app/login.html', {'form': AuthenticationForm()})


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


def contacts(request):
    return render(request, 'test_app/contacts.html')
