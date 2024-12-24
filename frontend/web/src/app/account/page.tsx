import Sidebar from '../dashboard/components/Sidebar';
import AccountList from './components/AccountList';
import AddAccountButton from './components/AddAccountButton';

const AccountPage = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-x-hidden overflow-y-auto p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-800">Minhas Contas</h1>
            <p className="text-gray-600">Gerencie suas contas bancárias</p>
          </div>
          
          <AccountList />
          <AddAccountButton />
        </main>
      </div>
    </div>
  );
};

export default AccountPage;
