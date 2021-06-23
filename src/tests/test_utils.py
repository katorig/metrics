from main.utils.send_email import send_email, notifiable
import unittest
from dynaconf import settings


class TestMetrics(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_send_email(self):
        settings.METRICS_SEND_TO = "ekaterina.gruzdova@tele2.ru"
        self.assertEqual(send_email(text='TEST'), 'Notification was sent')

    def test_send_email_to_many_people(self):
        settings.METRICS_SEND_TO = "ekaterina.gruzdova@tele2.ru, andrey.a.bogomolov@tele2.ru"
        self.assertEqual(send_email(text='TEST'), 'Notification was sent')

    def test_notification(self):
        settings.METRICS_SEND_TO = "ekaterina.gruzdova@tele2.ru"
        settings.METRICS_MODEL_ID = 'test'

        @notifiable
        def foo(flag, notify=0):
            print('Function foo is working')
            if flag == 1:
                text = 'test'
                return 'Error! Stop', notify, text
            else:
                return 'OK GOOD'

        self.assertRaises(SystemExit, lambda: foo(1, 1))
        self.assertEqual('OK GOOD', foo(0, 1))
        self.assertRaises(SystemExit, lambda: foo(1))
        self.assertEqual('OK GOOD', foo(0))


if __name__ == '__main__':
    unittest.main()
