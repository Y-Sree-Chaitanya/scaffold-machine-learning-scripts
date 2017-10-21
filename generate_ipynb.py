import argparse
import nbformat as nbf

nb = nbf.v4.new_notebook()

parser = argparse.ArgumentParser()
parser.add_argument("--train", "-trn", type=str, required=True)
parser.add_argument("--test","-tst",  type=str, required=True)
parser.add_argument("--output","-o",  type=str, required=True)
args = parser.parse_args()

train = args.train
test = args.test
output = args.output

extension_to_readfn = {"csv":"csv","json":"json","html":"html",".htm":"html","xlsx":"excel","xls":"excel"}

cells = []

readfiles_fn = "pd.read_"+extension_to_readfn[train.split('.').pop()]

cells.append(nbf.v4.new_code_cell("""import pandas as pd
train = """ + readfiles_fn +"('"+train+"""')
test = """ + readfiles_fn +"('"+test+"""')
train.head()"""))
cells.append(nbf.v4.new_code_cell("train.shape"))
cells.append(nbf.v4.new_code_cell("test.shape"))
cells.append((nbf.v4.new_code_cell("train.describe()"))
cells.append((nbf.v4.new_code_cell("train.corr()"))

if ".ipynb" not in output:
    nb_name = output + ".ipynb"
else:
    nb_name = output

nb['cells'] = cells

with open(nb_name, 'w') as f:
    nbf.write(nb, f)
