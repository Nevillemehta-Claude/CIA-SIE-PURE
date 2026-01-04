import { useInstruments } from '@/hooks/useInstruments'
import { ChevronDown } from 'lucide-react'

interface InstrumentSelectorProps {
  selectedId: string | null
  onSelect: (instrumentId: string) => void
}

export function InstrumentSelector({ selectedId, onSelect }: InstrumentSelectorProps) {
  const { data: instruments, isLoading } = useInstruments({ active_only: true })

  const selectedInstrument = instruments?.find((i) => i.instrument_id === selectedId)

  return (
    <div className="relative">
      <select
        className="w-full appearance-none rounded-lg border border-slate-600 bg-surface-secondary px-4 py-2 pr-10 text-white focus:border-accent-primary focus:outline-none focus:ring-2 focus:ring-accent-primary/20"
        value={selectedId ?? ''}
        onChange={(e) => onSelect(e.target.value)}
        disabled={isLoading}
      >
        <option value="">Select an instrument...</option>
        {instruments?.map((instrument) => (
          <option key={instrument.instrument_id} value={instrument.instrument_id}>
            {instrument.symbol} - {instrument.display_name}
          </option>
        ))}
      </select>
      <ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
    </div>
  )
}

