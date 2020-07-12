from robo import Robo
from userdata import email,password
import logging

if __name__ == "__main__":
    Iq = Robo('test001',email,password)

"""
To do:
___ implementar o weight_of_indicators persistente no banco de dados como indicadores:pesos
    somar caso o indicador acerte na compra ou venda, subtrair se errar na compra ou venda e ignorar HOLD
___ implementar sucess_rate com [acertos,erros,porcentagem_de_sucesso] pesistente no banco de dados
___ implementar buy_or_sell()
"""