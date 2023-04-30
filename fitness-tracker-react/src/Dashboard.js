import Header from "./Header";
import SideMenu from "./SideMenu";
import GoalTracker from "./GoalTracker";

const Dashboard = () => {
    return (
        <div class="dashboard">
            <Header />
            <div class="dashComp">
                <SideMenu />
                <GoalTracker />
            </div>
            
        </div>
        
    );
}

export default Dashboard;