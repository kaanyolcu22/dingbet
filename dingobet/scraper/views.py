from django.shortcuts import render

# Create your views here.
from flask import Flask
from TransfermarktClient import TransfermarktClient
from Live import parseLiveSoup

app = Flask(__name__)
transfermarktClient = TransfermarktClient()

@app.get("/live")
def live():
    soup = transfermarktClient.getLiveSoup()
    return parseLiveSoup(soup)

@app.get("/match-detail")
def matchDetail():
    return "match-detail"