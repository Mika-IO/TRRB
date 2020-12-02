import logging

from robo import Robo
from userdata import email, password

if __name__ == "__main__":
    Iq = Robo("test001", email, password)

"""
    TO DO
    
___ Implementar logging e testes
___ Implementar stop loss e stop gain
___ Checar vitoria e derrota
___ Implementar o weight_of_indicators:
    - Somar caso o indicador acerte na compra ou venda
    - Subtrair se errar na compra ou venda e ignorar HOLD
___ Implementar sucess_rate com:
    - Saldo máximo da sessão
    - Saldo mínimo da sessão
    - Numero de entradas
    - Numero de acertos 
    - Numero de erros
    - Porcentagem_de_sucesso
"""
