from django.shortcuts import render
from django.views import View

COUNTRY_DATA = {
    "ukraine": {
        "title": "Контакты - Украина",
        "city": "Одесса",
        "phone": "+380 67 676 7676",
        "email": "",
        "note": "Ценю потужность",
        "image": "images/ukraine.jpg",
        "show_image": True,
    },
    "bulgaria": {
        "title": "Контакты - Болгария",
        "city": "Бургас",
        "phone": "+359 676 767 676",
        "email": "",
        "note": "Зравейте, казвам се Кари",
        "image": "images/bulgaria.jpg",
        "show_image": True,
    },
    "china": {
        "title": "Контакты - Китай",
        "city": "Шанхай",
        "phone": "+86 676 767 6767",
        "email": "",
        "note": "你好！你好吗？你吃了？",
        "image": "",
        "show_image": False,
    }
}

class ContactsDetailView(View):
    template_name = 'contacts.html'

    def get(self, request, country=None):
        info = COUNTRY_DATA.get(country)
        has_image = bool(info and info.get('show_image') and info.get('image'))

        context = {
            'title': info['title'] if info else 'Контакты — Karina\'s Empire',
            'country_info': info,
            'has_image': has_image,
            'countries': COUNTRY_DATA,
        }
        return render(request, self.template_name, context)