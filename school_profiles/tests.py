from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from school_profiles.forms import StudentProfileForm


class CreateStudentProfileFormTests(TestCase):
    def test_form_valid(self):
        form = StudentProfileForm(data={'date_of_birth': '1980-07-31', 'names': 'Harry James', 'pesel': '000000000',
                                        'place_of_birth': "Godric's Hollow", 'surname': 'Potter'})
        # ^ Obviously this is not Harry's Potter PESEL
        self.assertTrue(form.is_valid())

    def test_required_date_of_birth_field(self):
        form = StudentProfileForm(data={})
        self.assertIn(_('This field is required.'), form.errors['date_of_birth'])

        form = StudentProfileForm(data={'date_of_birth': '1980-07-31'})  # Yes, Harry's Potter day of birth
        self.assertRaises(KeyError, lambda: form.errors['date_of_birth'])

    def test_required_names_field(self):
        form = StudentProfileForm(data={})
        self.assertIn(_('This field is required.'), form.errors['names'])

        form = StudentProfileForm(data={'names': 'Harry James'})
        self.assertRaises(KeyError, lambda: form.errors['names'])

    def test_required_place_of_birth_field(self):
        form = StudentProfileForm(data={})
        self.assertIn(_('This field is required.'), form.errors['place_of_birth'])

        form = StudentProfileForm(data={'place_of_birth': "Godric's Hollow"})  # Yes, Harry's Potter place of birth
        self.assertRaises(KeyError, lambda: form.errors['place_of_birth'])

    def test_required_surname_field(self):
        form = StudentProfileForm(data={})
        self.assertIn(_('This field is required.'), form.errors['surname'])

        form = StudentProfileForm(data={'surname': 'Potter'})
        self.assertRaises(KeyError, lambda: form.errors['surname'])
