import requests
import streamlit as st

API_ENDPOINT = "https://njbasil-ritche-prod-ritcher-classifier-cf5h5e.mo4.mogenius.io/classify"

# Create the header page content
st.title("Ritcher Classification App")
st.markdown(
    "### Classify the damage to a building caused by the Nepal earthquake",
    unsafe_allow_html=True,
)

# Upload a simple cover image
with open("./data/app_image.jpg", "rb") as f:
    st.image(f.read(), use_column_width=True)

def predict(building):
    """
    A function that sends a prediction request to the API and return damage predicted.
    """
    # Send the image to the API
    response = requests.post(
        API_ENDPOINT,
        headers={"content-type": "text/plain"},
        json=building,
    )

    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Status: {}".format(response.status_code))

def main():
    with st.expander("Click to enter/ change data"):
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            geo1 = st.number_input('Geo level 1 id',value = 17, step=1)
            geo2 = st.number_input('Geo level 2 id',value = 596, step=1)
            geo3 = st.number_input('Geo level 3 id',value = 11307, step=1)
            floor = st.number_input('Floor count',value = 3, step=1)
            age = st.number_input('Age',value = 20, step=1)
            area = st.number_input('Area',value = 7, step=1)
        with col2:
            height = st.number_input('Height',value = 6, step=1)
            land =  st.selectbox('Land surface condition',('n', 'o', 't'),)
            foundation =  st.selectbox('Land surface condition',('h', 'i', 'r', 'u', 'w'))
            roof =  st.selectbox('Land surface condition',('n', 'q', 'x'))
            ground_floor =  st.selectbox('Ground floor type',('f', 'm', 'v', 'x', 'z'))
            other_floor =  st.selectbox('Ground floor type',('j', 'q', 's', 'x'))
        with col3:
            position =  st.selectbox('Position',('j', 'o', 's', 't'))
            plan =  st.selectbox('Plan configuration',( 'a', 'c', 'd', 'f', 'm', 'n', 'o', 'q', 's', 'u'))
            ownership =  st.selectbox('Legal ownership status',( 'a', 'r', 'v', 'w'))
            abode_mud =  st.selectbox('Abode mud?',( 0,1))
            mm_stone =  st.selectbox('Mud, Mortar and Stone?',( 0,1))
            stone =  st.selectbox('Stone?',( 0,1))
        with col4:
            cm_Stone =  st.selectbox('Cement, Mortar and Stone?',( 0,1))
            mm_brick =  st.selectbox('Mud, Mortar and Brick?',( 0,1))
            cm_brick =  st.selectbox('Cement, Mortar and brick?',( 0,1))
            timber =  st.selectbox('Timber?',( 0,1))
            bamboo =  st.selectbox('Bamboo?',( 0,1))
            non_eng =  st.selectbox('RC Non Engineered?',( 0,1))
        with col5:
            rc_eng =  st.selectbox('RC Engineered?',( 0,1))
            other =  st.selectbox('Other material?',( 0,1))
            family = st.number_input('Family count',value = 1, step=1)
            secondary =  st.selectbox('Secondary use?',( 0,1))
            agri =  st.selectbox('Agriculture?',( 0,1))
            hotel =  st.selectbox('Hotel?',( 0,1))
            rental =  st.selectbox('Retal?',( 0,1))
        with col6:
            inst =  st.selectbox('Institution?',( 0,1))
            school =  st.selectbox('School?',( 0,1))
            industry =  st.selectbox('Industry?',( 0,1))
            health =  st.selectbox('health?',( 0,1))
            gov =  st.selectbox('Govermnet use?',( 0,1))
            police =  st.selectbox('Police station?',( 0,1))
            other =  st.selectbox('Other secondary use?',( 0,1))

    building = {"geo_level_1_id": geo1,
                "geo_level_2_id": geo2,
                "geo_level_3_id": geo3,
                "count_floors_pre_eq": floor,
                "age": age,
                "area_percentage": area,
                "height_percentage": height,
                "land_surface_condition": land,
                "foundation_type": foundation,
                "roof_type": roof,
                "ground_floor_type": ground_floor,
                "other_floor_type": other_floor,
                "position": position,
                "plan_configuration": plan,
                "has_superstructure_adobe_mud": abode_mud,
                "has_superstructure_mud_mortar_stone": mm_stone,
                "has_superstructure_stone_flag": stone,
                "has_superstructure_cement_mortar_stone": cm_Stone,
                "has_superstructure_mud_mortar_brick": mm_brick,
                "has_superstructure_cement_mortar_brick": cm_brick,
                "has_superstructure_timber": timber,
                "has_superstructure_bamboo": bamboo,
                "has_superstructure_rc_non_engineered": non_eng,
                "has_superstructure_rc_engineered": rc_eng,
                "has_superstructure_other": other,
                "legal_ownership_status": ownership,
                "count_families": family,
                "has_secondary_use": secondary,
                "has_secondary_use_agriculture": agri,
                "has_secondary_use_hotel": hotel,
                "has_secondary_use_rental": rental,
                "has_secondary_use_institution": inst,
                "has_secondary_use_school": school,
                "has_secondary_use_industry": industry,
                "has_secondary_use_health_post": health,
                "has_secondary_use_gov_office": gov,
                "has_secondary_use_use_police": police,
                "has_secondary_use_other": other}
    
    st.subheader("Your results")

    if st.button('Click here to make prediction'):
        if building is not None:
            with st.spinner("Predicting..."):
                prediction = predict(building)
                if prediction == "Damage predicted: almost complete destruction":
                    st.error(prediction)
                elif prediction == "Damage predicted: medium damage":
                    st.warning(prediction)
                else:
                    st.success(prediction)

if __name__ == "__main__":
    main()