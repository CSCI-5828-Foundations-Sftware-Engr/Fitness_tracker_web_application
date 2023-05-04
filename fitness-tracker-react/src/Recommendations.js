import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Chart from './Chart';

const Recommendations = () => {
    const location = useLocation();
    const user = location.state;
    const username = user.username
    const [balancedRecommendations, setBalancedRecommendations] = useState([]);
    const [proteinRecommendations, setProteinRecommendations] = useState([]);
    const [carbsRecommendations, setCarbsRecommendations] = useState([]);
    const [calorieRecommendations, setCalorieRecommendations] = useState([]);
    const [fatRecommendations, setFatRecommendations] = useState([]);

    useEffect(() => {
        fetch('https://fitness-tracker-staging.herokuapp.com/recommendations', {
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
                setBalancedRecommendations(data.response.balanced)
                setProteinRecommendations(data.response.high_protein)
                setCarbsRecommendations(data.response.low_carbs)
                setCalorieRecommendations(data.response.ideal_calorie_intake)
                setFatRecommendations(data.response.low_fat)

            })
            .catch(error => console.error(error));
    }, []);

    return (
        <div className="workout-container">
            <h3 class="intake">Ideal Calorie Intake: {calorieRecommendations}</h3>

            <div class="recommendation-table-display">
                <table class="recommendation-table">
                    <h3>Balanced Recommendations</h3>
                    <tbody>
                        {balancedRecommendations.map((recommendation, index) => (
                            <tr key={index}>
                                <td><a href={recommendation.url}>{recommendation.label}</a></td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                <table class="recommendation-table">
                    <h3>High Protein Recommendations</h3>
                    <tbody>
                        {proteinRecommendations.map((recommendation, index) => (
                            <tr key={index}>
                                <td><a href={recommendation.url}>{recommendation.label}</a></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div class="recommendation-table-display">
                <table class="recommendation-table">
                    <h3>Low carbs Recommendations</h3>
                    <tbody>
                        {carbsRecommendations.map((recommendation, index) => (
                            <tr key={index}>
                                <td><a href={recommendation.url}>{recommendation.label}</a></td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                <table class="recommendation-table">
                    <h3>Low Fat Recommendations</h3>
                    <tbody>
                        {fatRecommendations.map((recommendation, index) => (
                            <tr key={index}>
                                <td><a href={recommendation.url}>{recommendation.label}</a></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Recommendations;
