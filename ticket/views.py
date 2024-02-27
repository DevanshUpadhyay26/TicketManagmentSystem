from django.shortcuts import render,redirect
from django.contrib import messages
from .form import CreateTicketForm, UpdateTicketForm
from .models import Ticket
import datetime



#Ticket Details

def ticket_details(request,pk):
    ticket=Ticket.objects.get(pk=pk)
    context={'ticket':ticket}
    return render(request, 'ticket/ticket_details.html',context)



"""For Customer"""
#creating a ticket 

def create_ticket(request):
    if request.method=='POST':
        form=CreateTicketForm(request.POST)
        if form.is_valid():
            var=form.save(commit=False)
            var.created_by=request.user
            var.ticket_status ='Pending'
            var.save()
            messages.info(request,'Ticket has successfully created. Kindly wait for enginner to be assigned')
            return redirect('dashboard')
        else:
            messages.warning(request,'Something went wrong! Check your form')
            return redirect('create-ticket')
    else:
        form=CreateTicketForm()
        context={'form':form}
        return render(request, 'ticket/create_ticket.html',context)
    
#updating the ticket
    
def update_ticket(request,pk):
    ticket=Ticket.objects.get(pk=pk)
    if request.method=='POST':
        form=CreateTicketForm(request.POST)
        if form.is_valid():
            form.save()

            messages.info(request,'Ticket info has been updated. All changes are saved in database')
            return redirect('dashboard')
        else:
            messages.warning(request,'Something went wrong! Check your form')
            return redirect('create-ticket')
    else:
        form=UpdateTicketForm(instance=ticket)
        context={'form':form}
        return render(request, 'ticket/update_ticket.html',context)
    


#Viewing all created tickets
def all_tickets(request):
    tickets=Ticket.objects.filter(created_by=request.user)
    context={'ticket':tickets}
    return render(request, 'ticket/all_ticket.html',context)

#For Engineers

#Ticket Queue

def ticket_queue(request):
    tickets=Ticket.objects.filter(ticket_status='Pending')
    context={'ticket':tickets}
    return render(request, 'ticket/ticket_queue.html',context)


#accept the ticket from queue
def accept_ticket(request,pk):
    ticket=Ticket.objects.get(pk=pk)
    ticket.assigned_to=request.user
    ticket.ticket_status='Active'
    ticket.accepted_date=datetime.datetime.now()
    ticket.save()
    messages.info(request,'Ticket has been accepted, Kindly Resolve ASAP')
    return redirect('ticket-queue')



#Close the ticket from queue
def close_ticket(request,pk):
    ticket=Ticket.objects.get(pk=pk)
    ticket.ticket_status='Completed'
    ticket.is_resolved=True
    ticket.accepted_date=datetime.datetime.now()
    ticket.save()
    messages.info(request,'Ticket has been Resolved,Thank You for Support')
    return redirect('ticket-queue')


#active tickets working on
def workspace(request):
    tickets=Ticket.objects.filter(assigned_to=request.user,is_resolved=False)
    context={'tickets':tickets}
    return render(request,'ticket/workspace.html',context)


#Closed/Resolved Tickets

def all_closed_tickets(request):
    tickets=Ticket.objects.filter(assigned_to=request.user, is_resolved=True)
    context={'ticket':tickets}
    return render(request, 'ticket/all_closed_tickets.html',context)