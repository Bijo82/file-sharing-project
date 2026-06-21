from redis import Redis

Redis = Redis(host="localhost", port=6379, decode_responses=True) #without decode reponses it will give output as b'hello'

# r.set("france","paris")
# r.set("germany","berlin")

# france_cap = r.get("france")
# germany_cap = r.get("germany")

# print(france_cap)
# # print(germany_cap)

# r.set("0rt34f","filename:bijo,fileid:1,memory:file")

# print(r.get("0rt34f"))