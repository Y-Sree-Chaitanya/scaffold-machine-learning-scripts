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
#cells.append(nbf.v4.new_text_cell("### Exploratory Data Analysis"))
cells.append(nbf.v4.new_code_cell("train.shape"))
cells.append(nbf.v4.new_code_cell("test.shape"))
cells.append(nbf.v4.new_code_cell("train.describe()"))
cells.append(nbf.v4.new_code_cell("train.corr()"))
cells.append(nbf.v4.new_code_cell("train.isnul().sum()"))
cells.append(nbf.v4.new_code_cell("""import matplotlib.pyplot as plt
train.hist()
plt.show()"""))
cells.append(nbf.v4.new_code_cell("train.hist()"))
#cells.append(nbf.v4.new_text_call("### Preprocessing :"))
cells.append(nbf.v4.new_code_cell("columns_with_nan = [x for x in train.columns if (train[x].isnull().sum() != 0)]"))
print("Data Imputation startegy ?")
print("1. Int with median, Categorical with mode, Float with mean.")
print("2. Dub all missing values as unknown and -999.")
ch = input()
code = """from sklearn.base import TransformerMixin"""
if(ch == "1"):
    code = code + """class DataFrameImputer(TransformerMixin):
               def __init__(self):
                              ""
                              #impute columns of categorical with most frequent value in coulmn
                              #impute columns of other types with mean of column
                              #can extend to impute columns of integer type with median values
               def fit(self,X,y=None):
                              self.fill = pd.Series([X[c].value_counts().index[0] if X[c].dtype == np.dtype('O') else X[c].median() if X[c].dtype == np.dtype('int') else X[c].mean() for c in X],index=X.columns)
                              return self
               def transform(self,X,y=None):
                              return X.fillna(self.fill)
            """
if(ch == "2"):
    code = code + """class DataFrameImputer(TransformerMixin):
               def __init__(self):
                              ""
                              #impute columns of categorical with most frequent value in coulmn
                              #impute columns of other types with mean of column
                              #can extend to impute columns of integer type with median values
               def fit(self,X,y=None):
                              self.fill = pd.Series(["unknown" if X[c].dtype == np.dtype('O') else -999 for c in X],index=X.columns)
                              return self
               def transform(self,X,y=None):
                              return X.fillna(self.fill)
            """
cells.append(nbf.v4.new_code_cell(code + "train = DataFrameImputer().fit_transform(train)"))

if ".ipynb" not in output:
    nb_name = output + ".ipynb"
else:
    nb_name = output

nb['cells'] = cells

with open(nb_name, 'w') as f:
    nbf.write(nb, f)
