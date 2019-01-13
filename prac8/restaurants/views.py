from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.models import User
from bson.objectid import ObjectId
import json
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic.base import TemplateView
from django.views.generic import DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

# Modelo restaurantes sin modelos DJANGO (directamente base de datos mongoDB)
from .models import rest_collec, district_collec
from .models import Dish, RestaurantModel

from .forms import DishForm
# Create your views here.


class HomePageView(TemplateView):
    template_name = "index.html"


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    context_object_name = 'user_profile'
    model = User
    template_name = 'registration/my_page.html'
    slug_field = 'username'

# RESTAURANTS VIEWS
# Restaurants views old way

# Search rests view (only work with mongoDB)


@method_decorator(login_required, name='dispatch')
class SearchRestView(TemplateView):

    template_name = "restaurants/found_rest.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_search = self.request.GET.get('filter')
        type_search = self.request.GET.get('tipo_busqueda')

        restaurants = []

        if type_search == "rest_name":
            type_search = "name"

            for rest in rest_collec.find({type_search: {"$regex": ".*"+filter_search+".*", "$options": 'i'}}):
                restaurants.append(rest)
        elif type_search == "district_name":
            type_search = "name"
            found_district = district_collec.find_one(
                {type_search: {"$regex": ".*"+filter_search+".*", "$options": 'i'}})

            for rest in rest_collec.find({"location": {"$geoWithin": {"$geometry": found_district['geometry']}}}):
                restaurants.append(rest)

        print(len(restaurants))
        context = {
            "restaurants": restaurants,
            "len_rest": len(restaurants)
        }

        return context

# Edit rest view


@method_decorator(login_required, name='dispatch')
class EditRestView(TemplateView):
    template_name = 'restaurants/edit_rest.html'

    def get(self, request, **kwargs):
        rest_id = request.GET.get('rest_id')

        rest = rest_collec.find_one(ObjectId(rest_id))
        context = {"rest": rest}  # set your context
        return super(TemplateView, self).render_to_response(context)

    def post(self, request, **kwargs):
        try:
            rest_id = request.POST.get('rest_id')
            rest_name = request.POST.get('rest_name')
            rest_location = request.POST.get('rest_location')

            print(rest_id, " ", rest_name, " ", rest_location)
            rest_collec.find_one_and_update({"_id": ObjectId(rest_id)}, {'$set': {
                "name": rest_name,
                "location": rest_location
            }})
            print('Rest Modification done..')
            context = {"modified": True}  # set your context
        except:
            print('Rest Modification failed..')

        return super(TemplateView, self).render_to_response(context)


# NEW WAY (mongo and django ORM)
# Create restaurant
@method_decorator(login_required, name='dispatch')
class RestaurantCreateView(CreateView):
    template_name = 'restaurants/insert_rest.html'
    model = RestaurantModel
    fields = ['name', 'location']
    #success_url = reverse_lazy('dish_insert')

    def form_valid(self, form):
        self.object = form.save()

        context = self.get_context_data(form=form)
        context = {
            'inserted': True
        }

        return self.render_to_response(context)

# List rest


@method_decorator(login_required, name='dispatch')
class RestListView(ListView):
    template_name = 'restaurants/list_rest.html'
    model = RestaurantModel

    def get_queryset(self):
        rest_name = self.request.GET.get('filter')
        type_search = self.request.GET.get('tipo_busqueda')

        if type_search == "rest_name":
            type_search = "name"

        if(rest_name == None):
            rest_name = ""

        restaurants = []
        """ for rest in rest_collec.find({type_search: {"$regex": ".*"+rest_name+".*", "$options": 'i'}}):
            restaurants.append(rest) """
        return rest_collec.find_one()

    def get_context_data(self, **kwargs):
        filter_name = self.request.GET.get('filter')
        type_search = self.request.GET.get('tipo_busqueda')
        # Call the base implementation first to get a context
        context = super(RestListView, self).get_context_data(**kwargs)
        # Add in the filter
        context['filter_name'] = filter_name
        context['type_search'] = type_search

        return context


def busqueda_restaurantes(request):
    filter_name = request.GET.get('filterName')
    type_search = request.GET.get('typeSearch')
    page_length = request.GET.get('pageLength')
    num_page = request.GET.get('numPage')

    """ list_rests = RestaurantModel.objects.filter(
        name__contains=filter_name).order_by('name') """
    list_rests = []
    if type_search == "rest_name":
        type_search = "name"
        for rest in rest_collec.find({type_search: {"$regex": ".*"+filter_name+".*", "$options": 'i'}}):
            list_rests.append(rest)
    elif type_search == "district_name":
        type_search = "name"
        found_district = district_collec.find_one(
            {type_search: {"$regex": ".*"+filter_name+".*", "$options": 'i'}})
        for rest in rest_collec.find({"location": {"$geoWithin": {"$geometry": found_district['geometry']}}}):
            list_rests.append(rest)

    paginator = Paginator(list_rests, page_length)

    try:
        list_rests = paginator.get_page(num_page)
    except PageNotAnInteger:
        list_rests = paginator.get_page(int(num_page))
    except EmptyPage:
        list_rests = paginator.get_page(paginator.num_pages)

    list_rest = []

    for rest in list_rests:
        loc = str(rest['location']).replace("\'", "\"")
        locjson = json.loads(loc)

        restaurant = {
            'id': str(rest['_id']),
            'name': str(rest['name']),
            'location': locjson['coordinates']
        }
        list_rest.append(restaurant)

    rests = {
        'rests': list_rest,
        'pageLength': page_length,
        'numPage': num_page,
        'num_pages': paginator.num_pages,
        'num_rests': paginator.count
    }
    return JsonResponse(rests, safe=False)


# Edit Restaurant


@method_decorator(login_required, name='dispatch')
class RestEditView(UpdateView):
    template_name = 'restaurants/edit_rest.html'
    model = RestaurantModel
    fields = ['name', 'location']

    def form_valid(self, form):
        self.object = form.save()

        context = self.get_context_data(form=form)
        context = {
            'modified': True
        }

        return self.render_to_response(context)

# Delete Restaurant


@method_decorator(login_required, name='dispatch')
class RestDeleteView(DeleteView):
    model = RestaurantModel

    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        return reverse_lazy('rest_found')

# Map restaurant


class MapRestaurantView(TemplateView):
    template_name = 'restaurants/map_rest.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        longitud = kwargs.get('lon')
        latitud = kwargs.get('lat')
        context['longitud'] = longitud
        context['latitud'] = latitud
        return context


# Highcharts view
class ChartView(TemplateView):
    template_name = 'graphics.html'


# Obtain districts in JSON format
def getRestByDistricts(request):
    districts_names = list()
    districts_num = list()

    for district in district_collec.find():
        district_name = district['name']
        num_rests = 0
        num_rests = rest_collec.count_documents(
            {"location": {"$geoWithin": {"$geometry": district['geometry']}}})

        districts_names.append(district_name)
        districts_num.append(num_rests)

    district_rests = {
        'names': districts_names,
        'num_rests': districts_num
    }

    return JsonResponse(district_rests, safe=False)


# DISHES VIEWS
# Create dish


@method_decorator(login_required, name='dispatch')
class DishCreateView(CreateView):
    template_name = 'dishes/insert_dish.html'
    model = Dish
    fields = ['name', 'type_cousine', 'allergens', 'price']
    #success_url = reverse_lazy('dish_insert')

    def form_valid(self, form):
        self.object = form.save()

        context = self.get_context_data(form=form)
        context = {
            'inserted': True
        }

        return self.render_to_response(context)

# List dish


@method_decorator(login_required, name='dispatch')
class DishListView(ListView):
    template_name = 'dishes/list_dishes.html'
    model = Dish


# Edit dish
@method_decorator(login_required, name='dispatch')
class DishEditView(UpdateView):
    template_name = 'dishes/edit_dish.html'
    model = Dish
    fields = ['name', 'type_cousine', 'allergens', 'price']

    def form_valid(self, form):
        self.object = form.save()

        context = self.get_context_data(form=form)
        context = {
            'modified': True
        }

        return self.render_to_response(context)

# Delete dish


@method_decorator(login_required, name='dispatch')
class DishDeleteView(DeleteView):
    model = Dish
    success_url = reverse_lazy('dish_list')
