import numpy as np
import pandas as pd

class imovel:
    def __init__(self, price, rent, valorization, entrada):
        self.price = price
        self.rent = rent
        self.valorization = valorization/100
        self.entrada = entrada
    
    def pmt(self, param):
        a = param.rate_fin * (1+param.rate_fin)**param.prazo
        b = (1+param.rate_fin)**param.prazo - 1
        return (a/b) * (self.price - self.entrada)
    
    def invest(self, param):
        rest = self.pmt(param) - self.rent
        return rest
    
    def invest_returns(self, param):
        x = []
        m = self.entrada
        
        if self.invest(param) > 0:    
            for i in param.nper():
                m = m*(1 + param.rate_invest) + self.invest(param)
                x.append(m)
            
            return x
        
        else:
            for i in param.nper():
                m = 0
                x.append(m)
            
            return x
    
    def increase(self, param):
        
        monthly_rate = ((1 + self.valorization)**(1/12)) -1
        
        return [self.price * (1+ monthly_rate )**i for i in param.nper()]

    # time untill you can buy in cash the house with the money saved 
    def pay_off(self, param):
        
        ret = self.invest_returns(param)
        house_price_ot = self.increase(param)

        for i in range(param.prazo):
            if ret[i] > house_price_ot[i]:
                return i/12
                
        return 0

    def acumumulated_financing(self, param):
        pmt = self.pmt(param)

        return [pmt * i for i in range(1, param.prazo+1)]
    
    
class param:
    def __init__(self, rate_fin, prazo, rate_invest):
        self.rate_fin = ((1 + rate_fin/100)**(1/12)) -1
        self.prazo = prazo * 12
        self.rate_invest = ((1 + rate_invest/100)**(1/12)) -1
        
    def nper(self):
        n = self.prazo + 1
        return np.arange(1, n)

def table(results, param_):
    
    df = pd.DataFrame.from_dict(results, orient='index').transpose()
    
    df = df[["pmt", "nom_invest", "invest_return", "house_final_price", "acumulated", "pay_off", "amount"]]
    
    df.columns = ["Parcela do financiamento",
                  "Disponibilidade mensal para investimento", 
                  "Saldo do Montante investido em {:.0f} anos".format(param_.prazo/12), 
                  "Valor da Casa em 30 anos", 
                  "Preço pago pelo imóvel no final do financiamento",
                  "Anos necessários para comprar o imóvel a vista",
                  "Preço do Imóvel se comprado a vista com as economias", 
            ]
    
    df = df.transpose()
    
    return df.to_html(header=False, classes='table', border=0)

def formatter(number):

        return "R$ {:,.2f}".format(number).replace(',', '#').replace('.', ',').replace('#', '.')

def wrapper(imovel_, param_, str_format=False):

    pay_off_ = imovel_.pay_off(param_)

    def formatter(number):

        return "R$ {:,.2f}".format(number).replace(',', '#').replace('.', ',').replace('#', '.')


    if str_format:
        results = {
            'pmt': formatter(imovel_.pmt(param_)),
            'nom_invest': formatter(imovel_.invest( param_)),
            'invest_return': formatter(imovel_.invest_returns(param_)[-1]),
            'house_final_price': formatter(imovel_.increase(param_)[-1]),
            'acumulated': formatter(imovel_.acumumulated_financing(param_)[-1]),
            'amount': formatter(imovel_.invest_returns(param_)[int(pay_off_*12)]),
            'pay_off':int(pay_off_),
            'rent':formatter(imovel_.rent)
        }
    else:
        results = {
            'pmt': imovel_.pmt(param_),
            'nom_invest': imovel_.invest( param_),
            'invest_return': imovel_.invest_returns(param_),
            'house_final_price': imovel_.increase(param_),
            'acumulated': imovel_.acumumulated_financing(param_),
            'amount': imovel_.invest_returns(param_)[int(pay_off_*12)],
            'pay_off':pay_off_,
            'rent': imovel_.rent
        }

    return results


def buy_or_rent(imovel_, param_):
    
    if imovel_.rent >= imovel_.pmt(param_):

        results = wrapper(imovel_, param_, str_format=True)
        
        results['worth_to'] = "very_buy"
        results['nom_invest'] = "R$ 0,00"
        results['pay_off'] = "&infin;"
        
        results['table'] = table(results, param_)

        return results
    
    if imovel_.rent < imovel_.pmt(param_):
        
        if imovel_.invest_returns(param_)[-1] > imovel_.increase(param_)[-1]:
            results = wrapper(imovel_, param_, str_format=True)
            results['worth_to'] = "rent"
            results['table'] = table(results, param_)
            return results

        else:
            results = wrapper(imovel_, param_, str_format=True)
            results['worth_to'] = "buy"
            results['table'] = table(results, param_)
            return results