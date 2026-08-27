import streamlit as st
import requests
import json
import pandas as pd
import numpy as np # Added for np.exp

# Set up the Streamlit page
st.set_page_config(page_title="Housing Price Predictor", layout="wide")

st.title("🏡 Housing Price Prediction System")
st.write("""
This app predicts the sale price of a house based on its features. 
Use the sliders and input boxes below to set the feature values.
""")

# URL of the prediction server
URL = "http://127.0.0.1:8000/invocations"

# Create input fields for the user
st.sidebar.header("Input Features")

def user_input_features():
    # Main features that users can adjust
    overall_qual = st.sidebar.slider("Overall Quality", 1, 10, 5)
    gr_liv_area = st.sidebar.number_input("Above Ground Living Area (sq ft)", 500, 5000, 1710)
    year_built = st.sidebar.slider("Year Built", 1872, 2010, 1961)
    total_bsmt_sf = st.sidebar.number_input("Total Basement Area (sq ft)", 0, 6000, 850)
    garage_cars = st.sidebar.slider("Garage Cars", 0, 5, 2)
    garage_area = st.sidebar.number_input("Garage Area (sq ft)", 0, 1500, 500)
    full_bath = st.sidebar.slider("Full Bathrooms", 0, 4, 1)
    totrms_abvgrd = st.sidebar.slider("Total Rooms Above Ground", 2, 15, 7)
    
    # Additional numerical features
    lot_area = st.sidebar.number_input("Lot Area (sq ft)", 1000, 20000, 9600)
    year_remod = st.sidebar.slider("Year Remodeled", 1950, 2010, 1961)
    mas_vnr_area = st.sidebar.number_input("Masonry Veneer Area (sq ft)", 0, 2000, 0)
    bsmtfin_sf1 = st.sidebar.number_input("Basement Finished SF 1", 0, 5000, 700)
    bsmtfin_sf2 = st.sidebar.number_input("Basement Finished SF 2", 0, 5000, 0)
    bsmt_unf_sf = st.sidebar.number_input("Basement Unfinished SF", 0, 5000, 150)
    first_flr_sf = st.sidebar.number_input("1st Floor SF", 500, 5000, 856)
    second_flr_sf = st.sidebar.number_input("2nd Floor SF", 0, 5000, 854)
    low_qual_fin_sf = st.sidebar.number_input("Low Quality Finished SF", 0, 1000, 0)
    bsmt_full_bath = st.sidebar.slider("Basement Full Bathrooms", 0, 3, 1)
    bsmt_half_bath = st.sidebar.slider("Basement Half Bathrooms", 0, 2, 0)
    half_bath = st.sidebar.slider("Half Bathrooms", 0, 3, 0)
    bedroom_abvgr = st.sidebar.slider("Bedrooms Above Grade", 0, 8, 3)
    kitchen_abvgr = st.sidebar.slider("Kitchens Above Grade", 0, 3, 1)
    fireplaces = st.sidebar.slider("Fireplaces", 0, 5, 2)
    garage_yr_blt = st.sidebar.slider("Garage Year Built", 1900, 2010, 1961)
    wood_deck_sf = st.sidebar.number_input("Wood Deck SF", 0, 1000, 210)
    open_porch_sf = st.sidebar.number_input("Open Porch SF", 0, 1000, 0)
    enclosed_porch = st.sidebar.number_input("Enclosed Porch SF", 0, 1000, 0)
    three_season_porch = st.sidebar.number_input("3-Season Porch SF", 0, 1000, 0)
    screen_porch = st.sidebar.number_input("Screen Porch SF", 0, 1000, 0)
    pool_area = st.sidebar.number_input("Pool Area", 0, 1000, 0)
    misc_val = st.sidebar.number_input("Misc Value", 0, 10000, 0)
    mo_sold = st.sidebar.slider("Month Sold", 1, 12, 5)
    yr_sold = st.sidebar.slider("Year Sold", 2006, 2010, 2010)
    lot_frontage = st.sidebar.number_input("Lot Frontage (ft)", 20, 300, 80)
    overall_cond = st.sidebar.slider("Overall Condition", 1, 10, 7)
    ms_subclass = st.sidebar.selectbox("MS SubClass", [20, 30, 40, 45, 50, 60, 70, 75, 80, 85, 90, 120, 150, 160, 180, 190], index=0)

    # Create the complete data structure with all required features
    data = {
        "Order": 1,
        "PID": 5286,
        "MS SubClass": ms_subclass,
        "Lot Frontage": lot_frontage,
        "Lot Area": lot_area,
        "Overall Qual": overall_qual,
        "Overall Cond": overall_cond,
        "Year Built": year_built,
        "Year Remod/Add": year_remod,
        "Mas Vnr Area": mas_vnr_area,
        "BsmtFin SF 1": bsmtfin_sf1,
        "BsmtFin SF 2": bsmtfin_sf2,
        "Bsmt Unf SF": bsmt_unf_sf,
        "Total Bsmt SF": total_bsmt_sf,
        "1st Flr SF": first_flr_sf,
        "2nd Flr SF": second_flr_sf,
        "Low Qual Fin SF": low_qual_fin_sf,
        "Gr Liv Area": gr_liv_area,
        "Bsmt Full Bath": bsmt_full_bath,
        "Bsmt Half Bath": bsmt_half_bath,
        "Full Bath": full_bath,
        "Half Bath": half_bath,
        "Bedroom AbvGr": bedroom_abvgr,
        "Kitchen AbvGr": kitchen_abvgr,
        "TotRms AbvGrd": totrms_abvgrd,
        "Fireplaces": fireplaces,
        "Garage Yr Blt": garage_yr_blt,
        "Garage Cars": garage_cars,
        "Garage Area": garage_area,
        "Wood Deck SF": wood_deck_sf,
        "Open Porch SF": open_porch_sf,
        "Enclosed Porch": enclosed_porch,
        "3Ssn Porch": three_season_porch,
        "Screen Porch": screen_porch,
        "Pool Area": pool_area,
        "Misc Val": misc_val,
        "Mo Sold": mo_sold,
        "Yr Sold": yr_sold,
        # Categorical features with default values
        "MS Zoning": "RL",
        "Street": "Pave",
        "Alley": "NA",
        "Lot Shape": "Reg",
        "Land Contour": "Lvl",
        "Utilities": "AllPub",
        "Lot Config": "Inside",
        "Land Slope": "Gtl",
        "Neighborhood": "NAmes",
        "Condition 1": "Norm",
        "Condition 2": "Norm",
        "Bldg Type": "1Fam",
        "House Style": "1Story",
        "Roof Style": "Gable",
        "Roof Matl": "CompShg",
        "Exterior 1st": "VinylSd",
        "Exterior 2nd": "VinylSd",
        "Mas Vnr Type": "None",
        "Exter Qual": "TA",
        "Exter Cond": "TA",
        "Foundation": "CBlock",
        "Bsmt Qual": "TA",
        "Bsmt Cond": "TA",
        "Bsmt Exposure": "No",
        "BsmtFin Type 1": "GLQ",
        "BsmtFin Type 2": "Unf",
        "Heating": "GasA",
        "Heating QC": "TA",
        "Central Air": "Y",
        "Electrical": "SBrkr",
        "Kitchen Qual": "TA",
        "Functional": "Typ",
        "Fireplace Qu": "TA",
        "Garage Type": "Attchd",
        "Garage Finish": "Unf",
        "Garage Qual": "TA",
        "Garage Cond": "TA",
        "Paved Drive": "Y",
        "Pool QC": "NA",
        "Fence": "NA",
        "Misc Feature": "NA",
        "Sale Type": "WD",
        "Sale Condition": "Normal",
    }
    
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Display the user input
st.subheader("Your Input Features")
st.write(input_df)

# Prediction button
if st.button("Predict Price"):
    # Prepare the prediction payload
    prediction_payload = {
        "dataframe_records": input_df.to_dict('records')
    }

    try:
        response = requests.post(URL, headers={"Content-Type": "application/json"}, data=json.dumps(prediction_payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        result = response.json()
        
        # The prediction is often nested in the response
        if 'predictions' in result and len(result['predictions']) > 0:
            # The model returns log-transformed values
            log_price = result['predictions'][0]
            
            # Based on the training pipeline analysis:
            # 1. The target variable (SalePrice) was transformed using np.log1p() during training
            # 2. This means: log_price = ln(1 + SalePrice)
            # 3. To get back to SalePrice: SalePrice = exp(log_price) - 1
            
            # Apply the correct inverse transformation
            price = round(np.exp(log_price) - 1)
            
            # Validate the price makes sense
            if 50000 <= price <= 1000000:  # $50k to $1M range (reasonable)
                st.success(f"**Predicted Housing Price: ${price:,.2f}**")
                st.info(f"Log-transformed prediction (ln(1+price)): {log_price:.6f}")
                st.info(f"Conversion method: exp(log_price) - 1 (inverse of log1p)")
            else:
                st.warning("⚠️ **Price Prediction**")
                st.warning(f"The model predicted a price of ${price:,.2f}")
                st.info(f"Log-transformed prediction (ln(1+price)): {log_price:.6f}")
                st.info(f"Conversion method: exp(log_price) - 1 (inverse of log1p)")
            
            # Show the mathematical relationship
            st.write(f"**Mathematical Relationship:**")
            st.write(f"- Model output: ln(1 + SalePrice) = {log_price:.6f}")
            st.write(f"- Original price: SalePrice = e^({log_price:.6f}) - 1 = ${price:,.2f}")
            
            # Add context about expected price range
            st.write(f"**Expected Price Range:** Based on the dataset, typical house prices are $100,000 - $250,000")
            st.write(f"**Your Prediction:** ${price:,.2f}")
            
        else:
            st.error("Prediction not found in the response.")
            st.write(result)

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the prediction service at {URL}. Please ensure the deployment pipeline is running.")
        st.error(f"Error details: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Add some helpful information
st.sidebar.markdown("---")
st.sidebar.markdown("**Note:** This model uses log-transformed sale prices for prediction accuracy.")
st.sidebar.markdown("**Quality Ratings:** 1=Very Poor, 10=Very Excellent")
st.sidebar.markdown("**Condition Ratings:** 1=Very Poor, 10=Very Excellent")
