import Header from "./Header";
import SideMenu from "./SideMenu";
import GoalTracker from "./GoalTracker";
import UserProfile from "./UserProfile";

const Dashboard = () => {
    return (
        <div class="dashboard">
            <Header />
            <div class="dashComp">
                <SideMenu />
                <UserProfile />
            </div>
            
        </div>
        
    );
}

export default Dashboard;