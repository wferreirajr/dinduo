'use client';

const AddAccountButton = () => {
  const handleAddAccount = () => {
    // Implementar lógica para abrir modal ou navegar para página de criação
  };

  return (
    <button
      type="button"
      onClick={handleAddAccount}
      title="Adicionar nova conta"
      aria-label="Adicionar nova conta"
      className="fixed bottom-6 right-6 bg-blue-500 hover:bg-blue-600 text-white rounded-full p-4 shadow-lg transition-colors"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        aria-hidden="true"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M12 4v16m8-8H4"
        />
      </svg>
      <span className="sr-only">Adicionar nova conta</span>
    </button>
  );
};

export default AddAccountButton;
