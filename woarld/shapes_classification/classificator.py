import pickle

with open("shapes_classification/nn_model.pickle", "rb") as f:
    nn_model = pickle.load(f)
