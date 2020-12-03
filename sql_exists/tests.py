from django.conf import settings
from django.db import connection
from django.test import TestCase
from django.db.models import Exists, OuterRef

from sql_exists.factories import ColorFactory, AppleFactory
from sql_exists.models import Color, Apple


class TestM2MExists(TestCase):
    def test_exists(self):
        ColorFactory(name='緑')
        yellow = ColorFactory(name='黄')
        red = ColorFactory(name='赤')
        AppleFactory(name='シナノゴールド', color=yellow)
        AppleFactory(name='シナノスイート', color=red)
        AppleFactory(name='フジ', color=red)
        AppleFactory(name='シナノドルチェ', color=red)

        colors = Color.objects.filter(
            Exists(Apple.objects.filter(color=OuterRef('pk')))
        )

        # テストコードでは常にDEBUG=Falseになり、connection.queriesが取得できないことから強制書き換え
        # なお、今回の場合SQLが発行されるのは、list()のタイミング
        # ちなみに、Django1.11からはmanage.pyのオブションに `--debug-mode` もある
        # https://docs.djangoproject.com/en/3.1/ref/django-admin/#cmdoption-test-debug-mode
        settings.DEBUG = True

        self.assertListEqual(list(colors), [yellow, red])

        for query in connection.queries:
            print(query)

        settings.DEBUG = False
