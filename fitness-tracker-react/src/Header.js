import React from "react";
import logo from "./logo-svg.svg";

function Header(props) {
  console.log(props);
  return (
    <div className="header-with-logo">
      <img src={logo} width={200} height={70} />
      <div className="app-header">
        <div className="user-initial-circle">{props.user?.username.slice(0,1).toUpperCase()}</div>
      </div>
      
    </div>
  );
}

export default Header;