from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CustomerCreationForm


def register(request):

    if request.method == 'POST':

        form = CustomerCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Cadastro realizado com sucesso!'
            )

            return redirect('catalog:product_list')

    else:
        form = CustomerCreationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )