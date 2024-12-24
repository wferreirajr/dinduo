'use client';
import { useState, useEffect } from 'react';

interface Account {
  id: number;
  user_id: number;
  account_name: string;
  balance: string;
  account_type: string;
}

const AccountList = () => {
  const [accounts, setAccounts] = useState<Account[]>([]);

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const response = await fetch('/api/accounts');
        const data = await response.json();
        setAccounts(data);
      } catch (error) {
        console.error('Erro ao carregar contas:', error);
      }
    };

    fetchAccounts();
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {accounts.map((account) => (
        <div
          key={account.id}
          className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold text-gray-800">
              {account.account_name}
            </h3>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              {account.account_type}
            </span>
          </div>
          <div className="mt-4">
            <p className="text-sm text-gray-600">Saldo</p>
            <p className="text-2xl font-bold text-gray-900">
              {new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
              }).format(parseFloat(account.balance))}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default AccountList;
