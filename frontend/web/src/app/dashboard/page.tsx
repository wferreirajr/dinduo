'use client'

import { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import Footer from './Footer';
import { FaWallet, FaCreditCard, FaTags, FaChartBar, FaTachometerAlt } from 'react-icons/fa';

export default function Dashboard() {
  const [activeMenu, setActiveMenu] = useState('Dashboard');

  const menuItems = [
    { name: 'Dashboard', icon: FaTachometerAlt },
    { name: 'Conta', icon: FaWallet },
    { name: 'Cartão', icon: FaCreditCard },
    { name: 'Categoria', icon: FaTags },
    { name: 'Despesa', icon: FaChartBar },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />

      <div className="flex flex-grow">
        <Sidebar menuItems={menuItems} activeMenu={activeMenu} setActiveMenu={setActiveMenu} />

        <main className="flex-grow p-6">
          <h2 className="text-2xl font-semibold mb-6">{activeMenu}</h2>
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600">
              Conteúdo do {activeMenu} será exibido aqui.
            </p>
            <p className="mt-4 text-sm text-gray-500">
              Controle financeiro é a prática de registrar, analisar e planejar o fluxo de receitas e despesas da casa, 
              periódica e permanentemente, e de adquirir hábitos de consumo mais conscientes, garantindo o equilíbrio 
              entre necessidades e desejos, e entre o presente e o futuro.
            </p>
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}
