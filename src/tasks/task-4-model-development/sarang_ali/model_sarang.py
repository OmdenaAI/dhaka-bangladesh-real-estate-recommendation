import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
import category_encoders as ce
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Set random seed
np.random.seed(42)

# Suppress warnings
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Read df
df = pd.read_csv('prepare_df.csv', index_col='id')
amenities = df.filter(like='amenity')
df.drop(columns=amenities.columns, inplace=True)

# Data Splitting
train_X = df.drop(columns=['price', 'price_log'], axis=1)
train_y = df['price_log']

# Dividing and Selecting features
amenity_col = list(df.filter(like='amenity').columns)
cat_cols = list(set(df.select_dtypes(include=['object']).columns) - set(['city', 'locality']))
num_cols = list(set(df.select_dtypes(include='number').columns) - set(['price', 'price_log']) - set(amenity_col))
large_cat = ['zone']
small_cat = list(set(cat_cols) - set(large_cat))
number_cols = list(set(num_cols) - set(['city', 'locality']))

# Custom Transformers
class CatBoostEncoderTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns
        self.encoders = {}

    def fit(self, X, y=None):
        for col in self.columns:
            encoder = ce.CatBoostEncoder()
            encoder.fit(X[col], y)
            self.encoders[col] = encoder

        return self

    def transform(self, X):
        transformed_X = X.copy()

        for col, encoder in self.encoders.items():
            transformed_X[col] = encoder.transform(X[col])

        return transformed_X


class OneHotEncoderTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None, drop_original=True):
        self.columns = columns
        self.drop_original = drop_original
        self.encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        self.new_columns = None

    def fit(self, X, y=None):
        if self.columns is None:
            global small_cat
            self.columns = small_cat.copy()

        self.encoder.fit(X[self.columns])
        self.new_columns = self.encoder.get_feature_names_out(self.columns)

        return self

    def transform(self, X):
        transformed_X = pd.DataFrame(self.encoder.transform(X[self.columns]), columns=self.new_columns, index=X.index)

        if self.drop_original:
            transformed_X = X.drop(columns=self.columns).join(transformed_X)

        return transformed_X


class NumberColsStandardScaler(BaseEstimator, TransformerMixin):
    def __init__(self, number_cols=None):
        self.number_cols = number_cols
        self.scaler = StandardScaler()

    def fit(self, X, y=None):
        if self.number_cols is None:
            self.number_cols = X.select_dtypes(include='number').columns.tolist()

        self.scaler.fit(X[self.number_cols])

        return self

    def transform(self, X):
        transformed_X = X.copy()
        transformed_X[self.number_cols] = self.scaler.transform(X[self.number_cols])

        return transformed_X


class PassAmenityColumns(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X=None, y=None):
        return self

    def transform(self, df):
        return df


# Columns Transformer
large_cat_transformer = CatBoostEncoderTransformer(columns=large_cat)
Transformed_large_cat = large_cat_transformer.fit_transform(train_X[large_cat], train_y)
number_cols.append('zone')
train_X['zone'] = Transformed_large_cat['zone']
small_cat_transformer = OneHotEncoderTransformer(columns=small_cat, drop_original=True)
scaler_transformer = NumberColsStandardScaler(number_cols=number_cols)

preprocessor = ColumnTransformer(transformers=[
    ('small_cat', small_cat_transformer, small_cat),
    ('scaling', scaler_transformer, number_cols)
])
"""preprocessor = preprocessor.fit(train_X, train_y)
joblib.dump(preprocessor, 'preprocessor_sarang.pkl')"""

preprocessor = joblib.load('preprocessor_sarang.pkl')
prepared_train_X = preprocessor.transform(train_X)

# Model preparation and evaluation

"""rf_reg = RandomForestRegressor(max_features=8, n_estimators=15, random_state=42)
rf_reg.fit(prepared_train_X, train_y)
joblib.dump(rf_reg, 'RandomForrest_sarang.pkl')"""

# Load the trained model
model = joblib.load('RandomForrest_sarang.pkl')


def prepare_input_for_model(X):
    X_large_prepared = large_cat_transformer.transform(X)
    X['zone'] = X_large_prepared['zone']
    X = preprocessor.transform(X)
    return X


def make_prediction(input):
    input = pd.DataFrame(input, index=[0])
    prepared_input = prepare_input_for_model(X=input)
    prediction = model.predict(prepared_input)
    antilog_price = np.exp(prediction)

    return int(antilog_price)


# Make a prediction
"""predicted_price = make_prediction({
    'division': 'Dhaka',
    'building_type': 'Appartment',
    'building_nature': 'Residential',
    'purpose': 'Rent',
    'zone': 'Mohammadpur',
    'num_bed_rooms': 3,
    'num_bath_rooms': 3,
    'area': 1100
})

print(f"Predicted Price: {predicted_price}")"""
