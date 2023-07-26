from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import openai


def home(request):
    return render(request, 'home.html')


def chat_with_gpt(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Fetch the user's API key from the database
        api_key = request.user.api_key

        # Use the API key with the API to generate a response
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=150
        )
        gpt_response = response['choices'][0]['text']

        return render(request, 'chat_with_gpt.html', {'user_input': user_input, 'gpt_response': gpt_response})

    return render(request, 'chat_with_gpt.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the provided credentials are valid
        user = authenticate(username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            return redirect('calculator')  # Redirect to the calculator page after login
        else:
            # Invalid credentials, show an error message
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def calculator(request):
    if request.method == 'POST':
        num1 = int(request.POST.get('num1'))
        num2 = int(request.POST.get('num2'))
        operator = request.POST.get('operator')
        result = 0

        if operator == 'add':
            result = num1 + num2
        elif operator == 'subtract':
            result = num1 - num2
        elif operator == 'multiply':
            result = num1 * num2
        elif operator == 'divide':
            if num2 != 0:
                result = num1 / num2
            else:
                result = 'Error: Cannot divide by zero'
        else:
            result = 'Error: Invalid operator'

        # Fetch the user's API key from the database
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            api_key = user.api_key

            # Use the API key with the API to generate a response
            openai.api_key = api_key
            user_input = f"Calculate {num1} {operator} {num2}"  # Formulate a prompt for ChatGPT
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=user_input,
                max_tokens=150
            )
            gpt_response = response['choices'][0]['text']

            return render(request, 'calculator.html', {'result': result, 'gpt_response': gpt_response})
        else:
            return render(request, 'calculator.html', {'result': result})

    return render(request, 'calculator.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        api_key = request.POST.get('api_key')

        user = User.objects.create_user(username=username, password=password, api_key=api_key)
        # Save other user data to the model
        user.save()
        return redirect('calculator')

    return render(request, 'register.html')
