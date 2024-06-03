from django.shortcuts import render


def warehouse(request):
    nav_state = {"projects": "", 
                 "hant": "",
                 "calendar": "",
                 "employees": "",   
                 "warehouse": "active",
                 "purchase":  ""   
                 }
    
    data = {
        "nav": nav_state
    }
    return render(request, "warehouse.html", data)


def purchase(request):
    nav_state = {"projects": "", 
                 "hant": "",
                 "calendar": "",
                 "employees": "",   
                 "warehouse": "", 
                 "purchase":  "active"
                 }
    
    data = {
        "nav": nav_state
    }
    return render(request, "warehouse.html", data)
