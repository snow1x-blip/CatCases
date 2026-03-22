import { useEffect, useState } from 'react'
import Slots from './Slots'
import { spinCase, getCases, getCaseItems, BACKEND_URL } from '../api'

function Cases() {
  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [isCasesLoading, setIsCasesLoading] = useState(true);

  const [finalItem, setFinalItem] = useState(null);
  const [isSpinning, setIsSpinning] = useState(false);
  const [slots, setSlots] = useState([null, null, null]);
  const [itemsPool, setItemsPool] = useState([]);

  useEffect(() => {
    const loadCases = async () => {
      try {
        const loadedCases = await getCases();
        setCases(Array.isArray(loadedCases) ? loadedCases : []);
      } catch (error) {
        console.error('Failed to load cases:', error);
        setCases([]);
      } finally {
        setIsCasesLoading(false);
      }
    };

    loadCases();
  }, []);

  const handleSpin = async () => {
    if (!selectedCase || isSpinning) return;

    setIsSpinning(true);
    setFinalItem(null);
    setSlots([null, null, null]);

    try {
      const targetItem = await spinCase(selectedCase.id);
      const getRandomPoolItem = () => {
        if (itemsPool.length === 0) return targetItem;
        return itemsPool[Math.floor(Math.random() * itemsPool.length)];
      };

      let iteration = 0;
      const maxIterations = 20;
      const baseSpeed = 80;

      const spinInterval = setInterval(() => {
        setSlots([
          getRandomPoolItem(),
          getRandomPoolItem(),
          getRandomPoolItem()
        ]);
        iteration++;
        if (iteration >= maxIterations) {
          clearInterval(spinInterval);
          setTimeout(() => {
            setSlots([
              getRandomPoolItem(),
              targetItem,
              getRandomPoolItem()
            ]);
            setFinalItem(targetItem);
            setIsSpinning(false);
          }, 150);
        }
      }, baseSpeed);
    } catch (error) {
      console.error(error);
      alert("Ошибка: " + error.message);
      setIsSpinning(false);
    }
  };

  const handleOpenCase = async (caseItem) => {
    setSelectedCase(caseItem);
    setIsSpinning(false);
    setFinalItem(null);
    setSlots([null, null, null]);
    try {
      const items = await getCaseItems(caseItem.id);
      setItemsPool(Array.isArray(items) ? items : []);
    } catch (error) {
      console.error('Failed to load case items:', error);
      setItemsPool([]);
      alert("Не удалось загрузить содержимое кейса");
    }
  };

  const handleBackToCases = () => {
    setSelectedCase(null);
    setIsSpinning(false);
    setFinalItem(null);
    setSlots([null, null, null]);
    setItemsPool([]);
  };

  const getImageUrl = (imagePath) => {
    if (!imagePath) return '';
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
      return imagePath;
    }
    const base = BACKEND_URL.endsWith('/') ? BACKEND_URL.slice(0, -1) : BACKEND_URL;
    const path = imagePath.startsWith('/') ? imagePath : `/${imagePath}`;
    return `${base}${path}`;
  };

  if (!selectedCase) {
    return (
      <div className="w-full max-w-4xl flex-1 px-5 pb-10">
        <h2 className="mb-5 text-center text-xl font-semibold text-white/90">Выбери кейс</h2>
        {isCasesLoading ? (
          <p className="text-center text-white/70">Загрузка кейсов...</p>
        ) : cases.length === 0 ? (
          <p className="text-center text-white/70">Кейсы пока не настроены</p>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {cases.map((caseItem) => (
              <button
                key={caseItem.id}
                className="group cursor-pointer overflow-hidden rounded-2xl border border-white/10 bg-white/5 text-left transition hover:-translate-y-1 hover:border-[#3390ec]/50 hover:bg-white/8"
                onClick={() => handleOpenCase(caseItem)}
              >
                <div className="aspect-[4/3] w-full overflow-hidden bg-black/20">
                  <img
                    src={getImageUrl(caseItem.image_path)}
                    alt={caseItem.name}
                    className="h-full w-full object-cover transition group-hover:scale-105"
                  />
                </div>
                <div className="p-4">
                  <div className="text-base font-semibold text-white">{caseItem.name}</div>
                  <div className="mt-2 text-sm text-[#8cc4ff]">Открыть кейс</div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <>
      <div className="w-full px-5">
        <div className="mx-auto flex w-full max-w-4xl items-center justify-between">
          <button
            className="cursor-pointer rounded-lg border border-white/20 bg-white/10 px-3 py-1.5 text-sm text-white transition hover:bg-white/20"
            onClick={handleBackToCases}
          >
            ← Назад к кейсам
          </button>
          <div className="text-sm font-medium text-white/80">{selectedCase.name}</div>
        </div>
      </div>

      <Slots
        slots={slots}
        isSpinning={isSpinning}
        finalItem={finalItem}
        backendUrl={BACKEND_URL}
      />

      <div className="flex w-full justify-center px-5 pt-8 pb-12">
        <button
          className="relative cursor-pointer overflow-hidden rounded-xl border border-white/15 bg-linear-to-br from-[rgba(51,144,236,0.95)] to-[rgba(29,111,181,0.95)] px-14 py-[18px] text-[17px] font-bold tracking-[1.5px] text-white uppercase shadow-[0_6px_25px_rgba(51,144,236,0.5)] transition-all backdrop-blur-md hover:-translate-y-[3px] hover:shadow-[0_10px_35px_rgba(51,144,236,0.7)] disabled:cursor-not-allowed disabled:opacity-60 disabled:transform-none"
          onClick={handleSpin}
          disabled={isSpinning}
        >
          {isSpinning ? "Крутим..." : "Открыть кейс"}
        </button>
      </div>
    </>
  );
}

export default Cases
