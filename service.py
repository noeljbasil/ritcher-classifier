import  pandas      as      pd
import  bentoml
from    bentoml.io  import  JSON,Text
from    pydantic    import  BaseModel

class RitcherApplication(BaseModel):
    geo_level_1_id                             : int
    geo_level_2_id                             : int
    geo_level_3_id                             : int
    count_floors_pre_eq                        : int
    age                                        : int
    area_percentage                            : int
    height_percentage                          : int
    land_surface_condition                     : str
    foundation_type                            : str
    roof_type                                  : str
    ground_floor_type                          : str
    other_floor_type                           : str
    position                                   : str
    plan_configuration                         : str
    has_superstructure_adobe_mud               : int
    has_superstructure_mud_mortar_stone        : int
    has_superstructure_stone_flag              : int
    has_superstructure_cement_mortar_stone     : int
    has_superstructure_mud_mortar_brick        : int
    has_superstructure_cement_mortar_brick     : int
    has_superstructure_timber                  : int
    has_superstructure_bamboo                  : int
    has_superstructure_rc_non_engineered       : int
    has_superstructure_rc_engineered           : int
    has_superstructure_other                   : int
    legal_ownership_status                     : str
    count_families                             : int
    has_secondary_use                          : int
    has_secondary_use_agriculture              : int
    has_secondary_use_hotel                    : int
    has_secondary_use_rental                   : int
    has_secondary_use_institution              : int
    has_secondary_use_school                   : int
    has_secondary_use_industry                 : int
    has_secondary_use_health_post              : int
    has_secondary_use_gov_office               : int
    has_secondary_use_use_police               : int
    has_secondary_use_other                    : int

model_ref       = bentoml.xgboost.get("ritcher_predictor_model:dbx4bps6d65qaaav")
transformer     = model_ref.custom_objects['transformer']
model_runner    = model_ref.to_runner()

svc = bentoml.Service("ritcher_predictor_classifier", runners=[model_runner])

@svc.api(input=JSON(pydantic_model = RitcherApplication), output=Text())
async def classify(ritcher_application):
    dictionary      = ritcher_application.dict()
    dataframe       = pd.DataFrame(dictionary,index=[0])
    vector          = transformer.transform(dataframe)
    prediction      = await model_runner.predict.async_run(vector)
    prediction      = list(map(lambda x: x + 1, prediction))
    deploy_output   = ['low damage' if damage == 1 else 'medium damage' if damage == 2 else 'almost complete destruction' for damage in prediction]
    
    return (f"Damage predicted: {deploy_output[0]}")