import { useState } from 'react'
import { useBaskets, useCreateBasket, useDeleteBasket } from '@/hooks/useBaskets'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardHeader, CardTitle } from '@/components/common/Card'
import { Button } from '@/components/common/Button'
import { Badge } from '@/components/common/Badge'
import { Spinner } from '@/components/common/Spinner'
import { EmptyState } from '@/components/common/EmptyState'
import { FolderKanban, Plus, Trash2, BarChart3 } from 'lucide-react'

// Matches backend BasketType enum
type BasketType = 'LOGICAL' | 'HIERARCHICAL' | 'CONTEXTUAL' | 'CUSTOM'

export function BasketsPage() {
  const { data: baskets, isLoading } = useBaskets()
  const createMutation = useCreateBasket()
  const deleteMutation = useDeleteBasket()
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [formData, setFormData] = useState<{
    basket_name: string  // FIXED: matches backend field name
    description: string
    basket_type: BasketType
  }>({
    basket_name: '',
    description: '',
    basket_type: 'CUSTOM',
  })

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(formData, {
      onSuccess: () => {
        setShowCreateForm(false)
        setFormData({ basket_name: '', description: '', basket_type: 'CUSTOM' })
      },
    })
  }

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this basket?')) {
      deleteMutation.mutate(id)
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'CONFIRMATION':
        return 'success'
      case 'DIVERGENCE':
        return 'warning'
      default:
        return 'info'
    }
  }

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Spinner size="lg" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Analytical Baskets"
        description="Group charts for comparative analysis"
        actions={
          <Button
            onClick={() => setShowCreateForm(!showCreateForm)}
            leftIcon={<Plus className="h-4 w-4" />}
          >
            Create Basket
          </Button>
        }
      />

      {/* Create Form */}
      {showCreateForm && (
        <Card>
          <CardHeader>
            <CardTitle>Create New Basket</CardTitle>
          </CardHeader>
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-400">
                Name
              </label>
              <input
                type="text"
                value={formData.basket_name}
                onChange={(e) => setFormData({ ...formData, basket_name: e.target.value })}
                className="w-full rounded-lg border border-slate-600 bg-surface-tertiary px-4 py-2 text-white focus:border-accent-primary focus:outline-none focus:ring-2 focus:ring-accent-primary/20"
                placeholder="e.g., NIFTY Momentum Basket"
                required
              />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-400">
                Description
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full rounded-lg border border-slate-600 bg-surface-tertiary px-4 py-2 text-white focus:border-accent-primary focus:outline-none focus:ring-2 focus:ring-accent-primary/20"
                placeholder="Describe the purpose of this basket..."
                rows={3}
              />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-400">
                Type
              </label>
              <select
                value={formData.basket_type}
                onChange={(e) => setFormData({ ...formData, basket_type: e.target.value as BasketType })}
                className="w-full rounded-lg border border-slate-600 bg-surface-tertiary px-4 py-2 text-white focus:border-accent-primary focus:outline-none focus:ring-2 focus:ring-accent-primary/20"
              >
                <option value="LOGICAL">Logical</option>
                <option value="HIERARCHICAL">Hierarchical</option>
                <option value="CONTEXTUAL">Contextual</option>
                <option value="CUSTOM">Custom</option>
              </select>
            </div>
            <div className="flex gap-2">
              <Button type="submit" isLoading={createMutation.isPending}>
                Create Basket
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={() => setShowCreateForm(false)}
              >
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      )}

      {/* Baskets List */}
      {!baskets?.length ? (
        <EmptyState
          title="No Baskets"
          description="Create a basket to group charts for analysis."
          icon={<FolderKanban className="h-8 w-8 text-slate-400" />}
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {baskets.map((basket) => (
            <Card key={basket.basket_id} hover>
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-500/20">
                      <FolderKanban className="h-5 w-5 text-purple-400" />
                    </div>
                    <div>
                      <div className="font-display font-semibold">{basket.basket_name}</div>
                      <p className="text-sm text-slate-400">{basket.description}</p>
                    </div>
                  </div>
                  <Badge variant={getTypeColor(basket.basket_type) as 'success' | 'warning' | 'info'}>
                    {basket.basket_type}
                  </Badge>
                </div>

                <div className="flex items-center gap-2 border-t border-slate-700 pt-3">
                  <BarChart3 className="h-4 w-4 text-slate-500" />
                  <span className="text-sm text-slate-400">
                    {basket.chart_ids.length} charts
                  </span>
                </div>

                <div className="flex gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(basket.basket_id)}
                    isLoading={deleteMutation.isPending}
                    leftIcon={<Trash2 className="h-4 w-4 text-red-400" />}
                  >
                    Delete
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

