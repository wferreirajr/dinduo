export default function Home() {
  return (
    <div className="min-h-screen flex flex-col justify-between items-center p-8">
      <main className="flex flex-col items-center text-center">
        <h1 className="text-4xl font-bold mb-4">Bem-vindo ao DinDuo!</h1>
        <p className="text-lg mb-2">Gerencie suas finanças pessoais de forma simples e eficaz.</p>
        <p className="text-lg mb-8">Para começar, faça login ou cadastre-se no aplicativo.</p>

        <div className="flex space-x-4">
          <a
            className="px-6 py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors"
            href="/login"
          >
            Login
          </a>
          <a
            className="px-6 py-2 bg-white text-blue-600 border border-blue-600 rounded-full hover:bg-blue-50 transition-colors"
            href="/signup"
          >
            Cadastro
          </a>
        </div>
      </main>
      <footer className="w-full text-center mt-8">
        <p>&copy; 2024 DinDuo. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}
