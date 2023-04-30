import Header from "./Header";
import SideMenu from "./SideMenu";
import { useLocation } from 'react-router-dom';

const Dashboard = () => {
    const location = useLocation();
    const user = location.state;
    return (
        <div class="dashboard">
            <Header user={user} />         
            <SideMenu />
        </div>
        
    );
}

export default Dashboard;