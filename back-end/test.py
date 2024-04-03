from utils import Result
import json


print(type(Result.success("sss")))
res = json.loads(Result.success("sss"))

print(res['code'])

# print(json.load(Result.success("sss")).code)