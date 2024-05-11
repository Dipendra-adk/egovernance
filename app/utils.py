from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.contrib import messages
from .models import Tender, Bid 
from django.shortcuts import render, redirect

# def select_winner(tender):
#     # Retrieve bids for the tender
#     bids = tender.bid_set.all()
#     # Select winner based on criteria (e.g., highest bid amount)
#     winner_bid = bids.order_by('-amount').first()
#     if winner_bid:
#         tender.winner = winner_bid.bidder
#         tender.save()
#         send_winner_email(tender)

# def send_winner_email(tender):
#     subject = 'Congratulations! You won the tender'
#     recipient = tender.winner.email
#     # Render email template
#     email_html_template = 'winner_notification.html'
#     #email_text_template = 'email_templates/winner_notification.txt'
#     context = {'tender': tender}
#     html_content = render_to_string(email_html_template, context)
#     #text_content = strip_tags(render_to_string(email_text_template, context))
#     # Send email
#     #send_mail(subject, text_content, 'your@example.com', [recipient], html_message=html_content)
#     send_mail(subject, strip_tags(html_content), 'your_email@example.com', [recipient], html_message=html_content)


def select_winner(request, tender_id):
    tender = Tender.objects.get(id=tender_id)

    # Check if the deadline has passed
    if tender.deadline <= timezone.now():
        # Get the highest bid for this tender
        highest_bid = Bid.objects.filter(tender=tender).order_by('-amount').first()

        if highest_bid:
            winner = highest_bid.bidder

            # Send email to the winner
            subject = 'Congratulations! You have won the tender.'
            html_message = render_to_string('winner_email.html', {'tender': tender})
            plain_message = strip_tags(html_message)
            from_email = 'your-email@example.com'
            to_email = winner.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

            # Update the winner in the database
            tender.winner = winner
            tender.save()

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
