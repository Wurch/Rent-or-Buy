from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.models.formatters import FuncTickFormatter
from bokeh.embed import components
import random

def comparison_plot(house_final_price, invested_amount):

    x = ["Valor do Imóvel", "Montante Acumulado"]
    y = [house_final_price, invested_amount]

    p = figure(x_range=x, plot_width=400, plot_height=400, title="Valores ao final do financiamento", toolbar_location=None, tools="")
    p.vbar(x=x, width=0.9, bottom=0,
        top=y, color=random.sample(Spectral6, k=len(x)))

    def ticker():
        return "R$ {:,} mil".format(tick/1000)

    p.yaxis.formatter = FuncTickFormatter.from_py_func(ticker)
    p.sizing_mode = "scale_width"

    return components(p)
