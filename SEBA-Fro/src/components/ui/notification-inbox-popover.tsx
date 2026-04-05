"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Bell,
  GitMerge,
  FileText,
  ClipboardCheck,
  Mail,
  MessageSquareQuote,
  AlertCircle,
  LucideIcon,
} from "lucide-react";

interface Notification {
  id: number;
  user: string;
  action: string;
  target: string;
  timestamp: string;
  unread: boolean;
  icon: LucideIcon;
}

export const initialNotifications: Notification[] = [];

function NotificationInboxPopover() {
  const [notifications, setNotifications] = useState(initialNotifications);
  const unreadCount = notifications.filter((n) => n.unread).length;
  const [tab, setTab] = useState("all");

  const filtered = tab === "unread" ? notifications.filter((n) => n.unread) : notifications;

  const markAsRead = (id: number) => {
    setNotifications(
      notifications.map((n) => (n.id === id ? { ...n, unread: false } : n)),
    );
  };

  const markAllAsRead = () => {
    setNotifications(notifications.map((n) => ({ ...n, unread: false })));
  };

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button size="icon" variant="outline" className="relative shadow-none border-none bg-transparent hover:bg-white/10" aria-label="Open notifications">
          <Bell size={24} strokeWidth={2} aria-hidden="true" color="white" />
          {unreadCount > 0 && (
            <Badge className="absolute -top-1 left-full min-w-5 -translate-x-1/2 px-1 bg-primary border border-transparent shadow shadow-black/20 text-white rounded-full flex items-center justify-center pointer-events-none">
              {unreadCount > 99 ? "99+" : unreadCount}
            </Badge>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[380px] p-0 mr-4">
        {/* Header with Tabs + Mark All */}
        <Tabs value={tab} onValueChange={setTab}>
          <div className="flex items-center justify-between border-b px-3 py-2">
            <TabsList className="bg-transparent">
              <TabsTrigger value="all" className="text-sm">All</TabsTrigger>
              <TabsTrigger value="unread" className="text-sm">
                Unread {unreadCount > 0 && <Badge className="ml-1 px-1 bg-muted-foreground/20 text-foreground" variant="secondary">{unreadCount}</Badge>}
              </TabsTrigger>
            </TabsList>
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="text-xs font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                Mark all as read
              </button>
            )}
          </div>

          {/* Notifications List */}
          <div className="max-h-80 overflow-y-auto custom-scroll">
            {filtered.length === 0 ? (
              <div className="px-3 py-6 text-center text-sm text-muted-foreground flex flex-col items-center">
                <Bell size={24} className="mb-2 opacity-20" />
                No notifications
              </div>
            ) : (
              filtered.map((n) => {
                const Icon = n.icon;
                return (
                  <button
                    key={n.id}
                    onClick={() => markAsRead(n.id)}
                    className="flex w-full items-start gap-3 border-b px-3 py-3 text-left hover:bg-accent group transition-colors"
                  >
                    <div className="mt-1 text-muted-foreground group-hover:text-foreground transition-colors">
                      <Icon size={18} />
                    </div>
                    <div className="flex-1 space-y-1">
                      <p
                        className={`text-sm tracking-tight ${
                          n.unread ? "font-semibold text-foreground" : "text-foreground/80"
                        }`}
                      >
                        {n.user} {n.action}{" "}
                        <span className="font-medium text-foreground">{n.target}</span>
                      </p>
                      <p className="text-xs text-muted-foreground">{n.timestamp}</p>
                    </div>
                    {n.unread && (
                      <span className="mt-2 inline-block size-2 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.6)]" />
                    )}
                  </button>
                );
              })
            )}
          </div>
        </Tabs>

        {/* Footer */}
        <div className="px-3 py-2 text-center border-t">
          <Button variant="ghost" size="sm" className="w-full text-xs text-muted-foreground hover:text-foreground" onClick={() => window.location.href = '/notifications.html'}>
            View all notifications
          </Button>
        </div>
      </PopoverContent>
    </Popover>
  );
}

export { NotificationInboxPopover };
