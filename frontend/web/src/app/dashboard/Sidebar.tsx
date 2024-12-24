import { IconType } from 'react-icons';

interface MenuItem {
  name: string;
  icon: IconType;
}

interface SidebarProps {
  menuItems: MenuItem[];
  activeMenu: string;
  setActiveMenu: (menu: string) => void;
}

export default function Sidebar({ menuItems, activeMenu, setActiveMenu }: SidebarProps) {
  return (
    <>
      <nav className="bg-white w-64 p-6 hidden md:block">
        <ul className="space-y-4">
          {menuItems.map((item) => (
            <li key={item.name}>
              <button
                onClick={() => setActiveMenu(item.name)}
                className={`flex items-center w-full p-2 rounded transition-colors ${
                  activeMenu === item.name
                    ? 'bg-blue-100 text-blue-600'
                    : 'hover:bg-gray-100'
                }`}
              >
                <item.icon className="mr-3" />
                {item.name}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <nav className="md:hidden bg-white border-t fixed bottom-0 left-0 right-0">
        <ul className="flex justify-around">
          {menuItems.map((item) => (
            <li key={item.name}>
              <button
                onClick={() => setActiveMenu(item.name)}
                className={`p-4 flex flex-col items-center ${
                  activeMenu === item.name ? 'text-blue-600' : 'text-gray-600'
                }`}
              >
                <item.icon className="text-xl mb-1" />
                <span className="text-xs">{item.name}</span>
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </>
  );
}
