from django.shortcuts import render

# Create your views here.
def macroCalcView(request):
    template_name = "calculator/macro.html"
    return render(request,template_name,{})
