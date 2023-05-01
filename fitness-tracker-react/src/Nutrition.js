import React, { useState } from 'react';

const Nutrition = (props) => {
    const [calorieIntake, setCalorieIntake] = useState('');
    const [proteins, setProteins] = useState('');
    const [carbs, setCarbs] = useState('');
    const [fat, setFat] = useState('');
    const [water, setWater] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        fetch('http://127.0.0.1:5000/nutrition', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
               calorieIntake,
               proteins,
               carbs,
               fat,
               water
            }),
        })
            .then((response) => {
                // Handle the response from the API
                console.log(response);
            })
            .catch((error) => {
                // Handle errors
                console.error(error);
            });
    };

    return (
        <div className="nutrition-container">
            <h2>Enter Today's Nutrition Details </h2>
            <form className="nutrition-form" onSubmit={handleSubmit}>
                <div class="row">
                    <label htmlFor="calorieIntake">Calorie Intake:</label>
                    <input
                        id="calorieIntake"
                        placeholder="Enter Calories"
                        type="number"
                        value={calorieIntake}
                        onChange={(e) => setCalorieIntake(e.target.value)}
                    />
                </div>

                <div class="row">
                    <label htmlFor="proteins">Proteins(%):</label>
                    <input
                        id="proteins"
                        placeholder="Enter Proteins"
                        type="number"
                        value={proteins}
                        onChange={(e) => setProteins(e.target.value)}
                    />
                </div>

                <div class="row">
                    <label htmlFor="carbs">Carbs(%):</label>
                    <input
                        id="carbs"
                        placeholder="Enter Carbs"
                        type="number"
                        value={carbs}
                        onChange={(e) => setCarbs(e.target.value)}
                    />
                </div>

                <div class="row">
                    <label htmlFor="fat">Fat(%):</label>
                    <input
                        id="fat"
                        placeholder="Enter Fat"
                        type="number"
                        value={fat}
                        onChange={(e) => setFat(e.target.value)}
                    />
                </div>

                <div class="row">
                    <label htmlFor="water">Water Intake:</label>
                    <input
                        id="water"
                        placeholder="Enter Intake"
                        type="water"
                        value={water}
                        onChange={(e) => setWater(e.target.value)}
                    />
                </div>

                <button type="submit">Submit</button>
            </form>

        </div>
    );
};

export default Nutrition;
