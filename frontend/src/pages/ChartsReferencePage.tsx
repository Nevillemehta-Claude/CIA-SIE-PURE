import { Card } from '@/components/common/Card'
import { PageHeader } from '@/components/layout/PageHeader'
import { FileText } from 'lucide-react'

interface SampleChart {
  code: string
  name: string
  timeframe: string
  webhookId: string
  purpose: string
}

// Reference documentation: 12 sample chart configurations
const SAMPLE_CHARTS: SampleChart[] = [
  {
    code: '01A',
    name: 'Momentum Health',
    timeframe: 'Daily',
    webhookId: 'SAMPLE_01A',
    purpose: 'Overall momentum state assessment',
  },
  {
    code: '02',
    name: 'HTF Structure',
    timeframe: 'Weekly',
    webhookId: 'SAMPLE_02',
    purpose: 'Higher timeframe directional structure',
  },
  {
    code: '04A',
    name: 'Risk Extension',
    timeframe: '3H',
    webhookId: 'SAMPLE_04A',
    purpose: 'Risk extension levels on 3-hour timeframe',
  },
  {
    code: '04B',
    name: 'Support/Resistance',
    timeframe: '3H',
    webhookId: 'SAMPLE_04B',
    purpose: 'Support and resistance level identification',
  },
  {
    code: '05A',
    name: 'VWAP Execution',
    timeframe: 'Daily',
    webhookId: 'SAMPLE_05A',
    purpose: 'VWAP-based execution signals',
  },
  {
    code: '05B',
    name: 'Momentum Exhaustion',
    timeframe: 'Daily',
    webhookId: 'SAMPLE_05B',
    purpose: 'Detection of momentum exhaustion patterns',
  },
  {
    code: '05C',
    name: 'Extension Risk',
    timeframe: 'Daily',
    webhookId: 'SAMPLE_05C',
    purpose: 'Extension risk assessment on daily timeframe',
  },
  {
    code: '05D',
    name: 'VWAP Deviation',
    timeframe: 'Daily',
    webhookId: 'SAMPLE_05D',
    purpose: 'VWAP deviation analysis',
  },
  {
    code: '06',
    name: 'Macro Correlation',
    timeframe: 'Daily',
    webhookId: 'SAMPLE_06',
    purpose: 'Macroeconomic correlation analysis',
  },
  {
    code: '07',
    name: 'Primary Trend',
    timeframe: 'Daily',
    webhookId: 'SAMPLE_07',
    purpose: 'Primary trend identification',
  },
  {
    code: '08',
    name: 'Volume Analysis',
    timeframe: 'Daily',
    webhookId: 'SAMPLE_08',
    purpose: 'Volume profile and flow analysis',
  },
  {
    code: '09',
    name: 'Order Flow',
    timeframe: 'Daily',
    webhookId: 'SAMPLE_09',
    purpose: 'Order flow and liquidity analysis',
  },
]

export function ChartsReferencePage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Chart Reference"
        description="Reference guide for standard chart configurations used in CIA-SIE. These are example configurations to help you understand the system."
      />

      <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-4">
        <div className="mb-2 flex items-center gap-2 text-slate-300">
          <FileText className="h-5 w-5 text-accent-primary" aria-hidden="true" />
          <p className="text-sm italic">
            Note: These are example chart configurations for reference. Your actual charts are
            created dynamically and can be configured with any code, name, timeframe, and webhook ID
            you choose.
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {SAMPLE_CHARTS.map((chart) => (
          <Card key={chart.code} hover>
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <span
                  className="font-mono text-sm font-medium text-accent-primary"
                  aria-label={`Chart code: ${chart.code}`}
                >
                  {chart.code}
                </span>
                <span
                  className="rounded bg-slate-700 px-2 py-1 text-xs font-medium text-slate-300"
                  aria-label={`Timeframe: ${chart.timeframe}`}
                >
                  {chart.timeframe}
                </span>
              </div>

              <h3 className="font-display text-lg font-semibold text-white">{chart.name}</h3>

              <p className="text-sm text-slate-400">{chart.purpose}</p>

              <div className="border-t border-slate-700 pt-2">
                <div className="mb-1 text-xs font-medium text-slate-500">Webhook ID</div>
                <code className="block truncate rounded bg-slate-900 px-2 py-1 text-xs text-slate-400">
                  {chart.webhookId}
                </code>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}

