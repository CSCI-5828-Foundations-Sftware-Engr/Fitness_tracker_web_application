import React, { useState } from 'react';
import { FaRegUser, FaBullseye, FaUtensils, FaDumbbell, FaSignOutAlt} from 'react-icons/fa';
import { useNavigate } from "react-router-dom";

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
        id: 'nutrition',
        icon: <FaUtensils />,
        label: 'Nutrition'
      },
      {
        id: 'workout',
        icon: <FaDumbbell />,
        label: 'Workout'
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
                navigate('/login');
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
  
  return (
    <div className="side-menu">
      <ul>
        {getMenuItems()}
      </ul>
    </div>
  );
}

export default SideMenu;
