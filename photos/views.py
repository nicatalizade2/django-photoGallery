from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from . forms import UserRegisterForm
from photos.models import *




def loginUser(request):
    if request.method == 'POST':
        testusername = request.POST['username']
        testpassword = request.POST['password']
        user = authenticate(request, username=testusername, password=testpassword)
        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login.html')

def userRegister(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            user = authenticate(request, username=form.cleaned_data.get('username'), password=request.POST['password1'])
            if user is not None:
                login(request, user)
                return redirect('gallery')


    return render(request, 'photos/register.html', {
        'form': form
    })


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def gallery(request):
    user = request.user
    filter = request.GET.get('filter')
    if filter == None:
        photo = Photo.objects.filter(category__user=user)
    else:
        photo = Photo.objects.filter(category__name=filter, category__user=user)
        categories = Category.objects.filter(user=user)
    return render(request, 'photos/gallery.html', {
        'photos': photo,
        'categories': categories
    })


# @login_required(login_url='login')
# def viewPhoto(request, pk):
#     photo = Photo.objects.get(pk=pk)
#     return render(request, 'photos/photo.html', {
#         'photos': photo
#     })

@login_required(login_url='login')
def addPhoto(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    # categories = user.category_set.all() # or you can use this one

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('images')
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, create = Category.objects.get_or_create(name=data['category_new'], user=user)
        else:
            category = ''
        Photo.objects.create(category=category, image=image, description=data['description'])

        return redirect('gallery')

    return render(request, 'photos/add.html', {
        'categories': categories
    })

#
#
# if request.method == 'POST':
#        data = request.POST
#        image = request.FILES.get('images')
#        if data['category'] != 'none':  #'none' => value <option value='none'>Select a category...</option>
#            category = Category.objects.get(id=data['category'])
#        elif data['category_new'] != '':
#            category, create = Category.objects.get_or_create(name=data['category_new'])
#        else:
#            category = None
#        Photo.objects.create(category=category, image=image, description=data['description'])
#
#        return redirect('gallery')
