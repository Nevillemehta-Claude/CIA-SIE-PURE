import { useUsage, useBudget, useModels } from '@/hooks/useAI'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardHeader, CardTitle } from '@/components/common/Card'
import { Spinner } from '@/components/common/Spinner'
import { formatCurrency, formatNumber } from '@/lib/utils'
import { Cpu, DollarSign, BarChart3 } from 'lucide-react'
import { clsx } from 'clsx'

export function SettingsPage() {
  const { data: budget, isLoading: budgetLoading } = useBudget()
  const { data: usage, isLoading: usageLoading } = useUsage('monthly')
  const { data: models, isLoading: modelsLoading } = useModels()

  return (
    <div className="space-y-6">
      <PageHeader
        title="Settings"
        description="AI configuration and usage statistics"
      />

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Budget Status */}
        <Card>
          <CardHeader>
            <CardTitle>
              <div className="flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-accent-primary" />
                AI Budget
              </div>
            </CardTitle>
          </CardHeader>

          {budgetLoading ? (
            <div className="flex items-center justify-center py-8">
              <Spinner />
            </div>
          ) : budget ? (
            <div className="space-y-4">
              <div className="flex items-baseline justify-between">
                <span className="text-2xl font-bold">{formatCurrency(budget.remaining)}</span>
                <span className="text-sm text-slate-400">
                  remaining
                </span>
              </div>

              <div className="h-3 overflow-hidden rounded-full bg-slate-700">
                <div
                  className={clsx(
                    'h-full transition-all',
                    budget.percentage_used >= 90
                      ? 'bg-red-500'
                      : budget.percentage_used >= 80
                        ? 'bg-amber-500'
                        : budget.percentage_used >= 50
                          ? 'bg-yellow-500'
                          : 'bg-green-500'
                  )}
                  style={{ width: `${Math.min(budget.percentage_used, 100)}%` }}
                />
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Used: {budget.percentage_used.toFixed(1)}%</span>
                <span className={clsx(
                  budget.within_budget ? 'text-green-400' : 'text-red-400'
                )}>
                  {budget.within_budget ? 'Within Budget' : 'Over Budget'}
                </span>
              </div>

              {budget.alert_level && (
                <div className="rounded-lg bg-amber-500/10 p-3 text-sm text-amber-400">
                  ⚠️ {budget.message || `Budget alert: ${budget.alert_level}`}
                </div>
              )}
            </div>
          ) : null}
        </Card>

        {/* Usage Statistics */}
        <Card>
          <CardHeader>
            <CardTitle>
              <div className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-accent-primary" />
                Monthly Usage
              </div>
            </CardTitle>
          </CardHeader>

          {usageLoading ? (
            <div className="flex items-center justify-center py-8">
              <Spinner />
            </div>
          ) : usage ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="rounded-lg bg-surface-tertiary p-3">
                  <div className="text-sm text-slate-400">Total Requests</div>
                  <div className="text-xl font-semibold">{formatNumber(usage.requests_count)}</div>
                </div>
                <div className="rounded-lg bg-surface-tertiary p-3">
                  <div className="text-sm text-slate-400">Total Cost</div>
                  <div className="text-xl font-semibold">{formatCurrency(usage.total_cost)}</div>
                </div>
                <div className="rounded-lg bg-surface-tertiary p-3">
                  <div className="text-sm text-slate-400">Input Tokens</div>
                  <div className="text-xl font-semibold">{formatNumber(usage.input_tokens)}</div>
                </div>
                <div className="rounded-lg bg-surface-tertiary p-3">
                  <div className="text-sm text-slate-400">Output Tokens</div>
                  <div className="text-xl font-semibold">{formatNumber(usage.output_tokens)}</div>
                </div>
              </div>
            </div>
          ) : null}
        </Card>
      </div>

      {/* Available Models */}
      <Card>
        <CardHeader>
          <CardTitle>
            <div className="flex items-center gap-2">
              <Cpu className="h-5 w-5 text-accent-primary" />
              Available Models
            </div>
          </CardTitle>
        </CardHeader>

        {modelsLoading ? (
          <div className="flex items-center justify-center py-8">
            <Spinner />
          </div>
        ) : models?.models ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {models.models.map((model) => (
              <div
                key={model.id}
                className={clsx(
                  'rounded-lg border p-4',
                  model.id === models.default_model
                    ? 'border-accent-primary bg-accent-primary/10'
                    : 'border-slate-700 bg-surface-tertiary'
                )}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold">{model.display_name}</span>
                  {model.id === models.default_model && (
                    <span className="rounded bg-accent-primary/20 px-2 py-0.5 text-xs text-accent-primary">
                      Default
                    </span>
                  )}
                </div>
                <p className="mt-1 text-xs text-slate-500">{model.description}</p>
                <div className="mt-2 text-sm text-slate-400">
                  <div>Input: {formatCurrency(model.cost_per_1k_input_tokens)}/1K</div>
                  <div>Output: {formatCurrency(model.cost_per_1k_output_tokens)}/1K</div>
                </div>
              </div>
            ))}
          </div>
        ) : null}
      </Card>
    </div>
  )
}

