import { clsx } from 'clsx'
import { Loader2 } from 'lucide-react'

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const SIZE_CLASSES = {
  sm: 'h-4 w-4',
  md: 'h-6 w-6',
  lg: 'h-8 w-8',
} as const

export function Spinner({ size = 'md', className }: SpinnerProps) {
  return (
    <Loader2
      className={clsx(
        'animate-spin text-accent-primary',
        SIZE_CLASSES[size],
        className
      )}
    />
  )
}

