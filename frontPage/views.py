from django.shortcuts import render

def RenderPage(request):
    return render(request,'frontPage/front.html',)
