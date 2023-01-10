def criarDicionario(listaNomes,listaObjetos):
    dic = {}
    i = 0
    for nome in listaNomes:
        dic[nome] = listaObjetos[i]
        i+=1

    return dic