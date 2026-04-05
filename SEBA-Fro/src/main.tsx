import React from 'react'
import ReactDOM from 'react-dom/client'
import { NotificationInboxPopover } from './components/ui/notification-inbox-popover'
import { SebaDashboardOverview } from './components/ui/dashboard-overview'
import { SebaDashboardFeatures } from './components/ui/dashboard-features'
import './index.css'

const rootElement = document.getElementById('react-notification-root');
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <NotificationInboxPopover />
    </React.StrictMode>,
  )
}

const dashboardRoot = document.getElementById('react-dashboard-overview-root');
if (dashboardRoot) {
  ReactDOM.createRoot(dashboardRoot).render(
    <React.StrictMode>
      <SebaDashboardOverview />
    </React.StrictMode>,
  )
}

const featuresRoot = document.getElementById('react-dashboard-features-root');
if (featuresRoot) {
  ReactDOM.createRoot(featuresRoot).render(
    <React.StrictMode>
      <SebaDashboardFeatures />
    </React.StrictMode>,
  )
}
