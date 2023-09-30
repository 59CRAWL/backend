from joblib import load
import pandas as pd
import os

def model(csvfile):
    path = os.path.dirname(__file__)

    # Load all models first
    svm_path = os.path.join(path, 'models', 'SVM.joblib')
    svm = load(svm_path)
    
    ontime_path = os.path.join(path, 'models', 'ontime.joblib')
    ontime_model = load(ontime_path)

    delayed_path = os.path.join(path, 'models', 'delayed.joblib')
    delayed_model = load(delayed_path)

    # Read csvfile as a dataframe
    df = pd.read_csv(csvfile)
    
    # Configuring data to pass into SVM
    features = df[['Cargo Volume', 'Expected Duration (hours)', 'Weather (0=dry,1=wet)']]

    # Use SVM model to predict delay
    predicted_delay_output = svm.predict(features)

    # Add predicted delay binary to df
    df['Predicted Delay Binary'] = predicted_delay_output

    # Use model to predict duration
    # if delay binary is 0, use ontime_model, else use delayed_model
    predicted_duration_output = []
    for index, row in df.iterrows():
        if row['Predicted Delay Binary'] == 0:
            predicted_duration_output.append(ontime_model.predict(features.iloc[[index]])[0])
        else:
            predicted_duration_output.append(delayed_model.predict(features.iloc[[index]])[0])

    # Add predicted duration to data_output
    df['Predicted Duration (hours)'] = predicted_duration_output

    # Add predicted delay to data_output
    df['Predicted Delay'] = df['Predicted Delay Binary'].apply(lambda x: 'On Time' if x == 0 else 'Delayed')

    # Format ETA from str to datetime format DD/MM/YYYY HH:MM:SS
    df['ETA'] = pd.to_datetime(df['ETA'], dayfirst=True)

    # Create a function to calculate PTD
    def calculate_PTD(row):
        return row['ETA'] + pd.Timedelta(hours=row['Predicted Duration (hours)'])

    # Apply the function to each row in data_output format DD/MM/YYYY HH:MM:SS
    df['PTD'] = df.apply(calculate_PTD, axis=1).dt.strftime('%d/%m/%Y %H:%M:%S')
    df['PTD'] = pd.to_datetime(df['PTD'], dayfirst=True)

    return df

# file_path = 'mockData/port_mock_data.csv'
# with open(file_path, 'r') as file:
#     model(file)