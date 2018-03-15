from wtforms import Form, TextField, validators

class CreateCombatantForm(Form):
    names = TextField('Names', [validators.Length(min=5, max=70)])


class CombatantForm(Form):
    name = TextField('Name')