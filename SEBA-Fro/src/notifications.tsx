import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'
import { initialNotifications } from './components/ui/notification-inbox-popover'
import './index.css'

function NotificationsPage() {
  const [notifications, setNotifications] = useState(initialNotifications);

  const markAsRead = (id: number) => {
    setNotifications(
      notifications.map((n) => (n.id === id ? { ...n, unread: false } : n)),
    );
  };

  const markAllAsRead = () => {
    setNotifications(notifications.map((n) => ({ ...n, unread: false })));
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 flex justify-center py-12 px-4 selection:bg-indigo-500 selection:text-white font-sans" style={{backgroundImage: "radial-gradient(ellipse at top center, rgba(79, 70, 229, 0.15) 0%, transparent 60%)"}}>
      <div className="w-full max-w-3xl bg-zinc-950/80 backdrop-blur-xl border border-white/5 rounded-2xl shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-white/5">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight text-white bg-clip-text">Notifications</h1>
            <p className="text-sm text-zinc-400 mt-1">Manage all your alerts and messages.</p>
          </div>
          <div className="flex gap-4 items-center">
            <button
               onClick={markAllAsRead}
               className="text-sm font-medium text-zinc-300 hover:text-white bg-zinc-900 hover:bg-zinc-800 px-4 py-2 rounded-lg transition-colors border border-white/5"
            >
              Mark all as read
            </button>
            <a href="/index.html" className="text-sm text-blue-400 hover:text-blue-300 transition-colors">← Back to Dashboard</a>
          </div>
        </div>

        {/* List */}
        <div className="divide-y divide-white/5">
          {notifications.map((n) => {
            const Icon = n.icon;
            return (
              <div 
                key={n.id} 
                onClick={() => markAsRead(n.id)}
                className={`flex gap-4 p-6 cursor-pointer transition-all duration-200 ${
                  n.unread ? "bg-white/5 hover:bg-white/10" : "hover:bg-white/5 opacity-80"
                }`}
              >
                <div className={`mt-1 flex-shrink-0 ${n.unread ? "text-indigo-400" : "text-zinc-500"}`}>
                  <Icon size={24} />
                </div>
                <div className="flex-1">
                  <p className={`text-base ${n.unread ? "font-semibold text-zinc-100" : "font-normal text-zinc-400"}`}>
                    {n.user} {n.action} <span className="text-white font-medium">{n.target}</span>
                  </p>
                  <p className="text-sm text-zinc-500 mt-1">{n.timestamp}</p>
                </div>
                {n.unread && (
                   <div className="flex-shrink-0 self-center">
                     <span className="block size-3 rounded-full bg-indigo-500 shadow-[0_0_12px_rgba(79,70,229,0.8)]" />
                   </div>
                )}
              </div>
            );
          })}
        </div>

      </div>
    </div>
  )
}

const rootElement = document.getElementById('react-notifications-page-root');
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <NotificationsPage />
    </React.StrictMode>,
  )
}
