export default function Header() {
    return (
      <header className="bg-blue-600 text-white p-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">DinDuo</h1>
        <a
          href="/login"
          className="px-6 py-2 bg-white text-blue-600 rounded-full hover:bg-blue-50 transition-colors font-semibold"
        >
          Sair
        </a>
      </header>
    );
  }
  