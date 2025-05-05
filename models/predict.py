import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.linear_model import LinearRegression
from prophet import Prophet

import joblib
import os
import warnings
warnings.filterwarnings('ignore')

def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def make_prediction(historical_data, model_type='lstm'):
    # Prepare data
    data = historical_data['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    if model_type == 'lstm':
        # LSTM Model
        model_path = 'models/lstm_model.h5'
        if not os.path.exists(model_path):
            # Create training data
            training_data_len = int(np.ceil(len(data) * 0.8))
            
            train_data = scaled_data[0:training_data_len, :]
            x_train, y_train = [], []
            
            for i in range(60, len(train_data)):
                x_train.append(train_data[i-60:i, 0])
                y_train.append(train_data[i, 0])
            
            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
            
            # Build and train model
            model = create_lstm_model((x_train.shape[1], 1))
            model.fit(x_train, y_train, batch_size=1, epochs=1)
            model.save(model_path)
        else:
            model = create_lstm_model((60, 1))
            model.load_weights(model_path)
        
        # Make predictions
        test_data = scaled_data[-60:]
        x_test = np.array([test_data])
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        
        predictions = []
        current_batch = x_test[-1]
        
        for i in range(30):  # Predict 30 days
            current_pred = model.predict(current_batch.reshape(1, 60, 1))[0]
            predictions.append(current_pred)
            current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)
        
        predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    
    elif model_type == 'prophet':
        # Prophet Model
        df = historical_data.reset_index()
        df = df.rename(columns={'date': 'ds', 'Close': 'y'})
        
        model = Prophet(daily_seasonality=True)
        model.fit(df)
        
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        
        predictions = forecast['yhat'][-30:].values
    
    else:  # Linear Regression
        model_path = 'models/linear_model.pkl'
        if not os.path.exists(model_path):
            X = np.arange(len(data)).reshape(-1, 1)
            y = data
            model = LinearRegression()
            model.fit(X, y)
            joblib.dump(model, model_path)
        else:
            model = joblib.load(model_path)
        
        last_day = len(data)
        future_days = np.arange(last_day, last_day + 30).reshape(-1, 1)
        predictions = model.predict(future_days)
    
    return predictions.flatten()