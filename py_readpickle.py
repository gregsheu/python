import pickle
with open('kingsolarman88gmail.pickle', 'rb') as token:
    creds = pickle.load(token)


print(pickle.dumps(creds))
