import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import numpy as np
import pandas as pd

# Load the model
try:
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    print("Error: model.pkl file not found. Please ensure it's in the same directory as this script.")
    exit()

def test_predictions():
    sample_data = [
        {"Age": 30, "Years of Experience": 5, "Education Level": "Bachelor's"},
        {"Age": 40, "Years of Experience": 10, "Education Level": "Master's"},
        {"Age": 50, "Years of Experience": 15, "Education Level": "PhD"}
    ]
    
    for i, sample in enumerate(sample_data):
        # Prepare input data
        input_data = pd.DataFrame([sample])
        input_encoded = pd.get_dummies(input_data, columns=['Education Level'])
        required_columns = ['Age', 'Years of Experience', 'Education Level_Master\'s', 'Education Level_PhD']
        for col in required_columns:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[required_columns]
        
        # Make prediction
        prediction = model.predict(input_encoded)
        
        print(f"Sample {i+1}: ${prediction[0]:.2f}")

def predict_salary():
    try:
        education = education_var.get()
        experience = float(experience_entry.get())
        age = float(age_entry.get())

        # Validate input ranges
        if not 0 <= experience <= 25:
            raise ValueError("Years of Experience must be between 0 and 25.")
        if not 20 <= age <= 60:
            raise ValueError("Age must be between 20 and 60.")

        # Create a DataFrame with the input
        input_data = pd.DataFrame({
            'Age': [age],
            'Years of Experience': [experience],
            'Education Level': [education]
        })

        # Use pd.get_dummies to create the correct feature set
        input_encoded = pd.get_dummies(input_data, columns=['Education Level'])

        # Ensure all necessary columns exist
        required_columns = ['Age', 'Years of Experience', 'Education Level_Master\'s', 'Education Level_PhD']
        for col in required_columns:
            if col not in input_encoded.columns:
                input_encoded[col] = 0

        # Reorder columns to match the model's expected input
        input_encoded = input_encoded[required_columns]

        # Make prediction
        prediction = model.predict(input_encoded)

        result = f"Predicted Salary: ${prediction[0]:.2f}"
        messagebox.showinfo("Prediction Result", result)
    except ValueError as ve:
        messagebox.showwarning("Invalid Input", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Salary Prediction App")

# Create and place widgets
tk.Label(root, text="Education Level:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
education_var = tk.StringVar()
education_dropdown = ttk.Combobox(root, textvariable=education_var, values=["Bachelor's", "Master's", "PhD"], state="readonly")
education_dropdown.grid(row=0, column=1, padx=5, pady=5)
education_dropdown.set("Bachelor's")

tk.Label(root, text="Years of Experience:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
experience_entry = tk.Entry(root)
experience_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Age:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
age_entry = tk.Entry(root)
age_entry.grid(row=2, column=1, padx=5, pady=5)

predict_button = tk.Button(root, text="Predict Salary", command=predict_salary)
predict_button.grid(row=3, column=0, columnspan=2, pady=10)

# Add help text
help_text = (
    "Education: Select degree\n"
    "Experience: Enter years (0-25)\n"
    "Age: Enter age (20-60)"
)
help_label = tk.Label(root, text=help_text, justify="left", fg="gray")
help_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Start the GUI event loop
root.mainloop()

# Add this line at the end of your script, after root.mainloop()
test_predictions()