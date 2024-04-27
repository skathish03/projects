import streamlit as st
import requests

# Define the function to get exchange rates
def get_exchange_rates(api_key, base_currency):
    response = requests.get(f"https://api.freecurrencyapi.com/v1/latest?apikey={api_key}&base_currency={base_currency}")
    if response.status_code == 200:
        return response.json()['data']
    else:
        st.error("Failed to retrieve data. Please check your API key and internet connection.")
        return {}

# Streamlit app layout
st.title('Currency Converter')

# API key (you should use an environment variable or a secure method to store your API key)
api_key = st.text_input('Enter your API key for the exchange rate API:', type="password")

# Fetch all available currencies
if api_key:
    all_currencies = list(get_exchange_rates(api_key, 'USD').keys())
else:
    all_currencies = []

# Base currency selection
base_currency = st.selectbox('Select your base currency:', all_currencies)

# Target currency selection
target_currency = st.selectbox('Select the target currency:', all_currencies)

# Amount to convert
amount = st.number_input('Enter the amount you want to convert:', min_value=0.0, value=1.0)

# Convert button
if st.button('Convert'):
    if api_key:
        rates = get_exchange_rates(api_key, base_currency)
        if rates:
            target_rate = rates.get(target_currency)
            if target_rate:
                converted_amount = amount * target_rate
                st.success(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}")
            else:
                st.error(f"Failed to get the conversion rate for {target_currency}.")
    else:
        st.error("Please enter your API key.")