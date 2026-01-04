import { Card } from '@/components/common/Card'
import { Badge } from '@/components/common/Badge'
import type { Instrument } from '@/types/models'
import { Activity } from 'lucide-react'

interface InstrumentCardProps {
  instrument: Instrument
}

export function InstrumentCard({ instrument }: InstrumentCardProps) {
  return (
    <Card hover className="cursor-pointer">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent-primary/20">
          <Activity className="h-5 w-5 text-accent-primary" />
        </div>
        <div className="flex-1 space-y-1">
          <div className="flex items-center gap-2">
            <span className="font-display font-semibold">{instrument.symbol}</span>
            {instrument.is_active && <Badge variant="success">Active</Badge>}
          </div>
          <p className="text-sm text-slate-400">{instrument.display_name}</p>
        </div>
      </div>
    </Card>
  )
}

