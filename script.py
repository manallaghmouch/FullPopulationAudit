import random
import os
import csv 
import pickle

import numpy as np
import pandas as pd

from imblearn.over_sampling import RandomOverSampler, SMOTE
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

# Input parameters
num_logs = 100 # number of logs to create and to use for classification
percentages = [0.01, 0.02, 0.05]
total_iterations = 100

# Create dictionaries to store results
results_DT_dict = {}
results_RF_dict = {}
perc_anomalies_in_sample_dict = {}
len_deviations_dict = {}

# Open pickle files 
with open('X_df_audit_dict100.pkl', 'rb') as f:
    df_audit_dict = pickle.load(f)
with open('X_df_norm_dict100.pkl', 'rb') as f:
    df_norm_dict = pickle.load(f)
with open('X_deviations_dict100.pkl', 'rb') as f:
    deviations_dict = pickle.load(f)
with open('X_traces_dict100.pkl', 'rb') as f:
    traces_dict = pickle.load(f)
with open('X_eventlog_dict100.pkl', 'rb') as f:
    eventlog_dict = pickle.load(f)
with open('X_model_dict_audit100.pkl', 'rb') as f:
    model_dict_audit = pickle.load(f)
with open('X_model_dict_norm100.pkl', 'rb') as f:
    model_dict_norm = pickle.load(f)



# Define noise functions
def flip_labels(y, fraction):
    n_flip = int(len(y) * fraction)
    flip_indices = np.random.choice(len(y), n_flip, replace=False)
    y_noisy = y.copy()
    y_noisy.iloc[flip_indices] = np.random.choice([0, 1], n_flip)
    return y_noisy

def alter_rule_satisfaction(X, fraction):
    X_noisy = X.copy()
    n_alter = int(X_noisy.size * fraction)
    alter_indices = (np.random.choice(X_noisy.shape[0], n_alter), np.random.choice(X_noisy.shape[1], n_alter))
    X_noisy.values[alter_indices] = 1 - X_noisy.values[alter_indices]
    return X_noisy

def introduce_missing_rules(X, fraction):
    X_noisy = X.copy()
    n_missing = int(X_noisy.size * fraction)
    missing_indices = (np.random.choice(X_noisy.shape[0], n_missing), np.random.choice(X_noisy.shape[1], n_missing))
    X_noisy.values[missing_indices] = -1
    return X_noisy


# Define function to get performance metrics of classifier 
def save_mean_performance_in_dict(classifier, number_of_repetions, X_train, X_test, y_train, y_test):
    if classifier not in ['DT', 'RF']:
        raise ValueError("Invalid classifier. Choose 'DT' for Decision Tree or 'RF' for Random Forest.")

    temp_dict = {}
    performance_metrics = ["accuracy", "precision", "recall", "f1_score", "auc_score"]

    # apply classifier multiple times 
    for j in range(1, number_of_repetions + 1):

        if classifier == 'DT':
            clf = DecisionTreeClassifier()
        elif classifier == 'RF':
            clf = RandomForestClassifier()
        
        clf = clf.fit(X_train,y_train)
        y_pred = clf.predict(X_test)

        # print(clf.feature_importances_)

        nr_of_values_predicted = len(np.unique(y_pred))
        nr_of_values_true = len(np.unique(y_test))

        for i in performance_metrics: 
            temp_dict[i] = {}

            if i == "accuracy":
                temp_dict[i][j] = metrics.accuracy_score(y_test, y_pred)
            elif i == "precision":
                temp_dict[i][j] =  metrics.precision_score(y_test, y_pred) if nr_of_values_predicted > 1 else 0
            elif i == "recall":
                temp_dict[i][j] = metrics.recall_score(y_test, y_pred) if nr_of_values_predicted > 1 else 0
            elif i == "f1_score":
                temp_dict[i][j] = metrics.f1_score(y_test, y_pred) if nr_of_values_predicted > 1 else 0
            elif i == "auc_score":
                temp_dict[i][j] = metrics.roc_auc_score(y_test, y_pred) if nr_of_values_predicted > 1 & nr_of_values_true > 1 else 0

    # Calculate mean performance
    metrics_dict = {}
    for i in performance_metrics: 
        if i == "accuracy":
            metrics_dict[i] = np.array(list(temp_dict["accuracy"].values())).mean()
        elif i == "precision":
            metrics_dict[i] = np.array(list(temp_dict["precision"].values())).mean()
        elif i == "recall":
            metrics_dict[i] = np.array(list(temp_dict["recall"].values())).mean()
        elif i == "f1_score":
            metrics_dict[i] = np.array(list(temp_dict["f1_score"].values())).mean()
        elif i == "auc_score":
            metrics_dict[i] = np.array(list(temp_dict["auc_score"].values())).mean()

    return metrics_dict

random.seed(42)

# Classification
for h in range(1, num_logs+1):

    if h in traces_dict.keys():

        results_DT_dict[h] = {}
        results_RF_dict[h] = {}
        perc_anomalies_in_sample_dict[h] = {}
        len_deviations_dict[h] = {}

        for value in percentages: 

            perc_anomalies_in_sample_dict[h][value] = {}
            len_deviations_dict[h][value] = {}
            results_DT_dict[h][value] = {}
            results_RF_dict[h][value] = {}

        
            for i in range(1, 1+1):
            
                len_deviations = random.randint(100,1000) # total number of deviations that will be used for training and test purposes

                if len_deviations < len(traces_dict[h][value]):
                        
                    len_deviations_dict[h][value][i] = len_deviations
                    data = traces_dict[h][value].sample(len_deviations)
                    
                    # get index of 'label' column
                    label_index = data.columns.get_loc('label')

                    # select all columns after 'label' column
                    features = data.iloc[:, label_index + 1:]

                    X_train = features 
                    y_train = data['label'] 
                    
                    perc_anomalies_in_sample_dict[h][value][i] = np.sum(y_train)/len(y_train)

                    y_noisy = flip_labels(y_train, 0.05)  
                    # X_noisy1 = alter_rule_satisfaction(X_train, 0)  
                    # X_noisy = introduce_missing_rules(X_noisy1, 0)  

                    training_examples = data['case:concept:name'].tolist()
                    population = traces_dict[h][value]
                    test_set = population[~population['case:concept:name'].isin(training_examples)]

                    label_index_test = test_set.columns.get_loc('label')
                    features_test = test_set.iloc[:, label_index + 1:]

                    X_test = features_test
                    y_test = test_set['label'] 

                    nr_of_y_values = len(np.unique(y_train))    

                    if nr_of_y_values > 1:
                        # Random Oversampling (ROS)
                        X_resampled, y_resampled = RandomOverSampler().fit_resample(X_train, y_noisy)

                        metrics_DT_dict = save_mean_performance_in_dict("DT", 10, X_resampled, X_test, y_resampled, y_test)
                        metrics_RF_dict = save_mean_performance_in_dict("RF", 10, X_resampled, X_test, y_resampled, y_test)

                    else:
                        # metrics_DT_dict = save_mean_performance_in_dict("DT", 1, X_train, X_test, y_train, y_test)
                        # metrics_RF_dict = save_mean_performance_in_dict("RF", 1, X_train, X_test, y_train, y_test)  
                        pass                 

                    results_DT_dict[h][value][i] = metrics_DT_dict
                    results_RF_dict[h][value][i] = metrics_RF_dict

                    print(metrics_DT_dict)
                    print(metrics_RF_dict)

                else:
                    pass 
                
    else: 
        pass


# Store dictionaries
with open('results_RF_dict_10_noise.pkl', 'wb') as f:
    pickle.dump(results_RF_dict, f)
with open('results_DT_dic_10_noiset.pkl', 'wb') as f:
    pickle.dump(results_DT_dict, f)
with open('len_deviations_dict_10_noise.pkl', 'wb') as f:
    pickle.dump(len_deviations_dict, f)
with open('perc_anomalies_in_sample_dict_10_noise.pkl', 'wb') as f:
    pickle.dump(perc_anomalies_in_sample_dict, f)

# function to delete previous files from directory
# def remove_files(directory,start_with,end_with):
#     df=pd.DataFrame()
#     os.chdir(directory)
#     for file in os.listdir():
#         if file.startswith(str(start_with)) & file.endswith(str(end_with)):
#             os.remove(file)
#             print("file removed")
#     return df

# directory = 'G:\\Shared drives\\PhD Manal\\Projects\\Git\\DeclareModelHierarchy'

# remove_files(directory,'test','csv')

# Save results in csv files
for h in range(1, num_logs+1): 

    if h in results_DT_dict.keys():
        
        for value in percentages:
                
            for i in range(1,total_iterations+1):

                if i in len_deviations_dict[h][value].keys():

                    log_id = h
                    iteration = i 
                    num_traces_log = 10000
                    num_events_log = len(eventlog_dict[h])
                    num_activities_model = len(model_dict_audit[h].activities)
                    num_constraints_norm = len(model_dict_norm[h].constraints)
                    num_constraints_audit = len(model_dict_audit[h].constraints)
                    labeled_population = len(traces_dict[h][value])
                    labeled_sample = len_deviations_dict[h][value][i]
                    perc_anomalies_in_population = value # perc_anomalies_in_population_dict[h][value][i]
                    perc_anomalies_in_sample = perc_anomalies_in_sample_dict[h][value][i]
                    perc_test = 0.3
                
                    accuracy_DT = results_DT_dict[h][value][i]["accuracy"]
                    precision_DT = results_DT_dict[h][value][i]["precision"]
                    recall_DT = results_DT_dict[h][value][i]["recall"]
                    f1_score_DT = results_DT_dict[h][value][i]["f1_score"]
                    auc_score_DT = results_DT_dict[h][value][i]["auc_score"]

                    accuracy_RF = results_RF_dict[h][value][i]["accuracy"]
                    precision_RF = results_RF_dict[h][value][i]["precision"]
                    recall_RF = results_RF_dict[h][value][i]["recall"]
                    f1_score_RF = results_RF_dict[h][value][i]["f1_score"]
                    auc_score_RF = results_RF_dict[h][value][i]["auc_score"]

                    
                    result = {
                        "log_id": [],
                        "iteration": [],
                        "num_traces_log": [],
                        "num_events_log": [],
                        "num_activities_model": [],
                        "num_constraints_norm": [],
                        "num_activities_audit": [],
                        "labeled_population":[],
                        "labeled_sample":[],
                        "perc_anomalies_in_population":[],
                        "perc_anomalies_in_sample":[],
                        "perc_test":[],
                        "accuracy_DT": [],
                        "precision_DT": [],
                        "recall_DT": [],
                        "F1_score_DT": [],
                        "AUC_score_DT": [],
                        "accuracy_RF": [],
                        "precision_RF": [],
                        "recall_RF": [],
                        "F1_score_RF": [],
                        "AUC_score_RF": [],
                    }

                    df1 = pd.DataFrame(result)
                    df1.to_csv("test_result_{0}_{1}_{2}.csv".format(h,value,i), sep=',',index=False)

                    fields = [
                        log_id, 
                        iteration, 
                        num_traces_log,
                        num_events_log, 
                        num_activities_model,
                        num_constraints_norm,
                        num_constraints_audit, 
                        labeled_population, 
                        labeled_sample,
                        perc_anomalies_in_population,
                        perc_anomalies_in_sample,
                        perc_test,
                        accuracy_DT, 
                        precision_DT, 
                        recall_DT, 
                        f1_score_DT, 
                        auc_score_DT,
                        accuracy_RF, 
                        precision_RF, 
                        recall_RF, 
                        f1_score_RF, 
                        auc_score_RF
                    ]

                    with open(r"test_result_{0}_{1}_{2}.csv".format(h,value,i), 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(fields)

                else:
                    pass
    else: 
        pass


# Create dataframe from stored csv files 
def combine_result_files(directory):
    df=pd.DataFrame()
    os.chdir(directory)
    for file in os.listdir():
        if file.startswith('test_result') & file.endswith('csv'):
            aux=pd.read_csv(file)
            aux.reset_index(drop=True,inplace=True)
            df=pd.concat([df,aux])
            print("added line")
    return df

directory = 'G:\\Shared drives\\PhD Manal\\Projects\\Git\\DeclareModelHierarchy'

combined_df = combine_result_files(directory)

columns = {
    "log_id": [],
    "iteration": [],
    "num_traces_log": [],
    "num_events_log": [],
    "num_activities_model": [],
    "num_constraints_norm": [],
    "num_activities_audit": [],
    "labeled_population":[],
    "labeled_sample":[],
    "perc_anomalies_in_population":[],
    "perc_anomalies_in_sample":[],
    "perc_test":[],
    "accuracy_DT": [],
    "precision_DT": [],
    "recall_DT": [],
    "F1_score_DT": [],
    "AUC_score_DT": [],
    "accuracy_RF": [],
    "precision_RF": [],
    "recall_RF": [],
    "F1_score_RF": [],
    "AUC_score_RF": [],
}

combined_df.columns = columns
combined_df.to_csv('X_noise10.csv', index=False)
