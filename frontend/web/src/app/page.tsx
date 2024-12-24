'use client'

import { useState } from 'react';
import { FaChartLine, FaClipboardList, FaRegCheckCircle } from 'react-icons/fa';

export default function Home() {
  const [showMenu, setShowMenu] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">
            <a href='/'>
              DinDuo
            </a>
          </h1>
          <a
            href="/login"
            className="px-6 py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors font-semibold"
          >
            Login
          </a>
        </div>
      </header>

      <main className="flex-grow">
        <section className="bg-blue-600 text-white py-20">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl font-bold mb-4">Controle Financeiro é o Caminho para a Liberdade</h2>
            <p className="text-xl mb-8 text-center">Organize suas finanças, entenda seus gastos e alcance seus objetivos financeiros.</p>
            <a href="/signup" className="bg-white text-blue-600 px-6 py-3 rounded-full font-bold hover:bg-blue-100 transition-colors">
              Comece Agora - É Grátis!
            </a>
          </div>
        </section>

        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <h3 className="text-2xl font-bold text-center mb-12">O que é Controle Financeiro?</h3>
            <p className="text-lg mb-6 text-justify">
              Controle financeiro é a prática de registrar, analisar e planejar o fluxo de receitas e despesas da casa,
              periódica e permanentemente, e de adquirir hábitos de consumo mais conscientes, garantindo o equilíbrio
              entre necessidades e desejos, e entre o presente e o futuro.
            </p>
            <div className="grid md:grid-cols-3 gap-8 mt-12">
              <div className="text-center">
                <div className="bg-blue-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl">📊</span>
                </div>
                <h4 className="font-bold mb-2">Registrar Despesas e Receitas</h4>
                <p>Anote todas as entradas e saídas de dinheiro para ter uma visão clara das suas finanças.</p>
              </div>
              <div className="text-center">
                <div className="bg-blue-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl">💼</span>
                </div>
                <h4 className="font-bold mb-2">Utilizar Orçamento Doméstico</h4>
                <p>Planeje seus gastos futuros e acompanhe se estão de acordo com o programado.</p>
              </div>
              <div className="text-center">
                <div className="bg-blue-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl">🛒</span>
                </div>
                <h4 className="font-bold mb-2">Consumo Consciente</h4>
                <p>Adquira hábitos de consumo mais conscientes, equilibrando necessidades e desejos.</p>
              </div>
            </div>
          </div>
        </section>

        <section className="py-16 bg-gradient-to-b from-blue-50 to-white">
          <div className="container mx-auto px-4">
            <h3 className="text-3xl font-bold text-center mb-12 text-blue-600">Ferramentas para Controle Financeiro</h3>
            <div className="grid md:grid-cols-2 gap-12">
              <div className="bg-white rounded-lg shadow-lg p-6 transition-transform hover:scale-105">
                <div className="flex flex-col items-center mb-6">
                  <FaChartLine className="text-4xl text-blue-500 mb-2" />
                  <h4 className="font-bold text-2xl text-gray-800 text-center">Fluxo de Caixa</h4>
                </div>
                <p className="mb-6 text-gray-600 text-justify">
                  Visualize sua situação financeira atual com um demonstrativo organizado das entradas e saídas de dinheiro.
                </p>
                <ul className="space-y-3 flex flex-col items-center">
                  {['Registre receitas e despesas', 'Organize por categorias', 'Analise mensalmente'].map((item, index) => (
                    <li key={index} className="flex items-center">
                      <FaRegCheckCircle className="text-green-500 mr-2" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="bg-white rounded-lg shadow-lg p-6 transition-transform hover:scale-105">
                <div className="flex flex-col items-center mb-6">
                  <FaClipboardList className="text-4xl text-blue-500 mb-2" />
                  <h4 className="font-bold text-2xl text-gray-800 text-center">Orçamento Doméstico</h4>
                </div>
                <p className="mb-6 text-gray-600 text-justify">
                  Planeje e controle suas finanças de forma eficiente com uma projeção de receitas e despesas futuras.
                </p>
                <ul className="space-y-3 flex flex-col items-center">
                  {['Projete receitas e despesas para os próximos meses', 'Estabeleça metas de gastos por categoria', 'Compare o planejado com o realizado'].map((item, index) => (
                    <li key={index} className="flex items-center">
                      <FaRegCheckCircle className="text-green-500 mr-2" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </section>


        <section className="py-16 bg-white">
          <div className="container mx-auto px-4 text-center">
            <h3 className="text-2xl font-bold mb-8">Comece seu Controle Financeiro Hoje!</h3>
            <p className="text-lg mb-8 text-justify">
              Com o DinDuo, você tem todas as ferramentas necessárias para organizar suas finanças e
              conquistar seus objetivos. Não espere mais para começar sua jornada rumo à liberdade financeira.
            </p>
            <a href="/signup" className="bg-blue-600 text-white px-6 py-3 rounded-full font-bold hover:bg-blue-700 transition-colors">
              Criar Minha Conta Gratuita
            </a>
          </div>
        </section>
      </main>

      <footer className="bg-white shadow-md bg-gray-800 text-black py-8">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2024 DinDuo. Todos os direitos reservados.</p>
        </div>
      </footer>
    </div>
  );
}
