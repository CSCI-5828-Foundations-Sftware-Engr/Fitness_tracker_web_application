import React, { useState } from 'react';
import { FaRegUser, FaBullseye, FaUtensils, FaDumbbell, FaSignOutAlt, FaLightbulb} from 'react-icons/fa';
import { useNavigate } from "react-router-dom";
import GoalTracker from "./GoalTracker";
import UserProfile from "./UserProfile";
import Nutrition from "./Nutrition";
import Workout from "./Workout";

const SideMenu = () => {
  const navigate = useNavigate();
  const [selectedOption, setSelectedOption] = useState('goal');

  const handleOptionClick = (option) => {
    setSelectedOption(option);
  };
  const getMenuItems = () => {
    const items = [
      {
        id: 'profile',
        icon: <FaRegUser />,
        label: 'Profile'
      },
      {
        id: 'goal',
        icon: <FaBullseye />,
        label: 'Goal Tracking'
      },
      {
        id: 'workout',
        icon: <FaDumbbell />,
        label: 'Workout'
      },
      {
        id: 'nutrition',
        icon: <FaUtensils />,
        label: 'Nutrition'
      }, 
      {
        id: 'recommendation',
        icon: <FaLightbulb />,
        label: 'Recommendations'
      }, 
      {
        id: 'logout',
        icon: <FaSignOutAlt />,
        label: 'Logout'
      }
    ];
  
    return items.map(item => (
      <li
        key={item.id}
        className={item.id === selectedOption ? 'selected' : item.id === 'logout' ? 'logout' : ''}
        onClick={() =>  {
            if (item.id === 'logout') {
                navigate('/');
              } else {
                handleOptionClick(item.id);
              }
        }}
      >
        {item.icon}
        <span>{item.label}</span>
      </li>
    ));
  };

  const renderSelectedComponent = () => {
    switch (selectedOption) {
      case 'profile':
        return <UserProfile />;
      case 'goal':
        return <GoalTracker />;
      case 'nutrition':
        return <Nutrition />;
      case 'workout':
        return <Workout />;
      default:
        return null;
    }
  };
  
  return (
    <div class="dashboard-components">
    <div className="side-menu">
      <ul>
        {getMenuItems()}
      </ul>     
    </div>
    {renderSelectedComponent()}
    </div>
  );
}

export default SideMenu;
