import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';

const GoalTracker = () => {
  const location = useLocation();
  const user = location.state;
  const username = user.username
  const [current_weight, setCurrentWeight] = useState('');
  const [target_weight, setTargetWeight] = useState('');
  const [age, setAge] = useState('');
  const [height, setHeight] = useState('');
  const [steps_goal, setTargetSteps] = useState('');
  const [calorie_burn_goal, setCaloriesBurnGoal] = useState('');
  const [water_goal, setWaterGoal] = useState('');
  const [calorie_intake_goal, setCaloriesIntakeGoal] = useState('');
  const [protein_goal, setProteinGoal] = useState('');
  const [carbs_goal, setCarbsGoal] = useState('');
  const [fat_goal, setFatGoal] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch('http://127.0.0.1:5000/goal_tracking', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        current_weight,
        target_weight,
        age,
        height,
        steps_goal,
        calorie_burn_goal,
        water_goal,
        calorie_intake_goal,
        protein_goal,
        carbs_goal,
        fat_goal
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
          <label htmlFor="water_goal">Water Goal (in glasses):</label>
          <input
            id="water_goal"
            placeholder="Enter Water Goal"
            type="number"
            value={water_goal}
            onChange={(e) => setWaterGoal(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="current_weight">Current weight:</label>
          <input
            id="current_weight"
            placeholder="Enter Weight"
            type="number"
            value={current_weight}
            onChange={(e) => setCurrentWeight(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="target_weight">Targeted weight:</label>
          <input
            id="target_weight"
            placeholder="Enter Weight"
            type="number"
            value={target_weight}
            onChange={(e) => setTargetWeight(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="steps_goal">Target no. of steps:</label>
          <input
            id="steps_goal"
            placeholder="Enter Steps"
            type="number"
            value={steps_goal}
            onChange={(e) => setTargetSteps(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="protein_goal">Protein Goal:</label>
          <input
            id="protein_goal"
            placeholder="Enter Protein Goal"
            type="number"
            value={protein_goal}
            onChange={(e) => setProteinGoal(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="carbs_goal">Carbs Goal:</label>
          <input
            id="carbs_goal"
            placeholder="Enter Carbs Goal"
            type="number"
            value={carbs_goal}
            onChange={(e) => setCarbsGoal(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="fat_goal">Fat Goal:</label>
          <input
            id="fat_goal"
            placeholder="Enter Fat Goal"
            type="number"
            value={fat_goal}
            onChange={(e) => setFatGoal(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="calorie_burn_goal">Target Calories to Burn:</label>
          <input
            id="calorie_burn_goal"
            placeholder="Enter Distance"
            type="number"
            value={calorie_burn_goal}
            onChange={(e) => setCaloriesBurnGoal(e.target.value)}
          />
        </div>

        <div class="row">
          <label htmlFor="calorie_intake_goal">Target Calories Intake:</label>
          <input
            id="calorie_intake_goal"
            placeholder="Enter Calories"
            type="number"
            value={calorie_intake_goal}
            onChange={(e) => setCaloriesIntakeGoal(e.target.value)}
          />
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default GoalTracker;
