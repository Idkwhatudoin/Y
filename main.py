import tkinter as tk

from tkinter import messagebox

import cloudscraper as cs

from sklearn.linear_model import LinearRegression

import pandas as pd

import numpy as np

s = cs.create_scraper()

def crashPoint(num):

    info = s.get('https://rest-bf.blox.land/games/crash').json()['history'][num]['crashPoint']

    return info

# Function to run the prediction code

def run_prediction():

    # Call your prediction code here and store the result in the 'prediction' variable

    cid = s.get('https://rest-bf.blox.land/games/crash').json()['current']['_id']

    one = crashPoint(0)

    two = crashPoint(1)

    three = crashPoint(2)

    four = crashPoint(3)

    five = crashPoint(4)

    # create a dataframe with the historical crash points as the only column

    df = pd.DataFrame([one, two, three, four, five], columns=["crash_point"])

    # add a new column with the lagged values of the crash points

    df["lag1"] = df.crash_point.shift(1)

    df["lag2"] = df.crash_point.shift(2)

    # drop the missing values

    df = df.dropna()

    # split the data into features (lags) and target (crash points)

    X = df[["lag1", "lag2"]]

    y = df.crash_point

    # fit a linear regression model to the data

    lr = LinearRegression()

    lr.fit(X, y)

    # use the model to make a prediction for the next game

    last_crash_points = [two, three]  # use the last two crash points to make a prediction

    prediction = lr.predict([last_crash_points])

    # calculate the risky bet as well

    risky = (4 / (np.mean(prediction) - np.std(prediction)) / 7)

    risky = risky + prediction

    risky = risky * 1.25 + prediction

    # format the predictions to two decimal places

    prediction = "{:.2f}".format(prediction[0])

    risky = "{:.2f}".format(risky[0])

    real = f"{prediction} (risky: {risky})"

    # Update the label text with the prediction

    prediction_label.config(text="Prediction: " + real)

    game.config(text="Game UUID: " + cid)

# Create the main window

window = tk.Tk()

window.title("Boost • Crash Exploit")

window.configure(bg="#262626")

# Create a label for the title

title_label = tk.Label(window, text="Boost • Crash Exploit", font=("Arial", 18), fg="white", bg="#262626")

title_label.pack(pady=20)

# Create a label for the prediction

prediction_label = tk.Label(window, text="Prediction: ", font=("Arial", 12), fg="white", bg="#262626")

prediction_label.pack(pady=10)

game = tk.Label(window, text="Game UUID: ", font=("Arial", 12), fg="white", bg="#262626")

game.pack(pady=10)

# Create a predict button

predict_button = tk.Button(window, text="Predict", font=("Arial", 12), fg="white", bg="#0078D7",

                           relief="flat", command=run_prediction)

predict_button.config(width=10, height=2, bd=0)

predict_button.pack(pady=20)

# Function to show an about message box

def show_about():

    messagebox.showinfo("About", "Boost • Crash Exploit\nVersion 1.0\nThe most accurate crash exploit for bloxflip.\n© 2023 Your Company")

# Create an about button

about_button = tk.Button(window, text="About", font=("Arial", 12), fg="white", bg="#0078D7",

                         relief="flat", command=show_about)

about_button.config(width=10, height=2, bd=0)

about_button.pack()

# Run the GUI main loop

window.mainloop()

