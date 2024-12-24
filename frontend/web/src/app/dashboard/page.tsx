import Sidebar from './components/Sidebar';
import Header from './components/Header';
import DashboardCard from './components/DashboardCard';

const DashboardPage = () => {
  const userName = 'Marli'; // Substitua por lógica de autenticação real

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header userName={userName} />
        <main className="flex-1 overflow-x-hidden overflow-y-auto p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <DashboardCard
              title="Total de Contas"
              value="5"
              icon="wallet"
              color="bg-blue-100"
            />
            <DashboardCard
              title="Cartões Ativos"
              value="3"
              icon="credit-card"
              color="bg-green-100"
            />
            <DashboardCard
              title="Categorias"
              value="8"
              icon="tags"
              color="bg-yellow-100"
            />
            <DashboardCard
              title="Despesas Mensais"
              value="R$ 2.500,00"
              icon="chart-line"
              color="bg-red-100"
            />
          </div>
          {/* Adicione mais conteúdo do dashboard aqui */}
        </main>
      </div>
    </div>
  );
};

export default DashboardPage;
