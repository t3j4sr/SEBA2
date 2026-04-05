import React from 'react'
import ReactDOM from 'react-dom/client'
import { AuthLayout } from './components/auth/auth-layout'
import { LoginForm } from './components/auth/login-form'
import './index.css'

const rootElement = document.getElementById('react-auth-root');
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <AuthLayout>
        <LoginForm />
      </AuthLayout>
    </React.StrictMode>,
  )
}
