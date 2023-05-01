import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';

const Workout = () => {
    const location = useLocation();
    const user = location.state;
    const username = user.username
    const [total_steps, setTotalSteps] = useState('');
    const [calories_spent, setCaloriesSpent] = useState('');
    const [weight_measured, setWeight] = useState('');
    const [date, setCurrentDate] = useState(new Date().toLocaleDateString('en-CA'));

    const handleSubmit = (e) => {
        e.preventDefault();

        fetch('http://127.0.0.1:5000/workout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                date,
                total_steps,
                calories_spent,
                weight_measured
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
                    <label htmlFor="total_steps">Total Steps:</label>
                    <input
                        id="total_steps"
                        placeholder="Enter Steps"
                        type="number"
                        value={total_steps}
                        onChange={(e) => setTotalSteps(e.target.value)}
                    />
                </div>

                <div class="row">
                    <label htmlFor="calories_spent">Calories Spent:</label>
                    <input
                        id="calories_spent"
                        placeholder="Enter Calories"
                        type="number"
                        value={calories_spent}
                        onChange={(e) => setCaloriesSpent(e.target.value)}
                    />
                </div>

                <div class="row">
                    <label htmlFor="weight_measured">Weight:</label>
                    <input
                        id="weight_measured"
                        placeholder="Enter Weight"
                        type="number"
                        value={weight_measured}
                        onChange={(e) => setWeight(e.target.value)}
                    />
                </div>
                <button type="submit">Submit</button>
            </form>

        </div>
    );
};

export default Workout;
