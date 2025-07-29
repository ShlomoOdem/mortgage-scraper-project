# Interactive Mortgage Plot UI

A web-based interactive interface for creating custom mortgage parameter visualizations.

## 🚀 Quick Start

### Option 1: Using the launcher script (Recommended)
```bash
./start_interactive_ui.sh
```

### Option 2: Manual start
```bash
# Install dependencies
pip3 install -r requirements_ui.txt

# Start the server
python3 scripts/interactive_plot_ui.py
```

Then open your browser and go to: **http://localhost:5000**

## 📊 Features

### **Parameter Selection**
- **X-Axis**: Choose any parameter (Interest_Rate, Term_Months, Inflation_Rate, etc.)
- **Y-Axis**: Choose any parameter (default: Weighted Monthly Payment)
- **Label**: Optional parameter for color-coding data points

### **Fixed Parameters**
- Add multiple fixed parameters to filter data
- Each fixed parameter reduces the data set to show only matching records
- Perfect for isolating specific scenarios

### **Interactive Plots**
- Hover over any point to see all parameter values
- Zoom, pan, and explore the data
- Download plots as PNG images
- Responsive design works on all devices

## 🎯 Example Use Cases

### **1. Interest Rate Analysis**
- **X-Axis**: Interest_Rate
- **Y-Axis**: Weighted Monthly Payment (30 years)
- **Label**: Inflation_Rate
- **Fixed**: Term_Months=360, Amortization_Method=שפיצר

### **2. Term Length Comparison**
- **X-Axis**: Term_Months
- **Y-Axis**: Weighted Monthly Payment (30 years)
- **Label**: Interest_Rate
- **Fixed**: Inflation_Rate=2.0%, Amortization_Method=קרן שווה

### **3. Inflation Impact**
- **X-Axis**: Inflation_Rate
- **Y-Axis**: Weighted Monthly Payment (30 years)
- **Label**: Interest_Rate
- **Fixed**: Term_Months=240, Amortization_Method=שפיצר

## 🛠️ How to Use

### **Step 1: Configure Parameters**
1. **Select X-Axis Parameter**: Choose what to plot on the horizontal axis
2. **Select Y-Axis Parameter**: Choose what to plot on the vertical axis (default: Weighted Monthly Payment)
3. **Select Label Parameter** (Optional): Choose a parameter to color-code the data points

### **Step 2: Add Fixed Parameters**
1. Click **"Add Fixed Parameter"**
2. Select the parameter you want to fix
3. Choose the specific value for that parameter
4. Repeat for additional fixed parameters

### **Step 3: Create Plot**
1. Click **"Create Plot"**
2. Wait for the plot to generate
3. Explore the interactive visualization

## 📈 Understanding the Results

### **Data Points**
Each point represents a mortgage combination where:
- **X and Y values** match your selections
- **Label values** determine the color/marker
- **Fixed parameters** are held constant

### **Hover Information**
Hover over any point to see:
- All parameter values for that combination
- Fixed parameter values
- Exact X, Y, and label values

### **Plot Title**
The title shows:
- X vs Y relationship
- Label parameter (if selected)
- Fixed parameters and their values

## 🔧 Technical Details

### **Data Source**
- Uses `data/analyzed/combined_summary_files.csv`
- Contains 31,591 mortgage combinations
- Weighted payment range: 4,713 - 10,608 NIS

### **Available Parameters**
- **Numeric**: Term_Months, Inflation_Rate, Interest_Rate
- **Categorical**: Amortization_Method (שפיצר, קרן שווה)

### **Tolerance Settings**
For numeric fixed parameters:
- **Term_Months**: ±24 months
- **Inflation_Rate**: ±1.0%
- **Interest_Rate**: ±0.5%

## 🎨 UI Features

### **Modern Design**
- Clean, responsive interface
- Bootstrap 5 styling
- Font Awesome icons
- Gradient backgrounds

### **User Experience**
- Real-time parameter validation
- Loading indicators
- Success/error messages
- Intuitive controls

### **Interactive Elements**
- Dropdown menus for parameter selection
- Dynamic value loading
- Add/remove fixed parameters
- One-click plot generation

## 🚨 Troubleshooting

### **"No data points found"**
- Try reducing the number of fixed parameters
- Check that fixed parameter values exist in the data
- Try different parameter combinations

### **Server won't start**
- Check if port 5000 is available
- Install dependencies: `pip3 install -r requirements_ui.txt`
- Ensure data file exists: `data/analyzed/combined_summary_files.csv`

### **Plot not loading**
- Check browser console for errors
- Refresh the page
- Try a different browser

## 📁 Files

- `scripts/interactive_plot_ui.py` - Main Flask application
- `templates/interactive_plot_ui.html` - Web interface
- `start_interactive_ui.sh` - Launcher script
- `requirements_ui.txt` - Python dependencies

## 🎯 Tips for Best Results

1. **Start Simple**: Begin with just X and Y parameters
2. **Add Labels**: Use label parameters to see patterns
3. **Use Fixed Parameters**: Narrow down to specific scenarios
4. **Explore Combinations**: Try different parameter combinations
5. **Check Hover Data**: Always hover to see complete information

## 🔄 Related Scripts

- `scripts/plot_fixed_parameter_combinations.py` - Batch generation of fixed parameter plots
- `scripts/plot_clean_fixed_combinations.py` - Clean, focused analysis
- `scripts/plot_parameter_combinations.py` - Comprehensive parameter analysis

---

**Happy Plotting! 🏠📊** 