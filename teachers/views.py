from django.http import HttpResponse

def teachers(request):
    return HttpResponse("This is teacher home page")
