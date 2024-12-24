import Link from 'next/link';

const Header = ({ userName }) => {
  return (
    <header className="bg-white shadow-md p-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <div className="flex items-center space-x-4">
          <span className="text-gray-600">Bem-vindo, {userName}</span>
          <Link
            href="/dashboard/profile"
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Perfil
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
