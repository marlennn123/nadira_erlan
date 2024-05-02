my_list = ['Hotel','Room','PhotoRoom',
           'Booking','UserProfile',
           'Comment','Photo']

print(f'# автоматическое заполнение serializers')
for name in my_list:
    print(f"class {name}Serializer(serializers.ModelSerializer):\n\tclass Meta:\n\t\tmodel={name}\n\t\tfields='__all__'")
print(f'# автоматическое заполнение views')
for name in my_list:
    print(f"class {name}ViewSets(viewsets.ModelViewSet):\n\tqueryset = {name}.objects.all()\n\tserializer_class = {name}Serializer")
print(f'# автоматическое заполнение urls')
print('urlpatterns = [')
for name in my_list:
    print(f"\t path('{name.lower()}/', {name}ViewSets.as_view({{'get': 'list', 'post': 'create'}}),\n\t\tname='{name.lower()}_list'),")
    print(f"\t path('{name.lower()}/<int:pk>/', {name}ViewSets.as_view({{'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}}),\n\t\tname='{name.lower()}_detail'),")
print(']')



