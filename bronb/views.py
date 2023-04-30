from django.shortcuts import redirect


def redirect_room(request):
    return redirect('rooms_list_url', permanent=True)