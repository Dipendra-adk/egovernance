from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout,login  
from django.contrib import messages
from .models import Tender, Bid , Contact,Notification
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import TenderForm
from .models import Tender



def tender_list(request):
    tenders = Tender.objects.all()
    return render(request, 'tender/tender_list.html', {'tenders': tenders})


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
    return render(request, 'tender/tender_detail.html', context)

@login_required(login_url='login')
def place_bid(request, tender_id):
    tender = get_object_or_404(Tender, id=tender_id)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, 'Invalid bid amount!')
            return redirect('tender_detail', tender_id=tender_id)

        if amount >= tender.baseprice:
            messages.error(request, 'Bid must be less than the base price!')
            return redirect('place_bid', tender_id=tender_id)

        bidder = request.user
        bid = Bid.objects.create(tender=tender, bidder=bidder, amount=amount)
        messages.success(request, 'Bid placed successfully!')
        return redirect('tender_detail', tender_id=tender_id)
    
    return render(request, 'tender/place_bid.html', {'tender': tender})




# def place_bid(request, tender_id):
#     tender = get_object_or_404(Tender, id=tender_id)
    
#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         try:
#             amount = float(amount)
#         except ValueError:
#             messages.error(request, 'Invalid bid amount!')
#             return redirect('tender_detail', tender_id=tender_id)

#         if amount > tender.baseprice:
#             messages.error(request, 'Bid must be less than or equal to the base price!')
#             return redirect('tender_detail', tender_id=tender_id)

#         bidder = request.user
#         # Create Bid object with a valid reference to the tender
#         bid = Bid.objects.create(tender=tender, bidder=bidder, amount=amount)
#         messages.success(request, 'Bid placed successfully!')
#         return redirect('tender_detail', tender_id=tender_id)
    
#     return render(request, 'tender/place_bid.html', {'tender': tender})


#  to create notification when a bid is won
def process_winning_bid(bid):
    # Assuming bid is won and winner is determined
    Notification.objects.create(
        user=bid.bidder,
        bid=bid,
        tender=bid.tender
    )


def user_dashboard(request):
    user_notifications = Notification.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user_notifications': user_notifications})


@login_required(login_url='login')
def dashboard(request):
    # Fetch related information of the user
    user = request.user
    my_bids = Bid.objects.filter(bidder=user)
    
    context = {
        'user': user,
        'my_bids': my_bids
    }
    return render(request, 'dashboard.html', context)

# def select_winner(request, tender_id):
#     # Assuming you have a model named 'Tender' with a 'deadline' field
#     tender = Tender.objects.get(id=tender_id)

#     # Check if the deadline has passed
#     if tender.deadline <= timezone.now():
#         # Get the highest bid for this tender
#         highest_bid = Bid.objects.filter(tender=tender).order_by('-amount').first()

#         if highest_bid:
#             winner = highest_bid.bidder
#             # Update the winner in the database
#             tender.winner = winner
#             tender.save()

#             # Send email to the winner
#             subject = 'Congratulations! You have won the tender.'
#             html_message = render_to_string('winner_email.html', {'tender': tender})
#             plain_message = strip_tags(html_message)
#             from_email = 'adhikaridipendra972@gmail.com'
#             to_email = winner.email
#             send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
        
    
            
#             # to send message to user dashboard 
#             tender_name = tender.title
#             bid_amount = highest_bid.amount
#             message = f'Congratulations! You have won the tender "{tender_name}" with a bid amount of ${bid_amount}.'
#             messages.success(request, message)
            
#             # Redirect to the tender detail page
#             return redirect('tender_detail', tender_id=tender_id)
#         else:
#             # No bids submitted
#             print("No bids submitted for this tender.")

#         # Redirect to the tender detail page
#         return redirect('tender_detail', tender_id=tender_id)
#     else:
#         # Deadline hasn't passed yet
#         messages.info(request, "The deadline has not been reached.")
#         return redirect('tender_detail', tender_id=tender_id)
  


def select_winner(request, tender_id):
    tender = Tender.objects.get(id=tender_id)

    if tender.deadline <= timezone.now():
        lowest_bid = Bid.objects.filter(tender=tender).order_by('amount').first()

        if lowest_bid:
            winner = lowest_bid.bidder
            tender.winner = winner
            tender.save()

            # Send email to the winner
            subject = 'Congratulations! You have won the tender.'
            html_message = render_to_string('winner_email.html', {'tender': tender})
            plain_message = strip_tags(html_message)
            from_email = 'adhikaridipendra972@gmail.com'
            to_email = winner.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
        
            tender_name = tender.title
            bid_amount = lowest_bid.amount
            message = f'Congratulations! You have won the tender "{tender_name}" with a bid amount of ${bid_amount}.'
            messages.success(request, message)
            
            return redirect('tender_detail', tender_id=tender_id)
        else:
            print("No bids submitted for this tender.")

        return redirect('tender_detail', tender_id=tender_id)
    else:
        messages.info(request, "The deadline has not been reached.")
        return redirect('tender_detail', tender_id=tender_id)
    

def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        number = request.POST.get('number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        company_name = request.POST.get('company_name')  # Get company_name field
        # Create a dictionary to hold all form field values for Bidder model
        bidder_data = {
            'company_name': company_name,
            'email': email,
            'phone': number,
            'address': address
        }
        
        # Checking password match
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'signup.html')
        
        username = fname.lower() + lname.lower()
        
        # Checking if username is already taken
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken.")
            return render(request, 'signup.html')

        # Creating the user
        myuser = User.objects.create_user(username, email, pass2)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        
        # # Creating Bidder profile
        # bidder_form = BidderForm(bidder_data)
        # if bidder_form.is_valid():
        #     bidder = bidder_form.save(commit=False)
        #     bidder.user = myuser
        #     bidder.save()

        # Authenticate and login the user
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'User created and logged in successfully.')
            return redirect('/')
    
    return render(request, 'signup.html')

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

def index(request):
    categories = Tender.objects.values_list('category', flat=True).distinct()
    return render(request, 'index.html', {'categories': categories})

# def category(request, category):
#     tenders = Tender.objects.filter(category=category)
#     return render(request, 'category.html', {'results': tenders, 'query': category})

def about(request):
    return render(request, 'about.html')

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
 
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:  # Check if user is staff/admin
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            # Authentication failed
            return render(request, 'admin_login.html', {'error': 'Invalid username or password'})
    return render(request, 'admin_login.html')
def search_tenders(query):
    return Tender.objects.filter(title__icontains=query) | Tender.objects.filter(category__icontains=query)

def admin_user_check(user):
   # """Check if a user is an administrator""
   return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(admin_user_check)
def admin_dashboard(request):
    tenders = Tender.objects.all()
    tender_data = []

    for tender in tenders:
        tender_data.append({
            'title': tender.title,
            'category': tender.category,
            'status': tender.status,
            'winner': tender.winner.username if tender.winner else "Not yet decided"
        })

    return render(request, 'admin/admin_dashboard.html', {'tender_data': tender_data,'tenders': tenders})

# def admin_dashboard(request):
#     tenders_by_category = {}
#     for category_display, _ in Tender.CATEGORIES:
#         tenders = Tender.objects.filter(category=category_display)
#         tenders_by_category[category_display] = {
#             'count': tenders.count(),
#             'tenders': tenders,
#             'status': 'Closed' if tenders.filter(status='Closed').exists() else 'Active',
#             'winner': None  # Assume winner is None by default
#         }
#         # Check if the deadline is met and winner is known for each tender
#         for tender in tenders:
#             if tender.is_closed:
#                 tenders_by_category[category_display]['status'] = 'Closed'
#                 # Set the winner only if the tender status is 'Closed' and winner is not already set
#                 if tender.status == 'Closed' and not tenders_by_category[category_display]['winner']:
#                     tenders_by_category[category_display]['winner'] = tender.winner.username if tender.winner else None
#     return render(request, 'admin/admin_dashboard.html', {'tenders_by_category': tenders_by_category})


@login_required
@user_passes_test(admin_user_check)
def add_tender(request):
    categories = Tender.CATEGORIES
    status_choices = Tender.STATUS
          
    if request.method == 'POST':
        form = TenderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to admin dashboard after adding tender
    else:
        form = TenderForm()
    
  
    return render(request, 'admin/tender_create.html', {'form': form, 'categories': categories, 'status_choices': status_choices})

@login_required
@user_passes_test(admin_user_check)
def update_tender(request, pk):
    tender = get_object_or_404(Tender, pk=pk)
    if request.method == 'POST':
        form = TenderForm(request.POST, instance=tender)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to admin dashboard after updating tender
    else:
        form = TenderForm(instance=tender)
    return render(request, 'admin/tender_update.html', {'form': form, 'tender': tender})

@login_required
@user_passes_test(admin_user_check)
def delete_tender(request, pk):
    tender = get_object_or_404(Tender, pk=pk)
    if request.method == 'POST':
        tender.delete()
        return redirect('admin_dashboard')  # Redirect to admin dashboard after deleting tender
    return render(request, 'admin/tender_delete.html', {'tender': tender})

def search(request):
    query = request.GET.get('query')
    if query:
        results = search_tenders(query)
    else:
        results = []
    return render(request, 'search_result.html', {'results': results, 'query': query})