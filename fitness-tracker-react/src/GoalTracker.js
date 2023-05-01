import React, { useState } from 'react';

const GoalTracker = () => {
  const [currentWeight, setCurrentWeight] = useState('');
  const [targetWeight, setTargetWeight] = useState('');
  const [age, setAge] = useState('');
  const [height, setHeight] = useState('');
  const [targetSteps, setTargetSteps] = useState('');
  const [targetDistance, setTargetDistance] = useState('');
  const [waterGoal, setWaterGoal] = useState('');
  const [caloriesGoal, setCaloriesGoal] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
  
    fetch('http://127.0.0.1:5000/goal_tracking', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        currentWeight,
        targetWeight,
        age,
        height,
        targetSteps,
        targetDistance,
        waterGoal,
        caloriesGoal,
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
    <div className="goal-tracker-container">
      <h2>Set your Goals</h2>
      <form className="goal-tracker-form" onSubmit={handleSubmit}>
        <div class="row">
          <label htmlFor="currentWeight">Current weight:</label>
          <input
            id="currentWeight"
            placeholder="Enter Weight"
            type="number"
            value={currentWeight}
            onChange={(e) => setCurrentWeight(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="targetWeight">Targeted weight:</label>
          <input
            id="targetWeight"
            placeholder="Enter Weight"
            type="number"
            value={targetWeight}
            onChange={(e) => setTargetWeight(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="age">Age:</label>
          <input
            id="age"
            placeholder="Enter Age"
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="height">Height:</label>
          <input
            id="height"
            placeholder="Enter Height"
            type="number"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="targetSteps">Target no. of steps:</label>
          <input
            id="targetSteps"
            placeholder="Enter Steps"
            type="number"
            value={targetSteps}
            onChange={(e) => setTargetSteps(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="targetDistance">Distance to walk or run:</label>
          <input
            id="targetDistance"
            placeholder="Enter Distance"
            type="number"
            value={targetDistance}
            onChange={(e) => setTargetDistance(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="waterGoal">Water Goal (in glasses):</label>
          <input
            id="waterGoal"
            placeholder="Enter Water Goal"
            type="number"
            value={waterGoal}
            onChange={(e) => setWaterGoal(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="caloriesGoal">Target Calories to Burn:</label>
          <input
            id="caloriesGoal"
            placeholder="Enter Calories"
            type="number"
            value={caloriesGoal}
            onChange={(e) => setCaloriesGoal(e.target.value)}
          />
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default GoalTracker;
