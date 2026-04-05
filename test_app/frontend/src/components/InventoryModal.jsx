import React from 'react';
import { getImageUrl } from '../utils';

const InventoryModal = ({ isOpen, onClose, items, backendUrl }) => {
  if (!isOpen) return null;

  const rarityStyles = {
    common: 'border-[#b0b0b0]',
    rare: 'border-[#3390ec] shadow-[0_0_10px_rgba(51,144,236,0.2)]',
    epic: 'border-[#a335ee] shadow-[0_0_10px_rgba(163,53,238,0.2)]',
    legendary: 'border-[#ffd700] shadow-[0_0_15px_rgba(255,215,0,0.3)]',
  };

  return (
    <div
      className="animate-fade-in fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-[5px]"
      onClick={onClose}
    >
      <div
        className="animate-modal-slide-up flex max-h-[80vh] w-[90%] max-w-[500px] flex-col rounded-[20px] border border-[rgba(51,144,236,0.3)] bg-[#1a1a2e] p-5 shadow-[0_10px_40px_rgba(0,0,0,0.5)]"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-5 flex items-center justify-between border-b border-white/10 pb-2.5">
          <h2 className="text-xl font-semibold text-white">Твой Инвентарь</h2>
          <button
            className="cursor-pointer border-none bg-transparent text-2xl text-white/70 transition hover:text-white"
            onClick={onClose}
          >
            ✕
          </button>
        </div>
        
        <div className="grid max-h-[60vh] grid-cols-[repeat(auto-fill,minmax(80px,1fr))] gap-4 overflow-y-auto p-1">
          {items.length === 0 ? (
            <p className="col-[1/-1] mt-5 text-center text-[#666]">Пока пусто. Крути кейс!</p>
          ) : (
            items.map((item) => (
              <div
                key={item.id}
                className={`rounded-xl border bg-white/5 p-2.5 text-center transition hover:-translate-y-0.5 ${rarityStyles[item.rarity] || ''}`}
              >
                <div className="relative flex h-[60px] items-center justify-center">
                  <img
                    src={getImageUrl(item.image_path)}
                    alt={item.name}
                    className="h-[50px] w-[50px] object-contain"
                  />
                  <span className="absolute -right-1 -bottom-1 rounded-[10px] border border-[#555] bg-[#333] px-1.5 py-0.5 text-[10px] font-bold text-white">
                    {item.count}
                  </span>
                </div>
                <div className="mt-2 overflow-hidden text-ellipsis whitespace-nowrap text-[11px] text-[#ccc]">
                  {item.name}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default InventoryModal;
