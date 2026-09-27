import { NavLink, Outlet } from "react-router-dom";

export default function DashboardLayout() {
  const menu = [
    { name: "Dashboard", path: "/" },
    { name: "Documents", path: "/documents" },
    { name: "Upload", path: "/upload" },
    { name: "AI Chat", path: "/chat" },
    { name: "Analytics", path: "/analytics" },
  ];

  return (
    <div className="flex min-h-screen">
      <aside className="w-64 bg-slate-900 text-white p-6">
        <h1 className="text-2xl font-bold mb-8">
          KnowledgePulse AI
        </h1>

        <nav className="space-y-3">
          {menu.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `block rounded-lg px-4 py-3 ${
                  isActive
                    ? "bg-blue-600"
                    : "hover:bg-slate-700"
                }`
              }
            >
              {item.name}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="flex-1 bg-gray-100 p-8">
        <Outlet />
      </main>
    </div>
  );
}