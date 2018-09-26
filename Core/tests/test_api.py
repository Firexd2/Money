import datetime
from random import randint

from django.test import TestCase

from Auth.models import User
from Core.models import Settings, Configuration, CostCategory, Tags, Cost, Archive


class TestAjaxApi(TestCase):

    def setUp(self):
        """
        Создает:
        - юзера со всеми настройками
        - план
        - три тэга
        - три категории
        - 100 трат, с рандомным значением суммы с 1 или с 2 метками и раскидывает их рандомно по всем категориям
        """
        self.user = User.objects.create(username='test')
        self.user.set_password('123')

        settings = Settings.objects.create()
        self.user.settings = settings
        self.user.save()

        self.configuration = Configuration.objects.create(name='Семья', income=100)
        self.user.settings.configurations.add(self.configuration)

        # создаем метки
        tags = []
        for tag_name in ('первая метка', 'вторая метка', 'третья метка'):
            tags.append(Tags.objects.create(name=tag_name, user=self.user.username))

        # создаем категории
        for name_cat in ('Тест1', 'Тест2', 'Тест3'):
            cat_obj = CostCategory.objects.create(name=name_cat, max=300)

            self.configuration.category.add(cat_obj)

        # создаем траты
        cost = Cost.objects.create(value=123)
        cost.tags.add(tags[0])
        cost = Cost.objects.create(value=123)
        cost.tags.add(tags[1])
        cost = Cost.objects.create(value=123)
        cost.tags.add(tags[2])
        cost = Cost.objects.create(value=123)
        cost.tags.add(tags[0], tags[1])
        cost = Cost.objects.create(value=123)
        cost.tags.add(tags[0], tags[2])

        # записываем все траты
        categoryes = CostCategory.objects.all()
        for cost in Cost.objects.all():
            category = categoryes[randint(0, 2)]
            category.cost.add(cost)

        response = self.client.login(username=self.user.username, password='123')
        self.assertTrue(response)

    def test_ajax_change_tags_in_current(self):
        """
        Проверка на то, что скрипт перевода с одной метки на другую работает в текущем плане
        """

        before_data_cost_tags = [
            {'id': 1, 'tags': ['первая метка']},
            {'id': 2, 'tags': ['вторая метка']},
            {'id': 3, 'tags': ['третья метка']},
            {'id': 4, 'tags': ['первая метка', 'вторая метка']},
            {'id': 5, 'tags': ['первая метка', 'третья метка']},
        ]
        current_data_cost_tags = [{'id': cost.id, 'tags': [tag.name for tag in cost.tags.all()]}
                                  for cost in Cost.objects.all()]

        self.assertListEqual(before_data_cost_tags, current_data_cost_tags)

        # все траты с первой меткой, переделываем в траты со второй меткой
        data = {'src-tag': 'первая метка', 'dst-tag': 'вторая метка', 'current-costs': 'on', 'delete-src-tag': 'on',
                'name': self.configuration.name}
        response = self.client.post('/ajax/change_tags/', data=data)
        self.assertEqual(200, response.status_code)

        after_data_cost_tags = [
            {'id': 1, 'tags': ['вторая метка']},
            {'id': 2, 'tags': ['вторая метка']},
            {'id': 3, 'tags': ['третья метка']},
            {'id': 4, 'tags': ['вторая метка']},
            {'id': 5, 'tags': ['вторая метка', 'третья метка']},
        ]
        current_data_cost_tags = [{'id': cost.id, 'tags': [tag.name for tag in cost.tags.all()]}
                                  for cost in Cost.objects.all()]

        self.assertListEqual(after_data_cost_tags, current_data_cost_tags)
        # проверяем, что первоначальный тэг удалился после перевода всех трат на другой тэг
        self.assertFalse(Tags.objects.filter(name='первая метка', user=self.user.username))

    def test_ajax_change_tags_in_archive(self):
        """
        Проверка на то, что скрипт перевода с одной метки на другую работает в архивах
        """

        archive1 = Archive.objects.create(date_one=datetime.datetime.now())
        archive1.archive_costs.add(*[cost for cost in Cost.objects.all()[:2]])
        archive2 = Archive.objects.create(date_one=datetime.datetime.now())
        archive2.archive_costs.add(*[cost for cost in Cost.objects.all()[2:]])

        self.configuration.archive.add(archive1, archive2)

        before_data_cost_tags = [
            {'id': 1, 'tags': ['первая метка']},
            {'id': 2, 'tags': ['вторая метка']},
            {'id': 3, 'tags': ['третья метка']},
            {'id': 4, 'tags': ['первая метка', 'вторая метка']},
            {'id': 5, 'tags': ['первая метка', 'третья метка']},
        ]
        current_data_cost_tags = [{'id': cost.id, 'tags': [tag.name for tag in cost.tags.all()]}
                                  for cost in Cost.objects.all()]

        self.assertListEqual(before_data_cost_tags, current_data_cost_tags)

        data = {'src-tag': 'первая метка', 'dst-tag': 'вторая метка', 'archive-costs': 'on', 'delete-src-tag': 'on',
                'name': self.configuration.name}
        response = self.client.post('/ajax/change_tags/', data=data)
        self.assertEqual(200, response.status_code)

        after_data_cost_tags = [
            {'id': 1, 'tags': ['вторая метка']},
            {'id': 2, 'tags': ['вторая метка']},
            {'id': 3, 'tags': ['третья метка']},
            {'id': 4, 'tags': ['вторая метка']},
            {'id': 5, 'tags': ['вторая метка', 'третья метка']},
        ]
        current_data_cost_tags = [{'id': cost.id, 'tags': [tag.name for tag in cost.tags.all()]}
                                  for cost in Cost.objects.all()]

        self.assertListEqual(after_data_cost_tags, current_data_cost_tags)
        # проверяем, что первоначальный тэг удалился после перевода всех трат на другой тэг
        self.assertFalse(Tags.objects.filter(name='первая метка', user=self.user.username))
