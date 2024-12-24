'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const menuItems = [
  { name: 'Dashboard', href: '/dashboard', icon: '🏠' },
  { name: 'Conta', href: '/account', icon: '👤' },
  { name: 'Cartão', href: '/card', icon: '💳' },
  { name: 'Categoria', href: '/category', icon: '🏷️' },
  { name: 'Despesa', href: '/expense', icon: '💰' },
];

const Sidebar = () => {
  const pathname = usePathname();

  return (
    <aside className="bg-gray-800 text-white w-64 min-h-screen p-4">
      <nav className="space-y-2">
        {menuItems.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className={`flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-700 transition-colors w-full ${
              pathname === item.href ? 'bg-gray-700' : ''
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span className="text-sm font-medium">{item.name}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
