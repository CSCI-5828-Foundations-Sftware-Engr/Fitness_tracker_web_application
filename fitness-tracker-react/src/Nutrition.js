import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';

const Nutrition = () => {
    const location = useLocation();
    const user = location.state;
    const username = user.username
    const [calorie_intake, setCalorieIntake] = useState('');
    const [protein, setProteins] = useState('');
    const [carbs, setCarbs] = useState('');
    const [fat, setFat] = useState('');
    const [water_intake, setWater] = useState('');
    const [date, setCurrentDate] = useState(new Date().toLocaleDateString('en-CA'));

    const handleSubmit = (e) => {
        e.preventDefault();

        fetch('http://127.0.0.1:5000/nutrition', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                date,
                calorie_intake,
                protein,
                carbs,
                fat,
                water_intake
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
                    <label htmlFor="calorie_intake">Calorie Intake:</label>
                    <input
                        id="calorie_intake"
                        placeholder="Enter Calories"
                        type="number"
                        value={calorie_intake}
                        onChange={(e) => setCalorieIntake(e.target.value)}
                    />
                </div>

                <div class="row">
                    <label htmlFor="protein">Protein(%):</label>
                    <input
                        id="protein"
                        placeholder="Enter Protein"
                        type="number"
                        value={protein}
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
                    <label htmlFor="water_intake">Water Intake:</label>
                    <input
                        id="water_intake"
                        placeholder="Enter Intake"
                        type="number"
                        value={water_intake}
                        onChange={(e) => setWater(e.target.value)}
                    />
                </div>

                <button type="submit">Submit</button>
            </form>

        </div>
    );
};

export default Nutrition;
