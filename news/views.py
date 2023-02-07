from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import AddWebsite
from .models import Website
from .data_src import *
from .news_scrapper import *
from .utils import scrap_news





class NewsView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        scrapped_news = {}
        news = scrap_all_websites()
        for k, v in news.items():
            scrapped_news[k] = pd.DataFrame(v).to_html(escape=False, justify='center')
        return {'scrapped_news': scrapped_news}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class CryptoNewsView(TemplateView):
    template_name = 'news/crypto.html'

    def get_context_data(self, **kwargs):
        return {'news': cryptocomp_news().to_html(justify='center', escape=False)}





class TwitterView(TemplateView):
    template_name = 'news/twitter.html'



def websites(request):
    context = {}
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        websites = Website.objects.filter(user=profile)
        context['websites'] = websites
        context['add_form'] = AddWebsite()

        if request.method == 'POST':
            add_form = AddWebsite(request.POST)
            if add_form.is_valid():
                form_data = add_form.cleaned_data
                url = form_data['url']
                selector = form_data['selector']
                title = url.split('//')[1].split('.')[0]
                profile = UserProfile.objects.get(user=request.user)
                website = Website.objects.create(user=profile, title=title, url=url, selector=selector)
                website.save()


    return render(request, 'news/websites.html', context)








