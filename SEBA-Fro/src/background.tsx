import React from 'react'
import ReactDOM from 'react-dom/client'
import { Particles } from './components/ui/particles'
import './index.css'

const elements = document.querySelectorAll('.react-particles-root');
elements.forEach(rootElement => {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <Particles color="#818cf8" quantity={120} ease={20} className="absolute inset-0 z-[-1] pointer-events-none" />
    </React.StrictMode>,
  )
})
