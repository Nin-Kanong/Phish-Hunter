import { create } from 'zustand';
export const useAnalysisStore = create(set => ({ files: [], job: null, result: null, activeTab: 'overview', setFiles: x => set({ files: x }), setJob: x => set({ job: x, result: x?.result ?? null }), setResult: x => set({ result: x }), setTab: x => set({ activeTab: x }) }));
