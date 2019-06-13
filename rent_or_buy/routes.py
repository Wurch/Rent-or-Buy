from flask import render_template, url_for, redirect, request
from rent_or_buy.forms import SimulationParams
from rent_or_buy.calc import imovel, param, buy_or_rent
from rent_or_buy.plotter import comparison_plot
from rent_or_buy import app

@app.route("/", methods=['GET', 'POST'])
def home():
    form = SimulationParams()

    if request.method == 'POST' and form.validate_on_submit():

        imovel_params = imovel(
            price = form.price.data,
            rent = form.rent.data,
            entrada = form.advance.data,
            valorization = form.valorization.data,
            )
        economic_params = param(
            rate_fin = form.fin_rate.data,
            prazo = form.fin_term.data,
            rate_invest = form.invest_yield.data,
        )

        return render_template(
            'result.html',
            form=form, 
            calculated=buy_or_rent(imovel_params, economic_params),
            plot=comparison_plot(imovel_params.increase(economic_params)[-1], imovel_params.invest_returns(economic_params)[-1])
        )
    if request.method == 'POST' and not form.validate_on_submit():
       return render_template('home.html', form=form) 
    
    form = SimulationParams()
    return render_template('home.html', form=form)


@app.route("/about")
def about():
   return render_template('about.html') 