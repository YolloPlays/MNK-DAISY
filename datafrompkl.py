import pickle as pl

model = pl.load(open("best_model.pkl", "rb"))

print(model.get_params())
