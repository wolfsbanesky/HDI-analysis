import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, send_file, render_template
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

with open("countryframes.pickle", 'rb') as handle:
        countryframes = pickle.load(handle)
        
with open("hdi.pickle", 'rb') as handle:
        hditable = pickle.load(handle)

combinedtable = pd.DataFrame(columns = countryframes["Afghanistan"].columns)

for val in countryframes.values():
        combinedtable = pd.concat([combinedtable, val])

comparedict = {}
for i in range(1, len(combinedtable.columns)):
        comparedict[str(i)] = combinedtable.columns[i]
comparedict.pop("13")
comparedict.pop("2")

comparedict2 = {}
i = 1
for key in comparedict.keys():
        comparedict2[str(i)] = comparedict[key]
        i += 1
for key, val in comparedict2.items():
        print(key + ":" + " " + val)

selectedstat = comparedict2[input("Select the Statistic to Compare to Human Development Index: ")]

print(selectedstat)

fig, ax = plt.subplots(figsize = (6,6))
ax = sns.set_style(style = "darkgrid")

app = Flask(__name__)

@app.route('/')
def home():
        return render_template('index.html')

@app.route('/visualize')
def visualize():
        sns.scatterplot(data = combinedtable, x = selectedstat, y = "Percent Change, Human Development Index")
        canvas = FigureCanvas(fig)
        img = io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype = 'img/png')

if __name__ == "__main__":
        app.run()