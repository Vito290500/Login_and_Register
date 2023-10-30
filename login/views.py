from django.shortcuts import render
from django.views import View
import random
import smtplib
from django.urls import reverse

user_email = "vitodivenosawork@gmail.com"
token = "ndko nzzy vobb zndt"

from .models import UserData, EmailValidation

class MainPageView(View):

    def get(self, request):
        return render(request, "includes/index.html")

    def post(self, request):
        
        submitted = request.POST

        if submitted['username'] == '' or submitted['password'] == '':
            return render(request, "includes/index.html",{
                'empty_error' : "Empty field isn't valid",
            })

        else: 
            if UserData.objects.filter(username=submitted['username']).exists():
                password_query = UserData.objects.filter(username=submitted['username']).values('password')
                stored_password = password_query[0]['password']

                if stored_password == submitted['password']:
                    return render(request, "includes/welcome.html",{'nameuser': submitted['username']})
            
                else:
                    password_error = 'Password incorrect.'
                    return render(request, "includes/index.html", {
                        'error_pass' : password_error,
                        })
                
            else:
                username_error = f"There isn't any username {submitted['username']}"
                return render(request, "includes/index.html", {
                    'error_username': username_error,
                })
        
class EmailValidationView(View):
    
    def get(self, request):
        return render(request, "includes/email_validation.html")

    def post(self, request):
        
        email_to_validate = request.session['temporary_data']['email']
        query = EmailValidation.objects.filter(email = email_to_validate).values('otp')
        submitted = request.POST
        temporary = request.session['temporary_data']

        if query[0]['otp'] == submitted['otp']:

            user_registration = UserData(
                username = temporary['username'],
                first_name = temporary['first_name'],
                last_name = temporary['last_name'],
                email = temporary['email'],
                password = temporary['password'],
            )
            user_registration.save()

            row_todelete = EmailValidation.objects.filter(email = temporary['email'])
            row_todelete.delete()

            session = request.session
            session.clear()
            
            return render(request, "includes/successfull.html")
        
        else:
            email_validate_status = EmailValidation.objects.get(email=temporary['email'])
            attempt = int(email_validate_status.attempt)

            if attempt > 0 or attempt <= 3 and attempt != 0:
                error_handling = {}

                attempt -= 1
                email_validate_status.attempt = attempt
                email_validate_status.save()

                error_handling['error'] = f"OTP incorrect, please try again! you have {attempt + 1} left."
                return render(request, "includes/email_validation.html",
                        {'error_hadling' : error_handling})


            else:
                row_todelete = EmailValidation.objects.filter(email = email_to_validate)
                row_todelete.delete()

                session = request.session
                session.clear()
                        
                return render(request, "includes/unsuccessfull.html")

class RegisterPageView(View):

    def get(self, request):
        return render(request, "includes/register.html")
    
    def post(self, request):
        submitted = request.POST

        error_handling = {}

        if UserData.objects.filter(username=submitted['username']).exists():
            username_error = 'Username already exists.Please choose a different username.'
            error_handling['username_error'] = username_error

        if UserData.objects.filter(email=submitted['email']).exists():
            error_email = 'Email already exists.Please use a different email address.'
            error_handling['error_email'] = error_email

        if submitted['password'] != submitted['confirmpassword']:
            error_password = 'The password insert are not the same.'
            error_handling['error_password'] = error_password

        if submitted['username'] == '' or submitted['email'] == '' or submitted['first_name'] == '' or submitted['last_name'] == '' or submitted['password'] == '' or submitted['confirmpassword'] == '':
            field_error = "Make sure to not submit with empty fields."  
            error_handling['field_error'] = field_error

        if len(error_handling) >= 1:
            return render(request, "includes/register.html",{'error_handling': error_handling})     

        temporary_data = {
            'username': submitted['username'],
            'first_name': submitted['first_name'],
            'last_name': submitted['last_name'],
            'email': submitted['email'],
            'password': submitted['password'],
        }
        request.session['temporary_data'] = temporary_data

        otp = ''.join(str(random.randint(1, 10)) for _ in range(1, 5))

        validation_status = EmailValidation(email=submitted["email"],
                                             validation=False,
                                             otp=otp)

        validation_status.save()

        print(submitted['email'])

        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=user_email, password=token)
        connection.sendmail(from_addr=user_email, to_addrs= submitted['email'],
                            msg = f"Subject:Thanks for subscription!\n\nThis is your OTP: {otp}")
        connection.close()

        return render(request, "includes/email_validation.html")
    
def SuccessView(request):
    return render(request, "includes/successfull.html")

def UnSuccessView(request):
    return render(request, "includes/unsuccessfull.html")

def CheckEmailView(request):
    return render(request, "includes/check_email.html")

def ConfirmUpdatePass(request):
    return render(request, "includes/confirm_pass.html")

class ResetPasswordView(View):

    def get(self, request):
        return render(request, "includes/password_reset.html")


    def post(self, request):

        email_temporary = request.session['email_temporary']
        submitted = request.POST

        if submitted['newpassword'] == submitted['confirmpassword']:

            if submitted['newpassword'] == '' or submitted['confirmpassword'] == '':
                return render(request, "includes/password_reset.html",{
                    'empty': 'Empty field is not allowed.'
                })
                
            else:
                query = UserData.objects.filter(email=email_temporary)
                update = query.first()
                update.password = submitted['newpassword']
                update.save()

                session = request.session
                session.clear()
                
                return render(request, "includes/confirm_pass.html")

        else:
            return render(request, "includes/password_reset.html", {
                    'error': 'The two password are not the same.'
            })

class capture_value_view(View):

    def post(self, request):
        field_value = request.POST['field_value']
            
        email = UserData.objects.filter(username=field_value).values('email')
        email_user = email[0]['email']

        request.session['email_temporary'] = email_user

        link_url = request.build_absolute_uri(reverse('reset_password'))

        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=user_email, password=token)
        connection.sendmail(from_addr=user_email, to_addrs= email_user,
                                msg = f"Subject:Password Reset!\n\nClick here to reset the password: {link_url}")
        connection.close()

        return render(request, "includes/check_email.html")



