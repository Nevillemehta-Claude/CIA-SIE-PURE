import { Link } from 'react-router-dom'
import { SiloCard } from './SiloCard'
import { EmptyState } from '@/components/common/EmptyState'
import { Spinner } from '@/components/common/Spinner'
import type { Silo } from '@/types/models'
import { FolderKanban } from 'lucide-react'

interface SiloListProps {
  silos: Silo[]
  isLoading?: boolean
}

export function SiloList({ silos, isLoading }: SiloListProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Spinner size="lg" />
      </div>
    )
  }

  if (silos.length === 0) {
    return (
      <EmptyState
        title="No Silos"
        description="No silos found for this instrument."
        icon={<FolderKanban className="h-8 w-8 text-slate-400" />}
      />
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {silos.map((silo) => (
        <Link key={silo.silo_id} to={`/silos/${silo.silo_id}`}>
          <SiloCard silo={silo} />
        </Link>
      ))}
    </div>
  )
}

