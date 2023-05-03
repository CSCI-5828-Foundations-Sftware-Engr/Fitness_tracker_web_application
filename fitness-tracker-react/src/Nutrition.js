import React, { useState, useEffect} from 'react';
import { useLocation } from 'react-router-dom';
import Chart from './Chart';

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
    const [calorieIntakeData, setCalorieIntakeData] = useState('');
    const [waterIntakeData, setWaterIntakeData] = useState('');
    const [proteinIntakeData, setProteinIntakeData] = useState('');
    const [carbsIntakeData, setCarbsIntakeData] = useState('');
    const [fatIntakeData, setFatIntakeData] = useState('');

    useEffect(() => {
        fetch('https://fitness-tracker-staging.herokuapp.com/nutrition_analysis', {
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
                // Convert the data into the desired format
                console.log(data.data.data)
                const calorieData = data.data.data.map((item) => ({
                    date: item.date,
                    calories_intake: Number(item.calorie_intake),
                    target_calories: Number(data.data.target.calorie_intake_goal)
                }));
                setCalorieIntakeData(calorieData);

                const waterData = data.data.data.map((item) => ({
                    date: item.date,
                    water_intake: Number(item.water_intake),
                    target_water: Number(data.data.target.water_goal)
                }));
                setWaterIntakeData(waterData);

                const proteinData = data.data.data.map((item) => ({
                    date: item.date,
                    protein_intake: Number(item.protein),
                    target_protein: Number(data.data.target.protein_goal)
                }));
                setProteinIntakeData(proteinData);

                const carbsData = data.data.data.map((item) => ({
                    date: item.date,
                    carbs_intake: Number(item.carbs),
                    target_carbs: Number(data.data.target.carbs_goal)
                }));
                setCarbsIntakeData(carbsData);

                const fatData = data.data.data.map((item) => ({
                    date: item.date,
                    fat_intake: Number(item.fat),
                    target_fat: Number(data.data.target.fat_goal)
                }));
                setFatIntakeData(fatData);


            })
            .catch(error => console.error(error));
    });

    const caloriesTrackingChartData = {
        data: calorieIntakeData,
        xAxisDataKey: "date",
        barChartDataKey: "calories_intake",
        barChartName: "Calories Spent",
        lineChartDataKey: "target_calories",
        lineChartName: "Target Calories"
    };
    const waterIntakeTrackingChartData = {
        data: waterIntakeData,
        xAxisDataKey: "date",
        barChartDataKey: "water_intake",
        barChartName: "Water Intake (Glasses)",
        lineChartDataKey: "target_water",
        lineChartName: "Target Water Intake"
    };
    const proteinIntakeTrackingChartData = {
        data: proteinIntakeData,
        xAxisDataKey: "date",
        barChartDataKey: "protein_intake",
        barChartName: "Protein Intake (%)",
        lineChartDataKey: "target_protein",
        lineChartName: "Target Protein Intake"
    };
    const carbsIntakeTrackingChartData = {
        data: carbsIntakeData,
        xAxisDataKey: "date",
        barChartDataKey: "carbs_intake",
        barChartName: "Carbs (%)",
        lineChartDataKey: "target_carbs",
        lineChartName: "Target Carbs Intake"
    };
    const fatIntakeTrackingChartData = {
        data: fatIntakeData,
        xAxisDataKey: "date",
        barChartDataKey: "fat_intake",
        barChartName: "Fat (%)",
        lineChartDataKey: "target_fat",
        lineChartName: "Target Fat Intake"
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        fetch('https://fitness-tracker-staging.herokuapp.com/nutrition', {
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

            <div class="chart-grid">
                <Chart label="Protein Tracking" data={proteinIntakeTrackingChartData} />
                <Chart label="Carbs Tracking" data={carbsIntakeTrackingChartData} />
                <Chart label="Fat Tracking" data={fatIntakeTrackingChartData} />
                <Chart label="Calories Tracking" data={caloriesTrackingChartData} />
                <Chart label="Water Intake Tracking" data={waterIntakeTrackingChartData} />
            </div>

        </div>
    );
};

export default Nutrition;
