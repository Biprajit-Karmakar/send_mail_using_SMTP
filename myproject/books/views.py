from django.shortcuts import render, get_object_or_404, redirect

from myproject import settings
from .utils import send_email_to_cilent
from django.core.mail import send_mail, EmailMessage
from .models import Book
from .forms import BookForm


# def send_email(request):
#     send_email_to_cilent()
#     return redirect('/')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            data = form.cleaned_data
            print(data)
            
            subject = 'Book Created'
            message = 'Book Details: ' + str(form.cleaned_data)
            from_email = settings.EMAIL_HOST_USER
            to_mail = 'biprajit.qtec@gmail.com' 
            
            file_path = 'media/uploads/mypdf.pdf'
            with open(file_path, 'rb') as attachment:
                file_data = attachment.read()
                content_type = 'application/pdf'
                mail = EmailMessage(subject=subject, body=message, from_email=from_email, to=[to_mail])
                mail.attach('mypdf.pdf', file_data, content_type)
                print(file_data)
                mail.send()
            return redirect('book_list') 
    else:
        form = BookForm()
    
    return render(request, 'books/book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})
