import { useState } from 'react'
import StockAlerts from './pages/StockAlerts'
import StockAlertForm from './pages/StockAlertForm'
import './App.css'

function App() {

  return (
    <div className="app">
      <h1>📈 Real-Time Stock Market Alerts</h1>
      <StockAlertForm />
      <StockAlerts />
    </div>
  )
}

export default App
