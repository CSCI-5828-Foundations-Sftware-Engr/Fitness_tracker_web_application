import React, { useState } from 'react';

const GoalTracker = () => {
  const [currentWeight, setCurrentWeight] = useState('');
  const [targetWeight, setTargetWeight] = useState('');
  const [age, setAge] = useState('');
  const [height, setHeight] = useState('');
  const [targetSteps, setTargetSteps] = useState('');
  const [targetDistance, setTargetDistance] = useState('');
  const [waterGoal, setWaterGoal] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // You can handle the form submission logic here
  };

  return (
    <div className="goal-tracker-container">
      <h2>Goal Tracker</h2>
      <form className="goal-tracker-form" onSubmit={handleSubmit}>
        <label htmlFor="currentWeight">Current weight:</label>
        <input
          id="currentWeight"
          type="number"
          value={currentWeight}
          onChange={(e) => setCurrentWeight(e.target.value)}
        />

        <label htmlFor="targetWeight">Targeted weight:</label>
        <input
          id="targetWeight"
          type="number"
          value={targetWeight}
          onChange={(e) => setTargetWeight(e.target.value)}
        />

        <label htmlFor="age">Age:</label>
        <input
          id="age"
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />

        <label htmlFor="height">Height:</label>
        <input
          id="height"
          type="number"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
        />

        <label htmlFor="targetSteps">Target no. of steps:</label>
        <input
          id="targetSteps"
          type="number"
          value={targetSteps}
          onChange={(e) => setTargetSteps(e.target.value)}
        />

        <label htmlFor="targetDistance">Distance to walk or run:</label>
        <input
          id="targetDistance"
          type="number"
          value={targetDistance}
          onChange={(e) => setTargetDistance(e.target.value)}
        />

        <label htmlFor="waterGoal">Water Goal (in liters):</label>
        <input
          id="waterGoal"
          type="number"
          value={waterGoal}
          onChange={(e) => setWaterGoal(e.target.value)}
        />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default GoalTracker;
