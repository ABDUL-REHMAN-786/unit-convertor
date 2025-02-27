import streamlit as st
import pint

# Configure Streamlit
st.set_page_config(page_title="Advanced Unit Converter", page_icon="🔄", layout="centered")

# Initialize Pint for unit conversions
ureg = pint.UnitRegistry()

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Custom CSS for styling
st.markdown("""
    <style>
    /* Center buttons */
    .stButton>button {
        display: block;
        margin: 0 auto;
    }
    /* Custom card styling */
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: black;
        margin-bottom: 20px;
    }
    /* Custom success and error messages */
    .stSuccess {
        color: #28a745;
        background-color: #d4edda;
        border-color: #c3e6cb;
        padding: 10px;
        border-radius: 5px;
    }
    .stError {
        color: #dc3545;
        background-color: #f8d7da;
        border-color: #f5c6cb;
        padding: 10px;
        border-radius: 5px;
    }
    /* Custom header styling */
    .header {
        text-align: center;
        color: #2c3e50;
    }
    /* Custom footer styling */
    .footer {
        text-align: center;
        color: #7f8c8d;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header">
        <h1>🔄 Advanced Unit Converter</h1>
        <h4 style='color: gray;'>Convert between 1000+ units across multiple categories</h4>
        <hr style='border: 1px solid #ddd;'>
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🔄 Unit Converter App")
st.sidebar.markdown("### Select a category:")
page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "📏 Length & Distance",
    "⚖️ Weight & Mass",
    "🌡 Temperature",
    "🛢 Volume",
    "🚀 Speed",
    "📐 Area",
    "🎛 Power",
    "💡 Energy",
    "⏳ Time",
    "📦 Density",
    "🧪 Scientific & Misc"
])

# Homepage
if page == "🏠 Home":
    st.markdown("""
        <div class="card">
            <div style='text-align: center;'>
                <h2>Welcome to the Ultimate Unit Converter</h2>
                <p style='color: gray;'>A powerful, responsive, and professional unit converter supporting 1000+ units.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Features List
    st.markdown("""
        <div class="card">
            <h3>✅ Features:</h3>
            <ul>
                <li>Supports <strong>1000+ units</strong> across multiple categories</li>
                <li>Auto-Detect Units</li>
                <li>Responsive & Mobile-Friendly UI</li>
                <li>Copy Results & Conversion History</li>
                <li>Open Source & Free</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
else:
    # Unit Categories
    unit_categories = {
        "📏 Length & Distance": ["meter", "kilometer", "mile", "inch", "foot", "yard", "centimeter", "millimeter", "micrometer", "nanometer"],
        "⚖️ Weight & Mass": ["gram", "kilogram", "pound", "ounce", "ton", "stone", "carat"],
        "🌡 Temperature": ["celsius", "fahrenheit", "kelvin"],
        "🛢 Volume": ["liter", "milliliter", "gallon", "cup", "fluid_ounce_us", "pint", "quart"],
        "🚀 Speed": ["meter/second", "kilometer/hour", "mile/hour", "knot", "foot/second"],
        "📐 Area": ["square_meter", "square_kilometer", "square_mile", "square_foot", "acre", "hectare"],
        "🎛 Power": ["watt", "kilowatt", "horsepower", "megawatt"],
        "💡 Energy": ["joule", "calorie", "electron_volt", "kilojoule", "megajoule", "watt_hour", "kilowatt_hour"],
        "⏳ Time": ["second", "minute", "hour", "day", "week", "month", "year"],
        "📦 Density": ["kilogram/meter**3", "gram/milliliter", "pound/gallon", "ounce/inch**3"],
        "🧪 Scientific & Misc": ["newton", "pascal", "bar", "atmosphere", "coulomb", "farad", "henry", "ohm"]
    }

    st.markdown(f"<h2 style='text-align: center;'>{page}</h2>", unsafe_allow_html=True)
    
    # Select Units
    units = unit_categories[page]
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("Convert from:", units, key="from_unit")
    with col2:
        to_unit = st.selectbox("Convert to:", units, key="to_unit")
    
    # Input Value
    value = st.number_input("Enter Value:", format="%.4f", min_value=0.0, key="value")
    
    # Perform Conversion
    if st.button("Convert", key="convert_button"):
        try:
            # Check if units are compatible
            from_dim = ureg(from_unit).dimensionality
            to_dim = ureg(to_unit).dimensionality
            if from_dim != to_dim:
                st.error(f"⚠ Units are incompatible: Cannot convert {from_unit} to {to_unit}.")
            else:
                result = (value * ureg(from_unit)).to(ureg(to_unit))
                st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
                
                # Add to history
                st.session_state.history.append({
                    "from": f"{value} {from_unit}",
                    "to": f"{result:.4f} {to_unit}",
                    "category": page
                })
        except pint.errors.UndefinedUnitError:
            st.error("⚠ Invalid unit selected. Please check your inputs.")
        except Exception as e:
            st.error(f"⚠ An unexpected error occurred: {str(e)}")

    # Reset Button
    if st.button("Reset", key="reset_button"):
        st.session_state.history = []  # Clear history
        st.rerun()  # Reset the app

    # Display History
    if st.session_state.history:
        st.markdown("### 📜 Conversion History")
        for idx, entry in enumerate(st.session_state.history, start=1):
            st.markdown(f"""
                <div class="card">
                    <p><strong>{idx}.</strong> **{entry['from']}** → **{entry['to']}** (Category: {entry['category']})</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Clear History Button
        if st.button("Clear History", key="clear_history_button"):
            st.session_state.history = []
            st.rerun()

# --- FOOTER ---
st.markdown("""
    <hr style='border: 1px solid #ddd;'>
    <div class="footer">
        <p>Developed by <strong>Abdul Rehman</strong> | 📌 <i>Built with Streamlit & Pint</i></p>
    </div>
""", unsafe_allow_html=True)

# --- END ---