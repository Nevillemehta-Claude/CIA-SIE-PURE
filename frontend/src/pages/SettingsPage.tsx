/**
 * SettingsPage Component
 * 
 * Application settings and configuration.
 */

import { PageHeader, ContentArea } from '@components/layout'
import { Card } from '@components/atoms'
import { Settings, Cpu, Link as LinkIcon, Bell } from 'lucide-react'

/**
 * SettingsPage displays application configuration options.
 */
export function SettingsPage() {
  return (
    <ContentArea maxWidth="lg">
      <PageHeader 
        title="Settings"
        description="Configure your CIA-SIE application"
      />

      <div className="space-y-6">
        {/* AI Configuration */}
        <Card>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-lg bg-accent-primary/20">
              <Cpu className="h-5 w-5 text-accent-primary" aria-hidden="true" />
            </div>
            <h2 className="font-display text-lg font-semibold">AI Configuration</h2>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between py-3 border-b border-slate-700">
              <div>
                <p className="font-medium">Default Model</p>
                <p className="text-sm text-slate-400">Model used for narrative generation</p>
              </div>
              <select 
                className="bg-surface-tertiary border border-slate-600 rounded-lg px-3 py-2 text-sm"
                defaultValue="sonnet"
              >
                <option value="haiku">Claude 3 Haiku (Fast)</option>
                <option value="sonnet">Claude 3.5 Sonnet (Balanced)</option>
                <option value="opus">Claude 3 Opus (Advanced)</option>
              </select>
            </div>

            <div className="flex items-center justify-between py-3 border-b border-slate-700">
              <div>
                <p className="font-medium">Monthly Budget</p>
                <p className="text-sm text-slate-400">Maximum AI spending per month</p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-slate-400">$</span>
                <input 
                  type="number"
                  className="w-24 bg-surface-tertiary border border-slate-600 rounded-lg px-3 py-2 text-sm"
                  defaultValue={50}
                  min={1}
                />
              </div>
            </div>

            <div className="flex items-center justify-between py-3">
              <div>
                <p className="font-medium">Budget Alert Threshold</p>
                <p className="text-sm text-slate-400">Alert when usage exceeds this percentage</p>
              </div>
              <div className="flex items-center gap-2">
                <input 
                  type="number"
                  className="w-20 bg-surface-tertiary border border-slate-600 rounded-lg px-3 py-2 text-sm"
                  defaultValue={80}
                  min={50}
                  max={100}
                />
                <span className="text-slate-400">%</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Platform Connections */}
        <Card>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-lg bg-green-500/20">
              <LinkIcon className="h-5 w-5 text-green-500" aria-hidden="true" />
            </div>
            <h2 className="font-display text-lg font-semibold">Platform Connections</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between py-3 border-b border-slate-700">
              <div className="flex items-center gap-3">
                <div className="h-3 w-3 rounded-full bg-green-500" />
                <div>
                  <p className="font-medium">TradingView</p>
                  <p className="text-sm text-slate-400">Webhook receiver active</p>
                </div>
              </div>
              <span className="text-sm text-green-400">Connected</span>
            </div>

            <div className="flex items-center justify-between py-3">
              <div className="flex items-center gap-3">
                <div className="h-3 w-3 rounded-full bg-slate-500" />
                <div>
                  <p className="font-medium">Kite Connect</p>
                  <p className="text-sm text-slate-400">Optional watchlist integration</p>
                </div>
              </div>
              <button className="text-sm text-accent-primary hover:underline">
                Connect
              </button>
            </div>
          </div>
        </Card>

        {/* Notification Settings */}
        <Card>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-lg bg-amber-500/20">
              <Bell className="h-5 w-5 text-amber-500" aria-hidden="true" />
            </div>
            <h2 className="font-display text-lg font-semibold">Notifications</h2>
          </div>

          <div className="space-y-4">
            <label className="flex items-center justify-between py-3 cursor-pointer border-b border-slate-700">
              <div>
                <p className="font-medium">Contradiction Alerts</p>
                <p className="text-sm text-slate-400">Notify when contradictions are detected</p>
              </div>
              <input type="checkbox" defaultChecked className="w-5 h-5 accent-accent-primary" />
            </label>

            <label className="flex items-center justify-between py-3 cursor-pointer border-b border-slate-700">
              <div>
                <p className="font-medium">Stale Data Warnings</p>
                <p className="text-sm text-slate-400">Notify when data becomes stale</p>
              </div>
              <input type="checkbox" defaultChecked className="w-5 h-5 accent-accent-primary" />
            </label>

            <label className="flex items-center justify-between py-3 cursor-pointer">
              <div>
                <p className="font-medium">Budget Alerts</p>
                <p className="text-sm text-slate-400">Notify when approaching budget limit</p>
              </div>
              <input type="checkbox" defaultChecked className="w-5 h-5 accent-accent-primary" />
            </label>
          </div>
        </Card>

        {/* About Section */}
        <Card>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded-lg bg-slate-500/20">
              <Settings className="h-5 w-5 text-slate-400" aria-hidden="true" />
            </div>
            <h2 className="font-display text-lg font-semibold">About CIA-SIE</h2>
          </div>
          
          <div className="text-sm text-slate-400 space-y-2">
            <p>Version: 1.0.0</p>
            <p>
              CIA-SIE is a <strong className="text-slate-300">decision-support platform</strong> that
              displays trading signals from TradingView charts. It does not provide investment advice.
            </p>
            <p className="italic">
              All interpretations and decisions are entirely yours.
            </p>
          </div>
        </Card>
      </div>
    </ContentArea>
  )
}

