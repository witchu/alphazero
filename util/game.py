from importlib import import_module

def importState(game):
    return import_module(game + '.state')

def importPlayer(game):
    return import_module(game + '.player')

def importNn(game):
    return import_module(game + '.nn')
