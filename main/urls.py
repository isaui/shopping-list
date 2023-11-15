from django.urls import path
from main.views import show_main, create_product_flutter,edit_product_ajax,create_product,get_product_ajax, get_product_json,add_product_ajax,delete_product_ajax,show_xml, delete_product,show_json, show_xml_by_id, show_json_by_id , edit_product,register, login_user
from main.views import logout_user
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('get-product/', get_product_json, name='get_product_json'),
    path('get-product-ajax/<int:product_id>/', get_product_ajax, name='get_product_ajax'),
    path('create-product-ajax/', add_product_ajax, name='add_product_ajax'),
    path('delete-product-ajax/', delete_product_ajax, name='delete_product_ajax'),
    path('edit-product-ajax/', edit_product_ajax, name='edit_product_ajax'),
    path('create-product', create_product, name='create_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit/<int:id>', edit_product, name="edit_product" ),
    path('delete/<int:id>', delete_product, name='delete_product'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),

]
