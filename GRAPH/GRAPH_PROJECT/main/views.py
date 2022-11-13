from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.models import FigureImage
from matplotlib.figure import Figure
import os
from io import BytesIO
import base64

# Create your views here.

def index(request):

    if request.method == 'POST':
        X_list = []
        Y_list = []
        hdn_num = request.POST["hidden_numbers"]
        
       
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
        
        #plot graph   
        
        fig = Figure()
        ax = fig.subplots()
     
        ax.plot(X_list, Y_list)
        ax.grid()
       
       # save the figure to file
      
        cwd = os.getcwd() 
        path = os.path.join(cwd, 'media',"uploads",'cccccc.png')
       
        # f = ax.savefig(path)
        
        
        fig.savefig(path, dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', format='png',
        transparent=False, pad_inches=0.1,
        )
        
        FigureImag = FigureImage()
        FigureImag.figure = hdn_num
        FigureImag.graph = path
        
        
        FigureImag.save()
        
        
        imgs = FigureImage.objects.latest('id')
        Context = {'imgs':imgs.graph.url,'values':[]}
        
        print(f'\n\n\n\n\n\n{Context["imgs"]}\n\n\n\n\n\n')
     
        for c in range(0,len(X_list)):
            VALUES = {
                        "X": X_list[c],
                        "Y":  Y_list[c],
                        "index": f'({c+1})',
                    }

            Context['values'].append(VALUES.copy())

       
        return render(request, 'home.html', Context)

         
        

    else:
       return render(request, 'home.html')

