import pandas as pd

import seaborn as sb
import matplotlib.pyplot as plt

from typing import List, Tuple

def drop_features(features_to_drop:List[str], df:pd.DataFrame, drop_in_place:bool=True)->pd.DataFrame:
    """ Drop features in a dataframe """
    return df.drop(features_to_drop,axis=1,inplace=drop_in_place)

def plot_distribution_in_features(df:pd.DataFrame, fig_height:int=180, fig_width:int=20,
                                  subplot_ncols:int=2, subplot_nrows:int=None, features_to_ignore:List[str]=[]):
    
    """
        Plot distribution of each numerical feature in the given dataframe.
    """
    categorical_columns=[]
    numerical_columns=[]
    
    #if len(features_to_ignore)>0:
    #    df.drop(features_to_ignore, axis=1,inplace=True)
    
    # Determine categorical features and numerical ones
    for i in range(len(df.columns)):
        column_name = df.columns[i]
        
        if df[column_name].dtype == "O" : # Column type is Categorical
            categorical_columns.append(column_name)
        else: # Column type is Numerical
            numerical_columns.append(column_name)
            
    # Exclude from the numerical_columns the values from features_to_ignore, in order to ignore those features
    #     when plotting the charts
    for f in features_to_ignore:
        if f in numerical_columns:
            numerical_columns.remove(f) ## TODO : continue from here : remove f from numerical_columns
            
    
    # Compute the number of rows, which is equal to the number of numercial features
    if subplot_nrows is None:
        subplot_nrows=len(numerical_columns)
    
    
    plt.figure(figsize=(fig_width,fig_height))
    
    previous_used_line=0
    current_line=-1
    # Plot for each categorical feature
    for numerical_column in numerical_columns:
        print("Processing column : {}".format(numerical_column))
        plot_label_size = 15
        current_line+=1
        
        # Plot boxplot
        plt.subplot(subplot_nrows,subplot_ncols,current_line+previous_used_line+1)
        sb.boxplot(x=df.loc[:,numerical_column])
        plt.xlabel(numerical_column, size=plot_label_size)
        
        # Plot density plot
        plt.subplot(subplot_nrows,subplot_ncols,current_line+previous_used_line+2)
        df[numerical_column].plot(kind="density")
        plt.xlabel(numerical_column, size=plot_label_size)
        
        previous_used_line+=1


def plot_distribution_in_feature(df:pd.DataFrame, feature:str, fig_height:int=5, fig_width:int=20,
                                 subplot_ncols:int=2, subplot_nrows:int=1):
    """
        Plot distribution of the given feature
    """
    plt.figure(figsize=(fig_width,fig_height))
    column_name = feature
    plot_label_size = 15
    
    #ploting boxplot
    plt.subplot(subplot_nrows,subplot_ncols,1)
    sb.boxplot(x=df.loc[:,column_name])
    plt.xlabel(column_name, size=plot_label_size)
    
    #ploting density plot
    plt.subplot(subplot_nrows,subplot_ncols,2)
    df[column_name].plot(kind="density")
    plt.xlabel(column_name, size=plot_label_size)


def get_outlier_indexes(df:pd.DataFrame, feature:str, data_points_scale:float=1.5, 
                        lower_bound_quantile =.25, upper_bound_quantile=.75):
    """
        Return outliers indexes in the given feature (column).
        @params :
            - df : the dataframe to analyse
            - feature : the feature in which to search for outliers
            - data_points_scale : data points scale to use in order to determine good values ranges
            - lower_bound_quantile : quantile to use to determine good values' lower bound
            - upper_bound_quantile : quantile to use to determine good values' upper bound
        
        This function use the interquantile method in order to determine outliers.
    """
    # Lower bound quantile
    IQ1 = df[feature].quantile(lower_bound_quantile) #df[feature].quantile(0.25)
    # Upper bound quantile
    IQ3 = df[feature].quantile(upper_bound_quantile) #df[feature].quantile(0.75)
    # Median (middle) value between lower and upper bound quantiles
    IQR = IQ3-IQ1
    
    # Calculate lower and upper bounds value
    lower_bound = IQ1 - data_points_scale*IQR
    upper_bound = IQ3 + data_points_scale*IQR
    
    # Retrieve outliers indexes in the dataframe's feature
    outlier_indexes = df.index[ (df[feature]<lower_bound) | (df[feature]>upper_bound) ]
    return outlier_indexes

def remove_outliers_in_features(df:pd.DataFrame, data_points_scale:float=1.5, drop_in_place:bool=True,
                                features_to_ignore:List[str]=[])->pd.DataFrame:
    """
        Remove outliers in all features of the given dataframe
    """
    
    print("df.shape before outliers removal : {}".format(df.shape))
    
    categorical_columns=[]
    numerical_columns=[]
    
    #print("features_to_ignore")
    #print(features_to_ignore)
    
    if len(features_to_ignore)>0:
        df.drop(features_to_ignore, axis=1,inplace=True)
    
    # Determine categorical features and numerical ones
    for i in range(len(df.columns)):
        column_name = df.columns[i]
        
        if df[column_name].dtype == "O" : # Column type is Categorical
            categorical_columns.append(column_name)
        else: # Column type is Numerical
            numerical_columns.append(column_name)
            
            
    # Get the outliers indexes in each numerical feature 
    outliers_indexes = []
    for numerical_column in numerical_columns: #for feature in df.columns:
        outliers_indexes.extend( get_outlier_indexes(df,feature=numerical_column) )
        
    # Remove duplicate indexes
    outliers_indexes = set(outliers_indexes)
    print("Total number of outliers in data : {}".format(len(outliers_indexes)))
    
    # Drop samples wich have outlier in one of their features
    if drop_in_place:
        df.drop(outliers_indexes,inplace=drop_in_place, axis=0)
    else:
        df = df.drop(outliers_indexes,inplace=drop_in_place, axis=0)
        
    print("df.shape after outliers removal : {}".format(df.shape))
    
    return df

def remove_outliers_in_feature(df:pd.DataFrame, feature:str, data_points_scale:float=1.5, 
                               drop_in_place:bool=True)->pd.DataFrame:
    """
        Remove outliers in the wanted feature of the given dataframe
    """
    if df[feature].dtype == "O" :
        raise Exception("The feature {} is categorical, waiting for a numerical feature".format(feature))
    
    print("df.shape before outliers removal : {}".format(df.shape))
    
    # Retrieve outliers index in the given feature
    outliers_indexes = []
    outliers_indexes.extend( get_outlier_indexes(df,feature) )
    outliers_indexes = set(outliers_indexes)
    
    print("Total number of outliers in data : {}".format(len(outliers_indexes)))
    
    #df = df.drop(outliers_indexes,inplace=drop_in_place, axis=0)
    if drop_in_place:
        df.drop(outliers_indexes,inplace=drop_in_place, axis=0)
    else:
        df = df.drop(outliers_indexes,inplace=drop_in_place, axis=0)
        
    print("df.shape after outliers removal : {}".format(df.shape))
    
    return df

def remove_upper_bound_outliers_in_feature(df:pd.DataFrame, feature:str, upper_bound:float)->pd.DataFrame:
    """
        Remove outliers on the upper bound side in the wanted feature in the given dataframe
        @return : new dataframe without outlier in the wanted feature
        @params :
            df : given dataframe
            feature : feature in which to remove outlier
            upper_bound : upper bound value where any right side value is considered outlier
    """
    new_df = df.loc[df[feature]<upper_bound]
    remove_outliers_in_feature(new_df,feature=feature)
    plot_distribution_in_feature(new_df, feature=feature)
    return new_df

def remove_lower_bound_outliers_in_feature(df:pd.DataFrame, feature:str, lower_bound:float)->pd.DataFrame:
    """
        Remove outliers on the upper bound side in the wanted feature in the given dataframe
        @return : new dataframe without outlier in the wanted feature
        @params :
            df : given dataframe
            feature : feature in which to remove outlier
            upper_bound : lower bound value where any left side value is considered outlier
    """
    new_df = df.loc[ df[feature]>lower_bound ]
    remove_outliers_in_feature(new_df,feature=feature)
    plot_distribution_in_feature(new_df, feature=feature)
    return new_df

def drop_features_with_one_occurence(df:pd.DataFrame, features_to_ignore:List[str]=["SalePrice"])->pd.DataFrame:
    """ Drop features having only one occurence """
    print(f"Shape before processing: {df.shape}")
    for column in df.columns:
        if column not in features_to_ignore:
            if df[column].nunique()==1:
                print(f"Dropping feature {column}")
                df.drop([column],axis=1,inplace=True)
    print(f"Shape after processing: {df.shape}")
    return df


