from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count

from taggit.models import Tag

from .models import Contract
from .forms import EmailPostForm


def contract_list(request, tag_slug=None):
    object_list = Contract.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags_in=[tag])

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
    return render(request, "contract/contracts/list.html", {'page': page,
                                                            'contracts': contracts,
                                                            'tag': tag})

class ContactListView(ListView):
    queryset = Contract.published.all()
    context_object_name = 'contracts'
    paginate_by = 5
    template_name = 'contract/contracts/list.html'


def post_detail(request, year, month, day, post):
    contract = get_object_or_404(Contract, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # list of similar contracts
    contract_tags_ids = contract.tags.values_list('id', flat=True)
    similar_contracts = Contract.published.filter(tags__in=contract_tags_ids).exclude(id=post.id)
    similar_contracts = similar_contracts.annotate(same_tags=Count('tags')).order_by('-same_tags',
                                                                             '-publish')[:4]
    return render(request, 'blog/contract/detail.html', {'contract': contract,
                                                     'similar_contracts': similar_contracts})


def contract_share(request, contract_id):
    # Retrieve post by id
    contract = get_object_or_404(Contract, id=contract_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            contract_url = request.build_absolute_uri(contract.get_absolute_url())
            subject = 'Podii Consultants Would like tou to sign "{}" in order to proceed with the job'\
                .format(contract.title)
            message = 'View "{}" at {}\n\n{}\'s comments: {}'.format(contract.title, contract_url,)
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'contract': contract,
                                                    'form': form,
                                                    'sent': sent})




