import { useState, useEffect, useRef } from 'react'
import { Send, Bot, User, Loader2 } from 'lucide-react'
import axios from 'axios'

const Chat = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedProviders, setSelectedProviders] = useState(['GPT-4'])
  const messagesEndRef = useRef(null)

  const providers = [
    { id: 'GPT-4', name: 'GPT-4', model: 'gpt-4-turbo' },
    { id: 'Claude', name: 'Claude 3', model: 'claude-3-opus' },
    { id: 'Gemini', name: 'Gemini Pro', model: 'gemini-pro' },
  ]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setLoading(true)

    // Ajouter le message utilisateur
    setMessages(prev => [...prev, {
      role: 'user',
      content: userMessage
    }])

    try {
      const response = await axios.post('/api/chat/send', {
        message: userMessage,
        selected_providers: selectedProviders,
        selected_models: providers.reduce((acc, p) => {
          if (selectedProviders.includes(p.id)) {
            acc[p.id] = p.model
          }
          return acc
        }, {}),
        temperature: 0.7,
        max_tokens: 2000
      })

      // Ajouter les réponses des IA
      setMessages(prev => [...prev, {
        role: 'assistant',
        ai_responses: response.data.ai_responses,
        response_time: response.data.response_time
      }])
    } catch (error) {
      console.error('Error sending message:', error)
      setMessages(prev => [...prev, {
        role: 'error',
        content: 'Erreur lors de l\'envoi du message. Vérifiez que l\'API est démarrée.'
      }])
    } finally {
      setLoading(false)
    }
  }

  const toggleProvider = (providerId) => {
    setSelectedProviders(prev => {
      if (prev.includes(providerId)) {
        return prev.filter(id => id !== providerId)
      } else {
        return [...prev, providerId]
      }
    })
  }

  return (
    <div className="flex flex-col h-[calc(100vh-120px)] bg-gray-800 rounded-lg shadow-xl">
      {/* Header avec sélection des IA */}
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold text-white mb-3">
          Sélectionnez les IA
        </h2>
        <div className="flex flex-wrap gap-2">
          {providers.map(provider => (
            <button
              key={provider.id}
              onClick={() => toggleProvider(provider.id)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedProviders.includes(provider.id)
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {provider.name}
            </button>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            <Bot className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-lg">Commencez une conversation avec les IA</p>
            <p className="text-sm mt-2">
              Sélectionnez une ou plusieurs IA et posez votre question
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} className="space-y-2">
            {message.role === 'user' && (
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                  <User className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1 bg-gray-700 rounded-lg p-3">
                  <p className="text-white">{message.content}</p>
                </div>
              </div>
            )}

            {message.role === 'assistant' && (
              <div className="space-y-3">
                {Object.entries(message.ai_responses).map(([provider, response]) => (
                  <div key={provider} className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-sm font-semibold text-green-400">
                          {provider}
                        </span>
                        {message.response_time && (
                          <span className="text-xs text-gray-500">
                            {message.response_time}ms
                          </span>
                        )}
                      </div>
                      <div className="bg-gray-700 rounded-lg p-3">
                        <p className="text-white whitespace-pre-wrap">{response}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {message.role === 'error' && (
              <div className="bg-red-900/20 border border-red-700 rounded-lg p-3">
                <p className="text-red-400">{message.content}</p>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3 text-gray-400">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Les IA réfléchissent...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={sendMessage} className="p-4 border-t border-gray-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Posez votre question..."
            disabled={loading || selectedProviders.length === 0}
            className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-600 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={loading || !input.trim() || selectedProviders.length === 0}
            className="bg-primary-600 text-white rounded-lg px-6 py-3 font-medium hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <Send className="w-5 h-5" />
            Envoyer
          </button>
        </div>
        {selectedProviders.length === 0 && (
          <p className="text-sm text-red-400 mt-2">
            Veuillez sélectionner au moins une IA
          </p>
        )}
      </form>
    </div>
  )
}

export default Chat
