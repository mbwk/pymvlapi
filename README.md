pymvlapi
========

A Python wrapper for the MarketingVillas API


Example Usage
-------------

```
>>> from pymvlapi.endpoint import MarketingVillasApi
>>> api = MarketingVillasApi("myusername", "mypassword")
>>> api.get_villa_list()
[{'villa_id': 'Shangri La', 'sort_name': 'Shangri La', 'base_url': 'shangri-la', 'name': 'Shangri La'}, {'villa_id': 'Yalta', 'sort_name': 'Yalta', 'base_url': 'yalta', 'name': 'Villa Yalta'}, ... ]
```

