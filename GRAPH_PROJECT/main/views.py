from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.models import UserInfo, User, UserPoint
from matplotlib.figure import Figure
import numpy as np
import os
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

# Create your views here.

def linegraph(request):
    if request.method == 'POST' and request.user.is_authenticated and UserPoint.objects.get(user_id=request.user.id).point > 0:
        X_list = []
        Y_list = []
        hdn_num = request.POST["hidden_numbers"]
        graph_title = request.POST["graph_title"]
        X_title = request.POST["X_title"]
        Y_title = request.POST["Y_title"]
        Y_scale = int(request.POST["Y_scale"])
        X_scale = int(request.POST["X_scale"])
        
    
        XY = hdn_num.split(',')
        X = XY[0].split(' ')
        Y = XY[1].split(' ')
        
        
        def XYmaker(i, i_list):
            # make X and Y list from sorted inputs
            for num in i :  
                try:
                    newNum =  int(float(num))
                except:
                    newNum = 'notINT'
                if isinstance(newNum, int) :
                    i_list.append(newNum)
                    
        XYmaker(X, X_list)
        XYmaker(Y, Y_list)
        
        #change X and Y list to np arrays
        X_list = np.array(X_list)
        Y_list = np.array(Y_list)

        #plot graph   
    
        
        Xmax = max(X_list)
        Ymax = max(Y_list)
        Xmin = min(X_list)
        Ymin = min(Y_list)
        
        def makeRange(max, min, scale):
            #This functions makes the grid lines with 0 as the base for both X and Y axis
            if max < 0 :
                listRange = [*range(0, min-scale*2, -scale)]
                listRange.sort()
            elif min > 0 :
                listRange = [*range(0, max+scale, scale)]
                listRange.sort()
            else:
                listRange = [*range(0, max+scale, scale)]
                listRange2 = [*range(0, min-scale, -scale)]
                listRange = list(set(listRange + listRange2))
                listRange.sort()
            return listRange 
                   
        #Sets the grid lines    
        Yrange = makeRange(max=Ymax, min=Ymin, scale=int(Y_scale))
        Xrange = makeRange(max=Xmax, min=Xmin, scale=int(X_scale))
               
        #gets line of best fit
        a, b = np.polyfit(X_list, Y_list, 1)
        
        #get slope of line of best fit
        try:
            slope = ((a*X_list+b)[-1] - (a*X_list+b)[1] ) / (X_list[-1] - X_list[1])
            slope = round(slope, 5)
        except :
            slope = None 
        
        
           
        fig = Figure()
        ax = fig.subplots()
        ax.set_xlabel(f'{X_title}')
        ax.set_ylabel(f'{Y_title}')
        ax.set_title(f'{graph_title.upper()}')     
        ax.set_xticks(Xrange)
        ax.set_yticks(Yrange)
        ax.set_title(f'X scale = To {X_scale}units \nY scale = To {Y_scale}units', fontsize=6,loc='right',style='italic',)
        ax.plot(X_list, Y_list, "*")
        ax.plot(X_list, a*X_list+b,  "-")
        ax.grid()
       
       # save the figure to file
      
        # cwd = os.getcwd() 
        path =  'cccccc.jpg'


        fig.savefig(path, dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', format='jpg',
        transparent=False, pad_inches=0.1,
        )

        
        im = Image.open(path)

        im.convert('RGB') # convert mode

        # im.thumbnail((1080, 720)) # resize image

        thumb_io = BytesIO() # create a BytesIO object

        im.save(thumb_io, 'JPEG', quality=100) # save image to BytesIO object

        thumbnail = File(thumb_io, name=f'{graph_title}.jpg') # create a django friendly File object

        
        FigureImag = UserInfo()
        FigureImag.title = graph_title
        FigureImag.user = request.user
        FigureImag.graph=thumbnail
        
        for c,img in enumerate(UserInfo.objects.filter(user=request.user).all()):
            #This for loops loops through all the present user graphs obejects and deletes
            #them and their images from DB
            print(img.id , c, img.user)
            img.graph.delete(save=True)
            img.delete()
            
            
        print(f'\n\n\n{type(thumbnail)}\n\n\n')

        FigureImag.save()
        
        imgs =  UserInfo.objects.filter(user_id=request.user.id).latest('id')


        g = UserPoint.objects.get(user_id=request.user.id)
        g.point -= 1
        g.save()
        Context = {'imgs':imgs.graph.url,'values':[],'point': UserPoint.objects.get(user_id=request.user.id).point,'slope':slope}
        
     
        for c in range(0,len(X_list)):
            VALUES = {
                        "X": X_list[c],
                        "Y":  Y_list[c],
                        "index": f'({c+1})',
                    }

            Context['values'].append(VALUES.copy())

       
        
        return render(request, 'linegraph.html', Context)

    elif request.method == 'POST' and request.user.is_authenticated==False:
        Context = {'error':'You need to be logged in to plot graphs','class':'err'}
        return render(request, 'linegraph.html',Context)
    elif request.method == 'POST' and request.user.is_authenticated and UserPoint.objects.get(user_id=request.user.id).point <= 0:
        Context = {'error':'Sorry, but you need to buy more points to plot graphs','class':'err','point':UserPoint.objects.get(user_id=request.user.id).point}
        return render(request, 'linegraph.html',Context)
    
    else:
        if request.user.is_authenticated:
            Context = {'point': UserPoint.objects.get(user_id=request.user.id).point}
        else:
            Context = {'point': ''}
        return render(request, 'linegraph.html', context=Context)


def register(request):

    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        
        # print(request.POST)
        
        #Check if username is already taken in the database
        for users in User.objects.all():
            if username.lower() == users.username.lower():
                print(users.username.lower())
                context={'msg':'Username already exists'}
                return render(request, 'register.html',context)
            
        
        #save user
        U = User.objects.create_user(username=username,email='',password=password)
        UserPoint.objects.create(user=U)
        user = authenticate(request,username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    else:
       return render(request, 'register.html')

def loginpage(request):
    context={}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username, password=password)
        
        if user != None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'User does not exist or incorrect password')
            return render(request, 'login.html',context)

    else:
       return render(request, 'login.html',context)  

def logOutRequest(request):
    logout(request)
    return  redirect('index')

def home(request):
    return render(request, 'home.html') 

def verifyPayment(request):
    if request.method == 'GET':
        amount = request.GET.get("amount")
        amount = int(amount)
        print(amount)

        pointsToBeAdded = amount/20
        print(amount)
        g = UserPoint.objects.get(user_id=request.user.id)
        g.point += pointsToBeAdded
        g.save()
        
        
        return JsonResponse({'addedPoints': pointsToBeAdded,'totalPoints': g.point})
    