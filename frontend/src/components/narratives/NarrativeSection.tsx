interface NarrativeSectionProps {
  title: string
  content: string
}

export function NarrativeSection({ title, content }: NarrativeSectionProps) {
  return (
    <div className="space-y-2">
      <h4 className="text-sm font-medium uppercase text-slate-400">{title}</h4>
      <p className="text-slate-300">{content}</p>
    </div>
  )
}

