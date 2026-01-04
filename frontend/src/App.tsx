import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AppShell } from '@/components/layout/AppShell'
import {
  HomePage,
  InstrumentsPage,
  InstrumentDetailPage,
  SiloDetailPage,
  ChartDetailPage,
  ChatPage,
  SettingsPage,
  PlatformsPage,
  BasketsPage,
  NotFoundPage,
} from '@/pages'

function App() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/instruments" element={<InstrumentsPage />} />
          <Route path="/instruments/:instrumentId" element={<InstrumentDetailPage />} />
          <Route path="/silos/:siloId" element={<SiloDetailPage />} />
          <Route path="/charts/:chartId" element={<ChartDetailPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/chat/:scripId" element={<ChatPage />} />
          <Route path="/platforms" element={<PlatformsPage />} />
          <Route path="/baskets" element={<BasketsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  )
}

export default App

