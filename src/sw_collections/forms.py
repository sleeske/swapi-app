from django import forms

from sw_collections.providers.swapi.entities import Person


class ColumnsForm(forms.Form):
    OPTIONS = (
        (Person.Columns.NAME, Person.Columns.NAME),
        (Person.Columns.HEIGHT, Person.Columns.HEIGHT),
        (Person.Columns.MASS, Person.Columns.MASS),
        (Person.Columns.HAIR_COLOR, Person.Columns.HAIR_COLOR),
        (Person.Columns.SKIN_COLOR, Person.Columns.SKIN_COLOR),
        (Person.Columns.EYE_COLOR, Person.Columns.EYE_COLOR),
        (Person.Columns.BIRTH_YEAR, Person.Columns.BIRTH_YEAR),
        (Person.Columns.GENDER, Person.Columns.GENDER),
        (Person.Columns.HOMEWORLD, Person.Columns.HOMEWORLD),
        (Person.RenamedColumns.DATE, Person.RenamedColumns.DATE),
    )

    columns = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=OPTIONS
    )
