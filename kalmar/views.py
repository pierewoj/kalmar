from django.shortcuts import render, get_object_or_404
import redis
import json

def search(request):
    bag = {}   

    r = redis.StrictRedis(host='burrito', port=6379, db=0)
    query = request.GET.get('query', 'ddd')
    all_ing = r.smembers('ingredients')
    filtered_ing = filter(lambda x: query in x.decode("utf-8"), all_ing)
    all_recip_ids=set()
    for ing in filtered_ing:
        recip_ids = r.smembers(ing)
        all_recip_ids = all_recip_ids.union(recip_ids)

    recipies = []
    for recip_id in all_recip_ids:
        recip_json = r.get(recip_id).decode("utf-8")
        recip = json.loads(recip_json)
        recipies.append(recip)

    bag['recipies'] = recipies;
    return render(request, 'kalmar/search.html', bag)
