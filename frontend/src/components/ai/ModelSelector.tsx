import { clsx } from 'clsx'
import { useModels } from '@/hooks/useAI'
import { Spinner } from '@/components/common/Spinner'

interface ModelSelectorProps {
  selectedModel: string
  onSelect: (modelId: string) => void
  disabled?: boolean
}

export function ModelSelector({ selectedModel, onSelect, disabled }: ModelSelectorProps) {
  const { data, isLoading } = useModels()

  if (isLoading) {
    return <Spinner size="sm" />
  }

  if (!data?.models) {
    return null
  }

  return (
    <div className="flex gap-2">
      {data.models.map((model) => (
        <button
          key={model.id}
          onClick={() => onSelect(model.id)}
          disabled={disabled}
          className={clsx(
            'rounded-lg px-3 py-1.5 text-sm font-medium transition-colors',
            selectedModel === model.id
              ? 'bg-accent-primary text-white'
              : 'bg-surface-secondary text-slate-300 hover:bg-surface-tertiary hover:text-white',
            disabled && 'cursor-not-allowed opacity-50'
          )}
        >
          {model.display_name}
        </button>
      ))}
    </div>
  )
}

