from django.shortcuts import render
from django.views import View


class CountryBranch:
    def __init__(self, slug, name_ru, title, city, phone, email="", note="", image="", show_image=False):
        self.slug = slug
        self.name_ru = name_ru
        self.title = title
        self.city = city
        self.phone = phone
        self.email = email
        self.note = note
        self.image = image
        self.show_image = show_image


BRANCHES = {
    "ukraine": CountryBranch(
        slug="ukraine",
        name_ru="Украина",
        title="Контакты - Украина",
        city="Одесса",
        phone="+380 67 676 7676",
        email="",
        note="Ценю потужность",
        image="",
        show_image=True,
    ),
    "bulgaria": CountryBranch(
        slug="bulgaria",
        name_ru="Болгария",
        title="Контакты - Болгария",
        city="Бургас",
        phone="+359 676 767 676",
        email="",
        note="Зравейте, казвам се Кари",
        image="",
        show_image=True,
    ),
    "china": CountryBranch(
        slug="china",
        name_ru="Китай",
        title="Контакты - Китай",
        city="Шанхай",
        phone="+86 676 767 6767",
        email="",
        note="你好！你好吗？你吃了？",
        image="",
        show_image=False,
    ),
}


class ContactsDetailView(View):
    template_name = 'contacts.html'

    def get(self, request, country=None):
        branch = BRANCHES.get(country)
        has_image = bool(branch and branch.show_image and branch.image)

        context = {
            'title': branch.title if branch else "Контакты — Karina's Empire",
            'country_info': branch,
            'has_image': has_image,
            'empire_data': {
                'branches_dict': BRANCHES,
                'branches_list': list(BRANCHES.values()),
                'hq_contacts': {
                    'phone': '+359 87 758 2495',
                    'phone_note': 'Отвечаю через месяц, все таки не один бизнес на моих плечах.',
                    'email': 'zinovevakarina569@gmail.com',
                    'email_note': 'Почту я не проверяю если что',
                },
            },
            'base_banner': "Karina's Empire • Отвечаем на сообщения раз в месяц",
            'footer_fund': "€4000 ice cream fund open",
        }
        return render(request, self.template_name, context)