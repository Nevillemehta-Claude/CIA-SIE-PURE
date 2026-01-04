import { useState } from 'react'
import { usePlatforms, useConnectPlatform, useDisconnectPlatform, useSetupInstructions } from '@/hooks/usePlatforms'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, CardHeader, CardTitle } from '@/components/common/Card'
import { Button } from '@/components/common/Button'
import { Badge } from '@/components/common/Badge'
import { Spinner } from '@/components/common/Spinner'
import { EmptyState } from '@/components/common/EmptyState'
import { Plug, Check, X, ExternalLink, Copy, CheckCircle2 } from 'lucide-react'
import { clsx } from 'clsx'

export function PlatformsPage() {
  const { data: platforms, isLoading } = usePlatforms()
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null)
  const { data: setupInstructions, isLoading: setupLoading } = useSetupInstructions(selectedPlatform ?? '')
  const connectMutation = useConnectPlatform()
  const disconnectMutation = useDisconnectPlatform()
  const [copied, setCopied] = useState(false)

  const handleConnect = (platformName: string) => {
    connectMutation.mutate({ platform_name: platformName })
  }

  const handleDisconnect = (platformName: string) => {
    disconnectMutation.mutate(platformName)
  }

  const handleCopyWebhook = (url: string) => {
    navigator.clipboard.writeText(url)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!platforms?.length) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Platform Integrations"
          description="Connect your charting platforms to receive signals"
        />
        <EmptyState
          title="No Platforms Available"
          description="No platform integrations are currently configured."
          icon={<Plug className="h-8 w-8 text-slate-400" />}
        />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Platform Integrations"
        description="Connect your charting platforms to receive signals"
      />

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Platform Cards */}
        <div className="space-y-4">
          <h2 className="font-display text-lg font-semibold">Available Platforms</h2>
          {platforms.map((platform) => (
            <Card
              key={platform.name}
              className={clsx(
                'cursor-pointer transition-all',
                selectedPlatform === platform.name && 'ring-2 ring-accent-primary'
              )}
            >
              <div
                onClick={() => setSelectedPlatform(platform.name)}
                className="space-y-3"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div
                      className={clsx(
                        'flex h-10 w-10 items-center justify-center rounded-lg',
                        platform.connected ? 'bg-green-500/20' : 'bg-slate-600'
                      )}
                    >
                      <Plug
                        className={clsx(
                          'h-5 w-5',
                          platform.connected ? 'text-green-400' : 'text-slate-400'
                        )}
                      />
                    </div>
                    <div>
                      <div className="font-display font-semibold">{platform.display_name}</div>
                      <p className="text-sm text-slate-400">{platform.description}</p>
                    </div>
                  </div>
                  <Badge variant={platform.connected ? 'success' : 'default'}>
                    {platform.connected ? 'Connected' : 'Not Connected'}
                  </Badge>
                </div>

                <div className="flex items-center gap-2 border-t border-slate-700 pt-3">
                  {platform.supports_webhooks && (
                    <Badge variant="info">Webhooks</Badge>
                  )}
                  {platform.supports_realtime && (
                    <Badge variant="info">Realtime</Badge>
                  )}
                </div>

                <div className="flex gap-2">
                  {platform.connected ? (
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDisconnect(platform.name)
                      }}
                      isLoading={disconnectMutation.isPending}
                      leftIcon={<X className="h-4 w-4" />}
                    >
                      Disconnect
                    </Button>
                  ) : (
                    <Button
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleConnect(platform.name)
                      }}
                      isLoading={connectMutation.isPending}
                      leftIcon={<Check className="h-4 w-4" />}
                    >
                      Connect
                    </Button>
                  )}
                  {platform.setup_url && (
                    <a
                      href={platform.setup_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <Button
                        variant="ghost"
                        size="sm"
                        leftIcon={<ExternalLink className="h-4 w-4" />}
                      >
                        Docs
                      </Button>
                    </a>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Setup Instructions Panel */}
        <div className="space-y-4">
          <h2 className="font-display text-lg font-semibold">Setup Instructions</h2>
          {selectedPlatform ? (
            setupLoading ? (
              <Card>
                <div className="flex items-center justify-center py-8">
                  <Spinner />
                </div>
              </Card>
            ) : setupInstructions ? (
              <Card>
                <CardHeader>
                  <CardTitle>{setupInstructions.platform_name} Setup</CardTitle>
                </CardHeader>

                <div className="space-y-4">
                  {/* Webhook URL */}
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-400">
                      Webhook URL
                    </label>
                    <div className="flex items-center gap-2">
                      <code className="flex-1 rounded-lg bg-surface-tertiary px-3 py-2 text-sm text-slate-300">
                        {setupInstructions.webhook_url}
                      </code>
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => handleCopyWebhook(setupInstructions.webhook_url)}
                        leftIcon={copied ? <CheckCircle2 className="h-4 w-4 text-green-400" /> : <Copy className="h-4 w-4" />}
                      >
                        {copied ? 'Copied!' : 'Copy'}
                      </Button>
                    </div>
                  </div>

                  {/* Steps */}
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-400">
                      Steps
                    </label>
                    <ol className="space-y-2">
                      {setupInstructions.steps.map((step, index) => (
                        <li key={index} className="flex gap-3 text-sm">
                          <span className="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-accent-primary/20 text-xs font-bold text-accent-primary">
                            {index + 1}
                          </span>
                          <span className="text-slate-300">{step}</span>
                        </li>
                      ))}
                    </ol>
                  </div>

                  {/* Example Payload */}
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-400">
                      Example Webhook Payload
                    </label>
                    <pre className="overflow-x-auto rounded-lg bg-surface-tertiary p-3 text-xs text-slate-300">
                      {JSON.stringify(setupInstructions.example_payload, null, 2)}
                    </pre>
                  </div>
                </div>
              </Card>
            ) : (
              <Card>
                <EmptyState
                  title="No Setup Instructions"
                  description="Setup instructions are not available for this platform."
                />
              </Card>
            )
          ) : (
            <Card>
              <div className="py-8 text-center text-slate-400">
                <Plug className="mx-auto mb-3 h-8 w-8" />
                <p>Select a platform to view setup instructions</p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

