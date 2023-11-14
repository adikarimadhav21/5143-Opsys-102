from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import glob
import subprocess

app = Flask(__name__)

def plot_metrics(files):
    fig, axs = plt.subplots(1, 5, figsize=(20, 3))
    metrics = ['ATAT', 'ARWT', 'AIWT', 'CPU_UTIL', 'IO_UTIL']
    colors = ['blue', 'green', 'orange', 'red', 'purple', 'yellow', 'cyan', 'magenta', 'brown', 'black']
    legend_labels = []  

    for i, metric in enumerate(metrics):
        for j, file in enumerate(files):
            df = pd.read_csv(file)
            values = df[metric].values

         
            label = j  
            axs[i].bar(label, values, color=colors[j])  
            axs[i].set_title(metric)
            axs[i].set_ylabel('Values')

         
            if i == 1:  
                legend_labels.append(f'{j} -> {file}' )
                

    plt.tight_layout()
    
    
    fig.subplots_adjust(bottom=0.2)
    fig.legend(legend_labels, loc='lower center', ncol=len(legend_labels), fontsize='small')

    img = io.BytesIO()
    plt.savefig(img, format='svg')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return f"<img src='data:image/svg+xml;base64,{plot_url}'>"

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/plot', methods=['POST'])
def plot():
    selected_algo = request.form['algorithm']
    if selected_algo == 'FCFS':
        files = glob.glob('overall_stats_FCFS_*')
        plot = plot_metrics(files)
        return plot
    elif selected_algo == 'RR':
        files = glob.glob('overall_stats_RR_*.dat')
        plot = plot_metrics(files)
        return plot
    elif selected_algo == 'PB':
        files = glob.glob('overall_stats_PB_*.dat')
        plot = plot_metrics(files)
        return plot
    elif selected_algo == 'Combined':
        subprocess.run(["python3", "combined-visualisation.py"])
        return " "
    else:
        return "Algorithm not recognized"

if __name__ == '__main__':
    app.run(debug=True)
