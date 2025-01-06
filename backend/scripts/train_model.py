from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
import json
import os
import pandas as pd

def train_and_save_model(df4):
    # Prepare data
    dummies = pd.get_dummies(df4['location'])
    df4 = pd.concat([df4, dummies.drop('other', axis='columns')], axis='columns')
    df4 = df4.drop(['size', 'price_per_sqft', 'location'], axis='columns')

    X = df4.drop(['price'], axis='columns')
    y = df4['price']
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    # Train model
    lr_clf = LinearRegression()
    lr_clf.fit(X_train, y_train)
    # Save model to pickle file
    model_path = 'backend/model/bangalore_home_prices_model.pickle'
    with open(model_path, 'wb') as f:
        pickle.dump(lr_clf, f)
    # Save columns for later use
    columns = {'data_columns': [col.lower() for col in X.columns]}
    columns_path = 'backend/scripts/columns.json'
    with open(columns_path, 'w') as f:
        json.dump(columns, f)
    print(f'Model saved to {model_path}')
    print(f'Columns saved to {columns_path}')
    return lr_clf
