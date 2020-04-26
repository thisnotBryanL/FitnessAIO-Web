from django.shortcuts import render

# Create your views here.

# NOT USING THIS ONE
def macroCalcView(request):
    template_name = "calculator/macro.html"
    return render(request,template_name,{})

