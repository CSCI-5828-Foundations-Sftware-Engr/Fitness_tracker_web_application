import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Chart from './Chart';

const Workout = () => {
    const location = useLocation();
    const user = location.state;
    const username = user.username
    const [total_steps, setTotalSteps] = useState('');
    const [calories_spent, setCaloriesSpent] = useState('');
    const [weight_measured, setWeight] = useState('');
    const [date, setCurrentDate] = useState(new Date().toLocaleDateString('en-CA'));
    const [stepsData, setStepsData] = useState('');
    const [caloriesData, setCaloriesData] = useState('');
    const [weightData, setWeightData] = useState('');

    useEffect(() => {
        fetch('https://fitness-tracker-staging.herokuapp.com/workout_analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
            }),
        })
            .then(response => response.json())
            .then((data) => {

                const stepsData = data.data.data.map((item) => ({
                    date: item.date,
                    steps: Number(item.total_steps),
                    target_steps: Number(data.data.target.steps_goal)
                }));
                setStepsData(stepsData);

                const caloriesData = data.data.data.map((item) => ({
                    date: item.date,
                    calories: Number(item.calories_spent),
                    target_carbs: Number(data.data.target.calories_spent_goal)
                }));
                setCaloriesData(caloriesData);

                const weightData = data.data.data.map((item) => ({
                    date: item.date,
                    weight: Number(item.weight_measured),
                    target_weight: Number(data.data.target.target_weight)
                }));
                setWeightData(weightData);


            })
            .catch(error => console.error(error));
    });

    const stepsTrackingChartData = {
        data: stepsData,
        xAxisDataKey: "date",
        barChartDataKey: "steps",
        barChartName: "Steps",
        lineChartDataKey: "target_steps",
        lineChartName: "Target Steps"
    };
    const caloriesTrackingChartData = {
        data: caloriesData,
        xAxisDataKey: "date",
        barChartDataKey: "calories",
        barChartName: "Calories",
        lineChartDataKey: "target_calories",
        lineChartName: "Target Calories to Burn"
    };
    const weightTrackingChartData = {
        data: weightData,
        xAxisDataKey: "date",
        barChartDataKey: "weight",
        barChartName: "Weight (kg)",
        lineChartDataKey: "target_weight",
        lineChartName: "Target Weight"
    };



    const handleSubmit = (e) => {
        e.preventDefault();

        fetch('https://fitness-tracker-staging.herokuapp.com/workout', {
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

            <div class="chart-grid">
                <Chart label="Steps Tracking" data={stepsTrackingChartData} />
                <Chart label="Calories Burnt Tracking" data={caloriesTrackingChartData} />
                <Chart label="Weight Tracking" data={weightTrackingChartData} />
            </div>

        </div>
    );
};

export default Workout;
