import os
import pandas as pd
import matplotlib.pyplot as plt

current_directory = os.getcwd()

def slice_rr(filename):
    return filename[16:]

def slice_pb(filename):
    return filename[16:]

def slice_fcfs(filename):
    return filename[18:]

similar_outputs = {}

for f in os.listdir(current_directory):
    if os.path.isfile(os.path.join(current_directory, f)):
        extracted_slice = None
        if f.startswith("overall_stats_RR_"):
            extracted_slice = slice_rr(f)
        elif f.startswith("overall_stats_PB_"):
            extracted_slice = slice_pb(f)
        elif f.startswith("overall_stats_FCFS_"):
            extracted_slice = slice_fcfs(f)

        if extracted_slice is not None:
            if extracted_slice in similar_outputs:
                similar_outputs[extracted_slice].append(f)
            else:
                similar_outputs[extracted_slice] = [f]

for slice_files in similar_outputs.values():
    if len(slice_files) > 1: 
        data = {metric: [] for metric in ['ATAT', 'ARWT', 'AIWT', 'CPU_UTIL', 'IO_UTIL']}
        fig, axs = plt.subplots(1, len(data), figsize=(15, 5))

        plt.suptitle('Cpu Scheduling Algorithms', fontsize=16)

        for i, metric in enumerate(data):
            for j, file in enumerate(slice_files):
                df = pd.read_csv(file)
                data[metric].append(df[metric].values[0])
                axs[i].bar(j, data[metric][j])

            axs[i].set_ylabel('Values')
            axs[i].set_xticks(range(len(slice_files)))
            axs[i].set_xticklabels([file[14:-10] for file in slice_files], rotation=45)
            axs[i].set_title(f'{metric} Metrics')

        axs[0].set_xlabel('')

      
        fig.legend(slice_files, loc='lower center', ncol=len(slice_files), fontsize='small')

        plt.tight_layout()
        plt.subplots_adjust(top=0.8)  
        plt.show()
