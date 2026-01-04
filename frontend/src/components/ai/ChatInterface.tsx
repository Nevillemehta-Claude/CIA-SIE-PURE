import { useState } from 'react'
import { useSendMessage, useHistory } from '@/hooks/useChat'
import { useModels } from '@/hooks/useAI'
import { ModelSelector } from './ModelSelector'
import { Disclaimer } from '@/components/common/Disclaimer'
import { Spinner } from '@/components/common/Spinner'
import { Button } from '@/components/common/Button'
import { Send, User, Bot } from 'lucide-react'

interface ChatInterfaceProps {
  scripId: string
}

export function ChatInterface({ scripId }: ChatInterfaceProps) {
  const [message, setMessage] = useState('')
  const { data: modelsData } = useModels()
  const [selectedModel, setSelectedModel] = useState(modelsData?.default_model ?? 'claude-3-5-haiku-latest')
  const { data: historyData, isLoading: historyLoading } = useHistory(scripId)
  const sendMessage = useSendMessage(scripId)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim() || sendMessage.isPending) return

    sendMessage.mutate({ message, model: selectedModel })
    setMessage('')
  }

  return (
    <div className="flex h-full flex-col">
      {/* Header with Model Selector */}
      <div className="flex items-center justify-between border-b border-slate-700 pb-4">
        <h2 className="font-display text-lg font-semibold">AI Chat</h2>
        <ModelSelector
          selectedModel={selectedModel}
          onSelect={setSelectedModel}
          disabled={sendMessage.isPending}
        />
      </div>

      {/* Chat Messages */}
      <div className="flex-1 space-y-4 overflow-y-auto py-4">
        {historyLoading ? (
          <div className="flex items-center justify-center py-8">
            <Spinner size="lg" />
          </div>
        ) : historyData?.conversations.length === 0 ? (
          <div className="text-center text-slate-400">
            <p>No conversation history. Start chatting!</p>
          </div>
        ) : (
          historyData?.conversations.flatMap((conv) =>
            conv.messages.map((msg, idx) => (
              <div
                key={`${conv.conversation_id}-${idx}`}
                className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role === 'assistant' && (
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-accent-primary/20">
                    <Bot className="h-4 w-4 text-accent-primary" />
                  </div>
                )}
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    msg.role === 'user'
                      ? 'bg-accent-primary text-white'
                      : 'bg-surface-secondary text-slate-300'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                  {msg.role === 'assistant' && <Disclaimer variant="inline" />}
                </div>
                {msg.role === 'user' && (
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-surface-tertiary">
                    <User className="h-4 w-4 text-slate-300" />
                  </div>
                )}
              </div>
            ))
          )
        )}

        {sendMessage.isPending && (
          <div className="flex items-center gap-2 text-slate-400">
            <Spinner size="sm" />
            <span>Generating response...</span>
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="border-t border-slate-700 pt-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask about your charts..."
            className="flex-1 rounded-lg border border-slate-600 bg-surface-secondary px-4 py-2 text-white placeholder-slate-400 focus:border-accent-primary focus:outline-none focus:ring-2 focus:ring-accent-primary/20"
            disabled={sendMessage.isPending}
          />
          <Button
            type="submit"
            isLoading={sendMessage.isPending}
            leftIcon={<Send className="h-4 w-4" />}
          >
            Send
          </Button>
        </div>
      </form>
    </div>
  )
}

