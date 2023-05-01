import React, { useState } from 'react';

const Workout = (props) => {
    const [totalSteps, setTotalSteps] = useState('');
    const [caloriesSpent, setCaloriesSpent] = useState('');
    const [weight, setWeight] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        fetch('http://127.0.0.1:5000/workout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                totalSteps,
                caloriesSpent,
                weight
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
        <div className="workout-container">
            <h2>Enter Today's Workout Details </h2>
            <form className="workout-form" onSubmit={handleSubmit}>
                <div class="row">
                    <label htmlFor="totalSteps">Total Steps:</label>
                    <input
                        id="totalSteps"
                        placeholder="Enter Steps"
                        type="number"
                        value={totalSteps}
                        onChange={(e) => setTotalSteps(e.target.value)}
                    />
                </div>

                <div class="row">
                    <label htmlFor="caloriesSpent">Calories Spent:</label>
                    <input
                        id="caloriesSpent"
                        placeholder="Enter Calories"
                        type="number"
                        value={caloriesSpent}
                        onChange={(e) => setCaloriesSpent(e.target.value)}
                    />
                </div>

                <div class="row">
                    <label htmlFor="weight">Weight:</label>
                    <input
                        id="weight"
                        placeholder="Enter Weight"
                        type="number"
                        value={weight}
                        onChange={(e) => setWeight(e.target.value)}
                    />
                </div>
                <button type="submit">Submit</button>
            </form>

        </div>
    );
};

export default Workout;
