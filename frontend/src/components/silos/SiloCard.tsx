import { Card } from '@/components/common/Card'
import { Badge } from '@/components/common/Badge'
import type { Silo } from '@/types/models'
import { FolderKanban, Heart } from 'lucide-react'

interface SiloCardProps {
  silo: Silo
}

export function SiloCard({ silo }: SiloCardProps) {
  return (
    <Card hover className="cursor-pointer">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-500/20">
          <FolderKanban className="h-5 w-5 text-purple-400" />
        </div>
        <div className="flex-1 space-y-1">
          <div className="flex items-center gap-2">
            <span className="font-display font-semibold">{silo.silo_name}</span>
            {silo.is_active && <Badge variant="success">Active</Badge>}
          </div>
          {silo.heartbeat_enabled && (
            <div className="flex items-center gap-1 text-sm text-slate-400">
              <Heart className="h-3 w-3 text-red-400" />
              <span>Heartbeat every {silo.heartbeat_frequency_min}m</span>
            </div>
          )}
        </div>
      </div>
    </Card>
  )
}

