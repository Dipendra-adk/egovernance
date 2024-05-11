from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from .models import Tender, Bid , Contact
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags



@login_required
def tender_list(request):
    tenders = Tender.objects.all()
    return render(request, 'tender_list.html', {'tenders': tenders})

@login_required
def tender_detail(request, tender_id):
    tender = Tender.objects.get(id=tender_id)
    bids = tender.bids.all()
    # Retrieve the highest bid (if any)
    highest_bid = bids.order_by('-amount').first()
    context = {
        'tender': tender,
        'bids': bids,
        'winner': highest_bid,  # Pass the winner data to the template
    }
    return render(request, 'tender_detail.html', context)

@login_required
def place_bid(request, tender_id):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        bidder = request.user
        tender = Tender.objects.get(id=tender_id)
        baseprice = tender.baseprice
        if int(amount) < baseprice:
            messages.error(request,'Bid must be greater than or equal to the base price!')
            return redirect('tender_detail', tender_id=tender_id)
        
        bid = Bid.objects.create(tender=tender, bidder=bidder, amount=amount)
        return redirect('tender_detail', tender_id=tender_id)
    else:
        return render(request, 'place_bid.html', {'tender_id': tender_id})




@login_required
def dashboard(request):
    # Fetch related information of the user
    user = request.user
    my_bids = Bid.objects.filter(bidder=user)
    
    context = {
        'user': user,
        'my_bids': my_bids
    }
    return render(request, 'dashboard.html', context)

def select_winner(request, tender_id):
    # Assuming you have a model named 'Tender' with a 'deadline' field
    tender = Tender.objects.get(id=tender_id)

    # Check if the deadline has passed
    if tender.deadline <= timezone.now():
        # Get the highest bid for this tender
        highest_bid = Bid.objects.filter(tender=tender).order_by('-amount').first()

        if highest_bid:
            winner = highest_bid.bidder
            # Update the winner in the database
            tender.winner = winner
            tender.save()

            # Send email to the winner
            subject = 'Congratulations! You have won the tender.'
            html_message = render_to_string('winner_email.html', {'tender': tender})
            plain_message = strip_tags(html_message)
            from_email = 'adhikaridipendra972@gmail.com'
            to_email = winner.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
        
    
            
            # to send message to user dashboard 
            tender_name = tender.title
            bid_amount = highest_bid.amount
            message = f'Congratulations! You have won the tender "{tender_name}" with a bid amount of ${bid_amount}.'
            messages.success(request, message)
            
            # Redirect to the tender detail page
            return redirect('tender_detail', tender_id=tender_id)
        else:
            # No bids submitted
            print("No bids submitted for this tender.")

        # Redirect to the tender detail page
        return redirect('tender_detail', tender_id=tender_id)
    else:
        # Deadline hasn't passed yet
        messages.info(request, "The deadline has not been reached.")
        return redirect('tender_detail', tender_id=tender_id)
    

def signup(request):
    if request.method == 'POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname' )
            email = request.POST.get('email')
            number = request.POST.get('number')
            address = request.POST.get('address')
            city = request.POST.get('city')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2') 
            username = lname .lower() + fname.lower()
            
             # Checking password match
            if pass1 != pass2:
                messages.error(request,'Passwords do not match!')
                return render(request,'signup.html')
            
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username is already taken.")
                return render(request, 'signup.html')
        
            myuser = User.objects.create_user(username,email,pass2)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            
            user = authenticate(request , username = username , password = pass1)
            if user is not None:
                auth_login(request,user)
                messages.success(request,'User created and logged in successfully.')
                return redirect('/')
    
    return render(request,'signup.html')

def handlelogin(request):
        if request.method == "POST":
            username = request.POST.get('username')
            pass1 = request.POST.get('pass1')
            
            user = authenticate(request, username=username, password=pass1)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'You are logged in successfully.')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')

        return render(request, 'login.html')

def handlelogout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')

def home(request):
    return render(request, 'home.html')

def goal(request):
    return render(request, 'goal.html')

def contact(request):
     if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the contact form data to the database
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        # add a success message 
        messages.success(request,  "Your message has been sent!")   
        # Redirect to a same page  after POST
        return redirect('contact')  

     # If it's a GET request, just render the contact page
     return render(request, 'contact.html')