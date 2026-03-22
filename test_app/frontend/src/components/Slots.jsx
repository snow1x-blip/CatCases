import React from 'react';

const getImageUrl = (backendUrl, imagePath) => {
  if (!imagePath) return '';
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath;
  }
  const base = backendUrl.endsWith('/') ? backendUrl.slice(0, -1) : backendUrl;
  const path = imagePath.startsWith('/') ? imagePath : `/${imagePath}`;
  return `${base}${path}`;
};

const Slots = ({ slots, isSpinning, finalItem, backendUrl }) => {
  const renderSlot = (item, isMiddle = false) => {
    const baseSize = isMiddle
      ? 'h-[130px] w-[110px] sm:h-[160px] sm:w-[140px]'
      : 'h-[110px] w-[90px] sm:h-[140px] sm:w-[120px]';
    const middleState = isMiddle
      ? 'border-[rgba(51,144,236,0.5)] bg-[rgba(51,144,236,0.2)]'
      : '';
    const spinningState = isSpinning ? 'animate-slot-shake border-[rgba(51,144,236,0.5)]' : '';
    const winnerState = isMiddle && finalItem
      ? 'animate-win-pulse border-[rgba(51,144,236,0.9)] shadow-[0_0_40px_rgba(51,144,236,0.6),inset_0_0_40px_rgba(51,144,236,0.2)]'
      : '';

    return (
      <div
        className={`relative mb-3 flex items-center justify-center overflow-hidden rounded-2xl border-2 border-[rgba(51,144,236,0.3)] bg-[rgba(26,26,46,0.8)] shadow-[0_4px_20px_rgba(0,0,0,0.4),inset_0_0_20px_rgba(51,144,236,0.05)] backdrop-blur-md transition-all ${baseSize} ${middleState} ${spinningState} ${winnerState}`}
      >
        {item ? (
          <img
            src={getImageUrl(backendUrl, item.image_path)}
            alt=""
            className={`z-[2] object-contain ${isMiddle ? 'h-[85%] w-[85%]' : 'h-[80%] w-[80%]'}`}
            style={{
              filter: isMiddle && finalItem
                ? 'drop-shadow(0 0 20px rgba(51, 144, 236, 1))'
                : 'drop-shadow(0 0 10px rgba(51, 144, 236, 0.5))',
            }}
          />
        ) : (
          <span className="text-[42px] font-bold text-white/60 sm:text-[56px]">?</span>
        )}
        {isMiddle && finalItem && (
          <div className="animate-glow-pulse pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(51,144,236,0.3)_0%,_transparent_70%)]" />
        )}
      </div>
    );
  };

  return (
    <div className="flex w-full flex-1 items-center justify-center">
      <div className="flex flex-wrap items-start justify-center gap-2.5 p-5 sm:gap-4">
        <div className="flex w-[90px] flex-col items-center sm:w-[120px]">
          {renderSlot(slots[0])}
          <div className="min-h-5 w-full" />
        </div>

        <div className="flex w-[110px] flex-col items-center sm:w-[140px]">
          {renderSlot(slots[1], true)}
          <div
            className={`min-h-6 w-full max-w-[180px] overflow-hidden text-ellipsis whitespace-nowrap text-center text-xs font-bold tracking-[0.5px] text-white text-shadow-[0_2px_4px_rgba(0,0,0,0.8)] sm:text-sm ${finalItem ? 'animate-slide-up-fade' : 'translate-y-2.5 opacity-0'}`}
          >
            {slots[1]?.name || "????"}
          </div>
        </div>

        <div className="flex w-[90px] flex-col items-center sm:w-[120px]">
          {renderSlot(slots[2])}
          <div className="min-h-5 w-full" />
        </div>
      </div>
    </div>
  );
};

export default Slots;
