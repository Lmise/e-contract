from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Contract
from .forms import EmailContractForm


def contract_list(request):
    object_list = Contract.approved.all()

    paginator = Paginator(object_list, 5)  # 5 contracts in each page
    page = request.GET.get('page')
    try:
        contracts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        contracts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the last page of the results
        contracts = paginator.page(paginator.num_pages)
    return render(request, "contracts/list.html", {'page': page, 'contracts': contracts})

class ContactListView(ListView):
    queryset = Contract.approved.all()
    context_object_name = 'contracts'
    paginate_by = 5
    template_name = 'contracts/list.html'


def contract_detail(request, year, month, day, contract):
    contract = get_object_or_404(Contract, slug=contract,
                                 project_status='approved',
                                 project_publish_date__year=year,
                                 project_publish_date__month=month,
                                 project_publish_date__day=day)
    # list of similar contracts
    return render(request, 'contracts/detail.html', {'contract': contract})


def contract_share(request, contract_id):
    # Retrieve post by id
    contract = get_object_or_404(Contract, id=contract_id, status='approved')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailContractForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            contract_url = request.build_absolute_uri(contract.get_absolute_url())
            subject = 'Podii Consultants Would like tou to sign "{}" in order to proceed with the job'\
                .format(contract.title)
            message = 'View "{}" at {}\n\n{}\'s comments: {}'.format(contract.title, contract_url,)
            send_mail(subject, message, 'admin@site.com', [cd['to']])
            sent = True
        else:
            form = EmailContractForm()
    return render(request, 'contracts/share.html', {'contract': contract,
                                                    'form': form,
                                                    'sent': sent})




