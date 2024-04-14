import joblib

clf2 = joblib.load("model.pkl")


with open('test.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()


results = clf2.predict(lines)
for result in results:
    print(result)