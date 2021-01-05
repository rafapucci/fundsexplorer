# FundsExplorer Importer

FundsExplorer Importer is a Python script to handle and analysis [Clear](https://www.clear.com.br/) homebroker orders into the website [Funds Explorer](https://www.fundsexplorer.com.br/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -r requirements.txt
```

## Usage

```python
user = ReadUserFile('config/user.json') #json file with user and password from FundsExplorer
session = Login(user)
ReadFileFund('orders/orders.csv') #csv file from Clear homebroker
```

## user.json example file
```json
{
    "user": "email@email.com",
    "password": "senha123",
    "wallet": "xxxxx"
}

```

## Vídeo

[![FundsExplorerImporter](https://img.youtube.com/vi/oh6oY2mQWNI/0.jpg)](https://www.youtube.com/watch?v=oh6oY2mQWNI)