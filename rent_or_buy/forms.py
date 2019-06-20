from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SubmitField
from wtforms.validators import InputRequired, Length

class SimulationParams(FlaskForm):
    #House Params:
    price = IntegerField(
        label='Valor do imóvel desejado',
        validators=[InputRequired(message='Campo Obrigatório')],
        default=400000)
    rent = IntegerField(label='Valor do aluguel de um imóvel equivalente', default=1600)
    advance = IntegerField(label='Valor de entrada do financiamento',  default=0)
    valorization = FloatField(label='Valorização do imóvel',  default=2.5)

    #Economic Params:
    fin_rate = FloatField(label='Juros do financiamento', default=9)
    fin_term = IntegerField(label='Prazo do financiamento', default=30)
    invest_yield = FloatField(label='Retorno no mercado financeiro', default=6.5)

    submit = SubmitField('Simular')

