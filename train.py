import  pandas              as pd
import  numpy               as np
import  bentoml             
from    sklearn.preprocessing       import OneHotEncoder
from    sklearn.base                import BaseEstimator, TransformerMixin
from    sklearn.pipeline            import Pipeline
from    sklearn.preprocessing       import StandardScaler
from    sklearn.compose             import ColumnTransformer
from    xgboost                     import XGBClassifier

#reading data from downloaded files
print("Reading in data\n")
df_train    = pd.read_csv('data/train_values.csv',index_col='building_id')
y_train_df  = pd.read_csv('data/train_labels.csv',index_col='building_id')

#converting training labels into an array
y_train     = y_train_df.values.ravel()
y_train     = list(map(lambda x: x - 1, y_train)) #xgboost needs labels to start from zero

#defining different set of features
cat         = ['foundation_type', 'roof_type', 'ground_floor_type', 'other_floor_type']
num         = ['age', 'area_percentage', 'height_percentage', 'count_floors_pre_eq']
num_flag    = ['geo_level_1_id', 'geo_level_2_id', 'geo_level_3_id', 'has_superstructure_mud_mortar_stone', 'has_superstructure_cement_mortar_brick', 'has_superstructure_rc_non_engineered', 'has_superstructure_rc_engineered']

#custom transformer to engineer new feature
class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, drop_age = True): 
        self.drop_age = drop_age
    def fit(self, X, y=None):
        return self 
    def transform(self, X, y=None):
        age_ix, area_ix, height_ix, floor_ix = 0, 1, 2, 3 #indexes of the features
        
        for index in (age_ix, area_ix, height_ix, floor_ix):
            X.iloc[:,index] = np.log1p(X.iloc[:,index]) #log transform
                
        X_arr               =   X.values
        height_per_area     =   X_arr[:, height_ix] / X_arr[:, area_ix]
        hpa_aged            =   (X_arr[:, height_ix] / X_arr[:, area_ix]) * X_arr[:, age_ix]
        floors_per_height   =   X_arr[:, floor_ix] / X_arr[:, height_ix]

        if self.drop_age:
            X_del = np.delete(X_arr,[floor_ix,age_ix],1)
            return np.c_[X_del, height_per_area, hpa_aged, floors_per_height]
        else:
            X_del = np.delete(X_arr,floor_ix,1)
            return np.c_[X_del, height_per_area, hpa_aged, floors_per_height]


#defining the pipeline for numerical features
num_pipeline = Pipeline([
                        ('attribs_adder', CombinedAttributesAdder()),
                        ('std_scaler', StandardScaler()),
                        ])

#defining final tranformation pipeline
transform_pipeline = ColumnTransformer([('num_flag', 'passthrough', num_flag),
                                        ("num", num_pipeline, num),
                                        ("cat", OneHotEncoder(), cat),
                                        ], 
                                        remainder='drop')

#preparing data
print("Preparing data\n")
X_train = transform_pipeline.fit_transform(df_train)

#initializing XGBclassifier with the best params obtained from hyperparameter tuning
clf     = XGBClassifier(max_depth           = 17,
                        gamma               = 0.12553660022636093, 
                        reg_alpha           = 15.0, 
                        reg_lambda          = 0.2938474618567798,
                        colsample_bytree    = 0.9736583765805357,
                        min_child_weight    = 2.0,
                        n_estimators        = 180,
                        seed                = 0, 
                        objective           = 'multi:softprob', 
                        random_state        = 0)

#fit model to training data
print("Taining the model\n")
clf.fit(X_train,y_train)

#saving model
bentoml.xgboost.save_model("ritcher_predictor_model",clf,
                            custom_objects={
                                "transformer":transform_pipeline
                            },
                            signatures={
                                "predict":{
                                    "batchable": True,
                                    "batch_dim": 0,
                                }
                            })