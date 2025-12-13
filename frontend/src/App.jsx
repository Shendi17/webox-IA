import { useState } from 'react'
import Chat from './components/Chat'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-gray-900">
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-white">
            WeBox Multi-IA
          </h1>
          <p className="text-gray-400 text-sm">
            L'Interface IA la Plus Complète du Marché
          </p>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-6">
        <Chat />
      </main>
    </div>
  )
}

export default App
