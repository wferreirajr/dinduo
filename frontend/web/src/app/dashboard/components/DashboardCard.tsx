const DashboardCard = ({ title, value, icon, color }) => {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${color}`}>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold mb-2">{title}</h2>
            <p className="text-3xl font-bold">{value}</p>
          </div>
          <div className={`text-4xl ${color.replace('bg-', 'text-')}`}>
            <i className={`fas fa-${icon}`}></i>
          </div>
        </div>
      </div>
    );
  };
  
  export default DashboardCard;
  