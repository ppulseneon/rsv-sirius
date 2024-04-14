import joblib

def get_category(model, text):
    clf2 = joblib.load(model)
    predicted = [text]

    category = clf2.predict(predicted)
    return category[0]
