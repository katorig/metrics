from main.utils.send_email import send_email, notification
import unittest

send_to = "ekaterina.gruzdova@tele2.ru"


class TestMetrics(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_send_email(self):
        kwargs = {"send_to": send_to, "subject": "TEST", "text": "test"}
        self.assertEqual(send_email(kwargs), 'Notification was sent')

    def test_send_email_to_many_people(self):
        kwargs = {"send_to": "ekaterina.gruzdova@tele2.ru, andrey.a.bogomolov@tele2.ru",
                  "subject": "TEST", "text": "test"}
        self.assertEqual(send_email(kwargs), 'Notification was sent')

    def test_do_not_send_email(self):
        kwargs = {}
        self.assertRaises(KeyError, lambda: send_email(kwargs))

    def test_notification(self):
        @notification
        def foo(flag, **kwargs):
            print('Function foo is working')
            if flag == 1:
                return 'Error! Send notification'
            else:
                return 'OK'

        self.assertRaises(SystemExit, lambda: foo(1, send_to=send_to, subject='TEST', text='test'))
        self.assertEqual('OK', foo(0, send_to=send_to, subject='TEST', text='test'))
        self.assertRaises(SystemExit, lambda: foo(1))
        self.assertEqual('OK', foo(0))


if __name__ == '__main__':
    unittest.main()
