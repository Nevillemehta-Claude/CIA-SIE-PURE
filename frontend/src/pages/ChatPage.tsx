import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useInstruments } from '@/hooks/useInstruments'
import { ChatInterface } from '@/components/ai/ChatInterface'
import { InstrumentSelector } from '@/components/instruments/InstrumentSelector'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card } from '@/components/common/Card'
import { MessageSquare } from 'lucide-react'

export function ChatPage() {
  const { scripId: initialScripId } = useParams<{ scripId?: string }>()
  const [selectedInstrumentId, setSelectedInstrumentId] = useState<string | null>(initialScripId ?? null)
  const { data: instruments } = useInstruments({ active_only: true })

  const selectedInstrument = instruments?.find((i) => i.instrument_id === selectedInstrumentId)
  const scripId = selectedInstrument?.symbol

  return (
    <div className="flex h-full flex-col space-y-6">
      <PageHeader
        title="AI Chat"
        description="Ask questions about your chart signals"
      />

      <div className="max-w-md">
        <label className="mb-2 block text-sm text-slate-400">Select Instrument</label>
        <InstrumentSelector
          selectedId={selectedInstrumentId}
          onSelect={setSelectedInstrumentId}
        />
      </div>

      {scripId ? (
        <Card className="flex-1">
          <ChatInterface scripId={scripId} />
        </Card>
      ) : (
        <Card className="flex flex-1 items-center justify-center">
          <div className="text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-surface-tertiary">
              <MessageSquare className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-slate-400">Select an instrument to start chatting</p>
          </div>
        </Card>
      )}
    </div>
  )
}

