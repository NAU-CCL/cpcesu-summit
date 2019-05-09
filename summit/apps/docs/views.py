from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from summit.libs.auth.models import UserProfile

from .forms import DocumentForm
from .models import Document


def index(request):
    template_name = 'apps/docs/doc_index.html'

    try:
        all_docs = Document.objects.all().order_by('title')
    except ObjectDoesNotExist:
        all_docs = []

    viewable_docs = []

    # Filter down to viewable documents
    for doc in all_docs:
        if doc.is_published and \
                (doc.is_public or (not doc.is_public and request.user.is_authenticated)):
            viewable_docs.append(doc)

    context = {
        'pagetitle': 'Docs Index',
        'title': 'Docs Index',
        'docs': viewable_docs
    }

    return render(request, template_name, context)


def details(request):
    template_name = 'apps/docs/doc_details.html'

    context = {
        'pagetitle': 'Docs Details',
        'title': 'Docs Details',
    }

    page_id = request.GET.get('page_id', None)
    if page_id is None:
        return HttpResponseRedirect(reverse('summit.apps.docs:all_docs'))

    doc = None
    try:
        doc = Document.objects.get(page_id=page_id)
    except ObjectDoesNotExist:
        pass

    # If doc exists, if doc is published, and doc is viewable by user
    if doc is not None and doc.is_published and \
            (doc.is_public or (not doc.is_public and request.user.is_authenticated)):
        context['doc'] = doc
    else:
        context['doc'] = None

    return render(request, template_name, context)


@login_required()
def form(request):
    template_name = 'apps/docs/doc_form.html'
    page_id = request.GET.get('page_id', None)
    message = None

    if page_id is None:
        return HttpResponseRedirect(reverse('summit.apps.docs:all_docs'))

    form = DocumentForm()
    doc = None
    try:
        doc = Document.objects.get(page_id=page_id)
    except ObjectDoesNotExist:
        pass

    if doc is not None:
        form = DocumentForm(instance=doc)

    if request.method == "POST":
        form = DocumentForm(request.POST)

        # Form checking
        if form.is_valid():
            # Grab the user's profile
            try:
                profile = UserProfile.objects.get(user=request.user)
            except ObjectDoesNotExist:
                profile = None
                message = "You need to set up your user profile BEFORE you can make documents, projects, etc. Go to 'Welcome, {user name}' -> My Account for more details"

            if profile is not None:
                # Adding missing page_id and created_by if new doc
                if doc is None:
                    form.instance.page_id = page_id
                    form.instance.created_by = profile
                    # Edit info
                    form.instance.last_edited_by = profile

                    # Time to save and post to database
                    doc = form.save()
                else:
                    doc.last_edited_by = profile
                    doc.title = form.instance.title
                    doc.html_body = form.instance.html_body
                    doc.is_public = form.instance.is_public
                    doc.is_published = form.instance.is_published
                    doc.save()
                return HttpResponseRedirect(reverse('summit.apps.docs:doc_detail') + "?page_id=" + doc.page_id)



    context = {
        'pagetitle': 'Docs Form',
        'title': 'Docs Form',
        'form': form,
        'doc': doc,
        'message': message
    }

    return render(request, template_name, context)
