memory = {}

def save(company, data):
    memory[company] = data

def load(company):
    return memory.get(company, None)