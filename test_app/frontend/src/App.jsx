import { useState } from 'react'
import Cases from './components/cases'
import InventoryModal from './components/InventoryModal'
import { getInventory, BACKEND_URL } from './api'

if (window.Telegram && window.Telegram.WebApp) {
  window.Telegram.WebApp.ready();
  window.Telegram.WebApp.expand();
}

function App() {
  const [isInvOpen, setIsInvOpen] = useState(false);
  const [inventoryItems, setInventoryItems] = useState([]);

  const handleOpenInventory = async () => {
    setIsInvOpen(true);
    try {
      const data = await getInventory();
      setInventoryItems(data.items || []);
    } catch (err) {
      alert("Не удалось загрузить инвентарь");
    }
  };

  return (
    <div className="flex h-[100dvh] w-full flex-col items-center overflow-x-hidden overflow-y-auto bg-linear-to-b from-[#0a0a0a] to-[#1a1a2e]">
      <div className="flex w-full shrink-0 items-center justify-center px-5 pt-8 pb-5">
        <h1 className="rounded-2xl border border-white/10 bg-white/8 px-8 py-3.5 text-center text-2xl font-bold tracking-[0.5px] text-white shadow-[0_4px_20px_rgba(0,0,0,0.3)] backdrop-blur-md">
          Кото-Кейс
        </h1>
        <button
          className="ml-4 flex cursor-pointer items-center gap-1.5 rounded-lg border border-white/20 bg-white/10 px-4 py-2 text-sm text-white transition hover:bg-white/20"
          onClick={handleOpenInventory}
        >
          🎒 Инвентарь
        </button>
      </div>

      <Cases />

      <InventoryModal 
        isOpen={isInvOpen} 
        onClose={() => setIsInvOpen(false)} 
        items={inventoryItems} 
        backendUrl={BACKEND_URL} 
      />
    </div>
  )
}

export default App
