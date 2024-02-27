import pickle

def serialize(classe:object):
    serialized_data = pickle.dumps(classe)
    return serialized_data
    
def deserialize(serialized_data):
    classe = pickle.loads(serialized_data)
    return classe

def fragment_msg(mensagem,size_required):
    fragmentos = []
    tamanho_mensagem = len(mensagem)
    tamanho_fragmento = size_required

    for i in range(0, tamanho_mensagem, tamanho_fragmento):
        fragmento = mensagem[i:i+tamanho_fragmento]
        fragmentos.append(fragmento)
    
    return fragmentos