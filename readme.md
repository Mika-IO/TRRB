# TRRB BOOT

Trrb bot is a Python software to automate IQ Option inputs through scraping and analysis of the trader room indicators.

<p align="center">
  <img src="https://user-images.githubusercontent.com/55309160/87235970-43ad0500-c3b9-11ea-88c6-5c40ab72f7a3.PNG"/>
</p>

<p align="center">
   <img src="https://user-images.githubusercontent.com/55309160/87235972-47408c00-c3b9-11ea-9862-e933c44ef571.PNG"/>
</p>

###### OBS: This project is a proof  of concept. All methods of the class ROBO need to be refactored and have their responsibilities redistributed

## Installation

### Installing requirements

You must have python installed version 3.7 or higher

Just install all with:

'''
```bash
pip install -r requirements.txt
```

### Instantiating your own classes of bot

```
from robo import Robo
from userdata import email,password
import logging

id = 'name_of_your_bot_teste'
asset = 'EURUSD' 
value = 1
minutes = 1

if __name__ == "__main__":
    Iq = Robo(id, email, password, asset, value, minutes)
```

### Usage

Put your email and password in the userdata.py to IQ OPTION login like this:

```
email = 'your_email@email.email'
password = 'your_password
```
To execute the project the way it is:
   
    python main.py

## Todo 📝

>> Fazer rodar ✔️

>> Refatorar

>> Adicionar testes

>> Configurar modo PRATICE/REAL

>> Adicionar DB

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
